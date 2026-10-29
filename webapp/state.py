"""
Per-visitor state, kept in NiceGUI's user storage.
"""

import re
from datetime import datetime

from nicegui import app

from src.config.settings import DEFAULT_PROVIDER, has_api_key

PROVIDERS = ['Gemini', 'Groq', 'OpenAI', 'Ollama']

MAX_HISTORY = 200


def provider_options():
    """
    Providers with an API key first; labels show whether each is ready.
    """

    ordered = sorted(
        PROVIDERS,
        key=lambda p: (p == 'Ollama', not has_api_key(p), p != DEFAULT_PROVIDER),
    )

    def label(provider):
        if provider == 'Ollama':
            return 'Ollama (local only)'
        return provider if has_api_key(provider) else f'{provider} (no key)'

    return {provider: label(provider) for provider in ordered}


def get_provider():

    options = list(provider_options())
    provider = app.storage.user.get('provider')

    return provider if provider in options else options[0]


def set_provider(provider):

    app.storage.user['provider'] = provider


def plain_text(value):
    """
    Make LaTeX results readable in the history table and CSV.
    """

    text = str(value)

    if '\\' not in text:
        return text

    replacements = [
        (r'\\begin\{matrix\}', '['), (r'\\end\{matrix\}', ']'), (r'\\\\', '; '), (r'\s*&\s*', ', '),
        (r'\\sqrt\{([^{}]*)\}', r'√(\1)'), (r'\\frac\{([^{}]*)\}\{([^{}]*)\}', r'(\1)/(\2)'),
        (r'\\(left|right)', ''), (r'\\times', '×'), (r'\\cdot', '·'), (r'\\(quad|,|;)', ' '),
        (r'\\text\{([^{}]*)\}', r'\1'), (r'\\([a-zA-Z]+)', r'\1'), (r'[{}]', ''),
    ]

    for pattern, replacement in replacements:
        text = re.sub(pattern, replacement, text)

    return re.sub(r'\s+', ' ', text).strip()


def add_history(module, operation, input_data, result):

    history = app.storage.user.setdefault('history', [])

    history.append({
        'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'module': module,
        'operation': operation,
        'input': plain_text(input_data),
        'result': plain_text(result)[:300],
    })

    del history[:-MAX_HISTORY]


def get_history():

    return list(app.storage.user.get('history', []))


def clear_history():

    app.storage.user['history'] = []


# Vector databases cannot be serialised into user storage, so they are
# kept in memory, keyed by the visitor's browser id. Only the most
# recent visitors are kept to bound memory use.
_documents = {}

MAX_DOCUMENT_USERS = 20


def _browser_id():

    return app.storage.browser.get('id')


def set_documents(vector_db, names):

    _documents.pop(_browser_id(), None)
    _documents[_browser_id()] = {'db': vector_db, 'names': names}

    while len(_documents) > MAX_DOCUMENT_USERS:
        _documents.pop(next(iter(_documents)))


def get_documents():

    return _documents.get(_browser_id())


def clear_documents():

    _documents.pop(_browser_id(), None)
