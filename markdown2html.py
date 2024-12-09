#!/usr/bin/python3

"""
    markdown2html.py: Converts markdown files to HTML with parsing for headings.
"""

import sys
import os
import re


def parse_markdown(markdown_file):
    """
    Parses a markdown file to extract headings and convert them into corresponding HTML tags.
    """
    with open(markdown_file, 'r') as md_file:
        content = md_file.readlines()

    # Regex to match markdown headings (e.g., #, ##, etc.)
    heading_regex = re.compile(r"^(#{1,6})\s+(.*)")

    # Process markdown lines and convert them into HTML
    html_lines = []
    for line in content:
        match = heading_regex.match(line)
        if match:
            # Count number of # symbols to determine heading level
            heading_level = len(match.group(1))
            heading_text = match.group(2).strip()
            # Append the corresponding HTML heading tag
            html_lines.append(f"<h{heading_level}>{heading_text}</h{heading_level}>")
        else:
            # If it's not a heading, keep it as plain text
            html_lines.append(line.strip())

    # Join lines into a single string
    return "\n".join(html_lines)


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

    # Parse the markdown file
    html_content = parse_markdown(markdown_file)

    # Write the converted HTML to the output file
    with open(output_file, 'w') as html_file:
        html_file.write(html_content)

    sys.exit(0)


if __name__ == '__main__':
    main()
