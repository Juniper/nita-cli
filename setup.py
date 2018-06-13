# <*******************
#
# Copyright 2018 Juniper Networks, Inc. All rights reserved.
# Licensed under the Juniper Networks Script Software License (the "License").
# You may not use this script file except in compliance with the License, which is located at
# http://www.juniper.net/support/legal/scriptlicense/
# Unless required by applicable law or otherwise agreed to in writing by the parties, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#
# *******************>
"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import platform
import subprocess
import os
import re

def get_env_prefix():
  """
  Automatically identify os_type information which use for 
  install path of bash_completion.d
  """
  TARGET_BIN_PATH = '/usr/local/bin/'
  os_type = platform.system()
  cygwin = r'CYGWIN|cygwin'


  if os_type == "Linux":
    TARGET_COMPLETION_PATH = "/etc/bash_completion.d/"

  # Darwin is indicate Mac OS
  elif os_type == "Darwin":
    proc = subprocess.Popen(
      'brew --prefix', shell=True, stdout=subprocess.PIPE,
      stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    brew_prefix = "{0}/etc/bash_completion.d/".format(stdout.rstrip())
    TARGET_COMPLETION_PATH = brew_prefix

  # Return true if CYGWIN or cygwin there in os type string
  elif re.search(cygwin, os_type):
    TARGET_COMPLETION_PATH = '/etc/bash_completion.d/'
    TARGET_BIN_PATH = '/usr/bin/'
    if not os.path.exists(TARGET_COMPLETION_PATH):
      os.makedirs(TARGET_COMPLETION_PATH)

  else:
    raise ValueError('Unknown OS type found. This Operating System is not supported.')

  return TARGET_COMPLETION_PATH, TARGET_BIN_PATH


def run_autocomplete():
  """
  Run script that Generate file nita autocompletion.
  """
  cmd = 'python autocomplete'
  proc = subprocess.Popen(
    cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  stdout, stderr = proc.communicate()


TARGET_COMPLETION_PATH, TARGET_BIN_PATH = get_env_prefix()
run_autocomplete()

setup(
    name='nita_cli',
    version='0.0.2',
    description='NITA CLI',
    long_description='NITA command line wrapper',
    author='Jose Miguel Izquierdo',
    author_email='jizquierdo@juniper.net',
    install_requires=['pyyaml','jinja2'],
    url='',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    data_files=[(TARGET_BIN_PATH, ['nita']),
    (TARGET_COMPLETION_PATH, ['bash_completion.d/nita'])]
)