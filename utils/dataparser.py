import base64
import re

from app import cache
from utils import earthquake_data
from utils.parsers import qtm_parse, fm_parse, basel_parse, otaniemi_parse
from utils.catalog_types import CatalogTypes

PARSERS = {
    CatalogTypes.HYPO_EXT: qtm_parse,
    CatalogTypes.SCEDC_EXT: fm_parse,
    CatalogTypes.CSV_EXT: otaniemi_parse,
    CatalogTypes.DAT_EXT: basel_parse
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
    """Return file extension of the given file or raise an exception
    if there is none.

    Keyword arguments:
    filename -- Name of the file
    """
    extension_regex = re.compile(r'[.]\w+')
    matches = extension_regex.findall(filename)

    if len(matches) == 0:
        raise Exception('Not a recognised file type: {}'.format(filename))

    return matches[-1]


def get_parser(extension):
    """Return parser based on given extension or raise exception if
    no such parser exists for the given extension.

    Keyword arguments:
    extension -- Extension identifying the catalog type to parse
    """
    parser = PARSERS.get(extension, None)
    if parser is None:
        raise Exception('Could not parse file of type: {}'.format(extension))

    return parser


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
