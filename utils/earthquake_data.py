import os
import json
from datetime import datetime

import pandas as pd
from app import cache
from utils.catalog_types import CatalogTypes

TEMP_FILE_DF = './uploaded_df_%s.temp'
TEMP_FILE_EXT = './uploaded_ext_%s.temp'


class EarthquakeData:
    """Internal representation of uploaded catalog data."""

    def __init__(self, catalog_type, data):
        self.catalog_type = catalog_type
        self.data = data

    def get_datetime(self):
        """Returns a pandas Series with the datetimes for each of the
        earthquakes in the uploaded data.
        """
        return self.data['DATETIME']


class OtaniemiEarthquakeData(EarthquakeData):
    """Internal representation of the Otaniemi catalog data.
    """

    def __init__(self, data):
        EarthquakeData.__init__(CatalogTypes.CSV_EXT, data)

    def get_datetime(self):
        return self.data['TIME_UTC']


class BaselEarthquakeData(EarthquakeData):
    """Internal representation of the Basel catalog data.
    """

    def __init__(self, data):
        EarthquakeData.__init__(CatalogTypes.DAT_EXT, data)

    def get_datetime(self):
        return self.data['SourceDateTime']


class FMEarthquakeData(EarthquakeData):
    """Internal representation of the FM catalog data.
    """

    def __init__(self, data):
        data['DATETIME'] = data.apply(
            lambda x: datetime(
                int(x['YEAR']),
                int(x['MONTH']),
                int(x['DAY']),
                int(x['HOUR']),
                int(x['MINUTE']),
                int(x['SECOND'])
            ), axis=1)
        EarthquakeData.__init__(CatalogTypes.SCEDC_EXT, data)


class QTMEarthquakeData(EarthquakeData):
    """Internal representation of the QTM catalog data.
    """

    def __init__(self, data):
        data['DATETIME'] = data.apply(
            lambda x: datetime(
                int(x['YEAR']),
                int(x['MONTH']),
                int(x['DAY']),
                int(x['HOUR']),
                int(x['MINUTE']),
                int(x['SECOND'])
            ), axis=1)
        EarthquakeData.__init__(CatalogTypes.HYPO_EXT, data)


EXTENSIONS = {
    CatalogTypes.CSV_EXT: OtaniemiEarthquakeData,
    CatalogTypes.DAT_EXT: BaselEarthquakeData,
    CatalogTypes.HYPO_EXT: QTMEarthquakeData,
    CatalogTypes.SCEDC_EXT: FMEarthquakeData
}


# Cache timeout set to 10 hours.
@cache.memoize(timeout=36000)
def get_earthquake_data(session_id):
    """Return uploaded data saved on the server as an EarthquakeData object
    and remove temporary files holding the data. The dataframe contained by
    the object is empty if no data has been uploaded.

    Keyword arguments:
    session_id -- ID of the current session
    """
    try:
        if os.path.exists(TEMP_FILE_EXT % session_id):
            with open(TEMP_FILE_EXT % session_id, 'r') as file_in:
                extension = file_in.read()
            data = pd.read_json(TEMP_FILE_DF % session_id)

            os.remove(TEMP_FILE_DF % session_id)
            os.remove(TEMP_FILE_EXT % session_id)

            catalog_type = CatalogTypes(extension)
            data_wrapper = EXTENSIONS[catalog_type]
            return data_wrapper(data)

        return EarthquakeData('', pd.DataFrame())

    except Exception as ex:
        print(os.path.basename(__file__), ':', ex)
        return EarthquakeData('', pd.DataFrame())


def get_datetimes(df):
    """Extract datetimes from a DataFrame.

    Returns a pandas Series object that contains datetimes
    parsed from the given DataFrame.

    Keyword arguments:
    df -- A pandas DataFrame that contains the following columns:
        YEAR, MONTH, DAY, HOUR, MINUTE, SECOND
    """
    return df.apply(
        lambda x: datetime(
            int(x['YEAR']),
            int(x['MONTH']),
            int(x['DAY']),
            int(x['HOUR']),
            int(x['MINUTE']),
            int(x['SECOND'])
        ), axis=1)
