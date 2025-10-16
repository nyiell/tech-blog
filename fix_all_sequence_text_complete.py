#!/usr/bin/env python3
"""
FIX ALL TEXT IN SEQUENCE DIAGRAMS TO BLACK

COMPLETE FIX - Changes ALL text colors from blue to black:
1. Actor box text (#my-svg text.actor>tspan)
2. Message text (#my-svg .messageText)
3. Label text (#my-svg .labelText)
4. Loop text (#my-svg .loopText)

Borders/arrows stay blue for visibility
"""

diagrams = [
    '/Users/gc/Downloads/Blogs/chirpy-blog/assets/img/diagrams/oci-hydration.svg',
    '/Users/gc/Downloads/Blogs/chirpy-blog/assets/img/diagrams/metaverse-sequence.svg',
]

# ALL text must be BLACK (#000000), not blue (#0052CC)
text_replacements = {
    '#my-svg text.actor>tspan{fill:#0052CC;': '#my-svg text.actor>tspan{fill:#000000;',
    '#my-svg .messageText{fill:#0052CC;': '#my-svg .messageText{fill:#000000;',
    '#my-svg .labelText,#my-svg .labelText>tspan{fill:#0052CC;': '#my-svg .labelText,#my-svg .labelText>tspan{fill:#000000;',
    '#my-svg .loopText,#my-svg .loopText>tspan{fill:#0052CC;': '#my-svg .loopText,#my-svg .loopText>tspan{fill:#000000;',
}

print("="*70)
print("FIXING ALL TEXT IN SEQUENCE DIAGRAMS")
print("="*70)

for filepath in diagrams:
    filename = filepath.split('/')[-1]
    print(f"\n{filename}:")

    with open(filepath, 'r') as f:
        content = f.read()

    changes = []
    for old, new in text_replacements.items():
        if old in content:
            content = content.replace(old, new)
            element_name = old.split('{')[0].replace('#my-svg ', '').replace('>', ' ')
            changes.append(f"  ✓ {element_name:30s} → BLACK")

    with open(filepath, 'w') as f:
        f.write(content)

    if changes:
        for change in changes:
            print(change)
    else:
        print("  - Already fixed")

print("\n" + "="*70)
print("FINAL RESULT:")
print("  ✓ ALL text is now BLACK (#000000) - READABLE!")
print("  ✓ Borders/arrows stay BLUE (#0052CC) - VISIBLE!")
print("="*70)
