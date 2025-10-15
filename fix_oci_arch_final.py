#!/usr/bin/env python3
"""
Fix OCI architecture diagram - the colored boxes MUST have WHITE text, not gray!
"""

import re

filepath = '/Users/gc/Downloads/Blogs/chirpy-blog/assets/img/diagrams/oci-architecture.svg'

with open(filepath, 'r') as f:
    content = f.read()

# The problem: colored boxes with fill:#XXXX have text that's still gray/black
# We need to find each colored node and make its text WHITE

# Find all style="fill:#XXXXXX !important" and ensure text inside is white
# Replace the node label text color to white for colored boxes

# Strategy: For any rect with a color fill, make sure the text is white
content = re.sub(
    r'(<rect class="basic label-container" style="fill:#[0-9A-Fa-f]{6} !important"[^>]*>.*?<foreignObject[^>]*>.*?<div[^>]*style="[^"]*)',
    lambda m: m.group(0).replace('text-align: center;', 'text-align: center; color: #FFFFFF;'),
    content,
    flags=re.DOTALL
)

# Also make sure nodeLabel text is white for colored boxes
content = re.sub(
    r'(<g class="node default"[^>]*>.*?style="fill:#[0-9A-Fa-f]{6} !important".*?<span class="nodeLabel">)',
    lambda m: m.group(0).replace('<span class="nodeLabel">', '<span class="nodeLabel" style="color: #FFFFFF;">'),
    content,
    flags=re.DOTALL
)

# Simpler approach - just find and replace within colored node sections
# MA-5 (blue), HA-11 (red), GV-13 (orange), TF-21 (green) need WHITE text

sections_to_fix = [
    ('flowchart-MA-5', '#0052A3'),   # Migration Assets - blue
    ('flowchart-HA-11', '#CC0000'),  # Hydration Agent - red
    ('flowchart-GV-13', '#FF6600'),  # Golden Volumes - orange
    ('flowchart-TF-21', '#00AA00'),  # Terraform - green
]

for node_id, color in sections_to_fix:
    # Find the node section
    pattern = f'(<g class="node default" id="{node_id}".*?</g></g>)'

    def replace_text_color(match):
        section = match.group(0)
        # Replace any fill:#000000 or fill:#333333 in text with fill:#FFFFFF
        section = section.replace('fill:#000000', 'fill:#FFFFFF')
        section = section.replace('fill: #000000', 'fill: #FFFFFF')
        section = section.replace('color:#000000', 'color:#FFFFFF')
        section = section.replace('color: #000000', 'color: #FFFFFF')
        return section

    content = re.sub(pattern, replace_text_color, content, flags=re.DOTALL)

with open(filepath, 'w') as f:
    f.write(content)

print(f"✓ Fixed {filepath} - colored boxes now have WHITE text!")
