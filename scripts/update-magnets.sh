#!/usr/bin/env bash

# TODO python

cd "$(dirname "$0")"/..

./scripts/format-magnets.py
./scripts/magnets.rss.sh
./scripts/magnets2readme.py

