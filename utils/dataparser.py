import base64
import io
import pandas as pd

HYPO_EXT = '.hypo'


def parse_contents(contents, filename):
    """
    Parse the input into a dataframe using correct parser
    depending on the file extension, returning the dataframe.

    Keyword arguments:
    contents -- The contents of the uploaded file as a binary string
    filename -- Name of the uploaded file
    """
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)

    if filename.endswith(HYPO_EXT):
        return qtm_parse(decoded)


def qtm_parse(decoded_contents):
    """
    Return a dataframe containing tha parsed QTM catalog.

    Keyword arguments:
    decoded_contents -- Decoded contents of uploaded file
    """
    df = pd.read_table(
        io.StringIO(decoded_contents.decode('utf-8')),
        sep=r'\s+'
    )
    return df
