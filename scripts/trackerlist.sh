#!/usr/bin/env bash

set -e
#set -x # debug

# https://github.com/ngosang/trackerslist
url="https://github.com/ngosang/trackerslist/raw/master/trackers_best_ip.txt"
echo "fetching $url"
if ! trackers_best_ip="$(curl -sL "$url")"; then
  echo "error: failed to fetch trackers_best_ip"
  exit 1
fi
# remove empty lines
trackers_best_ip="$(echo "$trackers_best_ip" | grep .)"

trackerlist="$(
  echo "$trackers_best_ip"

  # https://rutracker.org/
  echo "http://bt.t-ru.org/ann?magnet"
  echo "http://bt2.t-ru.org/ann?magnet"
  echo "http://bt3.t-ru.org/ann?magnet"
  echo "http://bt4.t-ru.org/ann?magnet"
)"

echo "writing trackerlist.txt"
echo "$trackerlist" >trackerlist.txt
