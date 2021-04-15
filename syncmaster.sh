#!/bin/bash

cd pytorch
git config --local user.email "mszhanyi@users.noreply.github.com"
git config --local user.name "mszhanyi"
git status
git remote add upstream https://github.com/pytorch/pytorch
git remote -v
git fetch upstream
git merge upstream/master
git status
git remote set-url origin https://mszhanyi:${{secrets.PYTORCH_KEY}}@github.com/mszhanyi/pytorch.git
git push