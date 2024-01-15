#!/usr/bin/python3
"""Fabric script (based on the file 1-pack_web_static.py) that distributes
an archive to ymy web servers, using the function do_deploy"""
import os.path
from fabric.api import env
from fabric.api import put
from fabric.api import run

env.hosts = ['100.25.22.221', '100.25.104.96']


def do_deploy(archive_path):
    """method distributes an archive to your web servers."""
    if os.path.isfile(archive_path) is False:
        return False

    archive = archive_path.split("/")[-1]
    _file = archive.split(".")[0]

    if put(archive_path, "/tmp/{}".format(archive)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/".
            format(_file)).failed is True:
        return False
    if run("mkdir -p /data/web_static/releases/{}/".
            format(_file)).failed is True:
        return False
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
            format(archive, _file)).failed is True:
        return False
    if run("rm /tmp/{}".format(archive)).failed is True:
        return False
    if run("mv /data/web_static/releases/{}/web_static/* "
            "/data/web_static/releases/{}/".
            format(_file, _file)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/web_static".
            format(_file)).failed is True:
        return False
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
            format(_file)).failed is True:
        return False
    return True
