#!/usr/bin/python3
""" Fabric script that generates a .tgz archive """
from fabric.api import local
from datetime import datetime
from os import path, mkdir


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.
    """
    # Get the current date and time in the format YYYYMMDDHHMMSS
    date = datetime.now().strftime("%Y%m%d%H%M%S")

    # Define the path of the archive file to be created
    file_path = "versions/web_static_{}.tgz".format(date)

    # Check if the versions directory exists, if not create it
    if not path.exists("versions"):
        mkdir("versions")

    # Use local command to create .tgz archive of web_static directory
    local("tar -cvzf {} web_static".format(file_path))

    # Check if the archive was created successfully
    if path.exists(file_path):
        return file_path
    else:
        return None
