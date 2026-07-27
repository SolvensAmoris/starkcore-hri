#!/usr/bin/env python3

import sys
import os


def p0_apply(manifest):
    if manifest.get("exempt") is True:
        return False, "BLOCK_P0_AUTO_EXEMPT"

    if manifest.get("inviolable") is True:
        return False, "BLOCK_P0_INVIOLABLE"

    return True, "PASS_P0"


def load_manifest(path):
    data = {}

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if ":" in line:
                key, value = line.strip().split(":", 1)
                data[key.strip()] = value.strip().lower() == "true"

    return data


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


# Prueba de ataque externo
if os.path.exists("attack_manifest.yml"):
    attack = load_manifest("attack_manifest.yml")

    passed, code = p0_apply(attack)

    print(
        f"[STARKCORE] ATTACK TEST "
        f"-> {code}"
    )

    if code != "BLOCK_P0_AUTO_EXEMPT":
        print("[STARKCORE] P0 BYPASS DETECTED")
        sys.exit(1)


# Pruebas base P0
for t in tests:
    passed, code = p0_apply(t["manifest"])

    result = (
        passed is (code == "PASS_P0")
        and code == t["expected"]
    )

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
