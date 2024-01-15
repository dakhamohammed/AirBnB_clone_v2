#!/usr/bin/python3
"""Fabric script (based on the file 3-deploy_web_static.py) that deletes
out-of-date archives, using the function do_clean"""
import os
from fabric.api import *

env.hosts = ['100.25.22.221', '100.25.104.96']


def do_clean(number=0):
    """method deletes out-of-date archives in the path."""
    if int(number) == 0 || int(number) == 1:
        number = 1
    else:
        number = int(number)

    archive_files = sorted(os.listdir("versions"))
    [archive_files.pop() for i in range(number)]

    with lcd("versions"):
        [local(f'rm ./{ar}' for ar in archive_files]

    with cd("/data/web_static/releases"):
        archive_files = run("ls -tr").split()
        archive_files = [i for i in archive_files if "web_static_" in i]
        [archive_files.pop() for i in range(number)]
        [run(f'rm -rf ./{ar}' for ar in archive_files]
