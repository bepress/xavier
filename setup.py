#!/usr/bin/env python

import os
import re
import sys

from codecs import open

from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass into py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

packages = [
    'xavier',
]

requires = []
test_requirements = ['pytest>=2.8.0']

with open('xavier/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

with open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()


setup(
    name='xavier',
    version=version,
    description='Lambda bot',
    long_description=readme,
    author='Alex Kessinger',
    author_email='akessinger@bepress.com',
    packages=packages,
    package_data={'': ['LICENSE', 'NOTICE']},
    package_dir={'xavier': 'xavier'},
    include_package_data=True,
    install_requires=requires,
    license='Apache 2.0',
    zip_safe=False,
    cmdclass={'test': PyTest},
    tests_require=test_requirements,
)
