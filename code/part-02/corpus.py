"""Where the attack corpus lives.

Kept in one place so every script agrees, and so the path works on any
machine that clones this repo - not just the one it was written on.
"""

import os

# attack_db/ sits at the repo root, two levels up from code/part-02/.
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

ATTACK_DB = os.environ.get("ATTACK_DB", os.path.join(_REPO_ROOT, "attack_db"))


def category_path(category):
    """Path to one category's JSON file. benign uses a different filename."""
    filename = "samples.json" if category == "benign" else "attacks.json"
    return os.path.join(ATTACK_DB, category, filename)
