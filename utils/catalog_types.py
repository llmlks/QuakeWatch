from enum import Enum


class CatalogTypes(Enum):
    """Enum to hold different catalog types."""
    HYPO_EXT = '.hypo'
    SCEDC_EXT = '.scedc'
    CSV_EXT = '.csv'
    DAT_EXT = '.dat'
