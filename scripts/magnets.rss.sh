#!/usr/bin/env bash

# write magnets.rss file

# TODO python. bash is slow



# config

channel_title="milahu/deutschetorrents"
channel_description="$(
  echo "deutsche torrents von milahu"
)"

# channel_ttl: number of minutes that indicates how long a channel can be cached before refreshing from the source
channel_ttl=$((60 * 24 * 1)) # 1 day

#lastBuildDate=$(LC_ALL=C date --utc +"%a, %d %b %Y %H:%M:%S %z")
lastBuildDate=$(LC_ALL=C date +"%a, %d %b %Y %H:%M:%S %z")

# input file
magnets_txt="magnets.txt"

# output file
magnets_rss="magnets.rss"



# docs

# Torrent RSS feeds
# https://www.bittorrent.org/beps/bep_0036.html
# https://forum.qbittorrent.org/viewtopic.php?t=2531
# https://eztvx.to/ezrss.xml

# RSS
# https://www.rssboard.org/rss-specification
# https://validator.w3.org/feed/



set -e

cd "$(dirname "$0")"/..

function escape_html() { echo "$*" | sed 's/&/\&amp;/g; s/"/\&quot;/g; s/</\&lt;/g; s/>/\&gt;/g;'; }

# https://stackoverflow.com/questions/6250698/how-to-decode-url-encoded-string-in-shell
#function urldecode_plus() { : "${*//+/ }"; echo -e "${_//%/\\x}"; }
function urldecode() { echo -e "${*//%/\\x}"; }

echo "writing $magnets_rss"
{

cat <<EOF
<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0">
  <channel>
    <title>$(escape_html "$channel_title")</title>
    <description>$(escape_html "$channel_description")</description>
    <link>https://github.com/milahu/deutschetorrents</link>
    <link>http://it7otdanqu7ktntxzm427cba6i53w6wlanlh23v5i3siqmos47pzhvyd.onion/milahu/deutschetorrents#darktea.onion</link>
    <link>http://gg6zxtreajiijztyy5g6bt5o6l3qu32nrg7eulyemlhxwwl6enk6ghad.onion/milahu/deutschetorrents#righttoprivacy.onion</link>
    <link>http://git.dkforestseeaaq2dqz2uflmlsybvnq2irzn4ygyvu53oazyorednviid.onion/milahu/deutschetorrents#darkforest.onion</link>
    <copyright>public domain</copyright>
    <category></category>
    <ttl>$channel_ttl</ttl>
    <lastBuildDate>$lastBuildDate</lastBuildDate>
EOF

while read magnet_link; do

# If practical, the guid SHOULD be the info-hash of the torrent
# for the most part, clients expect the GUID to simply be a unique identifier for this piece of content
# v1 torrent
guid=$(echo "$magnet_link" | sed -E 's/^.*[?&]xt=urn:btih:([0-9a-fA-F]{40}).*$/\1/')
if [ -z "$guid" ]; then
  # v2 torrent
  guid=$(echo "$magnet_link" | sed -E 's/^.*[?&]xt=urn:btmh:([0-9a-fA-F]{68}).*$/\1/')
fi
if [ -z "$guid" ]; then
  echo "error: failed to parse guid from magnet link: $magnet_link"
  continue
fi

title="$(urldecode "$(echo "$magnet_link" | sed -E 's/^.*[?&]dn=([^&]+).*$/\1/')")"

echo "title: $title" >&2

# TODO incremental update
# use last lastBuildDate as pubDate for old magnets
#      <pubDate>$pubDate</pubDate>

cat <<EOF
    <item>
      <title>$(escape_html "$title")</title>
      <guid isPermaLink="false">$guid</guid>
      <enclosure type="application/x-bittorrent" url="$(escape_html "$magnet_link")"/>
    </item>
EOF

done < "$magnets_txt"

cat <<EOF
  </channel>
</rss>
EOF

} >"$magnets_rss"
