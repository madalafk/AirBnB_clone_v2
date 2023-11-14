#!/usr/bin/python3
"""
Fabric script based on the file 1-pack_web_static.py that distributes an
archive to the web servers
"""

from fabric.api import put, run, env
from os.path import exists

env.hosts = ['100.25.30.112', '54.237.113.234']


def do_deploy(archive_path):
    """Distributes an archive to the web servers."""
    if not exists(archive_path):
        print(f"Error: Archive {archive_path} does not exist.")
        return False

    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"

        print(f"Uploading {file_n} to /tmp/")
        put(archive_path, '/tmp/')

        print(f"Creating directory {path}{no_ext}/")
        run('mkdir -p {}{}/'.format(path, no_ext))

        print(f"Extracting {file_n} to {path}{no_ext}/")
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext))

        print(f"Removing /tmp/{file_n}")
        run('rm /tmp/{}'.format(file_n))

        print(f"Moving web_static contents to {path}{no_ext}/")
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))

        print(f"Removing {path}{no_ext}/web_static")
        run('rm -rf {}{}/web_static'.format(path, no_ext))

        print(f"Removing /data/web_static/current")
        run('rm -rf /data/web_static/current')

        print(f"Creating symlink to {path}{no_ext}/ at /data/web_static/current")
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))

        print("Deployment completed successfully.")
        return True

    except Exception as e:
        print(f"Error: {e}")
        return False

