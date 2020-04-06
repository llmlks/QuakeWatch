import io
import datetime
import pandas as pd


def qtm_parse(decoded_contents):
    """Return a dataframe containing the parsed QTM catalog.

    Keyword arguments:
    decoded_contents -- Decoded contents of uploaded file
    """
    df = pd.read_table(
        io.StringIO(decoded_contents.decode('utf-8')),
        sep=r'\s+'
    )
    return df


def fm_parse(decoded_contents):
    """Return a dataframe containing the parsed FM catalog.

    Keyword arguments:
    decoded_contents -- Decoded contents of the uploaded file
    """
    df = pd.read_table(
        io.StringIO(decoded_contents.decode('utf-8')),
        sep=r'\s+',
        names=[
            'YEAR', 'MONTH', 'DAY', 'HOUR', 'MINUTE', 'SECOND', 'EVENTID',
            'LATITUDE', 'LONGITUDE', 'DEPTH', 'MAGNITUDE', 'STRIKE', 'DIP',
            'RAKE', 'FPUncert', 'AFPUncert', 'FIRSTMOTIONS', 'MISFIT',
            'SPAMPRATIOS', 'AVGLOGMISFIT', 'QUALITY'
        ]
    )
    return df


def otaniemi_parse(decoded_contents):
    """Return a dataframe containing the parsed Otaniemi catalog.

    Keyword arguments:
    decoded_contents -- Decoded contents of the uploaded file
    """
    df = pd.read_csv(
        io.StringIO(decoded_contents.decode('utf-8')),
        sep=';',
        converters={
            'EASTING [m]': convert_to_float,
            'NORTHING [m]': convert_to_float,
            'M_HEL': convert_to_float,
            'M_W': convert_to_float
        }
    )
    return df


def basel_parse(decoded_contents):
    """Return a dataframe containing the parsed Basel catalog.

    Keyword arguments:
    decoded_contents -- Decoded contents of the uploaded file
    """

    rows = list(filter(
        lambda row: not row.startswith('#') and not len(row) == 0,
        decoded_contents.decode('utf-8').split('\n')
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
            '---', '---------', '------'
        ]
    )
    return df


def convert_to_float(x):
    """Convert a string to float, replacing commas with points."""
    return float(x.replace(',', '.'))
