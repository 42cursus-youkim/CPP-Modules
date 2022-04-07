#!/bin/bash

update_submodules() {
  for module in Module*/; do
    git -C $module checkout main && git -C $module pull &
  done
}

update_submodules
wait

git commit -am "Automated Update Submodules"
git tag -m "AutoUpdate" -a "UpdateSubmodules"
