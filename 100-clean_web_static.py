#!/usr/bin/python3
# Fabfile to delete out-of-date archives using do clean method.
import os
from fabric.api import *

env.hosts = ['100.25.22.221', '100.25.104.96']


def do_clean(number=0):
    """Delete out-of-date archives.
    Args:
        number: The number of archives to keep.

    If number is 0 or 1, keeps only the most recent archive. If
    number is 2, keeps the most and second-most recent archives,
    etc.
    """
    number = 1 if int(number) == 0 else int(number)

    archive_files = sorted(os.listdir("versions"))
    [archive_files.pop() for i in range(number)]
    with lcd("versions"):
        [local("rm ./{}".format(a)) for a in archive_files]

    with cd("/data/web_static/releases"):
        archive_files = run("ls -tr").split()
        archive_files = [a for a in archive_files if "web_static_" in a]
        [archive_files.pop() for i in range(number)]
        [run("rm -rf ./{}".format(a)) for a in archive_files]
