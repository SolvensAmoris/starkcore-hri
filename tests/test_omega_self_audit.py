#!/usr/bin/env python3

import hashlib
import json
import math
import sys
from datetime import datetime, timezone


EPS = 1e-6


def p0_check(record):
    if record.get("exempt") is True:
        return False, "BLOCK_OMEGA_P0_EXEMPT"

    if record.get("inviolable") is True:
        return False, "BLOCK_OMEGA_P0_INVIOLABLE"

    return True, "P0_OK"


def calculate_omega(record):
    return (
        record["A"]
        * record["T"]
        * record["G"]
        * (1 - record["U"])
    )


def validate_omega(record):
    ok, msg = p0_check(record)

    if not ok:
        return False, msg

    for key in ["A", "T", "G", "U", "Omega"]:
        if key not in record:
            return False, f"BLOCK_MISSING_{key}"

    for key in ["A", "T", "G", "U"]:
        if not 0 <= record[key] <= 1:
            return False, f"BLOCK_RANGE_{key}"

    calculated = calculate_omega(record)

    if not math.isclose(
        calculated,
        record["Omega"],
        abs_tol=EPS
    ):
        return False, "BLOCK_FORMULA_MISMATCH"

    for factor in ["A", "T", "G", "U"]:
        if not record["evidence"].get(factor):
            return False, f"BLOCK_NO_EVIDENCE_{factor}"

    return True, "OMEGA_OK"


def seal_trace(result):
    body = {
        "system": "STARKCORE",
        "layer": "OMEGA",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "result": result,
        "hash": ""
    }

    raw = json.dumps(
        body,
        sort_keys=True
    )

    body["hash"] = hashlib.sha256(
        raw.encode()
    ).hexdigest()

    with open(
        "evidence/omega/omega_trace.json",
        "w"
    ) as f:
        json.dump(body, f, indent=2)


def run():
    tests = [
        {
            "name": "valid",
            "record": {
                "A": 0.9,
                "T": 0.9,
                "G": 0.9,
                "U": 0.1,
                "Omega": 0.6561,
                "evidence": {
                    "A": "audit/A",
                    "T": "audit/T",
                    "G": "audit/G",
                    "U": "audit/U"
                }
            },
            "expect": True
        },
        {
            "name": "fake omega",
            "record": {
                "A": 0.9,
                "T": 0.9,
                "G": 0.9,
                "U": 0.1,
                "Omega": 1.0,
                "evidence": {
                    "A": "x",
                    "T": "x",
                    "G": "x",
                    "U": "x"
                }
            },
            "expect": False
        },
        {
            "name": "self exemption",
            "record": {
                "exempt": True
            },
            "expect": False
        }
    ]

    results = []

    for test in tests:
        ok, msg = validate_omega(test["record"])
        passed = ok == test["expect"]
        print(
            f"[STARKCORE] "
            f"{'PASS' if passed else 'FAIL'} "
            f"{test['name']} -> {msg}"
        )
        results.append(passed)

    final = all(results)

    seal_trace({
        "omega_compliant": final,
        "tests": len(results)
    })

    print(
        "[STARKCORE] "
        + ("Ω COMPLIANT" if final else "Ω BLOCKED")
    )

    return 0 if final else 1


if __name__ == "__main__":
    sys.exit(run())
