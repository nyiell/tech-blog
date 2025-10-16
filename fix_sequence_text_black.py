#!/usr/bin/env python3
"""
Fix sequence diagrams: Make ALL text BLACK for readability

CHANGES:
1. Actor box text: Blue → Black
2. Message text: Blue → Black
3. Label text: Blue → Black
4. Loop text: Blue → Black

Keep borders and arrows blue, but text must be BLACK
"""

diagrams = [
    '/Users/gc/Downloads/Blogs/chirpy-blog/assets/img/diagrams/oci-hydration.svg',
    '/Users/gc/Downloads/Blogs/chirpy-blog/assets/img/diagrams/metaverse-sequence.svg',
]

# These CSS rules need to change from blue (#0052CC) to black (#000000)
text_fixes = {
    '#my-svg text.actor>tspan{fill:#0052CC': '#my-svg text.actor>tspan{fill:#000000',
    '#my-svg .messageText{fill:#0052CC': '#my-svg .messageText{fill:#000000',
    '#my-svg .labelText,#my-svg .labelText>tspan{fill:#0052CC': '#my-svg .labelText,#my-svg .labelText>tspan{fill:#000000',
    '#my-svg .loopText,#my-svg .loopText>tspan{fill:#0052CC': '#my-svg .loopText,#my-svg .loopText>tspan{fill:#000000',
}

for filepath in diagrams:
    print(f"\nFixing {filepath.split('/')[-1]}...")

    with open(filepath, 'r') as f:
        content = f.read()

    changes_made = []
    for old, new in text_fixes.items():
        if old in content:
            content = content.replace(old, new)
            changes_made.append(f"  ✓ Changed: {old.split('{')[0]} text to BLACK")

    with open(filepath, 'w') as f:
        f.write(content)

    if changes_made:
        for change in changes_made:
            print(change)
    else:
        print("  - No changes needed")

print("\n" + "="*70)
print("SEQUENCE DIAGRAMS NOW HAVE:")
print("  - BLACK text (#000000) on white boxes - READABLE!")
print("  - Blue borders and arrows (#0052CC) - VISIBLE!")
print("="*70)
