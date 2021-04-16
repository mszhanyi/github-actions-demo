#!/usr/bin/env python3

def get_lastest_vc_ver():
    return "https://download.visualstudio.microsoft.com/download/pr/3105fcfe-e771-41d6-9a1c-fc971e7d03a7/e0c2f5b63918562fd959049e12dffe64bf46ec2e89f7cadde3214921777ce5c2/vs_BuildTools.exe"

def updatefile(file_name, line_idx, text):
    lines = []
    with open(file_name, mode='r', encoding="utf-8") as f:
        lines = f.readlines()
        lines[line_idx] = text + "\n"
    with open(file_name, mode='w', encoding="utf-8") as f:
        if len(lines) > 0:
            f.writelines(lines)

if __name__ == "__main__":
    update_text = f"$VS_DOWNLOAD_LINK = '{get_lastest_vc_ver()}'"
    updatefile("../pytorch/.circleci/scripts/vs_install.ps1", 4, update_text)