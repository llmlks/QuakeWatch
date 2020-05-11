import io
import datetime
import pandas as pd


def qtm_parse(contents):
    """Return a dataframe containing the parsed QTM catalog.

    Keyword arguments:
    contents -- Decoded contents of uploaded file
    """
    df = pd.read_table(
        io.StringIO(contents),
        sep=r'\s+'
    )
    return df


def fm_parse(contents):
    """Return a dataframe containing the parsed FM catalog.

    Keyword arguments:
    contents -- Decoded contents of the uploaded file
    """
    df = pd.read_table(
        io.StringIO(contents),
        sep=r'\s+',
        names=[
            'YEAR', 'MONTH', 'DAY', 'HOUR', 'MINUTE', 'SECOND', 'EVENTID',
            'LATITUDE', 'LONGITUDE', 'DEPTH', 'MAGNITUDE', 'STRIKE', 'DIP',
            'RAKE', 'FPUncert', 'AFPUncert', 'FIRSTMOTIONS', 'MISFIT',
            'SPAMPRATIOS', 'AVGLOGMISFIT', 'QUALITY'
        ]
    )
    return df


def otaniemi_parse(contents):
    """Return a dataframe containing the parsed Otaniemi catalog.

    Keyword arguments:
    contents -- Decoded contents of the uploaded file
    """
    df = pd.read_csv(
        io.StringIO(contents),
        sep=';',
        converters={
            'EASTING [m]': convert_to_float,
            'NORTHING [m]': convert_to_float,
            'M_HEL': convert_to_float,
            'M_W': convert_to_float
        }
    )
    return df


def basel_parse(contents):
    """Return a dataframe containing the parsed Basel catalog.

    Keyword arguments:
    contents -- Decoded contents of the uploaded file
    """

    rows = list(filter(
        lambda row: not row.startswith('#') and not len(row) == 0,
        contents.split('\n')
    ))

    df = pd.read_csv(
        io.StringIO('\n'.join(rows)),
        sep=r'\s+',
        names=[
            'SourceDateTime', 'LSrc', 'LATITUDE', 'LONGITUDE', 'Dep', 'X', 'Y',
            'Z', 'Mwx', 'MwGEL', 'MwSED', 'MLSED', 'ID', 'TpID', 'GELID',
            'SEDID'
        ],
        na_values=[
            '-.--', '-.-', '------', '--.-----', '-.-----',
            '---', '---------', '------',  '----'
        ]
    )
    return df


def fencat_parse(contents):
    """Return a dataframe containing the parsed FENCAT catalog.

    Keyword arguments:
    contents -- Decoded contents of the uploaded file
    """
    rows = list(map(
        lambda row: '\t'.join([
            row[:3], row[3], row[4:8], row[8:10], row[10:12], row[12],
            row[13:15], row[15:17], row[17:21], row[21:28], row[28:36],
            row[36], row[37], row[38:41], row[41], row[42:45], row[45:47],
            row[47:50], row[50:52], row[52:55], row[55:57], row[66:70],
            row[70], row[71:74], row[74:77], row[77], '', '', ''
        ]),
        filter(lambda r: len(r.strip()) == 78, contents.split('\n'))
    ))

    rows.extend(list(map(
        lambda row: '\t'.join([
            row[:3], row[3], row[4:8], row[8:10], row[10:12], row[12],
            row[13:15], row[15:17], row[17:21], row[21:28], row[28:36],
            row[36], row[37], row[38:41], row[41], row[42:45], row[45:47],
            row[47:50], row[50:52], row[52:55], row[55:57], row[66:70],
            row[70], row[71:74], row[74:77], row[77], row[78:82],
            row[83:86], row[86:]
        ]),
        filter(lambda r: len(r.strip()) == 91, contents.split('\n'))
    )))

    df = pd.read_table(
        io.StringIO('\n'.join(rows)),
        sep='\t',
        names=[
            'SOURCE', 'QUESTIONABLE ORIGIN', 'YEAR', 'MONTH', 'DAY', 'STATUS',
            'HOUR', 'MINUTE', 'SECOND', 'LATITUDE', 'LONGITUDE',
            'TIME UNCERTAINTY', 'LOCATION UNCERTAINTY', 'DEPTH',
            'DEPTH ID CODE', 'MAGNITUDE', 'MAG SCALE', 'MAGNITUDE2',
            'MAG2 SCALE', 'MAGNITUDE3', 'MAG3 SCALE', 'MAX INTENSITY',
            'INTENSITY STATUS', 'MACROSEISMIC REF', 'MEAN RADIUS', 'REGION',
            'NUM STATIONS', 'MAX AZIMUTH GAP', 'MIN STATION DIST'
        ],
        na_values=['  ', '   ', '    ']
    ).reset_index().rename(columns={'index': 'ID'})
    return df


def convert_to_float(x):
    """Convert a string to float, replacing commas with points."""
    return float(x.replace(',', '.'))
