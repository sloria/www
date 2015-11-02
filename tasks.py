from functools import partial

from invoke import task, run as inv_run
import os

DEPLOY_PATH = 'output'
REPO = 'https://github.com/sloria/sloria.github.io.git'

run = partial(inv_run, echo=True)

@task
def clean():
    if os.path.isdir(DEPLOY_PATH):
        run('rm -rf {deploy_path}'.format(deploy_path=DEPLOY_PATH))
        run('mkdir {deploy_path}'.format(deploy_path=DEPLOY_PATH))

@task
def build():
    run('pelican -s pelicanconf.py')

@task
def rebuild():
    clean()
    build()

@task
def regenerate():
    run('pelican -r -s pelicanconf.py')

@task
def serve():
    run('cd {deploy_path} && python -m SimpleHTTPServer'.format(deploy_path=DEPLOY_PATH))

@task
def reserve():
    build()
    serve()

@task
def publish():
    run('pelican content -o output -s pelicanconf.py')
    run('ghp-import output')
    run('git push {repo}  gh-pages:master'.format(repo=REPO))
