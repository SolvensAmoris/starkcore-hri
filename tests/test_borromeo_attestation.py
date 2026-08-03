import json
from pathlib import Path

from verify_borromeo_attestation import verify


def test_attestation_valida():

    ok, report = verify()

    assert ok is True


def test_attestation_detecta_estado_invalido(tmp_path):

    path = Path(
        "evidence/borromeo_validator_attestation.json"
    )

    original = path.read_text()

    data = json.loads(original)
    data["status"] = "INVALID"

    path.write_text(
        json.dumps(data)
    )

    ok, report = verify()

    path.write_text(original)

    assert ok is False


def test_attestation_detecta_commit_vacio():

    path = Path(
        "evidence/borromeo_validator_attestation.json"
    )

    original = path.read_text()

    data = json.loads(original)
    data["commit"] = ""

    path.write_text(
        json.dumps(data)
    )

    ok, report = verify()

    path.write_text(original)

    assert ok is False
