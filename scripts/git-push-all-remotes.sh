#!/usr/bin/env bash

for remote in $(git remote show); do
  echo "> git push $remote"
  git push $remote
done
