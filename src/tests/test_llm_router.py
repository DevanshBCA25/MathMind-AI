import pytest

from src.llm import router as router_module
from src.llm.router import LLMRouter


class FakeProvider:

    def __init__(self, failures, error="503 UNAVAILABLE"):
        self.failures = failures
        self.error = error
        self.calls = 0

    def generate_response(self, prompt):
        self.calls += 1
        if self.calls <= self.failures:
            raise RuntimeError(self.error)
        return "answer"


@pytest.fixture
def router(monkeypatch):
    monkeypatch.setattr(router_module, "RETRY_DELAY_SECONDS", 0)
    monkeypatch.setattr(router_module, "has_api_key", lambda p: p in ("Gemini", "Groq"))
    return LLMRouter()


def test_busy_model_is_retried(router):

    router.providers["Gemini"] = FakeProvider(failures=2)

    assert router.ask("Gemini", "hi") == "answer"
    assert router.providers["Gemini"].calls == 3


def test_busy_model_falls_back_to_another_provider(router):

    router.providers["Gemini"] = FakeProvider(failures=99)
    router.providers["Groq"] = FakeProvider(failures=0)

    answer = router.ask("Gemini", "hi")

    assert answer.startswith("answer")
    assert "Groq answered" in answer


def test_permanent_errors_are_not_retried(router):

    router.providers["Gemini"] = FakeProvider(failures=99, error="API key not valid")

    with pytest.raises(RuntimeError):
        router.ask("Gemini", "hi")

    assert router.providers["Gemini"].calls == 1
