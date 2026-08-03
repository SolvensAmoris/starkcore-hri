import json
import subprocess
from pathlib import Path


ATTESTATION = Path(
    "evidence/borromeo_validator_attestation.json"
)


def commit_exists(commit):
    result = subprocess.run(
        ["git", "cat-file", "-t", commit],
        capture_output=True,
        text=True
    )

    return result.returncode == 0


def verify():

    if not ATTESTATION.exists():
        return False, "ATTESTATION_MISSING"

    data = json.loads(
        ATTESTATION.read_text()
    )

    checks = []

    checks.append(
        (
            "status_verified",
            data.get("status") == "VERIFIED"
        )
    )

    checks.append(
        (
            "commit_exists",
            commit_exists(
                data.get("commit", "")
            )
        )
    )

    checks.append(
        (
            "tests_passed",
            data["tests"]["passed"] is True
        )
    )

    failed = [
        name for name, ok in checks
        if not ok
    ]

    if failed:
        return False, failed

    return True, checks


if __name__ == "__main__":
    ok, report = verify()

    print(
        json.dumps(
            {
                "verified": ok,
                "report": report
            },
            indent=2
        )
    )

    raise SystemExit(
        0 if ok else 1
    )
