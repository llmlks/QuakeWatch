from components import data_table


def get_layout(session_id):
    """Return layout for the data view.

    Keywords arguments:
    session_id -- ID of the current session
    """
    return data_table.get_component(session_id)
