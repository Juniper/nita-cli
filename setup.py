"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Import install to customize post installation action
from setuptools.command.install import install
# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path
import os, shutil
import platform
import subprocess

class InstallWrapper(install):
  """Provides a install wrapper for nita cli.py files
  to copy on /usr/local/bin/ and /etc/bash_completion.d/
  """

  _TARGET_BIN_PATH = "/usr/local/bin/"
  _TARGET_COMPLETION_PATH = '/etc/bash_completion.d/'
  _COPY_BIN = ['nita', 'cli.py']
  _COPY_AUTOCOMPLETION = ['bash_completion.d/nita']


  def run(self):
    # Run this first so the install stops in case 
    # these fail otherwise the Python package is
    # successfully installed
    self._run_autocomplete()
    self._copy_files()
    messages = '''# Those are following files copy by setup.py install.
    You should remove manually when you uninstalled nita_cli.
    - /usr/local/bin/nita
    - /usr/local/bin/cli.py
    - /etc/bash_completion.d/nita
    '''
    print (messages)

    # Run the standard PyPi copy
    install.run(self)


  def _run_autocomplete(self):
    cmd = 'python autocomplete'
    proc = subprocess.Popen(
      cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()


  def _copy_files(self):
    # Check to see that the required folders exists 
    # Do this first so we don't fail half way
    for folder in self._COPY_BIN:
      if not os.access(folder, os.R_OK):
        raise IOError("%s not readable from achive" % 
        folder)

    # Check to see we can write to the target
    if not os.access(self._TARGET_BIN_PATH, os.W_OK):
      raise IOError("%s not writeable by user" % 
      self._TARGET_BIN_PATH)

    # Copy files
    for file in self._COPY_BIN:
      target_path = os.path.join(
        self._TARGET_BIN_PATH, file)

      # Copy the files from the archive
      shutil.copy(file, self._TARGET_BIN_PATH)

    # Repeat same action for bash_completion
    for folder in self._COPY_AUTOCOMPLETION:
      if not os.access(folder, os.R_OK):
        raise IOError("%s not readable from achive" % 
        folder)

    # Check to see we can write to the target
    if not os.access(self._TARGET_COMPLETION_PATH, os.W_OK):
      raise IOError("%s not writeable by user" % 
      self._TARGET_COMPLETION_PATH)

    # Copy files
    for file in self._COPY_AUTOCOMPLETION:
      target_path = os.path.join(
        self._TARGET_COMPLETION_PATH, file)

      # Copy the files from the archive
      shutil.copy(file, self._TARGET_COMPLETION_PATH)


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
    cmdclass={'install': InstallWrapper}
)