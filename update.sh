#!/bin/bash

update_submodules() {
  for module in Module*/; do
    git -C $module checkout main && git -C $module pull &
  done
  wait
  echo Done.
}

push_commit() {
  timestamp=$(date +"%Y-%m-%dT%H%M")
  git commit -am "Automated submodules update"
  git tag -a "$timestamp" -m "Automated submodules update"
  git push
}

update_submodules
push_commit
