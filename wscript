#!/usr/bin/python3


import os
import functools
import subprocess
import waflib
import imp


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
    co.add_option(
            '--apps', action="store", default=None,
            help="Configuration apps to install.",
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

class Renderer:
    """ Renders many templates.
    """

    def __init__(self, templates_dirs, context):
        from jinja2 import Environment, FileSystemLoader
        self.env = Environment(loader=FileSystemLoader(templates_dirs))
        self.context = context
        self.templates = []

    def append(self, template_name, output_file):
        """ Append template to templates list.
        """
        self.templates.append((template_name, output_file))

    def render(self):
        """ Renders all templates.
        """
        from jinja2 import exceptions
        for template_name, output_file in self.templates:
            try:
                template = self.env.get_template(template_name)
            except exceptions.TemplateSyntaxError as e:
                print(('{0.filename} ({0.name}):'
                    '{0.lineno} {0.message}').format(e))
                raise
            waflib.Logs.info('Rendered: {0}.'.format(output_file))
            try:
                open(output_file, 'w').write(template.render(self.context))
            except IOError:
                os.makedirs(os.path.dirname(output_file))
                open(output_file, 'w').write(template.render(self.context))


class App:
    """ Configuration application.
    """

    def __init__(self, name, path, ctx):
        self.name = name
        self.path = path
        self.ctx = ctx
        self.env = ctx.env
        self.config = {}
        self.templates = os.path.join(path, 'templates')
        self.templates_dirs = os.path.join(path, 'templates_dirs')

        self.config_functions = {}
        self.config_functions['home'] = (
                lambda path: os.path.join(self.env.HOME_DIR, path))
        self.config_functions['scripts'] = (
                lambda path: os.path.join(self.env.BIN_DIR, path))
        self.config_functions['app'] = (
                lambda path: os.path.join(self.path, path))
        self.load_config()

    def load_config(self):
        """ Loads configuration from app config file.
        """
        path = os.path.join(self.path, 'config.py')
        with open(path) as fp:
            self.config.update(eval(fp.read(), self.config_functions))

    def render_templates(self):
        """ Renders templates.
        """
        renderer = Renderer(
                [self.templates],
                {
                    'env': self.env,
                    'config': self.config,
                    'app_name': self.name,
                    'app_path': self.path,
                    }
                )
        for target, template_name in self.config['templates'].items():
            renderer.append(template_name, target)
        renderer.render()

    def render_templates_dirs(self):
        """ Renders template dirs.
        """
        if 'templates_dirs' not in self.config:
            return
        renderer = Renderer(
                [self.templates, self.templates_dirs],
                {
                    'env': self.env,
                    'config': self.config,
                    'app_name': self.name,
                    'app_path': self.path,
                    }
                )
        def search(target, path):
            full_path = os.path.join(self.templates_dirs, path)
            if os.path.isdir(full_path):
                for file in os.listdir(full_path):
                    search(
                            os.path.join(target, file),
                            os.path.join(path, file))
            else:
                renderer.append(path, target)
        for target, templates_dir_name in (
                self.config['templates_dirs'].items()):
            search(target, templates_dir_name)
        renderer.render()

    def make_dirs(self):
        """ Makes directories.
        """
        for path in self.config.get('mkdir', ()):
            os.makedirs(path, exist_ok=True)

    def run_routines(self):
        """ Runs app's routines.
        """
        if 'routines' not in self.config:
            return
        self.routines = {}
        for name, details in self.config['routines'].items():
            path, module_name, function = details
            fpd = imp.find_module(module_name, [path])
            module = imp.load_module(module_name, *fpd)
            self.routines[name] = getattr(module, function)
        for info in self.config['exec']:
            self.routines[info['routine']](self.ctx, **info)


class AppsManager:
    """ Configuration apps manager.
    """

    def __init__(self, ctx):
        self.ctx = ctx
        self.env = ctx.env
        self.apps = {}

        self.load_apps()

    def load_apps(self):
        """ Loads configuration applications.
        """
        for name, path in self.env.APPS:
            self.apps[name] = App(name, path, self.ctx)

    def render_templates(self):
        """ Renders templates from all apps.
        """
        for app in self.apps.values():
            app.render_templates()

    def render_templates_dirs(self):
        """ Renders templates dirs from all apps.
        """
        for app in self.apps.values():
            app.render_templates_dirs()

    def make_dirs(self):
        """ Makes dirs for all apps.
        """
        for app in self.apps.values():
            app.make_dirs()

    def run_routines(self):
        """ Runs routines for all apps.
        """
        for app in self.apps.values():
            app.run_routines()


def configure(ctx):
    ctx.find_program('git')
    ctx.find_program('virtualenv')
    ctx.find_program('python3', var='PYTHON')

    ctx.env.CONFIG_DIR = os.path.abspath(os.path.curdir)
    ctx.env.APPS_DIR = os.path.join(ctx.env.CONFIG_DIR, 'apps')
    ctx.env.HOME_DIR = os.environ['HOME']
    ctx.env.BIN_DIR = os.path.join(ctx.env.HOME_DIR, '.bin')
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

    if ctx.options.apps is None:
        apps = os.listdir(ctx.env.APPS_DIR)
    else:
        apps = ctx.options.apps.split(',')

    ctx.env.APPS = [
            (name, os.path.join(ctx.env.APPS_DIR, name))
            for name in apps
            ]


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


def installdeps(ctx):
    """ Install all required dependencies.
    """

    sh = functools.partial(_sh, dry_run=ctx.options.dry_run)

    if not ctx.options.dry_run and not os.geteuid() == 0:
        sys.exit("Only root can run this script.")

    packages = [
        ]

    sh('apt-get install %s' % ' '.join(packages))


def build(ctx):
    """ Makes changes.
    """
    manager = AppsManager(ctx)
    manager.make_dirs()
    manager.render_templates()
    manager.render_templates_dirs()
    manager.run_routines()


# --------
# Hack to pass ``BuildContext`` to commands other than ``build``.
from waflib.Build import BuildContext
def use_build_context_for(*cmds):
    for cmd in cmds:
        type('BldCtx_' + cmd, (BuildContext,), {'cmd': cmd, 'fun': cmd})
use_build_context_for('installdeps')
# --------
