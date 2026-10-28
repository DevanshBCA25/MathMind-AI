"""
MathMind AI: start the web app.

    python main.py

Then open http://localhost:7860
"""

import os

from nicegui import ui

import webapp.pages  # noqa: F401  (registers the pages)

# Hugging Face shows a Space inside an iframe on huggingface.co, so the
# session cookie must be allowed in a cross-site frame there.
ON_HUGGING_FACE = bool(os.environ.get('SPACE_ID'))

ui.run(
    title='MathMind AI',
    favicon='🧠',
    host=os.environ.get('HOST', '0.0.0.0'),
    port=int(os.environ.get('PORT', 7860)),
    storage_secret=os.environ.get('STORAGE_SECRET', 'mathmind-ai-local-secret'),
    session_middleware_kwargs={'same_site': 'none', 'https_only': True} if ON_HUGGING_FACE else None,
    reload=False,
    show=False,
)
