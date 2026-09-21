"""Talk to a local model. This is Chapter 6's curl request, written in Python."""

import requests

# Any model you have pulled locally will work. This one is "abliterated",
# meaning its safety training has been stripped out. We want that on purpose:
# it keeps the model's own refusals from doing our shield's job for us.
MODEL = "mannix/llama3.1-8b-abliterated:q5_K_M"


def ask(system_prompt, user_message):
    """Send one system prompt and one user message. Return the reply text."""
    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            "stream": False,
            # temperature 0 asks for the most predictable reply it can give
            "options": {"temperature": 0},
        },
        timeout=300,
    )
    return response.json()["message"]["content"]


if __name__ == "__main__":
    print(ask("You are a helpful assistant.", "Say hello in one word."))
