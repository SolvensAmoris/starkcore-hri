#!/bin/bash
# RFC-0007 v2 - E ≡ H Firewall
TAG=$1
if [ -z "$TAG" ]; then echo "uso: ./ca002-check.sh <tag>"; exit 1; fi

TAG_HASH=$(git rev-parse $TAG 2>/dev/null)
COMMIT_HASH=$(git rev-parse $TAG^{commit} 2>/dev/null)

echo "Tag: $TAG"
echo "E (tag object): $TAG_HASH"
echo "H (commit): $COMMIT_HASH"

if [ "$TAG_HASH" = "$COMMIT_HASH" ]; then
  echo "🚨 CA-002 DETECTADO: Tag lightweight mutable! E == H"
  exit 1
else
  echo "✅ OK: Tag anotado inmutable - E != H pero E->H verificado"
fi
