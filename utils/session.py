import uuid

from dash import callback_context
from flask import request


def get_session_id():
    """Return the session ID from a cookie or None if not found."""
    return request.cookies.get('quakewatch_session_id')


def generate_session_id():
    """Generate a unique ID and set it as a cookie."""
    session_id = str(uuid.uuid4())
    callback_context.response.set_cookie(
       'quakewatch_session_id', session_id)
    return session_id
