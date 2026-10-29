"""
Calculation history for scripts and the command line.

The web app keeps each visitor's history in their own browser storage
(see webapp/state.py); this module is a simple in-memory store for
code that runs outside the web app.
"""

_history = []

MAX_RECORDS = 200


def _store():

    return _history


def load_history():

    return list(_store())


def save_history(record):

    history = _store()

    history.append(record)

    del history[:-MAX_RECORDS]


def clear_history():

    _store().clear()


def latest_records(limit=10):

    return load_history()[-limit:]
