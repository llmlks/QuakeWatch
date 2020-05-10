import os
import json
from datetime import datetime, timedelta

import pandas as pd
import numpy as np
from pyproj import Proj
from pyproj import Geod
from app import cache
from utils.catalog_types import CatalogTypes
from utils.dateutils import get_datetime

TEMP_FILE_DF = './uploaded_df_%s.temp'
TEMP_FILE_EXT = './uploaded_ext_%s.temp'
PROJECTION = Proj(init='epsg:3879')


class EarthquakeData:
    """Internal representation of uploaded catalog data."""

    def __init__(self, catalog_type, data):
        self.catalog_type = catalog_type
        self.data = data
        self.dates = pd.Series(dtype='datetime64[ns]')
        self.column_params = {
            column: (data[column].min(), data[column].max())
            for column in data.select_dtypes(np.number)
        }

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

    def get_templateids(self):
        """Return a pandas Series with the template IDs for each of
        the earthquakes in the uploaded data.
        """
        return self.data['TEMPLATEID'].unique()

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

    def filter_by_template_id(self, template):
        """Return a new EarthquakeData object filtered to contain only events
        that have the given template.

        Keyword arguments:
        template -- The template ID to use for filtering
        """
        return EarthquakeData(
            self.catalog_type,
            self.data[self.data['TEMPLATEID'] == template]
        )

    def get_column_params(self, column_name):
        """Return column name, minimum, and maximum as tuple.

        If the column does not exist, a None value is returned.
        The same applies to non-numeric columns.

        Keyword arguments:
        column_name -- Name of the column
        """

        params = self.column_params.get(column_name)

        if params is None:
            return None

        return (column_name, params[0], params[1])

    def get_location_uncertainties(self):
        """Return the uncertainty in location for each data point."""
        return 500

    def get_map_center(self):
        """Return coordinates to use for the initial positioning of the map."""
        return [33.7, -117.3]

    def get_initial_zoom(self):
        """Return initial zoom level to use for the map."""
        return 8

    def get_weight_matrix(self, x_axis_name, y_axis_name, nbins_x, nbins_y):
        """Return weight matrix and the bins for the heatmap.

        Keyword arguments:
        x_axis_name -- Name of the x-axis
        y_axis_name -- Name of the y-axis
        nbins_x -- Number of bins used for x-axis
        nbins_y -- Number of bins used for y-axis
        """

        xcats, xbins = pd.cut(self.data[x_axis_name], nbins_x, retbins=True)
        ycats, ybins = pd.cut(self.data[y_axis_name], nbins_y, retbins=True)

        z = self.data.groupby([xcats, ycats]).size().unstack()

        xbins = pd.Series(xbins, name=x_axis_name)
        ybins = pd.Series(ybins, name=y_axis_name)
        return z, xbins, ybins

    def get_default_timedelta(self):
        """Return the default timedelta for each catalog.
        """
        if self.catalog_type == CatalogTypes.DAT_EXT:
            return timedelta(weeks=4)
        return timedelta(weeks=1)


class OtaniemiEarthquakeData(EarthquakeData):
    """Internal representation of the Otaniemi catalog data.
    """

    def __init__(self, data):
        """Parse datetime string to datetime object,
        transform UTM coordinates to latitudes and longitudes,
        and cast strings to floats, where applicable.
        """
        if 'LONGITUDE' not in data.columns:
            lat_longs = list(map(
                lambda x: PROJECTION(x[0], x[1], inverse=True),
                list(zip(
                    data['EASTING [m]'].to_numpy(),
                    data['NORTHING [m]'].to_numpy()
                ))
            ))

            data = data.assign(
                LONGITUDE=pd.Series(list(map(lambda x: x[0], lat_longs))),
                LATITUDE=pd.Series(list(map(lambda x: x[1], lat_longs)))
            )

        data.M_HEL = data.M_HEL.apply(
            lambda x: float(str(x).replace(',', '.'))
        )
        data.M_W = data.M_W.apply(
            lambda x: float(str(x).replace(',', '.'))
        )

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

    def get_templateids(self):
        return None

    def filter_by_dates(self, datemin, datemax):
        return OtaniemiEarthquakeData(
            self.data[(self.dates <= datemax) & (self.dates >= datemin)]
        )

    def filter_by_template_id(self, template):
        return None

    def get_location_uncertainties(self):
        geod = Geod(ellps='WGS84')
        error_coordinates = [
            geod.fwd(
                self.data['LATITUDE'].to_numpy(),
                self.data['LONGITUDE'].to_numpy(),
                self.data['EllipseAzimuth [deg]'].to_numpy() + x[0],
                self.data[x[1]].to_numpy()
            )
            for x in [
                (0, 'AX1 [m]'), (90, 'AX2 [m]'),
                (180, 'AX1 [m]'), (270, 'AX2 [m]')
            ]
        ]

        error_coordinates = np.array(
            [list(zip(x[0], x[1])) for x in error_coordinates]
        )

        error_coordinates = error_coordinates.reshape(
            error_coordinates.size // 2, 2
        )

        return error_coordinates

    def get_map_center(self):
        return [60.193, 24.84]

    def get_initial_zoom(self):
        return 13


