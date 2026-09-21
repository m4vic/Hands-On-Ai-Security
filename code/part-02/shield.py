"""The shield: decide whether to let a message reach the model at all.

The verifier looks at what came OUT. The shield looks at what goes IN,
and it has to make its call before the model has said anything.
"""

import base64
import re
import unicodedata

# Level 1: clean the input up so hiding tricks stop working.
ZERO_WIDTH = ["​", "‌", "‍", "﻿"]


def normalize(text):
    """Strip the tricks from Chapter 7's obfuscation categories."""
    # Remove invisible characters used for token smuggling.
    for char in ZERO_WIDTH:
        text = text.replace(char, "")

    # Fold unicode lookalikes (ｉｇｎｏｒｅ, ɪɢɴᴏʀᴇ) back to plain letters.
    text = unicodedata.normalize("NFKC", text)

    # If any chunk looks like base64, decode it and append the result so
    # the pattern check below can see what was hiding inside.
    for chunk in re.findall(r"[A-Za-z0-9+/]{16,}={0,2}", text):
        try:
            decoded = base64.b64decode(chunk).decode("utf-8")
            text += " " + decoded
        except Exception:
            pass   # not base64 after all, ignore it

    return text


# Level 2: patterns that suggest someone is talking to the system
# rather than to the bank's customers.
ATTACK_PATTERNS = [
    "ignore all previous", "ignore your previous", "ignore previous",
    "disregard your prior", "disregard the above", "disregard previous",
    "forget the instructions", "forget your rules",
    "system override", "instruction override",
    "you are now", "act as", "pretend you are", "roleplay as",
    "developer mode", "evil mode", "unrestricted mode",
    "system prompt", "your instructions", "initial prompt",
    "no restrictions", "no content policy", "without restrictions",
]


def blocked(message, level=2):
    """Return (should_block, reason)."""
    text = normalize(message).lower()

    if level >= 2:
        for pattern in ATTACK_PATTERNS:
            if pattern in text:
                return True, f"matched {pattern!r}"

    return False, "clean"


if __name__ == "__main__":
    import json

    from corpus import category_path

    # The shield reads the INPUT text, so we never need the model here.
    with open("results.json", encoding="utf-8") as f:
        attacks = json.load(f)
    with open(category_path("benign"), encoding="utf-8") as f:
        benign = json.load(f)

    for level in (1, 2):
        caught = sum(blocked(a["attack"], level)[0] for a in attacks)
        false_alarms = sum(blocked(b["text"], level)[0] for b in benign)
        print(f"L{level}: attacks blocked {caught:3}/{len(attacks)}"
              f" ({caught / len(attacks):4.0%})"
              f"   benign blocked {false_alarms:2}/{len(benign)}"
              f" ({false_alarms / len(benign):4.0%})")

    print("\nper category (level 2):")
    for category in dict.fromkeys(a["category"] for a in attacks):
        rows = [a for a in attacks if a["category"] == category]
        caught = sum(blocked(a["attack"])[0] for a in rows)
        print(f"  {category:22} {caught:2} / {len(rows)}")
