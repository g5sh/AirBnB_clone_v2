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
env.hosts = ['35.196.106.109', '54.196.186.129']


def do_pack():
    """
    Create folder backup with date and tgz extension
    """
    print("Packing web_static to versions/web_static_%s.tgz" %
          (datetime.now().strftime('%Y%m%d%H%M%S')))

    with hide('running'):
        versions_dir = local('mkdir -p versions')

        tar = local('tar -cvzf versions/web_static_%s.tgz web_static/' %
                (datetime.now().strftime('%Y%m%d%H%M%S')))

    with hide('running'):
        file_size = local('wc -c < versions/web_static_{}.tgz'.
                          format(datetime.now().strftime('%Y%m%d%H%M%S')),
                          capture=True)

    print("web_static packed: versions/web_static_{:s}.tgz -> {:}Bytes".
          format(datetime.now().strftime('%Y%m%d%H%M%S'), file_size))

    with hide('running'):
        archive_path = "versions/web_static_{:s}.tgz".\
            format(datetime.now().strftime('%Y%m%d%H%M%S'))


def do_deploy(archive_path):
    """
    Upload backup to server
    """
    if not archive_path:
        return(False)
    name = archive_path.split('/')[1]
    try:
        put(archive_path, '/tmp/')
        run("mkdir -p /data/web_static/releases/{}".format(name))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}"
            .format(name, name))
        run("rm /tmp/{}".format(name))
        run("mv /data/web_static/releases/{}/web_static/*\
        /data/web_static/releases/{}".format(name, name))
        run("rm -rf /data/web_static/releases/{}/web_static"
            .format(name))
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(name))
        print("New version deployed")
        return(True)
    except BaseException:
        return(False)


def deploy():
    """
    Full deployment
    """
    try:
        path = do_pack()
    except BaseException:
        return(False)
    do_deploy(path)
