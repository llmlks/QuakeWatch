from enum import Enum


class CatalogTypes(Enum):
    """Enum to hold different catalog types."""
    HYPO_EXT = '.hypo'
    SCEDC_EXT = '.scedc'
    CSV_EXT = '.csv'
    DAT_EXT = '.dat'
    TXT_EXT = '.txt'
    FEN_EXT = '.FEN'


def is_california_data(catalog_type):
    """Return boolean indicating whether given catalog
    type contains data located in California.

    Keyword arguments:
    catalog_type -- String representing the catalog type to test
    """
    return catalog_type in [CatalogTypes.HYPO_EXT, CatalogTypes.SCEDC_EXT]
