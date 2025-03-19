#! /usr/bin/env bash

set -e
set -u
#set -x

md_dir="$1"
out_path="$2"

# generate index file
# workaround for https://github.com/mattduck/gh2md/issues/33
(
  #echo "# github issues"
  #echo
  # loop sections
  # TODO add more sections
  # TODO? generate multiple index files, one file per section
  # FIXME skip empty sections
  for selector in "open issue" "closed issue" "merged pr"; do
    section="${selector}s"
    selected_status=${selector% *}
    selected_type=${selector#* }
    echo "<h2>$section</h2>"
    echo '<details>'
    echo "<summary>$section</summary>"
    echo '<table>'
    find "$md_dir" -type f -name "*.$selected_type.$selected_status.md" | sort -n --reverse | while read md_path; do
      # 2021-06-16.1.pr.merged.md  2023-08-07.2.issue.open.md  2023-08-07.3.issue.open.md  2023-08-08.4.issue.open.md
      md_name=$(basename "$md_path")
      md_url="md/$md_name"
      number=$(echo "$md_name" | cut -d. -f 2)
      type=$(echo "$md_name" | cut -d. -f 3) # "pr" or "issue"
      status=$(echo "$md_name" | cut -d. -f 4) # pr: merged/?/?, issue: open/?
      num_comments=$(cat "$md_path" | grep -E '^#### <img src="https://avatars\.githubusercontent\.com/u/[0-9]+\?(u=[0-9a-f]+&)?v=[0-9]+" width="50">\[.*?\]\(https://github.com/.*?\) commented at \[.*\):$' | wc -l)
      text=$(pandoc -f commonmark -t plain --wrap=none "$md_path")
      title=$(echo "$text" | head -n1 | cut -d' ' -f4-)
      author=$(echo "$text" | head -n3 | tail -n1 | cut -d' ' -f1)
      datetime=$(echo "$text" | head -n3 | tail -n1 | cut -d' ' -f5-6 | sed 's/:$//')
      # FIXME: use only the first comment
      start=$(echo "$text" | tail -n +5 | head -c 200)
      start_escaped=$(echo "$start" | sed 's/"/\&quot;/g' | perl -0777 -pe 's/\n/&#10;/g')
      # debug
      echo "start: $start" >&2
      echo "start_escaped: $start_escaped" >&2
      #echo '<tr>'
      if false; then
        # column: icon
        if [[ "$type" == "issue" ]]; then
          if [[ "$status" == "open" ]]; then
            echo '<td><svg class="octicon octicon-issue-opened open" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"></path><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"></path></svg></td>'
          else
            echo '<td>TODO icon</td>'
          fi
        else
          echo '<td>TODO icon</td>'
        fi
      else
        # column: type
        #echo "<td>$type</td>"
        # column: status
        #echo "<td>$status</td>"
        # column: status + type
        #echo "<td>$status $type</td>"
        :
      fi
      # column: title, number, date, author
      #echo "<td><b><a href=\"$md_url\">$title</a></b><br>#$number opened on $datetime by $author</td>"
      comments_str=$(if ((num_comments > 0)); then echo " &#x1f4ac; $num_comments"; else echo ""; fi)
      echo "<tr><td><b><a href=\"$md_url\" title=\"$start_escaped\">$title</a></b><br>#$number opened on $datetime by $author$comments_str</td></tr>"
      # column: number of replies
      # https://www.fileformat.info/info/unicode/char/1f4ac/index.htm
      if false; then
        if ((num_comments > 0)); then
          echo "<td>&#x1f4ac; $num_comments</td>"
        else
          echo "<td></td>"
        fi
      fi
      #echo '</tr>'
    done
    echo '</table>'
    echo '</details>'
  done
) >"$out_path"
