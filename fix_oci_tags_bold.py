#!/usr/bin/env python3
"""
Fix OCI tags diagram - make colors BOLD and VIBRANT!
Change pale orange #FFB347 to deep BOLD orange
Make green and red more vibrant too
"""

import re

filepath = '/Users/gc/Downloads/Blogs/chirpy-blog/assets/img/diagrams/oci-tags.svg'

with open(filepath, 'r') as f:
    content = f.read()

# Replace pale/weak colors with BOLD vibrant ones
color_replacements = {
    '#FFB347': '#FF6600',  # Pale orange → BOLD DEEP ORANGE
    '#00AA00': '#00CC00',  # Medium green → BRIGHT GREEN
    '#CC0000': '#DD0000',  # Dark red → BRIGHT RED
}

for old_color, new_color in color_replacements.items():
    # Replace in both uppercase and lowercase
    content = content.replace(old_color, new_color)
    content = content.replace(old_color.lower(), new_color.lower())
    content = content.replace(old_color.upper(), new_color.upper())

with open(filepath, 'w') as f:
    f.write(content)

print(f"✓ Fixed {filepath} - colors are now BOLD and VIBRANT!")
print(f"  - Orange: {color_replacements['#FFB347']} (deep bold orange)")
print(f"  - Green: {color_replacements['#00AA00']} (bright green)")
print(f"  - Red: {color_replacements['#CC0000']} (bright red)")
