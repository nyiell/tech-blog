#!/usr/bin/env python3
"""
Fix oci-hydration.svg to have BRIGHT, VISIBLE colors for sequence diagram
Make it readable with bold colors like the other diagrams
"""

import re

filepath = '/Users/gc/Downloads/Blogs/chirpy-blog/assets/img/diagrams/oci-hydration.svg'

with open(filepath, 'r') as f:
    content = f.read()

# Make backgrounds white and bright
replacements = {
    'fill:#F5F5F5': 'fill:#FFFFFF',  # Light gray → Pure white
    'fill:#000000': 'fill:#0052CC',  # Black fill → Bold blue (for boxes)
    'stroke:#333333': 'stroke:#0052CC',  # Dark stroke → Bold blue
    'stroke:#555555': 'stroke:#0052CC',  # Medium stroke → Bold blue
    'stroke:#666666': 'stroke:#000000',  # Actor lines can stay darker
}

for old, new in replacements.items():
    content = content.replace(old, new)

# Make sure note boxes are visible with bold color
content = content.replace('fill:#FFFFCC', 'fill:#FFB347')  # Pale yellow → Bold orange

with open(filepath, 'w') as f:
    f.write(content)

print("✓ Fixed oci-hydration.svg with BRIGHT, BOLD colors!")
print("  - Boxes: Bold Blue #0052CC")
print("  - Notes: Bold Orange #FFB347")
print("  - Backgrounds: Pure White #FFFFFF")
