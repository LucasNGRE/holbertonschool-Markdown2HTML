import re

def parse_markdown(markdown_file):
    """
    Parses a markdown file to extract headings and convert them into corresponding HTML tags.
    Also handles unordered and ordered lists.
    """
    with open(markdown_file, 'r') as md_file:
        content = md_file.readlines()

    # Regex for headings, unordered lists, and ordered lists
    heading_regex = re.compile(r"^(#{1,6})\s+(.*)")
    unordered_list_regex = re.compile(r"^-\s+(.*)")
    ordered_list_regex = re.compile(r"^\*\s+(.*)")

    # Process markdown lines and convert them into HTML
    html_lines = []
    in_unordered_list = False  # Track if we're inside an unordered list
    in_ordered_list = False  # Track if we're inside an ordered list

    for line in content:
        # Match headings
        heading_match = heading_regex.match(line)
        unordered_list_match = unordered_list_regex.match(line)
        ordered_list_match = ordered_list_regex.match(line)

        if heading_match:
            # Handle headings
            heading_level = len(heading_match.group(1))
            heading_text = heading_match.group(2).strip()
            html_lines.append(f"<h{heading_level}>{heading_text}</h{heading_level}>")
            # Close any open list
            if in_unordered_list:
                html_lines.append("</ul>")
                in_unordered_list = False
            if in_ordered_list:
                html_lines.append("</ol>")
                in_ordered_list = False
        elif unordered_list_match:
            # Handle unordered lists
            if not in_unordered_list:
                # Open the unordered list
                html_lines.append("<ul>")
                in_unordered_list = True
            if in_ordered_list:
                # Close an ordered list if transitioning
                html_lines.append("</ol>")
                in_ordered_list = False
            item_text = unordered_list_match.group(1).strip()
            html_lines.append(f"<li>{item_text}</li>")
        elif ordered_list_match:
            # Handle ordered lists
            if not in_ordered_list:
                # Open the ordered list
                html_lines.append("<ol>")
                in_ordered_list = True
            if in_unordered_list:
                # Close an unordered list if transitioning
                html_lines.append("</ul>")
                in_unordered_list = False
            item_text = ordered_list_match.group(1).strip()
            html_lines.append(f"<li>{item_text}</li>")
        else:
            # Close any open lists if encountering other content
            if in_unordered_list:
                html_lines.append("</ul>")
                in_unordered_list = False
            if in_ordered_list:
                html_lines.append("</ol>")
                in_ordered_list = False
            html_lines.append(line.strip())

    # Ensure any remaining open list is closed
    if in_unordered_list:
        html_lines.append("</ul>")
    if in_ordered_list:
        html_lines.append("</ol>")

    # Join lines into a single string
    return "\n".join(html_lines)
