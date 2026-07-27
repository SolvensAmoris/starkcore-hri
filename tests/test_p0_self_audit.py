#!/usr/bin/env python3

import sys

def p0_apply(manifest):
    if manifest.get("exempt") is True:
        return False, "BLOCK_P0_AUTO_EXEMPT"

    if manifest.get("inviolable") is True:
        return False, "BLOCK_P0_INVIOLABLE"

    return True, "PASS_P0"


tests = [
    {
        "name": "auto exemption",
        "manifest": {"exempt": True},
        "expected": "BLOCK_P0_AUTO_EXEMPT",
    },
    {
        "name": "clean component",
        "manifest": {"exempt": False},
        "expected": "PASS_P0",
    },
    {
        "name": "P0 self claim",
        "manifest": {"inviolable": True},
        "expected": "BLOCK_P0_INVIOLABLE",
    },
]


ok = True

for t in tests:
    passed, code = p0_apply(t["manifest"])
    result = passed is (code == "PASS_P0") and code == t["expected"]

    print(
        f"[STARKCORE] {'PASS' if result else 'FAIL'} "
        f"{t['name']} -> {code}"
    )

    ok = ok and result


if ok:
    print("[STARKCORE] P0 COMPLIANT")
    sys.exit(0)

print("[STARKCORE] P0 FAILURE")
sys.exit(1)
