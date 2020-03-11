import base64
import io
import json

import pandas as pd

from app import cache
from utils import earthquake_data
from utils.parsers import qtm_parse, fm_parse, basel_parse, otaniemi_parse

HYPO_EXT = '.hypo'
SCEDC_EXT = '.scedc'
CSV_EXT = '.csv'
DAT_EXT = '.dat'
PARSERS = {
    HYPO_EXT: qtm_parse,
    SCEDC_EXT: fm_parse,
    CSV_EXT: otaniemi_parse,
    DAT_EXT: basel_parse
}


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

    file_extension = get_file_extension(filename)
    parser = get_parser(file_extension)

    eq_data = parser(decoded)

    save_uploaded_data(session_id, eq_data, file_extension)
    return eq_data


def get_file_extension(filename):
    """Return file extension based on the given filename or raise
    an exception if the file type is not one of the accepted ones.

    Keyword arguments:
    filename -- Name of the file, including file extension
    """
    if filename.endswith(HYPO_EXT):
        return HYPO_EXT
    elif filename.endswith(SCEDC_EXT):
        return SCEDC_EXT
    elif filename.endswith(CSV_EXT):
        return CSV_EXT
    elif filename.endswith(DAT_EXT):
        return DAT_EXT
    else:
        print('Not a recognised file type:', filename)
        raise Exception()


def get_parser(extension):
    """Return correct parser based on given extension.

    Keyword arguments:
    extension -- Extension identifying the catalog type to parse
    """
    return PARSERS.get(extension, None)


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
