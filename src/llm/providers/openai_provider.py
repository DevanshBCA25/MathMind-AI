import os

from dotenv import load_dotenv

load_dotenv()


class OpenAIProvider:

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv(
            "OPENAI_MODEL",
            "gpt-4o-mini",
        )

    def generate_response(self, prompt: str) -> str:

        if not self.api_key:
            raise RuntimeError(
                "OpenAI API key not configured. "
                "Please set OPENAI_API_KEY in .env"
            )

        try:
            from openai import OpenAI

            client = OpenAI(
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
                f"OpenAI generation failed: {error}"
            ) from error