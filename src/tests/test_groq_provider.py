import sys
import types

from src.llm.providers.groq_provider import GroqProvider, pick_chat_model


def test_pick_chat_model_skips_speech_and_guard_models():

    ids = ["whisper-large-v3", "llama-guard-4-12b", "llama-3.1-8b-instant", "openai/gpt-oss-120b"]

    assert pick_chat_model(ids) == "openai/gpt-oss-120b"
    assert pick_chat_model(["whisper-large-v3"]) is None


def test_retired_model_is_replaced(monkeypatch):

    used = []

    class Completions:
        def create(self, model, messages):
            used.append(model)
            if model == "old-model":
                raise Exception("Error code: 404 - model_not_found")
            message = types.SimpleNamespace(content=f"answer from {model}")
            return types.SimpleNamespace(choices=[types.SimpleNamespace(message=message)])

    class FakeGroq:
        def __init__(self, api_key):
            self.chat = types.SimpleNamespace(completions=Completions())
            self.models = types.SimpleNamespace(list=lambda: types.SimpleNamespace(
                data=[types.SimpleNamespace(id="whisper-large-v3"), types.SimpleNamespace(id="new-70b-versatile")]))

    monkeypatch.setitem(sys.modules, "groq", types.SimpleNamespace(Groq=FakeGroq))
    monkeypatch.setenv("GROQ_API_KEY", "test")
    monkeypatch.setenv("GROQ_MODEL", "old-model")

    provider = GroqProvider()

    assert provider.generate_response("hi") == "answer from new-70b-versatile"
    assert used == ["old-model", "new-70b-versatile"]
