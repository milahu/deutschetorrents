#!/usr/bin/env bash

set -eu
# set -x # debug

magnets_txt="$1" # assert argv1

[ -e "$magnets_txt" ] # assert that file exists

echo "fixing $magnets_txt"

line_suffix="$(grep -F t-ru.org/ann trackerlist.txt | xargs printf "&tr=%s" | sed 's/\?/%3F/g')"

while read line; do
  if [ "${line:0:8}" = "magnet:?" ]; then
    echo -n "$line"
    echo -n "$line_suffix"
    echo
  else
    echo "$line"
  fi
done < "$magnets_txt" | sponge "$magnets_txt"
