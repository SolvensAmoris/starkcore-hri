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


ok = True


# Ataque controlado
if os.path.exists("attack_manifest.yml"):
    attack = load_manifest("attack_manifest.yml")

    passed, code = p0_apply(attack)

    print(f"[STARKCORE] ATTACK TEST -> {code}")

    if code != "BLOCK_P0_AUTO_EXEMPT":
        print("[STARKCORE] P0 BYPASS DETECTED")
        sys.exit(1)


tests = [
    ("auto exemption", {"exempt": True}, "BLOCK_P0_AUTO_EXEMPT"),
    ("clean component", {"exempt": False}, "PASS_P0"),
    ("P0 self claim", {"inviolable": True}, "BLOCK_P0_INVIOLABLE"),
]


for name, manifest, expected in tests:
    passed, code = p0_apply(manifest)

    result = code == expected

    print(
        f"[STARKCORE] {'PASS' if result else 'FAIL'} "
        f"{name} -> {code}"
    )

    ok = ok and result


if ok:
    print("[STARKCORE] P0 COMPLIANT")
    sys.exit(0)

print("[STARKCORE] P0 FAILURE")
sys.exit(1)
