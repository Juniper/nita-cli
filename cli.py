#!/usr/bin/env python
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
"""
    Wrapper script for all NITA commands
"""
import sys
import os

KEY_SEPARATOR = ' '
DEBUG = False
# Red color to debug command mapped
CRED = '\033[91m'
CEND = '\033[0m'

def nested_keys(dictionary, path=None):
    """
    Function that returns all nested keys in a dictionary.
    """
    if path is None:
        path = []
    for key, value in sorted(dictionary.items()):
        newpath = path + [key]
        # Consider remove this piece!!!
        if 'jenkins' and 'remove' in newpath:
            newpath = newpath + ['--regex'] + ['REGEX']
        if isinstance(value, dict):
            for result in nested_keys(value, newpath):
                yield result
        else:
            yield ' '.join(newpath), value

def nested_keys_from(dictionary, path=None):
    """
    Function that returns all nested keys in a dictionary from a subkey.
    """
    subdictionary = dictionary.copy()
    if path is None:
        path = []
    else:
        for subkey in path:
            subdictionary = subdictionary[subkey]
        for key, value in sorted(subdictionary.items()):
            newpath = path + [key]
            if 'jenkins' and 'remove' in newpath:
                newpath = newpath + ['--regex'] + ['REGEX']
            if isinstance(value, dict):
                for result in nested_keys(value, newpath):
                    yield result
            else:
                yield ' '.join(newpath), value

def print_nested_keys(dictionary):
    """
    Function that prints a set of all nested keys (from root to leaf)
    in a dictionary with its correspondent value.
    """
    dictionary.pop('license', None)
    for cli, command in nested_keys(dictionary):
        print "   {} => {}".format(cli, command)

def print_nested_keys_from(dictionary, *subkeys):
    """
    Function that prints a set of all subnested keys (from subkeys to leaf)
    in a dictionary with its correspondent value.
    """
    dictionary.pop('license', None)
    for cli, command in nested_keys_from(dictionary, subkeys[0]):
        print "   {} => {}".format(cli, command)

def cli2command(cli, translator):
    """
    Function resolves cli command given to command to execute
    """
    try:
        for k in cli:
            translator = translator[str(k)]
    except KeyError as err:
        print "\n '{}' key does not exist! Command: '{}' is incorrect!\n".format(err.message, ' '.join(str(k) for k in cli))
        print "\n For a list of available commands, execute:\n\n >>>> 'nita --help' or 'nita -h' or 'nita ?'\n\n"
        sys.exit(1)

    if ' %s' in translator:
        # nita stats => Displays NITA containers runtime metrics [CPU %, MEM USAGE / LIMIT, MEM %, NET I/O, BLOCK I/O, PIDS]
        if 'stats' in cli:
            pass
        else:
            return translator % os.environ.get('PROJECT_PATH', os.environ['PWD'])

    return translator

def print_help(documentation, *args):
    """
    Print usage info
    """
    print ''
    print_nested_keys_from(documentation, args[0])
    print ''

def print_command_with_keys(dictionary, keys):
    """
    Function that prints the command as a string containing all keys passed
    as a list from the dictionary.
    """
    for root2leaf, _ in nested_keys(dictionary):
        command_keys = ''.join(root2leaf)
        match = {key in command_keys for key in keys}
        if match == set([True]):
            return command_keys

