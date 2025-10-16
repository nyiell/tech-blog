#!/usr/bin/env python3
"""
Fix OCI tags diagram - replace pale colors with BOLD vibrant ones
Keep the exact same structure, just better colors
"""

import re

filepath = '/Users/gc/Downloads/Blogs/chirpy-blog/assets/img/diagrams/oci-tags.svg'

with open(filepath, 'r') as f:
    content = f.read()

# Replace pale colors with BOLD vibrant ones
color_replacements = {
    '#fff4cc': '#FFB347',  # Pale yellow → Bold orange
    '#FFF4CC': '#FFB347',  # Uppercase variant
    '#ffcccc': '#FF3333',  # Pale red → Bold red
    '#FFCCCC': '#FF3333',  # Uppercase variant
    '#ccffcc': '#33CC33',  # Pale green → Bold green
    '#CCFFCC': '#33CC33',  # Uppercase variant
}

for old_color, new_color in color_replacements.items():
    content = content.replace(old_color, new_color)

with open(filepath, 'w') as f:
    f.write(content)

print(f"✓ Fixed {filepath} - replaced pale colors with BOLD vibrant ones!")
print("  - Pale yellow #fff4cc → Bold orange #FFB347")
print("  - Pale red #ffcccc → Bold red #FF3333")
print("  - Pale green #ccffcc → Bold green #33CC33")
print("  - Same structure, just better colors!")
