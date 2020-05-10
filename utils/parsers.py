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


def convert_to_float(x):
    """Convert a string to float, replacing commas with points."""
    return float(x.replace(',', '.'))
