#!/usr/bin/env python3

"""
    Wrapper script for all NITA commands.
"""
import sys
import os

KEY_SEPARATOR = ' '

# If True (-d option), prints and executes mapped command.
DEBUG = False
# If True (-e option), only prints mapped command.
ECHO  = False

# Red color to debug command mapped
CRED   = '\033[91m' # red
CBLUE  = '\033[34m' # blue
CPURP  = '\033[94m' # purple
CWHITE = '\033[37m' # white
CEND   = '\033[0m'  # end

def nested_keys(dictionary, path=None):
    """
    Function that returns all nested keys in a dictionary.
    """
    if path is None:
        path = []
    for key, value in sorted(dictionary.items()):
        newpath = path + [key]
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
        print("   {}".format(cli) + CPURP + " => " + CWHITE + " {}".format(command) + CEND)

def print_nested_keys_from(dictionary, *subkeys):
    """
    Function that prints a set of all subnested keys (from subkeys to leaf)
    in a dictionary with its correspondent value.
    """
    dictionary.pop('license', None)
    for cli, command in nested_keys_from(dictionary, subkeys[0]):
        print("   {}".format(cli) + CPURP + " => " + CWHITE + " {}".format(command) + CEND)

def cli2command(cli, translator):
    """
    Function resolves cli command given to command to execute.
    """
    try:
        for k in cli:
            translator = translator[str(k)]
    except KeyError as kerr:
        try:
            print(CRED + "\n '{}' key does not exist! Command: '{}' is incorrect!\n".format(kerr.message, ' '.join(str(k) for k in cli)) + CEND)
            print(CRED + "\n For a list of available commands, execute:\n\n >>>> 'nita --help' or 'nita -h' or 'nita ?'\n\n" + CEND)
            sys.exit(1)
        except AttributeError:
            print(CRED + "\n For a list of available commands, execute:\n\n >>>> 'nita --help' or 'nita -h' or 'nita ?'\n\n" + CEND)
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
    Print usage info.
    """
    print('')
    print_nested_keys_from(documentation, args[0])
    print('')

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
    and/or mapped values of a recently added commands!). 
    If so, it exits with rc=1
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
            print('')
            print(CRED + ' ERROR: There are commands missing their description!' + CEND)
            finish = True
        print('')
        print(CRED + ' >>> Please add them to the HELP tree!' + CEND)
        print('')

    if commands_missing:
        command_keys_list = [list(command) for command in list(commands_diff)]
        for item in command_keys_list:
            missing = print_command_with_keys(documentation, item)
            print('')
            print(CRED + ' ERROR: There are commands missing their mapping!' + CEND)
            finish = True
        print('')
        print(CRED + ' >>> Please add them to the COMMANDS tree!' + CEND)
        print('')

    if finish:
        sys.exit(1)

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
    global DEBUG, ECHO
    commands_vs_help_trees(commands, documentation)

    # Remove /usr/local/bin/ from first argument (/usr/local/bin/nita)
    root = sys.argv[0].split('/')[-1]
    cli = sys.argv[1:]
    cli.insert(0, root)
    try:
        if cli[1] == '-d':
            cli.pop(1)
            DEBUG = True
        if cli[1] == '-e':
            cli.pop(1)
            ECHO = True
    except IndexError:
        # If cli[1] does not exist 
        # (e.g. command = 'nita', do nothing!
        pass

    if is_help_cmd(cli):
        try:
            subcli = cli[:-1]
            print_help(documentation, subcli)
            sys.exit()
        except AttributeError:
            raw = cli2command(subcli, documentation)
            doc_help = raw.format(subcli)
            print("   {}".format(' '.join(str(k) for k in subcli)) + CPURP + " => " + CWHITE + "{}".format(doc_help) + CEND)
            print('')
        except KeyError as err:
            print(CRED + "\n '{}' key does not exist! Command: '{}' is incorrect!\n".format(err.message, ' '.join(str(k) for k in subcli)) + CEND)
            print(CRED + "\n For a list of available commands, execute:\n\n >>>> 'nita --help' or 'nita -h' or 'nita ?'\n\n"  + CEND)
            sys.exit(1)

    elif is_new_cmd(cli):
        try:
            name = cli[-1]
            subcli = cli[:-1]
            raw = cli2command(subcli, commands)
            command = raw.format(name)
            if ECHO:
                print("\n  >>>> command: " + CRED + "{}\n".format(command) + CEND)
                sys.exit(0)
            if DEBUG:
                print("\n  >>>> command: " + CRED + "{}\n".format(command) + CEND)
            os.system(command)
        except AttributeError:
            print(CRED + "\n Command: '{}' is missing the argument: $name!\n".format(' '.join(str(k) for k in cli)) + CEND)
            sys.exit(1)

    elif has_options(cli):
        try:
            option = cli[-2]
            value = cli[-1]
            subcli = cli[:-2]
            raw = cli2command(subcli, commands)
            command = raw.format(option, value)
            if ECHO:
                print("\n  >>>> command: " + CRED + "{}\n".format(command) + CEND)
                sys.exit(0)
            if DEBUG:
                print("\n  >>>> command: " + CRED + "{}\n".format(command) + CEND)
            os.system(command)
        except AttributeError:
            print(CRED + "\n Command: '{}' is missing the option: $value!\n".format(' '.join(str(k) for k in cli)) + CEND)
            sys.exit(1)

    else:
        try:
            command = cli2command(cli, commands)
            # if command is not a leaf in the dictionary (string),
            # but a branch with more leaves, command will not run!
            if isinstance(command, str):
                if ECHO:
                    print("\n  >>>> command: " + CRED + "{}\n".format(command) + CEND)
                    sys.exit(0)
                if DEBUG:
                    print("\n  >>>> command: " + CRED + "{}\n".format(command) + CEND)
                os.system(command)
            else:
                raise TypeError
        except TypeError:
            print(CRED + "\n Command: '{}' is not a full mapped command!\n\n Issue 'nita --help' or 'nita -h' or 'nita ?' for some insights...\n".format(' '.join(str(k) for k in cli)) + CEND)
            sys.exit(1)
