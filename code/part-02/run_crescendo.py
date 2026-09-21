"""Fire the crescendo sequences, one step at a time, in a real conversation."""

import json

from corpus import category_path
from conversation import Conversation
from shield import blocked
from verifier import verify

def load_sequences():
    """Group the crescendo corpus into ordered sequences.

    Each entry carries a sequence_id like 'chem_crescendo_3'. The trailing
    number is the step order; everything before it names the sequence.
    """
    with open(category_path("crescendo"), encoding="utf-8") as f:
        steps = json.load(f)

    sequences = {}
    for step in steps:
        name, _, number = step["sequence_id"].rpartition("_")
        sequences.setdefault(name, []).append((int(number), step))

    # Sort each sequence by step number so we climb in the right order.
    return {name: [s for _, s in sorted(pairs)]
            for name, pairs in sequences.items()}


def run_sequence(name, steps):
    chat = Conversation()          # one conversation for the whole climb
    rows = []
    print(f"\n=== {name} ===")
    for i, step in enumerate(steps, start=1):
        was_blocked, reason = blocked(step["text"])
        reply = chat.send(step["text"])
        verdict = verify(reply)
        rows.append({"sequence": name, "step": i, "text": step["text"],
                     "reply": reply, "verdict": verdict,
                     "shield_blocked": was_blocked})
        print(f"  step {i}  shield={'BLOCK' if was_blocked else 'pass '}"
              f"  verifier={verdict:9}  {step['text'][:52]}")
    return rows


if __name__ == "__main__":
    all_rows = []
    for name, steps in load_sequences().items():
        all_rows.extend(run_sequence(name, steps))

    with open("crescendo_results.json", "w", encoding="utf-8") as f:
        json.dump(all_rows, f, indent=2, ensure_ascii=False)

    print()
    print(f"steps fired        : {len(all_rows)}")
    print(f"blocked by shield  : {sum(r['shield_blocked'] for r in all_rows)}")
    print(f"flagged by verifier: {sum(r['verdict'] == 'hit' for r in all_rows)}")