def commands_vs_help_trees(commands, documentation):
    """
    Function that checks if commands & documentation trees
    have the same nested keys (i.e. tries to avoid missing documentation
    and or a mapped value of a newly added command!).
    """

    finish = False
    commands_set = {frozenset(root2leaf)
                    for root2leaf, value in nested_keys(commands)}
    help_set = {frozenset(root2leaf)
                for root2leaf, value in nested_keys(documentation)}

    help_diff = commands_set - help_set
    help_missing = help_diff != set([])
    commands_diff = help_set - commands_set
    commands_missing = commands_diff != set([])

    if help_missing:
        command_keys_list = [list(command) for command in list(help_diff)]
        for item in command_keys_list:
            missing = print_command_with_keys(commands, item)
            print ''
            print '     The following command: "' + missing + '" is missing its description!'
            finish = True
        print ''
        print ' >>> Please add it to the HELP tree!'
        print ''

    if commands_missing:
        command_keys_list = [list(command) for command in list(commands_diff)]
        for item in command_keys_list:
            missing = print_command_with_keys(documentation, item)
            print ''
            print '     The following command: "' + missing + '" is missing its mapped command!'
            finish = True
        print ''
        print ' >>> Please add it to the COMMANDS tree!'
        print ''

    if finish:
        sys.exit()

def is_help_cmd(cli):
    """
    Checks if the cli command is requesting 'help'.
    """
    if ('--help' in cli[-1]) or ('-h' in cli[-1]) or ('?' in cli[-1]):
        return True
    return False

def is_new_cmd(cli):
    """
    Checks if the cli command contains 'new' in it.
    """
    if 'new' in cli:
        return True
    return False

def has_options(cli):
    """
    Checks if the cli command contains any options (e.g. --regex $REGEX).
    """
    for item in cli:
        if '--' in item:
            return True
    return False

def main(commands, documentation):
    """
    Process commmand line and execute resultant command
    """
    global DEBUG
    commands_vs_help_trees(commands, documentation)

    # Remove /usr/local/bin/ from first argument (/usr/local/bin/nita)
    root = sys.argv[0].split('/')[-1]
    cli = sys.argv[1:]
    cli.insert(0, root)
    if cli[1] == '-d':
        cli.pop(1)
        DEBUG = True

    if is_help_cmd(cli):
        try:
            subcli = cli[:-1]
            print_help(documentation, subcli)
            sys.exit()
        except AttributeError:
            raw = cli2command(subcli, documentation)
            doc_help = raw.format(subcli)
            print "   {} => {}".format(' '.join(str(k) for k in subcli), doc_help)
            print ''
        except KeyError as err:
            print "\n '{}' key does not exist! Command: '{}' is incorrect!\n".format(err.message, ' '.join(str(k) for k in subcli))
            print "\n For a list of available commands, execute:\n\n >>>> 'nita --help' or 'nita -h' or 'nita ?'\n\n"
            sys.exit(1)

    elif is_new_cmd(cli):
        try:
            name = cli[-1]
            subcli = cli[:-1]
            raw = cli2command(subcli, commands)
            command = raw.format(name)
            if DEBUG:
                print (CRED + "\n  >>>> command: {}\n".format(command) + CEND)
            os.system(command)
        except AttributeError:
            print "\n Command: '{}' is missing the argument: $name!\n".format(' '.join(str(k) for k in cli))
            sys.exit(1)

    elif has_options(cli):
        try:
            option = cli[-2]
            value = cli[-1]
            subcli = cli[:-2]
            raw = cli2command(subcli, commands)
            command = raw.format(option, value)
            if DEBUG:
                print (CRED + "\n  >>>> command: {}\n".format(command) + CEND)
            os.system(command)
        except AttributeError:
            print "\n Command: '{}' is missing the option: $value!\n".format(' '.join(str(k) for k in cli))
            sys.exit(1)

    else:
        try:
            command = cli2command(cli, commands)
            # if command is not a leaf in the dictionary (string),
            # but a branch with more leaves, command will not run!
            if isinstance(command, str):
                if DEBUG:
                    print (CRED + "\n  >>>> command: {}\n".format(command) + CEND)
                os.system(command)
            else:
                raise TypeError
        except TypeError:
            print "\n Command: '{}' is not a mapped command!\n\n Issue 'nita --help' or 'nita -h' or 'nita ?' for some insights...\n".format(' '.join(str(k) for k in cli))
            sys.exit(1)
