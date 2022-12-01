#!/usr/bin/env python3
#
# RE(gex|cursively) SEARCH a directory
#
import os
import re
import sys
import argparse

parser = argparse.ArgumentParser(
    prog = 'research.py',
    description = 'RE(gex|cursively) SEARCH a directory'
)
parser.add_argument("-d", "--directory",
                    help="directory to scan",
                    required=True)
parser.add_argument("-r", "--regex",
                    help="regular expression to search for",
                    required=True)
parser.add_argument("-x", "--exclude",
                    help="comma separated list of dirs to exclude")
parser.add_argument("-i", "--ignorecase",
                    help="search case insensitive",
                    action='store_true')
parser.add_argument("-v", "--verbose",
                    help="increase verbosity",
                    action='store_true')
args = parser.parse_args()

directory = args.directory
if args.ignorecase:
    regex = re.compile(args.regex, flags=re.IGNORECASE)
else:
    regex = re.compile(args.regex)
exclude = args.exclude

def traverse_dir(path):
    """Traverse the directory of the given path and yield found files"""
    for root, dirs, files in os.walk(path):
        for file in files:
            yield os.path.join(root, file)
        if exclude:
            x = exclude.split(",")
            for d in x:
                if d in dirs:
                    dirs.remove(d)

def match_regex(file):
    """Search file for a match on command line regex and return a list of
    all matching lines including line number"""
    matches = []
    try:
        with open(file, 'r', encoding='UTF8') as f:
            line_num = 1
            for line in f:
                if regex.search(line):
                    matches.append(f"{ line_num }: { line }")
                line_num += 1
    finally:
        return matches

if __name__ == '__main__':
    for file in traverse_dir(directory):
        matches = match_regex(file)
        print(f"\n{ file }")
        for line in matches:
            line = line.strip('\n')
            print(line)
