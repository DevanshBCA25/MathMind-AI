SYSTEM_PROMPT = """
You are MathMind AI.

You are an AI Mathematics Tutor.

Always explain answers step by step.

Use Markdown formatting.

Be concise and accurate.
"""

# How many earlier messages are sent to the model as context.
CONTEXT_MESSAGES = 10


def build_chat_prompt(messages):
    """
    Turn a conversation into one prompt so every provider sees the
    system prompt and the recent history.
    """

    lines = [SYSTEM_PROMPT.strip(), "", "Conversation so far:"]

    for message in messages[-CONTEXT_MESSAGES:]:

        speaker = (
            "Student"
            if message["role"] == "user"
            else "MathMind"
        )

        lines.append(f"{speaker}: {message['content']}")

    lines.append("")
    lines.append(
        "Reply to the student's last message as MathMind. "
        "Write formulas in LaTeX between $ signs."
    )

    return "\n".join(lines)
