#!/usr/bin/env python3
"""
Fix OCI architecture diagram - match metaverse style exactly!
Colored boxes need style="color:#fff !important" on BOTH the g.label AND span.nodeLabel
"""

import re

filepath = '/Users/gc/Downloads/Blogs/chirpy-blog/assets/img/diagrams/oci-architecture.svg'

with open(filepath, 'r') as f:
    content = f.read()

# The 4 colored nodes that need white text
colored_nodes = [
    'flowchart-MA-5',   # Migration Assets - blue #0052A3
    'flowchart-HA-11',  # Hydration Agent - red #CC0000
    'flowchart-GV-13',  # Golden Volumes - orange #FF6600
    'flowchart-TF-21',  # Terraform Stack - green #00AA00
]

for node_id in colored_nodes:
    # Find the entire node section
    pattern = f'(<g class="node default" id="{node_id}"[^>]*>.*?</g></g>)'

    def fix_node(match):
        node = match.group(0)

        # Add style="color:#fff !important" to the <g class="label"> element
        node = re.sub(
            r'(<g class="label" style=)"([^"]*)"',
            r'\1"color:#fff !important"',
            node
        )
        node = re.sub(
            r'(<g class="label")(>)',
            r'\1 style="color:#fff !important"\2',
            node
        )

        # Add style="color:#fff !important" to the <span class="nodeLabel"> element
        node = re.sub(
            r'(<span class="nodeLabel")([ >])',
            r'\1 style="color:#fff !important"\2',
            node
        )

        # Also make sure the div has the color
        node = re.sub(
            r'(<div[^>]*style="[^"]*)(">)',
            lambda m: m.group(1) + '; color: rgb(255, 255, 255) !important' + m.group(2) if 'color:' not in m.group(1) else m.group(0),
            node
        )

        return node

    content = re.sub(pattern, fix_node, content, flags=re.DOTALL)

with open(filepath, 'w') as f:
    f.write(content)

print(f"✓ Fixed {filepath} - colored boxes now match metaverse diagram style!")
