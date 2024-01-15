#!/usr/bin/python3
"""Fabric script that generates a .tgz archive from the contents
of the web_static folder"""
import os.path
from fabric.api import local
from datetime import datetime


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
