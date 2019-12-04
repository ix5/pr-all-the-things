#!/usr/bin/python3

import os
import subprocess

from constants import *
from config import *

def checkout_branch(branchname):
    p = subprocess.Popen(
          ['git', 'checkout', '-b', branchname],
          stdin=subprocess.PIPE, stdout=subprocess.PIPE,
          encoding='utf8'  # python3 only
        )
    res = p.communicate()
    if res[1]:
        print("Error checking out %s: %s" % (branchname, res[1]))
    #p.returncode

def run_script(script_path, platform=None, device=None):
    _env = os.environ.copy()
    if platform:
        _env["PLATFORM"] = platform
    if device:
        _env["DEVICE"] = device
    p = subprocess.Popen(
          ['bash', script_path],
          stdin=subprocess.PIPE, stdout=subprocess.PIPE,
          env=_env,
          encoding='utf8'  # python3 only
        )
    res = p.communicate()
    if res[1]:
        print("Error running script %s: %s" % (script_path, res[1]))

def git_add_and_commit(commit_msg, pause_to_edit=False):
    p = subprocess.Popen(
          ['git', 'add', '-A'],
          stdin=subprocess.PIPE, stdout=subprocess.PIPE,
          encoding='utf8'  # python3 only
        )
    res = p.communicate()
    if res[1]:
        print("Error adding files: %s" % (res[1]))

    _cmd = ['git', 'commit']
    if pause_to_edit:
        _cmd.append("--edit")
    _cmd.extend(["-m", commit_msg])

    p = subprocess.Popen(
           _cmd,
          stdin=subprocess.PIPE, stdout=subprocess.PIPE,
          encoding='utf8'  # python3 only
        )
    res = p.communicate()

def git_push(branchname):
    p = subprocess.Popen(
          ['git', 'push', GITHUB_REMOTE_NAME, branchname],
          stdin=subprocess.PIPE, stdout=subprocess.PIPE,
          encoding='utf8'  # python3 only
        )

def git_create_pr(branchname):
    # TODO
    pass


def main():
    _current_dir = os.getcwd()
    print("Current dir: %s" % _current_dir)
    print("All devices: %s" % ALL_DEVICES)
    branchname = input("Branch to create: ")
    scriptname = input("Script to use: ")
    script_path = os.path.join(_current_dir, scriptname)
    commit_msg = input("Commit message: ")
    _platform='tama'
    for _device in ALL_DEVICES[_platform]:
        os.chdir(os.path.join(DEVICES_ROOT_DIR, "%s%s" % (DEVICE_PATH_TEMPLATE, _device)))
        checkout_branch(branchname)
        run_script(script_path, platform=_platform, device=_device)
        git_add_and_commit(commit_msg, False)
    os.chdir(_current_dir)
    print("All done!")

if __name__ == '__main__':
    main()
