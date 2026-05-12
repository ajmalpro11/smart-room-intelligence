#!/bin/bash
cd ~/smart-room
git pull --no-rebase
git add .
git commit -m "$1"
git push
