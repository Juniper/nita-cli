#!/usr/bin/env python3

import argparse

# Red color to debug command mapped
CRED   = '\033[91m' # red
CEND   = '\033[0m'  # end

def compare_dicts(dict1, dict2, dict1_name="dict1", dict2_name="dict2", path=""):
    """
    Recursively compares keys in two dictionaries and prints out differences.
    """
    for key in dict1:
        new_path = f"{path}['{key}']" if path else f"['{key}']"
        if key not in dict2:
            print(CRED + f"\n >>>>>>>> Key missing in {dict2_name}: {new_path}" + CEND )
        elif isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
            # If both values are dictionaries, recursively compare them
            compare_dicts(dict1[key], dict2[key], dict1_name, dict2_name, new_path)
        elif isinstance(dict1[key], dict) or isinstance(dict2[key], dict):
            # One is a dictionary and the other is not, so they differ
            print(CRED + f"\n >>>>>>>> Key type mismatch at {new_path}: one is a dictionary, the other is not." + CEND)
            
    for key in dict2:
        new_path = f"{path}['{key}']" if path else f"['{key}']"
        if key not in dict1:
            print(CRED + f"\n >>>>>>>> Key missing in {dict1_name}: {new_path}" + CEND)

def load_dicts_from_file(filepath):
    """
    Loads COMMANDS and HELP dictionaries from a specified file.
    """
    with open(filepath, 'r') as file:
        file_content = file.read()
    
    # Create a separate environment for executing the file's content
    env = {}
    exec(file_content, env)
    
    # Check if COMMANDS and HELP are in the environment
    if 'COMMANDS' not in env or 'HELP' not in env:
        raise ValueError("The specified file does not contain COMMANDS and/or HELP dictionaries.")
    
    return env['COMMANDS'], env['HELP']

if __name__ == '__main__':
    # Parse the file path from the command-line arguments
    parser = argparse.ArgumentParser(description="Compare keys in COMMANDS and HELP dictionaries.")
    parser.add_argument("file", help="Path to the file containing COMMANDS and HELP dictionaries")
    args = parser.parse_args()

    # Load the dictionaries from the specified file
    try:
        COMMANDS, HELP = load_dicts_from_file(args.file)
    except ValueError as e:
        print(e)
        exit(1)
    
    # Compare the dictionaries
    print()
    print(" >>>> Comparing COMMANDS and HELP dictionaries...")
    compare_dicts(COMMANDS, HELP, 'COMMANDS', 'HELP')
    print()
    print(" >>>> Comparison complete!")
    print()
