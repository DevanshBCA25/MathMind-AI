import os

from dotenv import load_dotenv

load_dotenv()


class GroqProvider:

    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.model = os.getenv(
            "GROQ_MODEL",
            "llama-3.3-70b-versatile",
        )

    def generate_response(self, prompt: str) -> str:

        if not self.api_key:
            raise RuntimeError(
                "Groq API key not configured. "
                "Please set GROQ_API_KEY in .env"
            )

        try:
            from groq import Groq

            client = Groq(
                api_key=self.api_key
            )

            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            )

            return response.choices[0].message.content

        except Exception as error:

            raise RuntimeError(
                f"Groq generation failed: {error}"
            ) from error