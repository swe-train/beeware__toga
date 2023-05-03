#!/usr/bin/env python
import re

from setuptools import setup

# Version handline needs to be programmatic because
# we can't import toga_curses to compute the version;
# and to support versioned subpackage dependencies
with open('toga_curses/__init__.py', encoding='utf8') as version_file:
    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]",
        version_file.read(),
        re.M
    )
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string.")

setup(
    version=version,
    install_requires=[
        'toga-core==%s' % version,
    ],
)
