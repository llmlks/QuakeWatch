import os
import json
from datetime import datetime

import pandas as pd
from pyproj import Proj
from app import cache
from utils.catalog_types import CatalogTypes
from utils.dateutils import get_datetime

TEMP_FILE_DF = './uploaded_df_%s.temp'
TEMP_FILE_EXT = './uploaded_ext_%s.temp'
PROJECTION = Proj(3879)


class EarthquakeData:
    """Internal representation of uploaded catalog data."""

    def __init__(self, catalog_type, data):
        self.catalog_type = catalog_type
        self.data = data

    def get_datetimes(self):
        """Returns a pandas Series with the datetimes for each of the
        earthquakes in the uploaded data.
        """
        return self.data['DATETIME']

    def get_latitudes(self):
        """Returns a pandas Series with the latitude for each of the
        earthquakes in the uploaded data.
        """
        return self.data['LATITUDE']

    def get_longitudes(self):
        """Returns a pandas Series with the longitude for each of the
        earthquakes in the uploaded data.
        """
        return self.data['LONGITUDE']


class OtaniemiEarthquakeData(EarthquakeData):
    """Internal representation of the Otaniemi catalog data.
    """

    def __init__(self, data):
        """Parse datetime string to datetime object and
        transform UTM coordinates to latitudes and longitudes.
        """
        data['TIME_UTC'] = data['TIME_UTC'].apply(
            lambda x: datetime.strptime(x, r'%Y-%m-%dT%H:%M:%S.%fZ')
        )

        lat_longs = list(map(
            lambda x: PROJECTION(x[0], x[1], inverse=True),
            list(zip(
                data['EASTING [m]'].apply(
                    lambda y: float(y.replace(',', '.'))
                ).to_numpy(),
                data['NORTHING [m]'].apply(
                    lambda y: float(y.replace(',', '.'))
                ).to_numpy()
            ))
        ))

        data['LATITUDE'] = pd.Series(list(map(lambda x: x[0], lat_longs)))
        data['LONGITUDE'] = pd.Series(list(map(lambda x: x[1], lat_longs)))

        EarthquakeData.__init__(self, CatalogTypes.CSV_EXT, data)

    def get_datetimes(self):
        return self.data['TIME_UTC']


class BaselEarthquakeData(EarthquakeData):
    """Internal representation of the Basel catalog data.
    """

    def __init__(self, data):
        data['SourceDateTime'] = data['SourceDateTime'].apply(
            lambda x: datetime.strptime(x, r'%Y-%m-%dT%H:%M:%S.%f')
        )
        EarthquakeData.__init__(self, CatalogTypes.DAT_EXT, data)

    def get_datetimes(self):
        return self.data['SourceDateTime']

    def get_latitudes(self):
        return self.data['Lat']

    def get_longitudes(self):
        return self.data['Lon']


class FMEarthquakeData(EarthquakeData):
    """Internal representation of the FM catalog data.
    """

    def __init__(self, data):
        data['DATETIME'] = data.apply(
            lambda x: get_datetime(
                int(x['YEAR']),
                int(x['MONTH']),
                int(x['DAY']),
                int(x['HOUR']),
                int(x['MINUTE']),
                x['SECOND']
            ), axis=1)
        EarthquakeData.__init__(self, CatalogTypes.SCEDC_EXT, data)


class QTMEarthquakeData(EarthquakeData):
    """Internal representation of the QTM catalog data.
    """

    def __init__(self, data):
        data['DATETIME'] = data.apply(
            lambda x: get_datetime(
                int(x['YEAR']),
                int(x['MONTH']),
                int(x['DAY']),
                int(x['HOUR']),
                int(x['MINUTE']),
                x['SECOND']
            ), axis=1)
        EarthquakeData.__init__(self, CatalogTypes.HYPO_EXT, data)


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
