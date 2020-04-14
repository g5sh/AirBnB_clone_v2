#!/usr/bin/python3
"""
Fabric script to create a backup
"""
from fabric.api import local
from fabric.api import hide
from datetime import datetime
import os


env.hosts = ['localhost']


def do_pack():
    n = datetime.now()
    name = "web_static_{}{}{}{}{}{}.tgz".format(n.year, n.month,
                                                n.day, n.hour,
                                                n.minute, n.second)
    local('sudo mkdir -p versions')
    local("sudo tar -cvzf versions/{} web_static".format(name))
    size = os.stat("versions/{}".format(name)).st_size
    print("web_static packed: versions/{} -> {}".format(name, size))
