"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import platform
import subprocess

def get_env_prefix():
  """
  Automatically identify os_type information which use for 
  install path of bash_completion.d
  """
  os_type = platform.system()

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

  return TARGET_COMPLETION_PATH

def run_autocomplete():
  """
  Run script that Generate file nita autocompletion.
  """
  cmd = 'python autocomplete'
  proc = subprocess.Popen(
    cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  stdout, stderr = proc.communicate()


TARGET_COMPLETION_PATH = get_env_prefix()
TARGET_BIN_PATH = "/usr/local/bin/"
run_autocomplete()

setup(
    name='nita_cli',
    version='0.0.1',
    description='Test nita cli',
    long_description='nita command line wrapper',
    author='JosemiJose Miguel Izquierdo Lopez',
    author_email='jizquierdo@juniper.net',
    install_requires=['pyyaml','jinja2'],
    url='',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    data_files=[(TARGET_BIN_PATH, ['nita', 'cli.py']),
    (TARGET_COMPLETION_PATH, ['bash_completion.d/nita'])]
)