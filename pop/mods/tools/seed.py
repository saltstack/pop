'''
Seed a new project with a directory tree and first files
'''
# Import python libs
import os


SETUP = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import python libs
import os
import sys
import shutil

# SETUPTOOLS WILL NOT BE TOLERATED!!
# I have made MANY python projects and those idiotic setuptools
# create pkg_resources deps and unnecessarily muddy up the
# startup process. They add NO useful features that cannot be
# easily derived from distutils, which is a clean and reasonable
# packaging system!

from distutils.core import setup
from distutils.core import Command

NAME = '%%NAME%%'
DESC = ("")

# Version info -- read without importing
_locals = {}
with open('{}/version.py'.format(NAME)) as fp:
    exec(fp.read(), None, _locals)
VERSION = _locals['version']
SETUP_DIRNAME = os.path.dirname(__file__)
if not SETUP_DIRNAME:
    SETUP_DIRNAME = os.getcwd()


class Clean(Command):
    user_options = []
    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        for subdir in (NAME, 'tests'):
            for root, dirs, files in os.walk(os.path.join(os.path.dirname(__file__), subdir)):
                for dir_ in dirs:
                    if dir_ == '__pycache__':
                        shutil.rmtree(os.path.join(root, dir_))


def discover_packages():
    modules = []
    for package in (NAME, ):
        for root, _, files in os.walk(os.path.join(SETUP_DIRNAME, package)):
            if '__init__.py' not in files:
                continue
            pdir = os.path.relpath(root, SETUP_DIRNAME)
            modname = pdir.replace(os.sep, '.')
            modules.append(modname)
    return modules


setup(name=NAME,
      author='',
      author_email='',
      url='',
      version=VERSION,
      description=DESC,
      classifiers=[
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Development Status :: 5 - Production/Stable',
          ],
      scripts=['scripts/%%NAME%%'],
      packages=discover_packages(),
      cmdclass={'clean': Clean},
      )
'''

SCRIPT = '''#!/usr/bin/env python3

import pop.hub

hub = pop.hub.Hub()
hub.tools.sub.add('%%NAME%%', pypath='%%NAME%%.mods.%%NAME%%', contracts_pypath='%%NAME%%.contracts.%%NAME%%', init=True)
'''

INIT = '''def new(hub):
    print('%%NAME%% works!')
'''

def new(hub):
    '''
    Given the option in hub.opts "seed_name" create a directory tree for a
    new pop project
    '''
    name = hub.opts['seed_name']
    hub.tools.seed.mkdir('scripts')
    hub.tools.seed.mkdir(name, 'mods', name)
    hub.tools.seed.mkdir(name, 'contracts', name)
    hub.tools.seed.mksetup(name)
    hub.tools.seed.mkscript(name)
    hub.tools.seed.mkinit(name)
    hub.tools.seed.mkversion(name)


def mkdir(hub, *args):
    '''
    Create the named dir
    '''
    path = os.getcwd()
    for dir_ in args:
        path = os.path.join(path, dir_)
        init_fn = os.path.join(path, '__init__.py')
        try:
            os.makedirs(path)
        except Exception:
            print('Failed to make {}'.format(path))
            continue
        with open(init_fn, 'w+') as fp:
            fp.write('')


def mksetup(hub, name):
    '''
    Create and write out a setup.py file
    '''
    path = os.getcwd()
    path = os.path.join(path, 'setup.py')
    setup_str = SETUP.replace('%%NAME%%', name)
    with open(path, 'w+') as fp:
        fp.write(setup_str)


def mkscript(hub, name):
    '''
    Create and write out a setup.py file
    '''
    path = os.getcwd()
    path = os.path.join(path, 'scripts', name)
    script_str = SCRIPT.replace('%%NAME%%', name)
    with open(path, 'w+') as fp:
        fp.write(script_str)


def mkinit(hub, name):
    '''
    Create the intial init.py
    '''
    path = os.getcwd()
    path = os.path.join(path, name, 'mods', name, 'init.py')
    init_str = INIT.replace('%%NAME%%', name)
    with open(path, 'w+') as fp:
        fp.write(init_str)


def mkversion(hub, name):
    '''
    Create the version.py file
    '''
    path = os.getcwd()
    path = os.path.join(path, name, 'version.py')
    with open(path, 'w+') as fp:
        fp.write('version = \'1.0.0\'')
