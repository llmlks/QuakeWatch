import base64
import io
import json

import pandas as pd

from app import cache
from utils import earthquake_data

HYPO_EXT = '.hypo'


def parse_contents(contents, filename, session_id):
    """Parse the input into a dataframe using correct parser
    depending on the file extension, saving the results.

    Keyword arguments:
    contents -- The contents of the uploaded file as a binary string
    filename -- Name of the uploaded file
    session_id -- ID of the current session
    """
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)

    if filename.endswith(HYPO_EXT):
        eq_data = qtm_parse(decoded)
        extension = HYPO_EXT

    save_uploaded_data(session_id, eq_data, extension)
    return eq_data


def qtm_parse(decoded_contents):
    """Return a dataframe containing tha parsed QTM catalog.

    Keyword arguments:
    decoded_contents -- Decoded contents of uploaded file
    """
    df = pd.read_table(
        io.StringIO(decoded_contents.decode('utf-8')),
        sep=r'\s+'
    )
    return df


def save_uploaded_data(session_id, data, extension):
    """Empty cache for current session, save the new data and
    file extension to file.

    Keyword arguments:
    session_id -- ID of the current session
    data -- Pandas dataframe containing the uploaded data
    extesions -- File extension of the uploaded file
    """
    cache.delete_memoized(earthquake_data.get_earthquake_data, session_id)

    data.to_json(earthquake_data.TEMP_FILE_DF % session_id)

    with open(earthquake_data.TEMP_FILE_EXT % session_id, 'w') as file_out:
        file_out.write(extension)
