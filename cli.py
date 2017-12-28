#!/usr/bin/env python
# <*******************
# 
# Copyright 2018 Juniper Networks, Inc. All rights reserved.
# Licensed under the Juniper Networks Script Software License (the "License").
# You may not use this script file except in compliance with the License, which is located at
# http://www.juniper.net/support/legal/scriptlicense/
# Unless required by applicable law or otherwise agreed to in writing by the parties, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
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
    for k,v in dictionary.items():
        newpath = path + [k]
        if isinstance(v, dict):
            for u in nested_keys(v, newpath):
                yield u
        else:
            yield newpath, v

def print_nested_keys(dictionary):
    """
    Function that prints a set of all nested keys (from root to leaf) 
    in a dictionary with its correspondent value.
    """
    dictionary.pop('license', None)
    for root2leaf, value in nested_keys(dictionary):
        print '   ' + KEY_SEPARATOR.join(root2leaf) + ' => ' + value

def cli2command(cli, translator):    
    for k in cli: 
        translator = translator[str(k)]
    return translator

def main(commands, help):
    # print 'Number of arguments:', len(sys.argv), 'arguments.'
    # print 'Argument List:', str(sys.argv)
    if 'help' in sys.argv:
        print ''
        print_nested_keys(help)
        print ''
        sys.exit()

    # Remove /usr/local/bin/ from first argument (/usr/local/bin/nita)
    root = sys.argv[0].split('/')[-1]
    cli = sys.argv[1:]
    cli.insert(0, root)

    try:
        command = cli2command(cli, commands)
        # If % vars in command
        if '%' in command:
                
            print ''
            print '  >>>> command: ', command % commands.PROJECT_PATH
            print ''
            os.system(command % commands.PROJECT_PATH)

        else:

            print ''
            print '  >>>> command: ', command
            print ''
            os.system(command)

    except KeyError as ke:
        print ''
        print('"' + ke.message + '" key does not exist at COMMANDS dictionary')
        print ''
