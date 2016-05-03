# -*- coding: utf-8 -*-

from contextlib import nested

from fabric.api import *
from fabric.contrib.project import rsync_project


def prepare_project():
    u"""
    Enters the directory and sources environment configuration.

    I know ``nested`` is deprecated, but what a nice shortcut it is here ;)
    """
    return nested(
        cd(PROJECT_PATH),
        prefix("source ../.virtualenvs/variablestars/bin/activate")
    )


PROJECT_PATH = "variablestars.net"

env.roledefs = {
    'web': ["variablestars2@variablestars.net"],
}
env.color = True
env.forward_agent = True
env.use_ssh_config = True


@task
@roles("web")
def git_pull():
    with cd(PROJECT_PATH):
        run("git pull origin master")


@task
@roles("web")
def upgrade_pip():
    with prepare_project():
        run("pip install pip setuptools wheel --upgrade")


@task
@roles("web")
def build_assets():
    local("make production_assets")


@task
@roles("web")
def update_requirements():
    with prepare_project():
        run("pip install -r requirements.txt")
        run("source ~/.nvm/nvm.sh && npm install --production")


@task
@roles("web")
def migrate():
    with prepare_project():
        run("python manage.py migrate")


@task
@roles("web")
def collect_static():
    rsync_project("{}/assets/build/".format(PROJECT_PATH), "assets/build/", delete=True)
    with prepare_project():
        run("python manage.py collectstatic --noinput")


@task
@roles("web")
def restart():
    run("appctl restart variablestars2")


@task
@roles("web")
def deploy():
    build_assets()
    git_pull()
    update_requirements()
    migrate()
    collect_static()
    restart()
