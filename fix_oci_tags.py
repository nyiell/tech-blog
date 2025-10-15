#!/usr/bin/env python3
"""
Fix OCI tags diagram - make text in colored diamond WHITE and readable
Also fix the green/red boxes at the bottom
"""

import re

filepath = '/Users/gc/Downloads/Blogs/chirpy-blog/assets/img/diagrams/oci-tags.svg'

with open(filepath, 'r') as f:
    content = f.read()

# Fix CHECK1 - the orange diamond that needs white text
# flowchart-CHECK1-11 has fill:#FFB347 (orange) but text is not white
pattern = r'(<g class="node default" id="flowchart-CHECK1-11"[^>]*>.*?</g>)'

def fix_check1(match):
    node = match.group(0)

    # Add style="color:#fff !important" to the <g class="label"> element
    node = re.sub(
        r'(<g class="label" style=)"([^"]*)"',
        r'\1"color:#fff !important"',
        node
    )
    node = re.sub(
        r'(<g class="label")(>)',
        r'\1 style="color:#fff !important"\2',
        node
    )

    # Add style="color:#fff !important" to the <span class="nodeLabel"> element
    node = re.sub(
        r'(<span class="nodeLabel">)',
        r'<span class="nodeLabel" style="color:#fff !important">',
        node
    )

    # Also make sure the div has the color
    node = re.sub(
        r'(<div[^>]*)(>)',
        lambda m: m.group(1) + ' style="color: rgb(255, 255, 255) !important"' + m.group(2) if 'style=' not in m.group(1) else m.group(0),
        node
    )

    return node

content = re.sub(pattern, fix_check1, content, flags=re.DOTALL)

# Fix the colored success/fail boxes - FAIL1, SUCCESS1, SUCCESS2
colored_boxes = [
    'flowchart-FAIL1-15',      # Red box
    'flowchart-SUCCESS1-17',   # Green box
    'flowchart-SUCCESS2-19',   # Green box
]

for box_id in colored_boxes:
    pattern = f'(<g class="node default" id="{box_id}"[^>]*>.*?</g>)'

    def fix_box(match):
        node = match.group(0)

        # Add style="color:#fff !important" to the <g class="label"> element
        node = re.sub(
            r'(<g class="label" style=)"([^"]*)"',
            r'\1"color:#fff !important"',
            node
        )
        node = re.sub(
            r'(<g class="label")(>)',
            r'\1 style="color:#fff !important"\2',
            node
        )

        # Add style="color:#fff !important" to the <span class="nodeLabel"> element
        node = re.sub(
            r'(<span class="nodeLabel">)',
            r'<span class="nodeLabel" style="color:#fff !important">',
            node
        )

        return node

    content = re.sub(pattern, fix_box, content, flags=re.DOTALL)

with open(filepath, 'w') as f:
    f.write(content)

print(f"✓ Fixed {filepath} - orange diamond and colored boxes now have WHITE text!")
