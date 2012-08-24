#!/usr/bin/python3


import os
import functools
import subprocess


def options(ctx):
    co = ctx.get_option_group('configure options')
    co.add_option(
            '--full-name', action="store", default=None,
            help="Specify full name of user. If missing parses /etc/passwd."
            )
    co.add_option(
            '--email', action="store", default=None,
            help="Specify email of user. If missing parses /etc/passwd."
            )

    so = ctx.add_option_group('setup options')
    so.add_option("--dry-run", action="store_true",
            default=False,
            help="Print commands, but do not execute.")
    so.add_option('--python', action='store',
            default='python',
            help='Set Python interpreter to use.')


def _parse_passwd(ctx):
    """ Parses /etc/passwd file and returns user information as dict.
    """
    for line in open('/etc/passwd'):
        fields = line[:-1].split(':')
        if fields[0] == ctx.env.USER:
            info = fields[4].split(',')
            return {
                    'uid': fields[2],
                    'gid': fields[3],
                    'home': fields[5],
                    'shell': fields[6],
                    'full_name': info[0],
                    'email': info[3],
                    }


def configure(ctx):
    ctx.find_program('git')
    ctx.find_program('virtualenv')
    ctx.find_program('python3', var='PYTHON')

    ctx.env.CONFIG_DIR = os.path.abspath(os.path.curdir)
    ctx.env.HOME_DIR = os.environ['HOME']
    ctx.env.USER = os.environ['USER']

    ctx.env.PASSWD_INFO = _parse_passwd(ctx)
    if ctx.options.full_name is None:
        ctx.env.FULL_NAME = ctx.env.PASSWD_INFO['full_name']
    else:
        ctx.env.FULL_NAME = ctx.options.full_name
    if ctx.options.email is None:
        ctx.env.EMAIL = ctx.env.PASSWD_INFO['email']
    else:
        ctx.env.EMAIL = ctx.options.email


def _sh(cmd, dry_run=False):
    print(cmd)
    if not dry_run:
        rcode = subprocess.call(cmd, shell=True)
        if rcode > 0:
            sys.exit(rcode)


def virtualenv(ctx):
    """ Initialize virtualenv environment.
    """
    sh = functools.partial(_sh, dry_run=ctx.options.dry_run)
    sh('virtualenv --python={0} env'.format(
        ctx.options.python))
    sh('env/bin/pip install MarkupSafe Jinja2')
