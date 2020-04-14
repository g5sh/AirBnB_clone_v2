#!/usr/bin/python3
"""
Fabric script to create a backup
"""
from fabric.api import local
from fabric.api import hide
from datetime import datetime


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
