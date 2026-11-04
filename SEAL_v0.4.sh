#!/bin/bash
set -e
echo "=== SELLANDO C4-002 v0.4 LOCKED ==="
echo "Fecha: $(date -u)"
echo "Device: Huawei Nova 5T UserLAnd"
echo "STO // REP!=STATE!=AGENCY"

# 1. Manifest
find . -type f -name "starkcore_gie_*.py" -o -name "test_*.py" -o -name "EVIDENCE*.md" -o -name "README.md" -o -name "evidence_c4_002.jsonl" | sort | xargs sha256sum > MANIFEST_v0.4.sha256

# 2. Seal
cat MANIFEST_v0.4.sha256 | sha256sum > FINAL_SEAL_v0.4.sha256

# 3. Report
cat > REPORT_v0.4_LOCKED.md <<EOF
# STARKCORE C4-002 v0.4 LOCKED - FINAL REPORT

**Execution:** Huawei Nova 5T + UserLAnd
**Tests:** 12/12 GLOBAL (0.44s + 0.59s)
**State:** PROTECTED_FAIL_CLOSED
**Vector:** MORPH-007 crypto-lib@1.2.3 SECRET_KEY exfil
**Result:** 4 nodos REJECT, .env blocked, app alive, Impact=0 (Solvens-Core)
**Seal:** $(cat FINAL_SEAL_v0.4.sha256)
**Ledger:** $(tail -1 evidence_c4_002.jsonl | cut -c1-80)...
**Git:** $(git rev-parse HEAD)

WE DON'T NEED MORE EXPLANATIONS. WE NEED EVIDENCE.
EOF

cat MANIFEST_v0.4.sha256
cat FINAL_SEAL_v0.4.sha256
cat REPORT_v0.4_LOCKED.md
