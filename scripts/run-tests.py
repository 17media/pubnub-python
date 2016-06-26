#!/usr/bin/env python
# Don't run tests from the root repo dir.
# We want to ensure we're importing from the installed
# binary package not from the CWD.

import os
from subprocess import check_call

_dname = os.path.dirname

REPO_ROOT = _dname(_dname(os.path.abspath(__file__)))
os.chdir(os.path.join(REPO_ROOT, 'tests'))

pyenv_version = os.getenv('PYENV_VERSION', 0)
travis_version = os.getenv('TRAVIS_PYTHON_VERSION', 0)
version = str(travis_version or pyenv_version)

print("Version is", version)


def run(command):
    return check_call(command, shell=True)

if version.startswith('2.7'):
    run('py.test --cov=../pubnub')
elif version.startswith('2.6'):
    run('py.test --cov=../pubnub --ignore=integrational/tornado/  --ignore=integrational/twisted/')
else:
    run('py.test --cov=../pubnub/ --ignore=integrational/twisted/')