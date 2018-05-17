#!/usr/bin/env python3
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

NAME = 'pop'
DESC = ('The Plugin Oriented Programming System')

# Version info -- read without importing
_locals = {}
with open('pop/version.py') as fp:
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
        for subdir in ('pop', 'tests'):
            for root, dirs, files in os.walk(os.path.join(os.path.dirname(__file__), subdir)):
                for dir_ in dirs:
                    if dir_ == '__pycache__':
                        shutil.rmtree(os.path.join(root, dir_))


def discover_packages():
    modules = []
    for package in ('pop', ):
        for root, _, files in os.walk(os.path.join(SETUP_DIRNAME, package)):
            if '__init__.py' not in files:
                continue
            pdir = os.path.relpath(root, SETUP_DIRNAME)
            modname = pdir.replace(os.sep, '.')
            modules.append(modname)
    return modules


setup(name=NAME,
      author='Thomas S Hatch',
      author_email='thatch45@gmail.com',
      url='https://rossosoft.com',
      version=VERSION,
      description=DESC,
      classifiers=[
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Development Status :: 5 - Production/Stable',
          ],
      packages=discover_packages(),
      cmdclass={'clean': Clean},
      )
