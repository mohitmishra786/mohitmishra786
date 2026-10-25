#!/usr/bin/env bash
# Commit the given paths (only if they changed) and push to the branch the
# workflow is running on, retrying with `git pull --rebase` on a race.
#
# Usage: scripts/commit_and_push.sh "<commit message>" <path> [<path>...]
#
# Every workflow that writes to the repo calls this, so all bot commits are
# `chore(bot): ... [skip ci]`, stage explicit paths only, and survive the
# occasional concurrent push from another workflow.
set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "usage: $0 <message> <path>..." >&2
  exit 2
fi

message="$1"
shift
branch="${GITHUB_REF_NAME:-$(git rev-parse --abbrev-ref HEAD)}"

git config user.name "github-actions[bot]"
git config user.email "41898282+github-actions[bot]@users.noreply.github.com"

git add -- "$@"
if git diff --cached --quiet; then
  echo "No changes to commit."
  exit 0
fi

git commit -m "chore(bot): ${message} [skip ci]"

for attempt in 1 2 3; do
  if git pull --rebase origin "$branch" && git push origin "HEAD:${branch}"; then
    echo "Pushed to ${branch} on attempt ${attempt}."
    exit 0
  fi
  echo "Push attempt ${attempt} failed; retrying..." >&2
  git rebase --abort 2>/dev/null || true
  sleep $((attempt * 10))
done

echo "Failed to push after 3 attempts." >&2
exit 1
