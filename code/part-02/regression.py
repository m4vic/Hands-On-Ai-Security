"""Freeze what your security posture is today, so you can tell when it moves.

A fix is a snapshot, not a permanent state. The model gets swapped, the
prompt gets edited, the corpus grows - and things you closed can quietly
reopen. This is the smallest tool that notices.
"""

import json
import sys

from attacker import CATEGORIES, run
from shield import blocked
from verifier import verify


def snapshot(model, label):
    """Fire the whole corpus and record one row per attack."""
    rows = []
    for r in run(CATEGORIES, model=model):
        was_blocked, _ = blocked(r["attack"])
        rows.append({
            "attack": r["attack"],
            "category": r["category"],
            "blocked": was_blocked,          # did the shield stop it
            "leaked": r["leaked"],            # did the canary fire
            "verdict": verify(r["reply"]),    # what the phrase bank thought
            "reply": r["reply"],
        })

    out = {"label": label, "model": model, "rows": rows}
    with open(f"baseline_{label}.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"\nsaved baseline_{label}.json")
    return out


def from_results(results_file, model, label):
    """Build a baseline from a run you already did.

    Re-firing 93 attacks to record a posture you already measured is a
    waste of several minutes. Chapter 8 saved every reply; this turns
    that file into a snapshot without touching the model.
    """
    with open(results_file, encoding="utf-8") as f:
        results = json.load(f)

    rows = []
    for r in results:
        was_blocked, _ = blocked(r["attack"])
        rows.append({
            "attack": r["attack"],
            "category": r["category"],
            "blocked": was_blocked,
            "leaked": r["leaked"],
            "verdict": verify(r["reply"]),
            "reply": r["reply"],
        })

    out = {"label": label, "model": model, "rows": rows}
    with open(f"baseline_{label}.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"saved baseline_{label}.json ({len(rows)} rows, no model calls)")
    return out


def load(label):
    with open(f"baseline_{label}.json", encoding="utf-8") as f:
        return json.load(f)


def compare(before, after):
    """What moved between two snapshots, in both directions."""
    # Attacks are identified by their text - the corpus is the fixed thing.
    old = {r["attack"]: r for r in before["rows"]}
    new = {r["attack"]: r for r in after["rows"]}
    shared = [a for a in old if a in new]

    fixed, regressed = [], []
    for attack in shared:
        # "landed" means the shield let it through AND it leaked the secret
        was = (not old[attack]["blocked"]) and old[attack]["leaked"]
        now = (not new[attack]["blocked"]) and new[attack]["leaked"]
        if was and not now:
            fixed.append(attack)
        elif now and not was:
            regressed.append(attack)

    print(f"\n{'=' * 62}")
    print(f"{before['label']}  ->  {after['label']}")
    print(f"{'=' * 62}")
    print(f"  attacks compared : {len(shared)}")
    print(f"  leaks before     : {sum(r['leaked'] for r in before['rows'])}")
    print(f"  leaks after      : {sum(r['leaked'] for r in after['rows'])}")
    print(f"  FIXED            : {len(fixed)}")
    print(f"  REGRESSED        : {len(regressed)}   <- these used to be safe")

    for attack in regressed:
        print(f"\n  [REGRESSION] {new[attack]['category']}")
        print(f"    attack: {attack[:78]}")
        print(f"    reply : {new[attack]['reply'][:110]}")

    return fixed, regressed


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "snapshot":
        # python regression.py snapshot <model>
        model = sys.argv[2]
        snapshot(model, label=model.split("/")[-1].replace(":", "_"))
    elif len(sys.argv) == 4 and sys.argv[1] == "compare":
        compare(load(sys.argv[2]), load(sys.argv[3]))
    else:
        print(__doc__)
        print("usage:")
        print("  python regression.py snapshot <model>")
        print("  python regression.py compare <label-before> <label-after>")
