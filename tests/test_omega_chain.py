#!/usr/bin/env python3

import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone

CHAIN = Path("evidence/omega/chain")
CHAIN.mkdir(parents=True, exist_ok=True)


def hash_record(data):
    raw = json.dumps(
        data,
        sort_keys=True,
        separators=(",", ":")
    )
    return hashlib.sha256(raw.encode()).hexdigest()


def create_genesis():
    record = {
        "version": 1,
        "omega": 0.5,
        "previous_hash": "GENESIS",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    record["hash"] = hash_record(record)

    (CHAIN / "omega_001.json").write_text(
        json.dumps(record, indent=2)
    )

    return record


def verify_chain():
    files = sorted(CHAIN.glob("omega_*.json"))

    previous = "GENESIS"

    for f in files:
        data = json.loads(f.read_text())

        if data["previous_hash"] != previous:
            return False, f"BLOCK_CHAIN_BROKEN {f}"

        saved_hash = data["hash"]
        data_copy = dict(data)
        del data_copy["hash"]

        if hash_record(data_copy) != saved_hash:
            return False, f"BLOCK_HASH_INVALID {f}"

        previous = saved_hash

    return True, "OMEGA_CHAIN_OK"


if __name__ == "__main__":
    if not list(CHAIN.glob("omega_*.json")):
        create_genesis()

    ok, msg = verify_chain()

    print(f"[STARKCORE] {'PASS' if ok else 'BLOCK'} {msg}")

    exit(0 if ok else 1)
