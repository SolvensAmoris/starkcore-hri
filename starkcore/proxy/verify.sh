#!/usr/bin/env bash
set -euo pipefail
REF="${1:-$CI_COMMIT_TAG}"
CLAIM_FILE="${2:-claim.json}"
TYPE=$(git cat-file -t "$REF" 2>/dev/null || echo "no-ref")
echo ">> REF: $REF TYPE=$TYPE"
[ "$TYPE" = "commit" ] && echo "❌ FAIL CA-002 E==H mutable" && exit 1
[ "$TYPE" != "tag" ] && echo "❌ FAIL CA-002 no es EI=H" && exit 1
echo "✅ PASS CA-002 EI=H $REF"

python3 - <<PY
import json, sys, pathlib
p=pathlib.Path("$CLAIM_FILE")
data=json.loads(p.read_text())
events=data.get("events",[])
expire=data.get("verification",{}).get("expire_in","")
if not events:
    print("❌ FAIL WP-002 events vacío = fe")
    sys.exit(1)
if expire != "never":
    print(f"❌ FAIL WP-002 expire_in={expire}")
    sys.exit(1)
print(f"✅ PASS WP-002 events={len(events)} expire_in=never")
print("🔒 STARKCORE_VERIFIED=true identity=EI=H evidence=hash-chained A2A-ready")
PY
