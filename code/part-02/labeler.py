"""Ask a local model to name the attack category, then check its homework.

Every chapter so far has used the corpus's category labels as if they were
free. They are not - somebody labeled those 93 attacks by hand. This asks
whether a model can do that job, and measures how often it is wrong.
"""

import json
import sys
import time

import requests

from corpus import category_path

CATEGORIES = [
    "direct_injection",
    "persona_replacement",
    "jailbreak",
    "system_extraction",
    "encoding_obfuscation",
    "token_smuggling",
    "many_shot",
    "indirect_injection",
]

# Short definitions matter more than you'd expect. Without them the model
# invents its own idea of what each word means.
DEFINITIONS = """\
direct_injection    - tells the model to ignore or replace its instructions
persona_replacement - gives the model a new name/character with no rules
jailbreak           - unlocks a "mode" or uses fiction/hypotheticals to bypass rules
system_extraction   - tries to make the model reveal its own system prompt
encoding_obfuscation- hides the payload in base64, rot13, unicode, morse, etc.
token_smuggling     - uses invisible characters or fake chat/template tags
many_shot           - fills the prompt with fake examples of the model complying
indirect_injection  - payload hidden in a document/email/webpage the model reads"""

# The obvious first attempt: name the categories, define each in a line.
PROMPT = """You are classifying prompt-injection attacks for a security dataset.

Categories:
{definitions}

Reply with ONLY the category name, nothing else.

Attack:
{attack}"""

# The other six definitions, WITHOUT direct_injection and
# indirect_injection. Leaving those two in was a real bug: their one-line
# definitions are wording-based ("tells the model to ignore its
# instructions"), which silently contradicts v2's delivery-based rule and
# cancels it out. Measured cost of that contradiction: 11 accuracy points.
OTHER_DEFINITIONS = "\n".join(
    line for line in DEFINITIONS.splitlines()
    if not line.startswith(("direct_injection", "indirect_injection"))
)

# The second attempt, after measuring the first. The difference is the
# explicit decision RULE for the distinction the model kept getting wrong:
# direct vs indirect is about how the text was DELIVERED, not how it reads.
PROMPT_V2 = """You are classifying prompt-injection attacks.

THE KEY DISTINCTION:
- direct_injection: the USER typed the malicious instruction themselves,
  straight into the chat.
- indirect_injection: the malicious instruction is EMBEDDED inside content
  (a document, email, webpage, review, calendar entry, code comment) that
  the user innocently asked the assistant to read, summarize or translate.

DECIDE BY DELIVERY, NOT BY WORDING. If the payload sits inside quoted or
attached content the user asked to be processed, it is indirect_injection,
no matter what the payload itself says.

Other categories:
{definitions}

Reply with ONLY the category name, nothing else.

Attack:
{attack}"""


def label(attack_text, model, prompt=PROMPT, definitions=DEFINITIONS):
    """Ask the model for one category name."""
    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": model,
            "messages": [{"role": "user", "content": prompt.format(
                definitions=definitions, attack=attack_text)}],
            "stream": False,
            "options": {"temperature": 0},
        },
        timeout=300,
    )
    raw = response.json()["message"]["content"].strip().lower()

    # The model may add punctuation or a sentence, so we look for a category
    # name anywhere in its answer.
    #
    # Check LONGEST names first. This is not a style choice - it is a bug
    # fix. "indirect_injection" contains "direct_injection" as a substring,
    # so checking in list order silently turned every correct
    # "indirect_injection" answer into "direct_injection". That one line
    # made the category score 0/9 in every run, and it was the measuring
    # instrument that was broken, not the model.
    for category in sorted(CATEGORIES, key=len, reverse=True):
        if category in raw:
            return category
    return "UNPARSEABLE"


def load_corpus():
    """Load every attack together with its true, human-assigned category."""
    rows = []
    for category in CATEGORIES:
        with open(category_path(category), encoding="utf-8") as f:
            for attack in json.load(f):
                rows.append({"text": attack["text"], "truth": category})
    return rows


def run(model, prompt=PROMPT, tag=""):
    rows = load_corpus()
    started = time.time()
    for i, row in enumerate(rows, start=1):
        defs = OTHER_DEFINITIONS if prompt is PROMPT_V2 else DEFINITIONS
        row["predicted"] = label(row["text"], model, prompt, defs)
        row["correct"] = row["predicted"] == row["truth"]
        print("." if row["correct"] else "X", end="", flush=True)
        if i % 40 == 0:
            print()
    elapsed = time.time() - started

    correct = sum(r["correct"] for r in rows)
    print(f"\n\nmodel     : {model}")
    print(f"accuracy  : {correct}/{len(rows)}  ({correct / len(rows):.0%})")
    print(f"time      : {elapsed:.0f}s  ({elapsed / len(rows):.1f}s per attack)")

    print("\nper category:")
    for category in CATEGORIES:
        sub = [r for r in rows if r["truth"] == category]
        hit = sum(r["correct"] for r in sub)
        print(f"  {category:22} {hit:2}/{len(sub)}")

    out = f"labels_{model.replace(':', '_').replace('/', '_')}{tag}.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)
    print(f"\nsaved {out}")
    return rows


if __name__ == "__main__":
    model = sys.argv[1] if len(sys.argv) > 1 else "qwen2.5:7b-instruct"
    # pass "v2" as the second argument to use the improved prompt
    if len(sys.argv) > 2 and sys.argv[2] == "v2":
        run(model, PROMPT_V2, tag="_v2")
    else:
        run(model)
