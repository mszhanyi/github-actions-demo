#!/usr/bin/env python3

import sys
import os
import json
import requests

API_VERSION = "v3"
BASE = "https://api.github.com"

HEADERS = {
    "Authorization": "token %s" % ${pytorch_token},
    "Accept": "application/vnd.github.%s+json;application/vnd.github.antiope-preview+json;application/vnd.github.shadow-cat-preview+json"
    % API_VERSION,
}

# URLs
# REPO_URL = "%s/repos/%s" % (BASE, "pytorch/pytorch")
REPO_URL = "%s/repos/%s" % (BASE, "mszhanyi/pytorch")
ISSUE_URL = "%s/issues" % REPO_URL
PULLS_URL = "%s/pulls" % REPO_URL

def open_pull_request(title, body, target, source, is_draft=False, can_modify=True):
    """Open pull request opens a pull request with a given body and content,
    and sets output variables. An unparsed response is returned.
    Parameters:
    title       (str) : the title to set for the new pull request
    body        (str) : the body to set for the new pull request
    target      (str) : the target branch
    source      (str) : the source branch
    is_draft   (bool) : indicate the pull request is a draft
    can_modify (bool) : indicate the maintainer can modify
    """
    print("No pull request from %s to %s is open, continuing!" % (source, target))

    # Post the pull request
    data = {
        "title": title,
        "body": body,
        "base": target,
        "head": source,
        "draft": is_draft,
        "maintainer_can_modify": can_modify,
    }
    print("Data for opening pull request: %s" % data)
    response = requests.post(PULLS_URL, json=data, headers=HEADERS)
    if response.status_code != 201:
        #abort_if_fail(response, "Unable to create pull request")
        print(response)

    return response

open_pull_request("[Don't review]Update VS by Robot", "", "master", "mszhanyi:zhanyi/updatevcver", is_draft=True)