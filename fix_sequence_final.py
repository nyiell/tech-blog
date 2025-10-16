#!/usr/bin/env python3
"""
FINAL FIX: Replace &gt; with > and change ALL text to BLACK
"""

diagrams = [
    '/Users/gc/Downloads/Blogs/chirpy-blog/assets/img/diagrams/oci-hydration.svg',
    '/Users/gc/Downloads/Blogs/chirpy-blog/assets/img/diagrams/metaverse-sequence.svg',
]

replacements = {
    'text.actor&gt;tspan{fill:#0052CC': 'text.actor>tspan{fill:#000000',
    '.labelText&gt;tspan{fill:#0052CC': '.labelText>tspan{fill:#000000',
    '.loopText&gt;tspan{fill:#0052CC': '.loopText>tspan{fill:#000000',
    '.noteText&gt;tspan{fill:rgb(183': '.noteText>tspan{fill:#000000',
}

for filepath in diagrams:
    with open(filepath, 'r') as f:
        content = f.read()

    for old, new in replacements.items():
        content = content.replace(old, new)

    with open(filepath, 'w') as f:
        f.write(content)

    print(f"✓ Fixed {filepath.split('/')[-1]}")

print("\n✓ ALL TEXT IS NOW BLACK - READABLE!")
