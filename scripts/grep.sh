#!/usr/bin/env bash

#set -eux

regex=
for arg in "$@"; do
  regex+="$arg."
done
regex="${regex:0: -1}"
regex="magnet:\S+dn=\S*$regex\S+"

# echo "regex: $regex" >&2 # debug

grep -i -E -h -o "$regex" magnets.txt tempseeds.txt $(cat src/magnet-files.txt) issues/github/md/*
