#!/usr/bin/env python3
"""
Offline installation of NITA CLI
"""

# Always prefer setuptools over distutils
#from setuptools import setup, find_packages
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
        brew_prefix = "{0}/etc/bash_completion.d/".format(
            stdout.rstrip().decode("utf-8"))
        TARGET_COMPLETION_PATH = brew_prefix

    # Return true if CYGWIN or cygwin there in os type string
    elif re.search(cygwin, os_type):
        TARGET_COMPLETION_PATH = '/etc/bash_completion.d/'
        TARGET_BIN_PATH = '/usr/bin/'
        if not os.path.exists(TARGET_COMPLETION_PATH):
            os.makedirs(TARGET_COMPLETION_PATH)

    else:
        raise ValueError(
            'Unknown OS type found. This Operating System is not supported.')

    return TARGET_COMPLETION_PATH, TARGET_BIN_PATH


def run_autocomplete():
    """
    Run script that Generate file nita autocompletion.
    """
    cmd = 'python3 autocomplete'
    proc = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()

def cp_nita(TARGET_COMPLETION_PATH):
    """
    Copy nita to /usr/local/bin/ and to autocompletion path.
    """
    subprocess.call(['cp', 'nita', '/usr/local/bin/nita'])
    subprocess.call(['cp', 'bash_completion.d/nita', TARGET_COMPLETION_PATH + 'nita'])


TARGET_COMPLETION_PATH, TARGET_BIN_PATH = get_env_prefix()
run_autocomplete()

# Include data files if those exist
# for that we iterate the folder and append the files
data_files_list = [(TARGET_BIN_PATH, ['nita'])]
for file in os.listdir('bash_completion.d/'):
    f1 = 'bash_completion.d/' + file
    if os.path.isfile(f1):  # skip directories
        data_files_list.append((TARGET_COMPLETION_PATH, [f1]))

# Copy nita to /usr/local/bin/
cp_nita(TARGET_COMPLETION_PATH)
