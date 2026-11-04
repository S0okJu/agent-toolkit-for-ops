#!/usr/bin/env bash
# Save a finished Markdown document to Bear under #ai-inbox.
# Updates the existing #ai-inbox note with the same title instead of duplicating it.
# Usage: save_to_bear.sh <file.md>
set -euo pipefail

# Content goes through stdin on purpose: --content interprets \n, \t, \\ and would
# corrupt literal escapes in code blocks. stdin is stored verbatim.

TAG="ai-inbox"
file="${1:?usage: save_to_bear.sh <file.md>}"

bear="$(command -v bearcli || true)"
[[ -z "$bear" && -x /Applications/Bear.app/Contents/MacOS/bearcli ]] && bear=/Applications/Bear.app/Contents/MacOS/bearcli
[[ -n "$bear" ]] || { echo "bearcli not found; is Bear installed?" >&2; exit 1; }

title="$(grep -m1 '^# ' "$file" | sed 's/^# //')"
[[ -n "$title" ]] || { echo "no '# ' title heading in $file" >&2; exit 1; }

id="$("$bear" search "@title \"$title\" #$TAG" --format tsv --fields id,title 2>/dev/null \
  | awk -F'\t' -v t="$title" '$2 == t { print $1; exit }')"

if [[ -n "$id" ]]; then
  # overwrite derives tags from content, so the tag must be in the body.
  { cat "$file"; printf '\n\n#%s\n' "$TAG"; } | "$bear" overwrite "$id"
  echo "updated: $id $title"
else
  "$bear" create --tags "$TAG" --fields id,title < "$file"
fi
