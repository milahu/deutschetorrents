#!/usr/bin/env python3

# write magnets.txt to readme.md



magnets_path = "magnets.txt"
readme_path = "readme.md"



import os
import sys
import re



os.chdir(os.path.dirname(sys.argv[0]) + "/..")
#print(os.getcwd())



with open(magnets_path, "r") as f:
  magnets = f.read().strip()

if magnets == "":
  raise ValueError("magnets.txt is empty")

if "```" in magnets:
  raise ValueError("found '```' in magnets.txt")

magnets += "\n"



with open(readme_path, "r") as f:
  readme = f.read()

regex = r"(.*?)<!-- <magnets_txt> -->.*?<!-- </magnets_txt> -->(.*)"
matches = re.fullmatch(regex, readme, re.DOTALL)

readme = (
  matches.group(1) +
  "<!-- <magnets_txt> -->\n" +
  "\n" +
  "<details open><summary>" + magnets_path + "</summary>\n" +
  "\n" +
  "```\n" +
  magnets +
  "```\n" +
  "\n" +
  "</details>\n" +
  "\n" +
  "<!-- </magnets_txt> -->" +
  matches.group(2)
)

print("writing", readme_path)
with open(readme_path, "w") as f:
  f.write(readme)
