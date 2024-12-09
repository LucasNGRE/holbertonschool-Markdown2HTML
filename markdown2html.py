#!/usr/bin/python3

"""
    markdown2html.py: Converts markdown files to HTML with parsing for headings and unordered lists.
"""

import sys
import os
import re


def parse_markdown(markdown_file):
    """
    Parses a markdown file to extract headings and convert them into corresponding HTML tags.
    Also handles unordered lists.
    """
    with open(markdown_file, 'r') as md_file:
        content = md_file.readlines()

    # Regex to match markdown headings (e.g., #, ##, etc.)
    heading_regex = re.compile(r"^(#{1,6})\s+(.*)")
    # Regex to match unordered list items (e.g., - Hello)
    unordered_list_regex = re.compile(r"^-\s+(.*)")

    # Process markdown lines and convert them into HTML
    html_lines = []
    in_list = False  # Track if we're inside a list

    for line in content:
        # Match headings
        heading_match = heading_regex.match(line)
        unordered_list_match = unordered_list_regex.match(line)

        if heading_match:
            # Handle headings
            heading_level = len(heading_match.group(1))
            heading_text = heading_match.group(2).strip()
            html_lines.append(f"<h{heading_level}>{heading_text}</h{heading_level}>")
            # If a heading appears, close any open list
            if in_list:
                html_lines.append("</ul>")
                in_list = False
        elif unordered_list_match:
            # Handle unordered lists
            if not in_list:
                # Open the unordered list
                html_lines.append("<ul>")
                in_list = True
            item_text = unordered_list_match.group(1).strip()
            html_lines.append(f"<li>{item_text}</li>")
        else:
            # If not a heading or list item, add a newline safely
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_lines.append(line.strip())

    # Ensure any remaining open list is closed
    if in_list:
        html_lines.append("</ul>")

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
