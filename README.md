# Hands-On AI Security

**A builder's book, not a hunter's book.** You build an attacker, a defender,
and a target — three small systems that grow up together across the book —
and you learn AI security by breaking and fixing your own machines, not by
reading about someone else's.

[![Code: Apache 2.0](https://img.shields.io/badge/code-Apache--2.0-blue.svg)](LICENSE)
[![Book: CC BY-SA 4.0](https://img.shields.io/badge/book-CC%20BY--SA%204.0-lightgrey.svg)](LICENSE-BOOK)
[![Status: in progress](https://img.shields.io/badge/status-in%20progress-orange.svg)](#status)

--
## What this is
Most security writing is a *hunter's* book: here's a bug class, here's where
it hides, go find it in the wild. This isn't that. There's no scope question
and no authorization question here — the target is always yours. You build
the system, you build the thing that attacks it, and you build the thing that
defends it, and you watch all three collide on a machine that's entirely
yours.

**Proof over assurance** runs through every part of it. A claim that a
system is safe is worth nothing until something you built and ran
demonstrates it — not a vendor's datasheet, not a model card, not "the
prompt tells it not to." Every number in this book traces back to something
actually built and actually run — including a "hardening" system prompt
that, tested for real, stopped **zero** of six attacks.

Not written for one role. Useful to a bug-bounty hunter extending into AI
targets, someone learning AI who needs the security lens, a red/blue teamer
who wants real backend and model internals instead of vendor talk.

## Status

| Part | Covers | Status |
|---|---|---|
| **One — Foundation** | Vocabulary, the deterministic-vs-probabilistic reframe, the OWASP web + LLM maps, the 7-class threat taxonomy, real dated incidents, the HTTP/API/SQL machinery underneath it all | written |
| **Two — Prompt Injection** | Direct *and* indirect injection, still text-only. Build a target, an attacker, a shield and a verifier; hit the judge problem; watch a model upgrade regress your posture | written |
| **Three — Agentic Attacks** | The target grows real tools. Tool abuse, MCP, multi-agent handoffs, a real guardrail survey, and a harness that verifies from the tool-call trace rather than the text | planned |
| **Four — AI-Driven Cybersecurity** | An original benchmark of vulnerable agent targets, taught from both sides: how to break it, how to fix it | planned |

Each part is complete on its own - you finish it having gained something,
not holding an IOU for a later part.

## Read it

Part One is written and builds to PDF. The book text itself is not in this
repository - this repo carries the code, the attack corpus and the figures
so you can run everything the book builds.

## Who this is for

**Part One assumes nothing** — a motivated beginner can start there. **From
Part Two onward**, the book assumes comfort with Python and basic ML, and
gets genuinely technical. Full frontier-model fine-tuning is acknowledged as
a compute reality most readers won't have; the achievable, teachable
technique — BERT-scale fine-tuning on a free notebook — is the one you'll
actually do.

## Running the code

Everything runs locally. No API keys, no cloud, no bill.

You need [Ollama](https://ollama.com) with a model pulled. The book uses an
*abliterated* (safety-stripped) model as the target on purpose — so that when
an attack fails later, it failed because **your** shield stopped it, not
because the model's own training caught it first:

```bash
ollama pull mannix/llama3.1-8b-abliterated:q5_K_M
pip install -r requirements.txt
```

Then, from `code/part-02/`:

```bash
python target.py       # a support bot with a secret worth stealing
python attacker.py     # fire all 93 attacks, check for the leaked canary
python shield.py       # measure the defense (needs no model at all)
python labeler.py      # ask a local model to classify attacks, score it
python judge.py        # ask a model "did the attack work?", score it too
python regression.py   # freeze a posture, diff it after any change
```

Any model works — edit `MODEL` in `llm.py`. The attack corpus lives in
`attack_db/`, and `corpus.py` finds it relative to the repo, so a fresh
clone runs as-is.

## Before you begin

**You only test systems you own, or have explicit, written authorization to
test.** Every attacker, target, and defender in this book runs on your own
machine, on purpose — so that rule is easy to keep, but the responsibility
to keep it is yours.

## License

This project is split deliberately.

**Open — Part One (Foundation) and Part Two (Prompt Injection):**

- Code and the attack corpus — [Apache-2.0](LICENSE)
- Book text and figures — [CC BY-SA 4.0](LICENSE-BOOK)

Use it, adapt it, translate it, build on it — commercially or not. Two
conditions: credit **Sanskar Jajoo**, and if you distribute something built
on the book material, keep it under the same license.

**Reserved — Part Three (Agentic Attacks) and Part Four (AI-Driven
Cybersecurity):** © Sanskar Jajoo, all rights reserved. These are the deeper
agentic-AI and security materials, and no license is granted for them.

Full detail, including what a license can and cannot require, is in
[LICENSING.md](LICENSING.md).

## Citation

This repo includes a `CITATION.cff`, so GitHub's **"Cite this repository"**
button produces a correct APA or BibTeX entry.

```
Jajoo, S. (2026). Hands-On AI Security.
https://github.com/m4vic/Hands-On-Ai-Security
```

## Contact

Issues and discussion welcome on this repo. For anything else: reach out via
[github.com/m4vic](https://github.com/m4vic).
