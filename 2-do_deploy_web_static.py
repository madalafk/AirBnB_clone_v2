#!/usr/bin/python3
"""
A PY script to distributes a .tgz archive using Fabric.
"""
import os
from datetime import datetime
from fabric.api import local, env, put, run

"""
my Remote webservers details
"""
env.hosts = ["100.25.30.112", "54.237.113.234"]
env.user = "ubuntu"
env.key_filename = "~/.ssh/school"

def do_pack():
    #Generates a .tgz archive from the contents of web_static folder.
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


def do_deploy(archive_path):
    """
    Distributing archived file to host servers.
        - Argument:
            - archive_path: The path to the archived file.
    """
    if not os.path.exists(archive_path):
        return False
    try:
        file_name = os.path.basename(archive_path)
        folder_name = file_name.replace(".tgz", "")
        folder_path = "/data/web_static/releases/{}/".format(folder_name)
        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(folder_path))
        run("tar -xzf /tmp/{} -C {}".format(file_name, folder_path))
        run("rm /tmp/{}".format(file_name))
        run("mv {}/web_static/* {}".format(folder_path, folder_path))
        run("rm -rf {}/web_static".format(folder_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(folder_path))
        print("New version deployed!")
        return True
    except Exception:
        return False
