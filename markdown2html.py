#!/usr/bin/env python3
"""
Markdown to HTML converter.
Usage: markdown2html.py <markdown_file> <html_file>
"""

import sys
import os
import re

def parse_markdown(markdown_file):
    """
    Parses a markdown file and converts it into HTML.
    """
    with open(markdown_file, 'r') as md_file:
        content = md_file.readlines()

    # Regex patterns
    heading_regex = re.compile(r"^(#{1,6})\s+(.*)")  # Headings
    unordered_list_regex = re.compile(r"^-\s+(.*)")  # Unordered lists
    ordered_list_regex = re.compile(r"^\*\s+(.*)")   # Ordered lists

    # HTML output lines
    html_lines = []
    in_unordered_list = False  # Track if inside an unordered list
    in_ordered_list = False    # Track if inside an ordered list

    for line in content:
        line = line.rstrip()
        
        # Match headings
        heading_match = heading_regex.match(line)
        unordered_list_match = unordered_list_regex.match(line)
        ordered_list_match = ordered_list_regex.match(line)

        if heading_match:
            # Handle headings
            heading_level = len(heading_match.group(1))
            heading_text = heading_match.group(2).strip()
            html_lines.append(f"<h{heading_level}>{heading_text}</h{heading_level}>")
            # Close any open lists
            if in_unordered_list:
                html_lines.append("</ul>")
                in_unordered_list = False
            if in_ordered_list:
                html_lines.append("</ol>")
                in_ordered_list = False

        elif unordered_list_match:
            # Handle unordered lists
            if not in_unordered_list:
                html_lines.append("<ul>")
                in_unordered_list = True
            if in_ordered_list:
                html_lines.append("</ol>")
                in_ordered_list = False
            item_text = unordered_list_match.group(1).strip()
            html_lines.append(f"<li>{item_text}</li>")

        elif ordered_list_match:
            # Handle ordered lists
            if not in_ordered_list:
                html_lines.append("<ol>")
                in_ordered_list = True
            if in_unordered_list:
                html_lines.append("</ul>")
                in_unordered_list = False
            item_text = ordered_list_match.group(1).strip()
            html_lines.append(f"<li>{item_text}</li>")

        else:
            # Handle other lines or paragraphs
            if in_unordered_list:
                html_lines.append("</ul>")
                in_unordered_list = False
            if in_ordered_list:
                html_lines.append("</ol>")
                in_ordered_list = False
            if line.strip():  # Avoid adding empty paragraphs
                html_lines.append(f"<p>{line.strip()}</p>")

    # Close any remaining open lists
    if in_unordered_list:
        html_lines.append("</ul>")
    if in_ordered_list:
        html_lines.append("</ol>")

    return "\n".join(html_lines)

def main():
    # Ensure correct usage
    if len(sys.argv) != 3:
        print("Usage: ./markdown2html.py <markdown_file> <html_file>")
        sys.exit(1)

    markdown_file = sys.argv[1]
    html_file = sys.argv[2]

    # Check if the markdown file exists
    if not os.path.isfile(markdown_file):
        print(f"Missing {markdown_file}")
        sys.exit(1)

    # Parse markdown and convert to HTML
    html_content = parse_markdown(markdown_file)

    # Write the HTML content to the output file
    with open(html_file, 'w') as html_out:
        html_out.write(html_content)

if __name__ == "__main__":
    main()
