#!/bin/bash
set -ex

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
python -m pip install lxml
python ../scripts/updatevcver.py

git commit -a -m "Update Lastest VS"
git status
git push

