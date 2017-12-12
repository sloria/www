from functools import partial

from invoke import task, run as inv_run
import os

DEPLOY_PATH = 'output'
REPO = 'https://github.com/sloria/sloria.github.io.git'

run = partial(inv_run, echo=True)


def do_clean(ctx):
    if os.path.isdir(DEPLOY_PATH):
        run('rm -rf {deploy_path}'.format(deploy_path=DEPLOY_PATH))
        run('mkdir {deploy_path}'.format(deploy_path=DEPLOY_PATH))


@task
def clean(ctx):
    do_clean(ctx)


@task
def build(ctx, clean=False):
    if clean:
        do_clean(ctx)
    run('pelican -o output -s pelicanconf.py')


@task
def rebuild(ctx):
    clean(ctx)
    build(ctx)


@task
def regenerate(ctx):
    run('pelican -r --debug -s pelicanconf.py')


@task
def serve(ctx, port=1234):
    run('cd {deploy_path} && python -m pelican.server {port}'.format(
        deploy_path=DEPLOY_PATH, port=port))


@task
def reserve(ctx):
    build(ctx)
    serve(ctx)


@task
def publish(ctx):
    clean(ctx)
    run('pelican content -o output -s pelicanconf.py')
    run('ghp-import output')
    run('git push {repo}  gh-pages:master'.format(repo=REPO))
