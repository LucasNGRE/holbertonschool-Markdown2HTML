#!/usr/bin/python3

"""
    markdown2html.py: Converts markdown files to html files.
"""

import sys
import os


def main():
    """
        Main function of the script.
    """
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)

    markdown_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.isfile(markdown_file):
        print(f"Missing {markdown_file}", file=sys.stderr)
        sys.exit(1)

    sys.exit(0)

main()
