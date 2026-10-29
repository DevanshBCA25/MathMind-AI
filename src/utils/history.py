"""
Per-user calculation history.

History is kept in the user's Streamlit session, so on a shared
deployment every visitor sees only their own work. Outside Streamlit
(tests, scripts) an in-memory list is used instead.
"""

_fallback_history = []

HISTORY_KEY = "mathmind_history"

MAX_RECORDS = 200


def _store():

    try:
        import streamlit as st
        from streamlit.runtime.scriptrunner import get_script_run_ctx

        if get_script_run_ctx() is None:
            return _fallback_history

        if HISTORY_KEY not in st.session_state:
            st.session_state[HISTORY_KEY] = []

        return st.session_state[HISTORY_KEY]

    except Exception:
        return _fallback_history


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
