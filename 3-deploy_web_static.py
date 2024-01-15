#!/usr/bin/python3
"""Fabric script (based on the file 2-do_deploy_web_static.py) that creates
and distributes an archive to my web servers, using the function deploy"""
import os.path
from fabric.api import env
from fabric.api import local
from fabric.api import put
from fabric.api import run
from datetime import datetime

env.hosts = ['100.25.22.221', '100.25.104.96']


def do_pack():
    """Fabric script that generates a .tgz archive from the contents
    of the web_static folder."""
    _time = datetime.utcnow()
    archive = "versions/web_static_{}{}{}{}{}{}.tgz".format(_time.year,
                                                            _time.month,
                                                            _time.day,
                                                            _time.hour,
                                                            _time.minute,
                                                            _time.second)

    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    if local("tar -cvzf {} web_static".format(archive)).failed is True:
        return None

    return archive


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


def deploy():
    """method that creates and distributes an archive to my web servers"""
    archive_file = do_pack()
    if archive_file is None:
        return False
    return do_deploy(archive_file)
