#!/usr/bin/env bash

# https://github.com/milahu/darknet-git-hosting-services

owner=milahu
repo=deutschetorrents

function git_remote_add_onion() {
  local remote="$1"
  local url="$2"
  git remote add "$remote" "$url" ||
  git remote set-url "$remote" "$url"
  git config --add remote."$remote".proxy socks5h://127.0.0.1:9050
}

remote=darktea.onion
url=http://it7otdanqu7ktntxzm427cba6i53w6wlanlh23v5i3siqmos47pzhvyd.onion/$owner/$repo
git_remote_add_onion "$remote" "$url"

remote=righttoprivacy.onion
url=http://gg6zxtreajiijztyy5g6bt5o6l3qu32nrg7eulyemlhxwwl6enk6ghad.onion/$owner/$repo
git_remote_add_onion "$remote" "$url"

remote=darkforest.onion
url=http://git.dkforestseeaaq2dqz2uflmlsybvnq2irzn4ygyvu53oazyorednviid.onion/$owner/$repo
git_remote_add_onion "$remote" "$url"

git_remote_add_onion gdatura.onion http://gdatura24gtdy23lxd7ht3xzx6mi7mdlkabpvuefhrjn4t5jduviw5ad.onion/$owner/$repo
