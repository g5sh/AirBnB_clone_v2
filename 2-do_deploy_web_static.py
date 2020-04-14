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


def do_deploy(archive_path):
    """
    Upload backup to server
    """
    if path.exists(archive_path):
        file_name = archive_path.split('/')[1]
        clean_name = file_name.split('.')[0]
        put(archive_path, '/tmp/')
        run('sudo mkdir -p /data/web_static/releases/{}'.format(clean_name))
        run('sudo tar -xzf /tmp/{0} -C /data/web_static/releases/{1}'.
            format(file_name, clean_name))
        run('sudo mv /data/web_static/releases/{0}/web_static/* '
            '/data/web_static/releases/{1}'.format(clean_name, clean_name))
        run('sudo rm /tmp/{}'.format(file_name))
        run('sudo rm -rf /data/web_static/current')
        run('sudo rm -rf /data/web_static/releases/{}/web_static/'.
            format(clean_name))
        run('sudo ln -sf /data/web_static/releases/{} /data/web_static/current'.
            format(clean_name))
        print('New version deployed!')
        return True
    else:
        return False