class BaselEarthquakeData(EarthquakeData):
    """Internal representation of the Basel catalog data.
    """

    def __init__(self, data):
        data = data[data.LATITUDE.notnull() & data.Mwx.notnull()]

        EarthquakeData.__init__(self, CatalogTypes.DAT_EXT, data)
        self.dates = data['SourceDateTime'].apply(
            lambda x: datetime.strptime(x, r'%Y-%m-%dT%H:%M:%S.%f')
        )

    def get_eventids(self):
        return self.data['ID']

    def get_depths(self):
        return pd.to_numeric(self.data['Dep'])

    def get_magnitudes(self):
        return self.data['Mwx']

    def get_templateids(self):
        return self.data['TpID'].dropna().unique()

    def filter_by_dates(self, datemin, datemax):
        return BaselEarthquakeData(
            self.data[(self.dates <= datemax) & (self.dates >= datemin)]
        )

    def filter_by_template_id(self, template):
        return BaselEarthquakeData(
            self.data[self.data['TpID'] == template]
        )

    def get_map_center(self):
        return [47.585, 7.593]

    def get_initial_zoom(self):
        return 13


class FMEarthquakeData(EarthquakeData):
    """Internal representation of the FM catalog data.
    """

    def __init__(self, data):
        EarthquakeData.__init__(self, CatalogTypes.SCEDC_EXT, data)
        if 'DateTime' in data.columns:
            self.dates = data['DateTime']
        else:
            self.dates = data.agg(
                lambda x: get_datetime(
                    int(x['YEAR']),
                    int(x['MONTH']),
                    int(x['DAY']),
                    int(x['HOUR']),
                    int(x['MINUTE']),
                    x['SECOND']
                ), axis=1)
            self.dates.rename('DateTime', inplace=True)
            self.data = self.data.assign(DateTime=self.dates)

    def get_templateids(self):
        return None

    def filter_by_dates(self, datemin, datemax):
        return FMEarthquakeData(
            self.data[(self.dates <= datemax) & (self.dates >= datemin)]
        )

    def filter_by_template_id(self, template):
        return None


class QTMEarthquakeData(EarthquakeData):
    """Internal representation of the QTM catalog data.
    """

    def __init__(self, data):
        EarthquakeData.__init__(self, CatalogTypes.HYPO_EXT, data)
        if 'DateTime' in data.columns:
            self.dates = data['DateTime']
        else:
            self.dates = data.agg(
                lambda x: get_datetime(
                    int(x['YEAR']),
                    int(x['MONTH']),
                    int(x['DAY']),
                    int(x['HOUR']),
                    int(x['MINUTE']),
                    x['SECOND']
                ), axis=1)
            self.dates.rename('DateTime', inplace=True)
            self.data = self.data.assign(DateTime=self.dates)

    def filter_by_dates(self, datemin, datemax):
        return QTMEarthquakeData(
            self.data[(self.dates <= datemax) & (self.dates >= datemin)]
        )

    def filter_by_template_id(self, template):
        return QTMEarthquakeData(
            self.data[self.data['TEMPLATEID'] == template]
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


@cache.memoize(timeout=36000)
def get_earthquake_data_by_dates(session_id, datemin, datemax):
    eq_data = get_earthquake_data(session_id)
    return eq_data.filter_by_dates(datemin, datemax)
