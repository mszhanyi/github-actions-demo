#!/bin/bash

git checkout -b zhanyi/updatevcver
date +%s > report.txt
git commit -m "Add changes" -a
git remote set-url origin https://mszhanyi:${pytorch_token}@github.com/mszhanyi/pytorch.git
git push --set-upstream origin zhanyi/test1