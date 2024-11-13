#!/usr/bin/env python3

# remove torrents from file2
# which are already in file1

# example use:
# ./scripts/dedupe.py magnets.txt src/rutracker.org/todo.txt -n
# ./scripts/dedupe.py magnets.txt src/rutracker.org/todo.txt

# TODO accept multiple files
# file1 is read-only
# file2, file3, file4, ... are writable
# dedupe cascade:
# remove torrents from file2 which are already in file1
# remove torrents from file3 which are already in file1, file2
# remove torrents from file4 which are already in file1, file2, file3
# ...

import os
import sys
import re

path1 = sys.argv[1]
path2 = sys.argv[2]
noop = False
if len(sys.argv) == 4 and sys.argv[3] == "-n":
    noop = True

f1 = open(path1)
f2 = open(path2)

hashes1 = set()

# TODO also support v2 torrents (rare)
r = r"xt=urn:btih:([0-9a-fA-F]{40})"

for line in f1.readlines():
    m = re.search(r, line)
    hash = m.group(1)
    hashes1.add(hash)

str2 = ""

len2a = 0
len2b = 0

for line in f2.readlines():
    m = re.search(r, line)
    hash = m.group(1)
    len2a += 1
    if hash in hashes1:
        # remove this line
        continue
    # keep this line
    len2b += 1
    if noop:
        # print result to stdout
        print(line, end="")
    else:
        str2 += line

f1.close()
f2.close()

if noop == False:
    # write result to path2
    if len2b < len2a:
        print(f"reduced lines from {len2a} to {len2b}", file=sys.stderr)
        with open(path2, "w") as f:
            f.write(str2)
    else:
        print("no change", file=sys.stderr)
