#!/usr/bin/env python3
"""
Fix BOTH sequence diagrams with consistent bold colors
"""

diagrams = [
    '/Users/gc/Downloads/Blogs/chirpy-blog/assets/img/diagrams/oci-hydration.svg',
    '/Users/gc/Downloads/Blogs/chirpy-blog/assets/img/diagrams/metaverse-sequence.svg',
]

replacements = {
    'fill:#000000': 'fill:#0052CC',  # Black → Bold blue
    'stroke:#000000': 'stroke:#0052CC',  # Black stroke → Bold blue
    'stroke:#333333': 'stroke:#0052CC',  # Dark gray → Bold blue
    'stroke:#555555': 'stroke:#0052CC',  # Medium gray → Bold blue
    'fill:#FFFFCC': 'fill:#FFB347',  # Pale yellow → Bold orange
}

for filepath in diagrams:
    with open(filepath, 'r') as f:
        content = f.read()

    for old, new in replacements.items():
        content = content.replace(old, new)

    with open(filepath, 'w') as f:
        f.write(content)

    print(f"✓ Fixed {filepath.split('/')[-1]}")

print("\nBoth sequence diagrams now use BOLD colors:")
print("  - Bold Blue #0052CC for boxes, text, lines")
print("  - Bold Orange #FFB347 for notes")
