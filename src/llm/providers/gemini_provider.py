import os

from dotenv import load_dotenv

load_dotenv()


class GeminiProvider:

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = os.getenv(
            "GEMINI_MODEL",
            "gemini-2.0-flash",
        )

    def generate_response(self, prompt: str) -> str:

        if not self.api_key:
            raise RuntimeError(
                "Gemini API key not configured. "
                "Please set GEMINI_API_KEY in .env"
            )

        try:
            from google import genai

            client = genai.Client(
                api_key=self.api_key
            )

            response = client.models.generate_content(
                model=self.model,
                contents=prompt,
            )

            if not response.text:
                raise RuntimeError(
                    "Gemini returned an empty response."
                )

            return response.text

        except Exception as error:

            raise RuntimeError(
                f"Gemini generation failed: {error}"
            ) from error