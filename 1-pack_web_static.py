#!/usr/bin/phyton3
import os
from fabric.api import local, run, prefix, env
from datetime import datetime


env.host = ['localhost']

def do_pack():
    time = datetime.now()
    web  = "web_static_{}{}{}{}{}{}.tgz".format(time.year,
                                                time.month,
                                                time.day,
                                                time.hour,
                                                time.minute,
                                                time.second)
    local('mkdir -p versions')
    local("tar -cvfz versions/{} web_static".format(web))
    size = os.stat("versions/{}".format(web)).st_size
    print("web_static package: versions/{} -> {}".format(web, size))
