from functools import partial

from invoke import task, run as inv_run
import os

DEPLOY_PATH = 'output'

run = partial(inv_run, echo=True)


def do_clean(ctx):
    if os.path.isdir(DEPLOY_PATH):
        run('rm -rf {deploy_path}'.format(deploy_path=DEPLOY_PATH))
        run('mkdir {deploy_path}'.format(deploy_path=DEPLOY_PATH))

@task
def clean(ctx):
    do_clean(ctx)

@task
def build(ctx, debug=False, clean=False):
    if clean:
        do_clean(ctx)
    run('NODE_ENV={} pelican -o output -s pelicanconf.py'.format(
        'development' if debug else 'production',
    ))

@task
def rebuild(ctx):
    clean(ctx)
    build(ctx)

@task
def dev(ctx):
    clean(ctx)
    run('NODE_ENV=development pelican -r --debug -s pelicanconf.py')
