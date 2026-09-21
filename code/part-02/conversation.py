"""A target that remembers. Chapter 8's target forgot everything instantly.

Every attack so far has been one message. A crescendo attack is a
staircase, and you cannot climb a staircase if the target forgets the
previous step.
"""

import requests

from llm import MODEL
from target import SYSTEM_PROMPT


class Conversation:
    """Holds the running message history for one conversation."""

    def __init__(self, system_prompt=SYSTEM_PROMPT):
        # The history starts with the system prompt and grows from there.
        self.messages = [{"role": "system", "content": system_prompt}]

    def send(self, user_message):
        """Add a user message, get the reply, remember both."""
        self.messages.append({"role": "user", "content": user_message})

        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": MODEL,
                "messages": self.messages,     # the WHOLE history, every time
                "stream": False,
                "options": {"temperature": 0},
            },
            timeout=300,
        )
        reply = response.json()["message"]["content"]

        # The model's own reply becomes part of the history too. This is
        # what lets turn 4 lean on what the model agreed to in turn 2.
        self.messages.append({"role": "assistant", "content": reply})
        return reply


if __name__ == "__main__":
    chat = Conversation()
    print(chat.send("My name is Sam."))
    print()
    print(chat.send("What did I just tell you my name was?"))
