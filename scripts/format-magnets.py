#!/usr/bin/env python3

# TODO: xclip -o -sel c

# TODO remove unicode junk like ".⭐"

import os
import sys
import urllib.parse
import re

os.chdir(os.path.dirname(sys.argv[0]) + "/..")
#print(os.getcwd())

magnets_txt = "magnets.txt"

#with open(0, "r") as f: # read from stdin
with open(magnets_txt, "r") as f:
  src = f.read()

res = []

for url in src.split("\n"):
  url = url.strip()
  if url == "":
    continue
  url_parsed = urllib.parse.urlparse(url)
  if url_parsed.scheme != "magnet":
    continue
  query_dict = urllib.parse.parse_qs(url_parsed.query)
  """
  query_list = urllib.parse.parse_qsl(url_parsed.query)
  def query_get(key):
    # get first value by key, or None
    return next(q for q in query_list if q[0] == key)[1]
  def query_item(key):
    # get first item by key, or None
    return next(q for q in query_list if q[0] == key)
  remove_keys = []
  key = "dn"
  item = query_item(key)
  if item:
    query_list_2.push(item)
    remove_keys.append(key)
  """
  #if False:
  if True:
    # remove trackers
    if "tr" in query_dict:
      del query_dict["tr"]
  # put name first
  query_list = []
  def quote_pretty(s):
    # >>> urllib.parse.quote_plus("% \n \r \t ? & = #", "/:")
    # '%25+%0A+%0D+%09+%3F+%26+%3D+%23'
    return (s
      ).replace("%", "%25"
      #).replace(" ", "+"
      ).replace(" ", "."
      ).replace("[", ""
      ).replace("]", ""
      ).replace("(", ""
      ).replace(")", ""
      ).replace("<", ""
      ).replace(">", ""
      ).replace("\n", "%0a"
      ).replace("\r", "%0d"
      ).replace("\t", "%09"
      #).replace("?", "%3f"
      ).replace("&", "%26"
      #).replace("=", "%3d"
      ).replace("#", "%23"
      )
  if "dn" in query_dict:
    #query_list.append("dn=" + urllib.parse.quote_plus(query_dict["dn"][0]))
    dn = query_dict["dn"][0]
    del query_dict["dn"]
    dn = quote_pretty(dn)
    dn = re.sub("^Bitsearch\.to\.", "", dn)
    dn = dn.replace(".⭐", "").replace("⭐", "")
    query_list.append("dn=" + dn)
  for key in query_dict:
    if key in ("ws",):
      # ws = webseed url, for example ws=https://archive.org/download/
      continue
    for val in query_dict[key]:
      quote_safe = "/:"
      query_list.append(key + "=" + urllib.parse.quote(val, quote_safe))
  url = "magnet:?" + "&".join(query_list)
  res.append(url)

res = list(set(res)) # get unique list

res.sort()

print("writing", magnets_txt)

with open(magnets_txt, "w") as f:
  f.write("\n".join(res) + "\n")
