#!/usr/bin/env python

import re

from codecs import open

from setuptools import setup

packages = [
    'xavier',
    'xavier.aws',
    'xavier.slack',
]

requires = [
    "requests>=2.4",
    "routes>=2.4",
    "frozendict",
]
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
    url="https://github.com/bepress/xavier",
    packages=packages,
    package_data={'': ['LICENSE']},
    package_dir={'xavier': 'xavier'},
    include_package_data=True,
    install_requires=requires,
    license='MIT',
    zip_safe=False,
    tests_require=test_requirements,
)
