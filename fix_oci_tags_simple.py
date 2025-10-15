#!/usr/bin/env python3
"""
Remove ALL colors from OCI tags diagram - make it simple and readable
Everything will be black text on white/light gray backgrounds
"""

import re

filepath = '/Users/gc/Downloads/Blogs/chirpy-blog/assets/img/diagrams/oci-tags.svg'

with open(filepath, 'r') as f:
    content = f.read()

# Remove all color fills - replace with white or light gray
color_replacements = {
    'fill:#FF6600': 'fill:#F5F5F5',  # Orange → Light gray
    'fill:#00CC00': 'fill:#F5F5F5',  # Green → Light gray
    'fill:#DD0000': 'fill:#F5F5F5',  # Red → Light gray
}

for old_color, new_color in color_replacements.items():
    content = content.replace(old_color, new_color)

# Remove all white text styling - make text black
white_text_patterns = [
    (r'style="color:#fff !important"', 'style=""'),
    (r'style="color:#fff !important" style="color: #FFFFFF;"', 'style=""'),
    (r' style="color:#fff !important"', ''),
]

for pattern, replacement in white_text_patterns:
    content = re.sub(pattern, replacement, content)

with open(filepath, 'w') as f:
    f.write(content)

print(f"✓ Fixed {filepath}")
print("  - Removed ALL colors")
print("  - Everything is now black text on light backgrounds")
print("  - Simple and readable!")
