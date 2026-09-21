"""Fire the benign corpus at the target and save the replies.

These are the hard negatives from Chapter 7 - ordinary questions that
happen to contain words like "ignore", "override", "bypass", "inject".
Any defense has to let these through.
"""

import json

from corpus import category_path
from target import target

def main():
    with open(category_path("benign"), encoding="utf-8") as f:
        samples = json.load(f)

    results = []
    for sample in samples:
        reply = target(sample["text"])
        results.append({"text": sample["text"], "reply": reply,
                        "tags": sample.get("tags", [])})
        print(".", end="", flush=True)

    with open("benign_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\nsaved {len(results)} benign replies")


# Without this guard, importing the file would fire 30 real model calls.
if __name__ == "__main__":
    main()
