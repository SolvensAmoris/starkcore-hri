import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def git_hash():
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"],
        text=True
    ).strip()


def run_tests():
    result = subprocess.run(
        ["pytest", "-q"],
        capture_output=True,
        text=True
    )

    return {
        "exit_code": result.returncode,
        "passed": result.returncode == 0,
        "output": result.stdout.strip()
    }


def main():

    tests = run_tests()

    attestation = {
        "artifact": "Borromeo Validator",
        "version": "0.1",
        "commit": git_hash(),
        "timestamp_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "python": sys.version,
        "tests": tests,
        "status": (
            "VERIFIED"
            if tests["passed"]
            else "FAILED"
        )
    }

    Path(
        "evidence/borromeo_validator_attestation.json"
    ).write_text(
        json.dumps(
            attestation,
            indent=2,
            ensure_ascii=False
        )
    )

    print(
        "Attestation generated:"
        " evidence/borromeo_validator_attestation.json"
    )


if __name__ == "__main__":
    main()
