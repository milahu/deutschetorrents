#!/usr/bin/env bash

# push to clearnet remotes first, this is faster
for remote in $(git remote show | grep -v '\.onion$'); do
  echo "> git push $remote"
  git push $remote --force
done

for remote in $(git remote show | grep '\.onion$'); do
  echo "> git push $remote"
  git push $remote --force
done
