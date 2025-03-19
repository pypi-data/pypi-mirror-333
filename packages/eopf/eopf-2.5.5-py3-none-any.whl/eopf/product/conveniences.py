from typing import TYPE_CHECKING, Any, Optional, Union

from eopf.product.eo_group import EOGroup
from eopf.product.eo_product import EOProduct

if TYPE_CHECKING:  # pragma: no cover
    from eopf.product.eo_container import EOContainer


def init_product(
    product_name: str,
    **kwargs: Any,
) -> EOProduct:
    """Convenience function to create a valid EOProduct base.

    Parameters
    ----------
    product_name: str
        name of the product to create
    **kwargs: any
        Any valid named arguments for EOProduct

    Returns
    -------
    EOProduct
        newly created product

    See Also
    --------
    eopf.product.EOProduct
    eopf.product.EOProduct.is_valid
    """
    product = EOProduct(product_name, **kwargs)

    # TODO : open the product ?
    for group_name in product.MANDATORY_FIELD:
        product[group_name] = EOGroup(group_name)
    return product


def get_product_type(eo_obj: Union["EOProduct", "EOContainer"]) -> Optional[str]:
    """Convenience function to retrieve product:type from EOProduct/EOContainer

    Parameters
    ----------
    eo_obj: Union[EOProduct, EOContainer]
        product or container

    Returns
    -------
    Optional[str]
        product_type

    """
    try:
        return eo_obj.attrs["stac_discovery"]["properties"]["product:type"]
    except KeyError:
        return None


def set_product_type(eo_obj: Union["EOProduct", "EOContainer"], intype: Optional[str]) -> None:
    """Convenience function to retrieve product:type from EOProduct/EOContainer

    Parameters
    ----------
    eo_obj: Union[EOProduct, EOContainer]
        product or container
    type: str
        product:type

    """
    eo_obj.attrs.setdefault("stac_discovery", {}).setdefault("properties", {})["product:type"] = intype


# -----------------------------------------------
