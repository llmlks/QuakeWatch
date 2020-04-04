import os
import json
from datetime import datetime, timedelta

import pandas as pd
import numpy as np
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
        self.dates = pd.Series(dtype='datetime64[ns]')

    def get_datetimes(self):
        """Return a pandas Series with the datetimes for each of the
        earthquakes in the uploaded data.
        """
        return self.dates

    def get_latitudes(self):
        """Returns a pandas Series with the latitude for each of the
        earthquakes in the uploaded data.
        """
        return self.data['LATITUDE']

    def get_longitudes(self):
        """Return a pandas Series with the longitude for each of the
        earthquakes in the uploaded data.
        """
        return self.data['LONGITUDE']

    def get_depths(self):
        """Return a pandas Series with the depth for each of the
        earthquakes in the uploaded data. Unit is meters.
        """
        return self.data['DEPTH'] * 1000

    def get_magnitudes(self):
        """Return a pandas Series with the local magnitude for each of
        the earthquakes in the uploaded data.
        """
        return self.data['MAGNITUDE']

    def get_eventids(self):
        """Return a pandas Series with the event IDs for each of
        the earthquakes in the uploaded data.
        """
        return self.data['EVENTID']

    def get_daterange(self):
        """Return minimum and maximum dates in the data as timestamps."""
        return self.dates.min(), self.dates.max()

    def get_data_by_daterange(self, datemin, datemax):
        """Return data filtered to contain only events that happened between
        given dates, inclusive.

        Keyword arguments:
        datemin -- Datetime object for the start of the date range
        datemax -- Datetime object for the end of the date range
        """
        return self.data[(self.dates <= datemax) & (self.dates >= datemin)]

    def filter_by_dates(self, datemin, datemax):
        """Return a new EarthquakeData object filtered to contain only events
        that happened between given dates, inclusive.

        Keyword arguments:
        datemin -- Datetime object for the start of the date range
        datemax -- Datetime object for the end of the date range
        """
        return EarthquakeData(
            self.catalog_type,
            self.data[(self.dates <= datemax) & (self.dates >= datemin)]
        )

    def get_normalized_column(self, column_name):
        """Return a numpy array containing the values from the
        given column normalized to the range [0,1].

        If the column does not exist, a None value is returned.
        No normalization is performed on columns that are not
        numeric.

        Keyword arguments:
        column_name -- Column to normalise
        """
        if column_name is None or column_name not in self.data.columns:
            return None

        column = self.data[column_name].to_numpy()

        if not np.issubdtype(column.dtype, np.number):
            return column

        if column.min() <= 0:
            column -= column.min()

        if column.max() > 1:
            column /= column.max()

        return column


class OtaniemiEarthquakeData(EarthquakeData):
    """Internal representation of the Otaniemi catalog data.
    """

    def __init__(self, data):
        """Parse datetime string to datetime object and
        transform UTM coordinates to latitudes and longitudes.
        """
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

        self.dates = data['TIME_UTC'].apply(
            lambda x: datetime.strptime(x, r'%Y-%m-%dT%H:%M:%S.%fZ')
        )

    def get_eventids(self):
        return self.data['ID']

    def get_depths(self):
        return -self.data['ALTITUDE [m]']

    def get_magnitudes(self):
        return self.data['M_HEL']

    def filter_by_dates(self, datemin, datemax):
        return OtaniemiEarthquakeData(
            self.data[(self.dates <= datemax) & (self.dates >= datemin)]
        )


class BaselEarthquakeData(EarthquakeData):
    """Internal representation of the Basel catalog data.
    """

    def __init__(self, data):
        EarthquakeData.__init__(self, CatalogTypes.DAT_EXT, data)
        self.dates = data['SourceDateTime'].apply(
            lambda x: datetime.strptime(x, r'%Y-%m-%dT%H:%M:%S.%f')
        )

    def get_eventids(self):
        return self.data['ID']

    def get_latitudes(self):
        return self.data['Lat']

    def get_longitudes(self):
        return self.data['Lon']

    def get_depths(self):
        return self.data['Dep']

    def get_magnitudes(self):
        return self.data['MLSED']

    def filter_by_dates(self, datemin, datemax):
        return BaselEarthquakeData(
            self.data[(self.dates <= datemax) & (self.dates >= datemin)]
        )


class FMEarthquakeData(EarthquakeData):
    """Internal representation of the FM catalog data.
    """

    def __init__(self, data):
        EarthquakeData.__init__(self, CatalogTypes.SCEDC_EXT, data)
        self.dates = data.apply(
            lambda x: get_datetime(
                int(x['YEAR']),
                int(x['MONTH']),
                int(x['DAY']),
                int(x['HOUR']),
                int(x['MINUTE']),
                x['SECOND']
            ), axis=1)

    def filter_by_dates(self, datemin, datemax):
        return FMEarthquakeData(
            self.data[(self.dates <= datemax) & (self.dates >= datemin)]
        )


class QTMEarthquakeData(EarthquakeData):
    """Internal representation of the QTM catalog data.
    """

    def __init__(self, data):
        EarthquakeData.__init__(self, CatalogTypes.HYPO_EXT, data)
        self.dates = data.apply(
            lambda x: get_datetime(
                int(x['YEAR']),
                int(x['MONTH']),
                int(x['DAY']),
                int(x['HOUR']),
                int(x['MINUTE']),
                x['SECOND']
            ), axis=1)

    def filter_by_dates(self, datemin, datemax):
        return QTMEarthquakeData(
            self.data[(self.dates <= datemax) & (self.dates >= datemin)]
        )


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
