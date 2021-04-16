#!/usr/bin/env python3

import sys
import os
import json
import requests

def set_env(name, value):
    """helper function to echo a key/value pair to the environement file
    Parameters:
    name (str)  : the name of the environment variable
    value (str) : the value to write to file
    """
    '''
    environment_file_path = os.environ.get("GITHUB_ENV")

    with open(environment_file_path, "a") as environment_file:
        environment_file.write("%s=%s" % (name, value))
    '''
    
API_VERSION = "v3"
BASE = "https://api.github.com"

HEADERS = {
    "Authorization": "token %s" % os.environ.get("pytorch_token"),
    "Accept": "application/vnd.github.%s+json;application/vnd.github.antiope-preview+json;application/vnd.github.shadow-cat-preview+json"
    % API_VERSION,
}

print(HEADERS)

# URLs
REPO_URL = "%s/repos/%s" % (BASE, "pytorch/pytorch")
# REPO_URL = "%s/repos/%s" % (BASE, "mszhanyi/pytorch")
ISSUE_URL = "%s/issues" % REPO_URL
PULLS_URL = "%s/pulls" % REPO_URL

def find_pull_request(listing, source):
    """Given a listing and a source, find a pull request based on the source
    (the branch name).
    Parameters:
    listing (list) : the list of PR objects (dict) to parse over
    source   (str) : the source (head) branch to look for
    """
    if listing:
        for entry in listing:
            if entry.get("head", {}).get("ref", "") == source:
                print("Pull request from %s is already open!" % source)
                return entry
            
def list_pull_requests(target, source):
    """Given a target and source, return a list of pull requests that match
    (or simply exit given some kind of error code)
    Parameters:
    target (str) : the target branch
    source (str) : the source branch
    """
    # Check if the branch already has a pull request open
    params = {"base": target, "head": source, "state": "open"}
    print("Params for checking if pull request exists: %s" % params)
    response = requests.get(PULLS_URL, params=params)

    # Case 1: 404 might warrant needing a token
    if response.status_code == 404:
        response = requests.get(PULLS_URL, params=params, headers=HEADERS)
    if response.status_code != 200:
        abort_if_fail(response, "Unable to retrieve information about pull requests")

    return response.json()

def set_pull_request_groups(response):
    """Given a response for an open or updated PR, set metadata
    Parameters:
    response (requests.Response) : a requests response, unparsed
    """
    # Expected return codes are 0 for success
    pull_request_return_code = (
        0 if response.status_code == 201 else response.status_code
    )
    response = response.json()
    print("::group::github response")
    print(response)
    print("::endgroup::github response")
    number = response.get("number")
    html_url = response.get("html_url")
    print("Number opened for PR is %s" % number)
    set_env("PULL_REQUEST_NUMBER", number)
    print("::set-output name=pull_request_number::%s" % number)
    set_env("PULL_REQUEST_RETURN_CODE", pull_request_return_code)
    print("::set-output name=pull_request_return_code::%s" % pull_request_return_code)
    set_env("PULL_REQUEST_URL", html_url)
    print("::set-output name=pull_request_url::%s" % html_url)
    
def create_pull_request(
    source,
    target,
    body,
    title,
    assignees,
    reviewers,
    team_reviewers,
    is_draft=False,
    can_modify=True,
    state="open",
):
    """Create pull request is the base function that determines if the PR exists,
    and then updates or creates it depending on user preferences.
    """
    listing = list_pull_requests(target, source)

    # Determine if the pull request is already open
    entry = find_pull_request(listing, source)
    response = None

    # Case 1: we found the PR, the user wants to pass
    if entry and os.environ.get("PASS_IF_EXISTS"):
        print("PASS_IF_EXISTS is set, exiting with success status.")
        sys.exit(0)

    # Does the user want to update the existing PR?
    if entry and os.environ.get("PULL_REQUEST_UPDATE"):
        response = update_pull_request(entry, title, body, target, state)
        set_pull_request_groups(response)

    # If it's not open, we open a new pull request
    elif not entry:
        response = open_pull_request(title, body, target, source, is_draft, can_modify)
        set_pull_request_groups(response)

    # If we have a response, parse into json (no longer need retvals)
    response = response.json() if response else None

    # If we have opened or updated, we can add assignees
    if response and assignees:
        add_assignees(response, assignees)
    if response and (reviewers or team_reviewers):
        add_reviewers(response, reviewers, team_reviewers)

def update_pull_request(entry, title, body, target, state=None):
    """Given an existing pull request, update it.
    Parameters:
    entry      (dict) : the pull request metadata
    title       (str) : the title to set for the new pull request
    body        (str) : the body to set for the new pull request
    target      (str) : the target branch
    state      (bool) : the state of the PR (open, closed)
    """
    print("PULL_REQUEST_UPDATE is set, updating existing pull request.")

    data = {
        "title": title,
        "body": body,
        "base": target,
        "state": state or "open",
    }
    # PATCH /repos/{owner}/{repo}/pulls/{pull_number}
    url = "%s/%s" % (PULLS_URL, entry.get("number"))
    print("Data for updating pull request: %s" % data)
    response = requests.patch(url, json=data, headers=HEADERS)
    if response.status_code != 200:
        abort_if_fail(response, "Unable to create pull request")

    return response

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

#open_pull_request("[Don't review]Update VS by Robot", "", "master", "mszhanyi:zhanyi/updatevcver", is_draft=True)
if __name__ == "__main__"
    os.environ['PULL_REQUEST_UPDATE'] = 1
    create_pull_request(source="mszhanyi:zhanyi/updatevcver", target="master", body="", title="[Don't review] Update VS by Robot", 
                    assignees=None, reviewers=None, team_reviewers=None, is_draft=True, can_modify=True)