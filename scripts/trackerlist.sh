#!/usr/bin/env bash

set -e
#set -x # debug

function check_command() {
  local cmd
  for cmd in "$@"; do
    if command -v "$cmd" >/dev/null; then
      continue
    fi
    echo "error: missing command: $cmd"
    exit 1
  done
}

check_command curl netselect grep sed xargs

# https://github.com/ngosang/trackerslist
url="https://github.com/ngosang/trackerslist/raw/master/trackers_all_ip.txt"
echo "fetching $url"
if ! trackers_all_ip="$(curl -sL "$url")"; then
  echo "error: failed to fetch trackers_all_ip"
  exit 1
fi

# select nearest trackers for this location
# this requires root access for ping
# sed -E 's/^\s*([0-9]+) (.*)$/\2#dt=\1ms/'
num_pings=100
num_servers=5
netselect_result="$(
  echo "$trackers_all_ip" |
  grep '^udp://' |
  xargs sudo netselect -v -s999 -t$num_pings
)"

echo "writing trackerlist.netselect.txt"
echo "$netselect_result" >trackerlist.netselect.txt

trackerlist="$(
  echo "$netselect_result" |
  head -n$num_servers |
  sed -E 's/^\s*([0-9]+) (.*)$/\2/'

  # https://github.com/ngosang/trackerslist/raw/master/trackers_all_i2p.txt
  echo "http://opentracker.r4sas.i2p/a"
)"

echo "writing trackerlist.txt"
echo "$trackerlist" >trackerlist.txt
