import base64
import io
import pandas as pd

HYPO_EXT = '.hypo'


def parse_contents(contents, filename):
    """
    Parse the input into a dataframe using correct parser
    depending on the file extension
    """
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)

    if filename.endswith(HYPO_EXT):
        return qtm_parse(decoded)


def qtm_parse(decoded_contents):
    """
    Parse the QTM catalog
    """
    df = pd.read_table(
        io.StringIO(decoded_contents.decode('utf-8')),
        sep=r'\s+'
    )
    return df
