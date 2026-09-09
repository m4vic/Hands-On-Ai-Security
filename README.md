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
| **I — Foundation** | Vocabulary, the deterministic-vs-probabilistic reframe, the OWASP web + LLM maps, the 7-class threat taxonomy, real dated incidents, the HTTP/API/SQL machinery underneath it all |  written — [PDF](upcoming) |
| **II — Direct Prompt Injection** | Build your first real attacker: direct injection, jailbreaking, role hijack, obfuscation, system-prompt extraction, a fuzzer, and the judge problem | in progress |
| **III — Indirect Prompt Injection** | The attack that doesn't come from the user at all — it rides in through data the model reads | planned |
| **IV — Creating Attacks** | Attack tooling, corpora, and the honest reality of building a labeled dataset at scale | planned |
| **V — Creating Defense** | From pattern matching to a trained classifier, an honest survey of real guard products, and the regression problem | planned |

Parts I–V are the complete core arc. A tool-layer/lab-infrastructure
extension (MCP, agent supply chain, hands-on practice environments) and a
traditional-cybersecurity merge (classic web bugs meeting the agentic attack
surface) are planned as a follow-on, not required to finish the core story.

## Read it

Part I is a finished PDF: **[Hands-On-AI-Security-Part-I-Foundation.pdf](Hands-On-AI-Security-Part-I-Foundation.pdf)**

Building from source needs a LaTeX toolchain + pandoc:
```bash
./build-pdf.sh
```

## Who this is for

**Part I assumes nothing** — a motivated beginner can start there. **From
Part II onward**, the book assumes comfort with Python and basic ML, and
gets genuinely technical. Full frontier-model fine-tuning is acknowledged as
a compute reality most readers won't have; the achievable, teachable
technique — BERT-scale fine-tuning on a free notebook — is the one you'll
actually do.

## Before you begin

**You only test systems you own, or have explicit, written authorization to
test.** Every attacker, target, and defender in this book runs on your own
machine, on purpose — so that rule is easy to keep, but the responsibility
to keep it is yours.

## License

TBD — will be added before Part II ships.

## Contact

Issues and discussion welcome on this repo. For anything else: reach out via
[github.com/m4vic](https://github.com/m4vic).
