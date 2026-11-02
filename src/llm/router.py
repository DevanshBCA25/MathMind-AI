import time

from src.config.settings import has_api_key

from src.llm.providers.openai_provider import (
    OpenAIProvider,
)

from src.llm.providers.gemini_provider import (
    GeminiProvider,
)

from src.llm.providers.groq_provider import (
    GroqProvider,
)

from src.llm.providers.ollama_provider import (
    OllamaProvider,
)


# Busy or rate-limited models usually recover within seconds.
RETRY_ATTEMPTS = 3
RETRY_DELAY_SECONDS = 2

TEMPORARY_ERRORS = ("503", "429", "UNAVAILABLE", "RESOURCE_EXHAUSTED", "overloaded", "high demand", "rate limit")


def is_temporary(error):

    text = str(error).lower()

    return any(marker.lower() in text for marker in TEMPORARY_ERRORS)


class LLMRouter:

    SUPPORTED_PROVIDERS = [
        "OpenAI",
        "Gemini",
        "Groq",
        "Ollama",
    ]

    def __init__(self):

        self.providers = {
            "OpenAI": OpenAIProvider(),
            "Gemini": GeminiProvider(),
            "Groq": GroqProvider(),
            "Ollama": OllamaProvider(),
        }

    def ask(
        self,
        provider: str,
        prompt: str,
    ) -> str:

        if not provider:
            raise ValueError(
                "LLM provider is required."
            )

        if provider not in self.providers:

            raise ValueError(
                f"Unsupported provider: {provider}. "
                f"Supported providers: "
                f"{', '.join(self.SUPPORTED_PROVIDERS)}"
            )

        if not prompt or not prompt.strip():

            raise ValueError(
                "Prompt cannot be empty."
            )

        try:
            return self._ask_with_retry(provider, prompt.strip())

        except Exception as error:

            if not is_temporary(error):
                raise

            # The chosen model stayed busy: let another configured
            # provider answer rather than showing an error.
            for backup in self.SUPPORTED_PROVIDERS:

                if backup in (provider, "Ollama") or not has_api_key(backup):
                    continue

                try:
                    answer = self._ask_with_retry(backup, prompt.strip(), attempts=1)
                except Exception:
                    continue

                return f"{answer}\n\n_({provider} was busy, so {backup} answered.)_"

            raise

    def _ask_with_retry(self, provider, prompt, attempts=RETRY_ATTEMPTS):

        for attempt in range(1, attempts + 1):

            try:
                return self.providers[provider].generate_response(prompt)

            except Exception as error:

                if attempt == attempts or not is_temporary(error):
                    raise

                time.sleep(RETRY_DELAY_SECONDS * attempt)

    def get_available_providers(self):

        return list(
            self.providers.keys()
        )