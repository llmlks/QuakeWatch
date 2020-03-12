import os
import json
from datetime import datetime

import pandas as pd
from app import cache

TEMP_FILE_DF = './uploaded_df_%s.temp'
TEMP_FILE_EXT = './uploaded_ext_%s.temp'


class EarthquakeData:
    """Internal representation of uploaded catalog data."""

    def __init__(self, catalog_type, data):
        self.catalog_type = catalog_type
        self.data = data


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

            return EarthquakeData(extension, data)

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
