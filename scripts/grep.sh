#!/usr/bin/env bash

#set -eux

regex="$1"

grep -i -E -h -o "magnet:\S+dn=\S*$regex\S+" magnets.txt tempseeds.txt $(cat src/magnet-files.txt) issues/github/md/*
