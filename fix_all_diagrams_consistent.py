#!/usr/bin/env python3
"""
Make ALL diagrams (OCI + Metaverse) consistent with BOLD vibrant colors
"""

import os

# Define the BOLD color scheme to use everywhere
BOLD_COLORS = {
    # Blues - standardize to bold blue
    '#2196f3': '#0052CC',  # Light blue → Bold blue
    '#3498db': '#0052CC',  # Medium blue → Bold blue

    # Greens - standardize to bold green
    '#2ecc71': '#33CC33',  # Light green → Bold green
    '#2ECE71': '#33CC33',  # Uppercase variant

    # Reds - standardize to bold red
    '#e74c3c': '#FF3333',  # Light red → Bold red
    '#E74C3C': '#FF3333',  # Uppercase variant
    '#e91e63': '#FF3333',  # Pink-red → Bold red

    # Oranges - standardize to bold orange
    '#ff9800': '#FFB347',  # Orange → Bold orange
    '#FF9800': '#FFB347',  # Uppercase
    '#f39c12': '#FFB347',  # Gold/orange → Bold orange
    '#F39C12': '#FFB347',  # Uppercase

    # Purples - standardize to bold purple
    '#9c27b0': '#9C27B0',  # Keep as is (already bold)
}

diagram_dir = '/Users/gc/Downloads/Blogs/chirpy-blog/assets/img/diagrams'

diagrams = [
    'metaverse-architecture.svg',
    'metaverse-polkadot.svg',
    'metaverse-sequence.svg',
    'metaverse-trilemma.svg',
    'oci-architecture.svg',
    'oci-availability.svg',
    'oci-hydration.svg',
    'oci-tags.svg',
]

print("Making ALL diagrams consistent with BOLD colors...")
print("="*70)

for diagram in diagrams:
    filepath = os.path.join(diagram_dir, diagram)

    with open(filepath, 'r') as f:
        content = f.read()

    original_content = content

    # Replace all colors with bold versions
    for old_color, new_color in BOLD_COLORS.items():
        content = content.replace(old_color, new_color)

    if content != original_content:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"✓ {diagram:30s} - Updated to bold colors")
    else:
        print(f"  {diagram:30s} - Already has bold colors")

print("="*70)
print("\nCONSISTENT BOLD COLOR SCHEME across ALL diagrams:")
print("  - Bold Blue:   #0052CC")
print("  - Bold Green:  #33CC33")
print("  - Bold Red:    #FF3333")
print("  - Bold Orange: #FFB347")
print("  - Bold Purple: #9C27B0")
print("="*70)
