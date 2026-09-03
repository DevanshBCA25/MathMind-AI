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

        return self.providers[
            provider
        ].generate_response(
            prompt.strip()
        )

    def get_available_providers(self):

        return list(
            self.providers.keys()
        )