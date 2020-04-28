import dash_table

from utils import earthquake_data


def get_component(session_id):
    """Fetch catalog data from cache and return it as a dash DataTable.

    Keywords arguments:
    session_id -- ID of the current session
    """
    eq_data = earthquake_data.get_earthquake_data(session_id)

    if eq_data is not None and eq_data.data.shape != (0, 0):
        return dash_table.DataTable(
            data=eq_data.data.to_dict('records'),
            columns=[
                {'name': i, 'id': i} for i in eq_data.data.columns
            ],
            style_table={
                'overflow': 'auto',
                'padding': '1em'
            },
            page_action='native',
            page_current=0,
            page_size=20,
            sort_action='native',
            sort_mode='single',
            sort_by=[],
            filter_action='native'
        )
    return 'No uploaded data found'
