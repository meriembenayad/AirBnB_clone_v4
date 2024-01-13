#!/usr/bin/python3
"""
Creates and distributes an archive to your web servers
"""
""" from fabric.api import env """
do_pack = __import__('2-do_deploy_web_static').do_pack
do_deploy = __import__('2-do_deploy_web_static').do_deploy

""" env.hosts = ['3.85.196.229', '34.207.221.84'] """


def deploy():
    """
    Creates & Distributes an archive to the web servers.
    """
    archive_path = do_pack()

    if archive_path is None:
        return False

    return do_deploy(archive_path)
