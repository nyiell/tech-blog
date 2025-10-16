#!/bin/bash
cd /Users/gc/Downloads/Blogs/chirpy-blog/assets/img/diagrams
for f in metaverse-architecture.svg metaverse-polkadot.svg metaverse-sequence.svg metaverse-trilemma.svg oci-architecture.svg oci-availability.svg oci-hydration.svg oci-tags.svg
do
  echo "=== $f ==="
  grep -o 'fill:#[A-Fa-f0-9]\{6\}' "$f" | sort -u
done
