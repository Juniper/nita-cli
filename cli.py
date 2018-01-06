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

def nested_keys(dictionary, path=None):
    """
    Function that returns all nested keys in a dictionary.
    """
    if path is None:
        path = []
    for key, value in dictionary.items():
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

def cli2command(cli, translator):
    """
    Function resolves cli command given to command to exec
    """
    try:
        for k in cli:
            translator = translator[str(k)]
    except KeyError as err:
        print ''
        print " '{}' key does not exist! Command: '{}' is incorrect!".format(err.message, ' '.join(str(k) for k in cli))
        print ''
        print ' For a list of available commands, execute: '
        print ''
        print ' >>>>  nita help'
        print ''
        sys.exit(1)

    if '%' in translator:
        return translator % os.environ.get('PROJECT_PATH', os.environ['PWD'])

    return translator

def print_help(documentation):
    """
    Print usage info
    """
    print ''
    print_nested_keys(documentation)
    print ''
    sys.exit()

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

def is_new_command(cli):
    if 'new' in cli:
        return True
    return False

def is_jenkins_rm_command(cli):
    if 'jenkins' and 'remove' in cli:
        return True
    return False

def main(commands, documentation):
    """
    Process commmand line and execute resultant command
    """
    commands_vs_help_trees(commands, documentation)
    
    if 'help' in sys.argv:
        print_help(documentation)

    # Remove /usr/local/bin/ from first argument (/usr/local/bin/nita)
    root = sys.argv[0].split('/')[-1]
    cli = sys.argv[1:]
    cli.insert(0, root)

    if is_new_command(cli):
        try:
            name = cli[-1]
            subcli = cli[:-1]
            raw = cli2command(subcli, commands)
            command = raw.format(name)
            print ''
            print '  >>>> command: ', command
            print ''
            os.system(command)
        except AttributeError:
            print ''
            print " Command: '{}' is missing the argument: $name!".format(' '.join(str(k) for k in cli))
            print ''
            sys.exit(1)
    elif is_jenkins_rm_command(cli):
        try:
            regex = cli[-1]
            subcli = cli[:-2]
            raw = cli2command(subcli, commands)
            command = raw.format(regex)
            print ''
            print '  >>>> command: ', command
            print ''
            os.system(command)
        except AttributeError:
            print ''
            print " Command: '{}' is missing the option: $regex!".format(' '.join(str(k) for k in cli))
            print ''
            sys.exit(1)
    else:
        command = cli2command(cli, commands)
        print ''
        print '  >>>> command: ', command
        print ''
        os.system(command)
