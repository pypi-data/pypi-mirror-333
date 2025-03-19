import time
from functools import wraps
from typing import Any, Callable

import dask
from dask.array import Array
from distributed import Future, get_client

from eopf.config.config import EOConfiguration
from eopf.daskconfig import ClusterType
from eopf.daskconfig.dask_context_manager import DaskContext
from eopf.logging.log import EOLogging


def init_from_eo_configuration() -> DaskContext:
    logger = EOLogging().get_logger("eopf.daskconfig.dask_utils")
    conf = EOConfiguration()
    # init defaults
    cluster_config = {}
    auth_config = {}
    client_config = {}
    cluster_type = None
    performance_report_file = None

    if conf.has_value("dask_context__cluster_type"):
        cluster_type_str = conf.__getattr__("dask_context__cluster_type")

        if cluster_type_str == ClusterType.ADDRESS.value:
            if not conf.has_value("dask_context__addr"):
                raise Exception("missing addr conf for ADDRESS cluster")
            logger.debug("Initializing an ADDRESS dask cluster")
            return DaskContext(cluster_type_str, address=conf.__getattr__("dask_context__addr"))
        else:
            for c in conf.param_list_available:
                if c.startswith("dask_context__cluster_config__"):
                    if c.startswith("dask_context__cluster_config__auth__"):
                        auth_config[c.replace("dask_context__cluster_config__auth__", "")] = conf.__getattr__(c)
                    else:
                        cluster_config[c.replace("dask_context__cluster_config__", "")] = conf.__getattr__(c)
                if c.startswith("dask_context__client_config__"):
                    client_config[c.replace("dask_context__client_config__", "")] = conf.__getattr__(c)
        cluster_type = ClusterType(cluster_type_str)
    for c in conf.param_list_available:
        if c.startswith("dask_context__client_config__"):
            client_config[c.replace("dask_context__client_config__", "")] = conf.__getattr__(c)
        if c == "dask_context__performance_report_file":
            performance_report_file = conf.__getattr__(c)

    if len(client_config) != 0:
        logger.debug(f"Initialising a client with conf : {client_config} ")
    else:
        logger.debug("Initialising a client without conf")

    if len(auth_config) > 0:
        cluster_config["auth"] = auth_config

    return DaskContext(
        cluster_type=cluster_type,
        client_config=client_config,
        cluster_config=cluster_config,
        performance_report_file=performance_report_file,
    )


def remote_dask_cluster_decorator(config: dict[Any, Any]) -> Any:
    """Wrapper function used to setup a remote dask cluster and run the wrapped function on it

    Parameters
    ----------
    config: Dict
        dictionary with dask cluster configuration parameters

    Returns
    ----------
    Any: the return of the wrapped function

    Examples
    --------
    >>> dask_config = {
    ...    "cluster_type": "gateway",
    ...    "cluster_config": {
    ...        "address": "http://xxx.xxx.xxx.xxx/services/dask-gateway",
    ...        "auth": {
    ...            "auth": "jupyterhub",
    ...            "api_token": "xxxxxxxxxxxxxx"
    ...        },
    ...        "image": "registry.eopf.copernicus.eu/cpm/eopf-cpm:feat-create-docker-image",
    ...        "worker_memory": 4,
    ...        "workers" : 8
    ...    },
    ...    "client_config": {
    ...        "timeout" : "320s"
    ...    }
    ... }
    ...
    >>> @remote_dask_cluster_decorator(dask_config)
    >>> def convert_to_native_python_type():
    ...     safe_store = EOSafeStore("data/olci.SEN3")
    ...     nc_store = EONetCDFStore("data/olci.nc")
    ...     convert(safe_store, nc_store)
    """
    logger = EOLogging().get_logger("eopf.daskconfig.dask_utils")

    def wrap_outer(fn: Callable[[Any, Any], Any]) -> Any:
        @wraps(fn)
        def wrap_inner(*args: Any, **kwargs: Any) -> Any:
            if config:
                from dask_gateway import Gateway
                from dask_gateway.auth import JupyterHubAuth

                gateway_api_token = config["cluster_config"]["auth"]["api_token"]
                gateway_url = config["cluster_config"]["address"]
                processor_image = config["cluster_config"]["image"]
                workers = config["cluster_config"].get("workers", 2)
                worker_mem = config["cluster_config"].get("worker_memory", 4)

                auth = JupyterHubAuth(api_token=gateway_api_token)
                gateway = Gateway(address=gateway_url, auth=auth)
                if len(gateway.list_clusters()) > 0:
                    cluster = gateway.connect(gateway.list_clusters()[0].name)
                    cluster_addr = f"{gateway_url}/clusters/{gateway.list_clusters()[0].name}/status"
                    logger.info(f"A cluster was found, reusing, open dashboard at: {cluster_addr}")
                else:
                    cluster = gateway.new_cluster(image=processor_image, worker_memory=worker_mem)
                    cluster_addr = f"{gateway_url}/clusters/{gateway.list_clusters()[0].name}/status"
                    logger.info(f"Cluster created, open dashboard at: {cluster_addr}")
                cluster.scale(workers)
                client = cluster.get_client()
                client.__enter__()
            result = fn(*args, **kwargs)
            return result

        return wrap_inner

    return wrap_outer


