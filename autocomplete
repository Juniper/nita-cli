#!/usr/bin/env python3

"""
    Python3 module to generate autocomplete feature
"""

import importlib.machinery
import yaml
from jinja2 import Environment, FileSystemLoader

# Constants
CLI_COMMAND = 'nita'
TEMPLATES = 'templates/'
CLI_TEMPLATE = CLI_COMMAND + '.j2'
TMP = 'tmp/'
VARS = TMP + 'vars.yml'
COMPLETION = 'bash_completion.d/'
CLI_SCRIPT = COMPLETION + CLI_COMMAND

AUTOCOMPLETE = {}

loader = importlib.machinery.SourceFileLoader(CLI_COMMAND, CLI_COMMAND)
source = loader.load_module()


def autocomplete_values(dictionary, root):
    """
    Function that returns a dictionary with list of possible
    autocompletion values in a nested dictionary.
    """

    if isinstance(dictionary, dict):
        for key, value in dictionary.items():
            # Dive into a nested level.
            if isinstance(value, dict):
                try:
                    if AUTOCOMPLETE[root][key]:
                        for item in value.keys():
                            AUTOCOMPLETE[root][key].append(item)
                except KeyError:
                    AUTOCOMPLETE[root][key] = list(value.keys())

                value = autocomplete_values(value, root)
            else:
                try:
                    if key not in AUTOCOMPLETE[root]:
                        AUTOCOMPLETE[root][key] = ''
                except KeyError:
                    pass
    else:
        print('It is not dictionary')
    return dictionary

if __name__ == '__main__':

    AUTOCOMPLETE['opts'] = list(source.COMMANDS.get(CLI_COMMAND).keys())
    AUTOCOMPLETE[CLI_COMMAND] = {}
    autocomplete = autocomplete_values(source.COMMANDS, CLI_COMMAND)

    with open(VARS, 'w') as yaml_file:
        yaml.dump(AUTOCOMPLETE, yaml_file, default_flow_style=False)

    config_data = yaml.safe_load(open(VARS))

    env = Environment(loader=FileSystemLoader(TEMPLATES),
                      trim_blocks=True, lstrip_blocks=True)
    template = env.get_template(CLI_TEMPLATE)

    # print(template.render(config_data))
    output = template.render(config_data)

with open(CLI_SCRIPT, 'w') as f:
    f.write(output)
