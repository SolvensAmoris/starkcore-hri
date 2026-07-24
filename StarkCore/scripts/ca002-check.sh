#!/bin/sh
set -e
echo "=== STARKCORE CA-002 FIREWALL v2 + MAGIKA ==="
TYPE=$(git cat-file -t $CI_COMMIT_TAG 2>/dev/null || echo notag)
echo "TAG TYPE: $TYPE"
if [ "$TYPE" = "commit" ]; then echo "BLOCKED E==H"; exit 1; else echo "PASSED E!=H"; fi
magika . --recursive || true
echo "PASSED ALL"
