# Hands-On AI Security

**A builder's book, not a hunter's book.** You build an attacker, a defender,
and a target — three small systems that grow up together across the book —
and you learn AI security by breaking and fixing your own machines, not by
reading about someone else's.

[![License: TBD](https://img.shields.io/badge/license-TBD-lightgrey.svg)](#license)
[![Status: in progress](https://img.shields.io/badge/status-in%20progress-orange.svg)](#status)

---

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

TBD — not yet chosen. Treat the code here as read-only reference
until a license is added.

## Contact

Issues and discussion welcome on this repo. For anything else: reach out via
[github.com/m4vic](https://github.com/m4vic).
