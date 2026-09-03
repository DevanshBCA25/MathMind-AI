import os

from dotenv import load_dotenv

load_dotenv()


class OllamaProvider:

    def __init__(self):

        self.base_url = os.getenv(
            "OLLAMA_BASE_URL",
            "http://localhost:11434",
        )

        self.model = os.getenv(
            "OLLAMA_MODEL",
            "llama3.2",
        )

    def generate_response(self, prompt: str) -> str:

        try:
            import requests

            url = (
                f"{self.base_url}/api/generate"
            )

            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
            }

            response = requests.post(
                url,
                json=payload,
                timeout=120,
            )

            response.raise_for_status()

            data = response.json()

            answer = data.get(
                "response",
                "",
            )

            if not answer:
                raise RuntimeError(
                    "Ollama returned an empty response."
                )

            return answer

        except requests.exceptions.ConnectionError as error:

            raise RuntimeError(
                "Ollama is not running. "
                "Start Ollama and make sure the "
                "selected model is available."
            ) from error

        except Exception as error:

            raise RuntimeError(
                f"Ollama generation failed: {error}"
            ) from error