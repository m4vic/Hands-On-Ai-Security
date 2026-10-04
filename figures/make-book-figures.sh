#!/usr/bin/env bash
# Render the BOOK version of each stepped Part One figure: one vector PDF
# showing the finished diagram (the last board).
#
# The video wants the boards separately, so the picture assembles on camera.
# The book wants the whole thing at once, as vector, so it stays sharp in
# print. Same .d2 source, two outputs - which is the reason the figures are
# text-defined in the first place.
#
# Output: <name>.pdf  (single file, sits alongside the <name>/ board folder)
set -euo pipefail
cd "$(dirname "$0")"

D2="${D2_BIN:-/c/Program Files/D2/d2}"

STEPPED=(
  01-1-three-fields-colliding
  02-2-the-two-channels
  03-1-the-two-maps
  04-1-the-seven-classes
  05-1-the-quiet-leak
  05-2-echoleak-chain
  06-1-request-and-response
)

for name in "${STEPPED[@]}"; do
  src="$name.d2"
  [ -f "$src" ] || { echo "skip (missing): $src"; continue; }

  # Highest step number defined in the file = the finished diagram.
  last=$(grep -oE '^[[:space:]]+[0-9]+:[[:space:]]*\{' "$src" \
         | grep -oE '[0-9]+' | sort -n | tail -1)
  if [ -z "$last" ]; then
    echo "skip (no steps found): $src"; continue
  fi

  echo "rendering $name  (final board: steps.$last)"
  "$D2" --layout elk --target="steps.$last" "$src" "$name.pdf"
done

echo
echo "done. book figures are the single .pdf files; video boards stay in <name>/"
