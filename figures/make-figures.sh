#!/usr/bin/env bash
# Render the Part One and Part Two figures for the video course.
#
# These are built as D2 "steps": each .d2 produces a numbered sequence of
# boards (index.png, 1.png, 2.png, ...) that assemble the diagram one piece
# at a time. Cut between them in the edit so the picture builds while you
# narrate, instead of landing all at once.
#
# ELK, not the default dagre: ELK preserves declaration order, routes edges
# orthogonally instead of straight through boxes, and keeps earlier elements
# in place as later boards add to them. Dagre fails all three here.
#
# Usage:  ./make-figures.sh            # render all Part One figures
#         ./make-figures.sh 01-1-*.d2  # render specific ones
set -euo pipefail
cd "$(dirname "$0")"

D2="${D2_BIN:-/c/Program Files/D2/d2}"
SCALE="${SCALE:-2}"

# Part One only. Part Two/Three figures were laid out for dagre and are left
# alone deliberately - re-rendering them with ELK would change their layout.
DEFAULT_FIGURES=(
  01-1-three-fields-colliding.d2
  02-2-the-two-channels.d2
  03-1-the-two-maps.d2
  04-1-the-seven-classes.d2
  05-1-the-quiet-leak.d2
  05-2-echoleak-chain.d2
  06-1-request-and-response.d2
  07-1-seven-vs-nine.d2
  07-2-obfuscated-persona.d2
  07-3-crescendo-staircase.d2
  08-1-the-attack-loop.d2
  09-1-shield-vs-verifier.d2
  09-2-three-verifiers.d2
  09-3-the-shields-lever.d2
  10-1-where-the-attack-lives.d2
  11-1-the-prompts-lever.d2
  12-1-four-judges.d2
  13-1-three-zoom-levels.d2
)

FIGURES=("$@")
if [ ${#FIGURES[@]} -eq 0 ]; then
  FIGURES=("${DEFAULT_FIGURES[@]}")
fi

for src in "${FIGURES[@]}"; do
  [ -f "$src" ] || { echo "skip (missing): $src"; continue; }
  out="${src%.d2}.png"
  echo "rendering $src"
  "$D2" --layout elk --scale "$SCALE" "$src" "$out"
done

echo
echo "done. stepped figures land in a folder per figure:"
echo "  <name>/index.png  <name>/1.png  <name>/2.png ..."
