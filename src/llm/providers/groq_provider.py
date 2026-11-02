import os

import src.config.settings  # noqa: F401  (loads .env and Streamlit secrets)

DEFAULT_MODEL = "llama-3.3-70b-versatile"

# Models that cannot chat (speech, safety filters, embeddings).
NOT_CHAT = ("whisper", "tts", "guard", "embed", "playai", "orpheus", "prompt-guard")

# Larger general models first.
PREFERRED = ("versatile", "70b", "120b", "gpt-oss", "llama-4", "llama", "qwen", "kimi", "mixtral", "gemma")


def pick_chat_model(model_ids):
    """
    Choose the best chat model from the ids Groq says the key can use.
    """

    chat = [m for m in model_ids if not any(word in m.lower() for word in NOT_CHAT)]

    if not chat:
        return None

    def rank(model_id):
        name = model_id.lower()
        for position, word in enumerate(PREFERRED):
            if word in name:
                return position, name
        return len(PREFERRED), name

    return sorted(chat, key=rank)[0]


def is_missing_model(error):

    text = str(error).lower()

    return "model_not_found" in text or "decommissioned" in text or "does not exist" in text


class GroqProvider:

    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.model = os.getenv("GROQ_MODEL") or DEFAULT_MODEL

    def generate_response(self, prompt: str) -> str:

        if not self.api_key:
            raise RuntimeError(
                "Groq API key not configured. "
                "Please set GROQ_API_KEY in .env"
            )

        try:
            from groq import Groq

            client = Groq(api_key=self.api_key)

            try:
                return self._chat(client, prompt)
            except Exception as error:
                # Groq retires models often; switch to one that still exists.
                if not is_missing_model(error):
                    raise
                replacement = pick_chat_model([m.id for m in client.models.list().data])
                if not replacement or replacement == self.model:
                    raise
                self.model = replacement
                return self._chat(client, prompt)

        except Exception as error:

            raise RuntimeError(
                f"Groq generation failed: {error}"
            ) from error

    def _chat(self, client, prompt):

        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
        )

        return response.choices[0].message.content
