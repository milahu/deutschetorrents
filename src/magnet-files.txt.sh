#!/usr/bin/env bash

cd "$(dirname "$0")/.."

echo "writing src/magnet-files.txt"

ls \
  src/dht/german-* \
  src/dht/multi-ger.txt \
  src/dht/todo.txt \
  src/rutracker.org/todo.txt \
  src/rutracker.org/magnets.txt \
  src/trash/magnets.txt \
  src/temp-seeds/magnets.txt \
  | sort >src/magnet-files.txt
