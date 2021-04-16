#!/usr/bin/env python3

import requests
import lxml.html as lh

def get_lastest_vs():
    url =  "https://docs.microsoft.com/en-us/visualstudio/releases/2019/history"

    response = requests.get(url)

    doc = lh.fromstring(response.content)

    idx = 1
    versions = doc.xpath(f"//main//tbody//tr[{idx}]/td[1]")
    links = doc.xpath(f"//main//tbody//tr[{idx}]/td[4]/a[3]/@href")
    if not links[0].endswith("vs_BuildTools.exe"):
        raise ValueError("Fails to get correct vs_BuildTools")
    
    return versions[0].text_content(), links[0]

def updatefile(file_name, updates):
    lines = []
    with open(file_name, mode='r', encoding="utf-8") as f:
        lines = f.readlines()
        for item in updates:
            lines[item[0]] = item[1] + "\n"
    with open(file_name, mode='w', encoding="utf-8") as f:
        if len(lines) > 0:
            f.writelines(lines)

if __name__ == "__main__":
    version, link = get_lastest_vs()
    updates = []
    updates.append((3, f"# {version} buildTools"))
    updates.append((4, f"$VS_DOWNLOAD_LINK = '{link}'"))
    updatefile("../pytorch/.circleci/scripts/vs_install.ps1", updates)