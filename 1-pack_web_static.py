#!/usr/bin/python3
"""
A script to generate a .tgz archive using Fabric.
"""
import os
from datetime import datetime
from fabric.api import local


def do_pack():
    """ Generates a .tgz archive from the contents of web_static folder. """
    if not os.path.isdir("versions"):
        os.mkdir("versions")
    cur_time = datetime.now()
    output = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        cur_time.year,
        cur_time.month,
        cur_time.day,
        cur_time.hour,
        cur_time.minute,
        cur_time.second
    )
    try:
        print("Packing web_static to {}".format(output))
        local("tar -cvzf {} web_static".format(output))
        archize_size = os.stat(output).st_size
        print("web_static packed: {} -> {} Bytes".format(output, archize_size))
        return output
    except Exception:
        return None