def local_dask_cluster_decorator(cluster_config: dict[Any, Any]) -> Any:
    """
    Wrapper function used to setup a local dask cluster and run the wrapped function on it
    This wrapper can run with / without a pre-defined configuration.
    Note that the call of the wrapped function must be made inside
    the if __name__ == "__main__" if used in python standalone programs,
    this is not required for dynamic environments like IPython.

    Parameters
    ----------
    cluster_config: Dict
        dictionary with dask cluster configuration parameters

    Returns
    ----------
    Any: the return of the wrapped function

    Examples
    --------
    ... "cluster_config": {
    ...     "n_workers": 2,
    ...     "worker_memory": "2GB",
    ...     "threads_per_worker" : 2
    ... }
    ...
    ... @local_dask_cluster_decorator(config=cluster_config)
    ... def conv_to_zarr(input_prod, output_prod):
    ...     ss = EOSafeStore(input_prod)
    ...     zs = EOZarrStore(output_prod)
    ...     convert(ss, zs)
    ...
    ... if __name__ == "__main__":
    ...     input_path = <...>
    ...     output_path = <...>
    ...     conv_to_zarr(input_path, output_path)
    """
    logger = EOLogging().get_logger("eopf.daskconfig.dask_utils")

    def wrap_outer(fn: Callable[[Any, Any], Any]) -> Any:
        @wraps(fn)
        def wrap_inner(*args: Any, **kwargs: Any) -> Any:
            n_workers = cluster_config.get("n_workers", 4)
            memory_limit = cluster_config.get("memory_limit", "8GB")
            worker_threads = cluster_config.get("threads_per_worker", 2)
            with DaskContext(
                cluster_type=ClusterType.LOCAL,
                cluster_config={
                    "n_workers": n_workers,
                    "threads_per_worker": worker_threads,
                    "memory_limit": memory_limit,
                },
            ) as ctx:  # noqa
                if ctx.client is not None:
                    logger.info(f"Dask dashboard address: {ctx.client.dashboard_link}")
                return fn(*args, **kwargs)

        return wrap_inner

    return wrap_outer


EOConfiguration().register_requested_parameter(
    "dask_utils__compute__step",
    9999,
    True,
    description="Number of dask future computed simultaneously in dask_utils",
)


def compute(*args: Any, **kwargs: Any) -> None:
    """
    Custom compute function that checks if a Dask client is available.
    If a client is available, it uses client.compute.
    Otherwise, it falls back to dask.compute.
    Blocking call until everything is done
    """
    # Check if a Dask client is already instantiated
    logger = EOLogging().get_logger("eopf.daskconfig.dask_utils")
    collection = args[0] if isinstance(args[0], (list, tuple)) else [args[0]]
    try:
        client = get_client()
    except Exception:
        client = None

    start_idx = 0
    step = int(EOConfiguration().__getattr__("dask_utils__compute__step"))
    total_futures = len(collection)
    while start_idx < total_futures:
        end_index = min(start_idx + step, total_futures)
        if client is None:
            logger.debug("Computing without client ")
            dask.compute(collection[start_idx:end_index], **kwargs)
        else:
            logger.debug(f"Computing using client {id(client)}")
            fu = []
            for idx, d in enumerate(collection[start_idx:end_index]):
                logger.debug(f"Sending {d} to the client with priority {10*idx}")
                fu.append(client.compute(d, priority=10 * idx, **kwargs))
            while fu:
                for idx, r in enumerate(fu):
                    if r.done():
                        logger.debug(f"{idx}:{r} is finished !")
                        fu[idx] = None
                fu = [x for x in fu if x is not None]
                # wait not to have an infinite loop
                if fu:
                    time.sleep(0.1)
        start_idx += step


def scatter(data: Array, **kwargs: Any) -> Future | Array:
    logger = EOLogging().get_logger("eopf.daskconfig.dask_utils")
    try:
        client = get_client()
    except Exception:
        client = None

    if client is not None:
        logger.debug(f"scattering on client client {id(client)} with options : {kwargs}")
        return client.scatter(data, **kwargs)
    else:
        # No client, can't future the data
        logger.debug("No client in scatter : returning data itself ")
        return data
