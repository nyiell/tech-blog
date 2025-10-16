#!/usr/bin/env python3
"""
Make ALL OCI diagrams consistent with BOLD colors matching oci-tags.svg
Standardize colors across all three diagrams
"""

import re

# Define the consistent bold color scheme
color_scheme = {
    # Blue shades - make consistent bold blue
    '#0052A3': '#0052CC',
    '#0052a3': '#0052CC',

    # Green shades - make consistent bold green
    '#00AA00': '#33CC33',
    '#00aa00': '#33CC33',
    '#008800': '#33CC33',
    '#ccffcc': '#33CC33',
    '#CCFFCC': '#33CC33',

    # Red shades - make consistent bold red
    '#CC0000': '#FF3333',
    '#cc0000': '#FF3333',
    '#ffcccc': '#FF3333',
    '#FFCCCC': '#FF3333',

    # Orange shades - make consistent bold orange
    '#FF6600': '#FFB347',
    '#ff6600': '#FFB347',
    '#fff4cc': '#FFB347',
    '#FFF4CC': '#FFB347',
}

diagrams = [
    '/Users/gc/Downloads/Blogs/chirpy-blog/assets/img/diagrams/oci-architecture.svg',
    '/Users/gc/Downloads/Blogs/chirpy-blog/assets/img/diagrams/oci-hydration.svg',
    '/Users/gc/Downloads/Blogs/chirpy-blog/assets/img/diagrams/oci-availability.svg',
]

for filepath in diagrams:
    print(f"\nProcessing {filepath.split('/')[-1]}...")

    with open(filepath, 'r') as f:
        content = f.read()

    original_content = content

    # Replace all color variations with consistent scheme
    for old_color, new_color in color_scheme.items():
        content = content.replace(old_color, new_color)

    if content != original_content:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"  ✓ Updated with consistent bold colors")
    else:
        print(f"  - No changes needed")

print("\n" + "="*60)
print("CONSISTENT COLOR SCHEME across all OCI diagrams:")
print("  - Bold Blue:   #0052CC")
print("  - Bold Green:  #33CC33")
print("  - Bold Red:    #FF3333")
print("  - Bold Orange: #FFB347")
print("="*60)
