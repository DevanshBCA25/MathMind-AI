from typing import Dict, List


class ConversationMemory:
    """
    Lightweight conversation memory for RAG conversations.
    """

    def __init__(self, max_messages: int = 10):

        self.max_messages = max_messages
        self.messages: List[Dict[str, str]] = []

    def add_user_message(
        self,
        message: str,
    ):

        self.messages.append(
            {
                "role": "user",
                "content": message,
            }
        )

        self._trim()

    def add_assistant_message(
        self,
        message: str,
    ):

        self.messages.append(
            {
                "role": "assistant",
                "content": message,
            }
        )

        self._trim()

    def add_message(
        self,
        role: str,
        content: str,
    ):

        self.messages.append(
            {
                "role": role,
                "content": content,
            }
        )

        self._trim()

    def get_messages(self):

        return self.messages.copy()

    def get_recent_messages(
        self,
        count: int = 5,
    ):

        return self.messages[-count:]

    def get_formatted_history(self):

        history = []

        for message in self.messages:

            role = message["role"].capitalize()

            content = message["content"]

            history.append(
                f"{role}: {content}"
            )

        return "\n".join(history)

    def clear(self):

        self.messages = []

    def is_empty(self):

        return len(self.messages) == 0

    def _trim(self):

        if len(self.messages) > self.max_messages:

            self.messages = self.messages[
                -self.max_messages:
            ]