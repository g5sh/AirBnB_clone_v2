#!/usr/bin/python3
"""
Fabric script to create a backup
"""
from fabric.api import local
from fabric.api import hide
from fabric.api import put
from fabric.api import run
from datetime import datetime
from os import path
from fabric.api import env


env.user = 'ubuntu'
env.hosts = ['35.185.87.99', '54.196.186.129']

def do_pack():
    '''Packes web_static in tgz format'''
    n = datetime.now()
    name = "web_static_{}{}{}{}{}{}.tgz".format(
        n.year, n.month, n.day, n.hour, n.minute, n.second)
    local('sudo mkdir -p versions')
    local("sudo tar -cvzf versions/{} web_static".format(name))
    size = os.stat("versions/{}".format(name)).st_size
    print("web_static packed: versions/{} -> {}".format(name, size))
    path = "versions/{}".format(name)
    return(path)


def do_deploy(archive_path):

    if not archive_path:
        return(False)
    name = archive_path.split('/')[1]
    try:
        put(archive_path, '/tmp/')
        run("sudo mkdir -p /data/web_static/releases/{}".format(name))
        run("sudo tar -xzf /tmp/{} -C /data/web_static/releases/{}"
            .format(name, name))
        run("sudo rm /tmp/{}".format(name))
        run("sudo mv /data/web_static/releases/{}/web_static/*\
        /data/web_static/releases/{}".format(name, name))
        run("sudo rm -rf /data/web_static/releases/{}/web_static"
            .format(name))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(name))
        print("New version deployed")
        return(True)
    except BaseException:
        return(False)


def deploy():

    try:
        path = do_pack()
    except BaseException:
        return(False)
    do_deploy(path)
