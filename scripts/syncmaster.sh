#!/bin/bash

cd ../pytorch
git config --local user.email "mszhanyi@users.noreply.github.com"
git config --local user.name "mszhanyi"
git status
git remote add upstream https://github.com/pytorch/pytorch
git remote -v
git fetch upstream
git merge upstream/master
git status
git remote set-url origin https://mszhanyi:${pytorch_token}@github.com/mszhanyi/pytorch.git
git push

git checkout -b zhanyi/updatevcver
git branch --set-upstream-to=origin/zhanyi/updatevcver zhanyi/updatevcver
git pull
date +%s > report.txt
git add -A
git commit -m "Add changes"
git status
git push --set-upstream origin zhanyi/updatevcver
