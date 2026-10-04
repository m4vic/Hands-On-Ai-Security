# Licensing

This project is deliberately split. Parts One and Two are open. Parts Three
and Four are not, and are reserved as commercial material.

Author: **Sanskar Jajoo**

---

## What is open

| Material | Licence |
|---|---|
| Part One (Foundation) and Part Two (Prompt Injection) — book text and figures | **CC BY-SA 4.0** |
| Code for those parts (`code/part-02/`) | **Apache-2.0** |
| The attack corpus (`attack_db/`) | **Apache-2.0** |

### CC BY-SA 4.0, in plain terms

You may **share** it (copy and redistribute, any medium) and **adapt** it
(remix, translate, build on it), **including commercially**.

Two conditions:

1. **Credit.** Name the author — Sanskar Jajoo — link the licence, and state
   whether you changed anything.
2. **ShareAlike.** If you build on it and distribute the result, that result
   must carry this same licence. You may not take this work, extend it, and
   close the extension.

That second condition is the reason this is BY-SA rather than plain BY: the
material stays open as it travels.

### Apache-2.0, in plain terms

Use, modify and distribute the code, commercially or not. Preserve the
copyright and `NOTICE`, and state what you changed. It includes an express
patent grant, and it comes with no warranty.

---

## What is not open

**Part Three (Agentic Attacks) and Part Four (AI-Driven Cybersecurity)** —
text, code, figures and lab material — are **© Sanskar Jajoo, all rights
reserved.** No licence is granted. They are the intended commercial
product: the deeper agentic-AI and cybersecurity material.

This is the ordinary legal default, not a special restriction. It simply
means permissions have not been granted yet.

### Why the split is structured this way

An open licence is **irrevocable for any version you publish.** Once a
version of a work is released under CC BY-SA or Apache-2.0, it remains
usable under that licence permanently. You can relax terms later; you can
never tighten them on something already out.

So the reserved parts stay closed *until* a decision is made, rather than
being opened and regretted. `sync-to-repo.sh` enforces this mechanically —
it publishes only chapters 1-13 and aborts if anything numbered 14 or above
reaches the public repository.

---

## What a licence cannot do

Worth stating plainly, because it is widely misunderstood.

**Copyright protects expression, not knowledge.** These licences govern
copying this *text, these figures and this code*. They do not — and legally
cannot — stop someone from reading the work, understanding an idea such as
verifying an agent from its tool-call trace, and teaching that idea in their
own words without crediting anyone.

Attribution is required when someone copies or adapts the material itself.
For the ideas, credit is a matter of academic and professional courtesy, not
licence terms.

---

## Citing this work

A `CITATION.cff` file is included, so GitHub shows a **"Cite this
repository"** button that produces correct APA and BibTeX entries.

```
Jajoo, S. (2026). Hands-On AI Security.
https://github.com/m4vic/Hands-On-Ai-Security
```

---

## Adding the licence files

The canonical legal texts are not reproduced here by hand — a transcription
error in a licence is a real problem. Add them from the authoritative source:

- **Apache-2.0** — https://www.apache.org/licenses/LICENSE-2.0.txt, saved as
  `LICENSE` (or `LICENSE-CODE`)
- **CC BY-SA 4.0** — https://creativecommons.org/licenses/by-sa/4.0/legalcode.txt,
  saved as `LICENSE-BOOK`

On GitHub, *Add file → Create new file → `LICENSE`* offers a licence picker
that inserts the canonical Apache-2.0 text for you.

Add a copyright line naming the author and the year to both.
