#!/usr/bin/env python3

import os
import sys
import urllib.parse
import re

if len(sys.argv) > 1:
    magnets_txt_list = sys.argv[1:]
else:
    os.chdir(os.path.dirname(sys.argv[0]) + "/..")
    #print(os.getcwd())
    magnets_txt_list = ["magnets.txt"]

for magnets_txt in magnets_txt_list:

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
      query_dict = urllib.parse.parse_qs(url_parsed.query.replace("+", "%2B"))
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
      if False:
        # remove trackers
        if "tr" in query_dict:
          del query_dict["tr"]
      elif False:
        if "tr" in query_dict:
          # keep private trackers
          trackers = []
          for tr in query_dict["tr"]:
            if re.match(r"http://bt[0-9]*.t-ru\.org/ann\?magnet", tr):
              # rutracker.org
              # grep -F t-ru.org/ann trackerlist.txt | xargs printf "&tr=%s" | sed 's/\?/%3F/g'
              trackers.append(tr)
              continue
            # TODO keep more trackers
          trackers = list(set(trackers))
          trackers.sort()
          query_dict["tr"] = trackers
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
        dn = re.sub(r"^bitsearch\.to\.", "", dn, flags=re.I)
        dn = re.sub(r"^Bitsearch\.to\.", "", dn, flags=re.I)
        dn = dn.replace(".⭐", "").replace("⭐", "")
        if "bitsearch" in dn.lower():
          print("FIXME remove 'bitsearch' from dn:", dn)
          sys.exit(1)
        # TODO remove more junk
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

    # FIXME dedupe magnet links by hash
    res = list(set(res)) # get unique list

    res.sort(key=lambda s: s.lower()) # case-insensitive sort

    print("writing", magnets_txt)

    with open(magnets_txt, "w") as f:
      f.write("\n".join(res) + "\n")
