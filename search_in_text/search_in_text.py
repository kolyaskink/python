import argparse
import re


class MyException(Exception):
    pass


def get_config():

    """ Parse config file and save data as a dictionary"""
    try:
        with open('config.txt') as f:
            settings = {}
            for line in f:
                line = line.strip()
                settings[(line.split('=')[0])] = (line.split('=')[1])
    except IOError:
        raise MyException("Config file not found")
    return settings


def get_params():

    """ Take setting from the CLI parameters. Do the same what get_config does"""

    parser = argparse.ArgumentParser(description='Script to generate a CF template for Studios Jenkins.')
    parser.add_argument('--file_path', '-f', action='store', required=True,
                        help="name of the file to search in")
    parser.add_argument('--case_sensitivity', '-c', action='store', required=False,
                        help="Case sensitive search. Could be 'yes' or 'no'",
                        default='no')
    parser.add_argument('--advanced_search', '-a', action='store', required=False,
                        help="Split search pattern between lines",
                        default='no')
    parser.add_argument('--search_pattern', '-s', action='store', required=True,
                        help="String to search for")
    args = parser.parse_args()
    settings = {'file_path': args.file_path, 'case_sensitivity': args.case_sensitivity,
                'search_pattern': args.search_pattern, 'advanced_search': args.advanced_search}
    return settings


def parse_file_advanced(get_params):

    try:
        with open(get_params['file_path']) as f:
            s = ""
            for line in f:
                s = s + line.strip()
        for m in re.finditer(get_params['search_pattern'],s):
            print("'{0}':{1}-{2}".format(
                m.group(), m.start(), m.end()
            ))
    except IOError:
        raise MyException("Source file not found")


def parse_file_simple(get_params):

    """
        Load a file with text, verify it and save as a string
        Case non-sensitive
    """

    try:
        with open(get_params['file_path']) as f:
            i = 0
            for line in f:
                line = line.strip()
                if get_params['case_sensitivity'].lower() == 'no':
                    if line.lower() == get_params['search_pattern'].lower():
                        print(line)
                        i += 1
                elif get_params['case_sensitivity'].lower() == 'yes':
                    if line == get_params['search_pattern']:
                        print(line)
                        i += 1
                else:
                    print("case_sensitivity value could be yes or no")
            if i == 0:
                print("No match found")
    except IOError:
        raise MyException("Source file not found")
    except KeyError:
        raise MyException("Can't parse config file")


def main(get_params):

    """ Find a string inside a file. Show the match"""

    if get_params['advanced_search'].lower() == 'yes':
        parse_file_advanced(get_params)
    elif get_params['advanced_search'].lower() == 'no':
        parse_file_simple(get_params)

main(get_params())
