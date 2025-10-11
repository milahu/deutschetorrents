#!/bin/sh

set -x

cat ~/new-magnets.txt >>tempseeds.txt
./scripts/format-magnets.py tempseeds.txt
git add tempseeds.txt
git commit -m "up tempseeds.txt"
# ./scripts/git-push-all-remotes.sh
