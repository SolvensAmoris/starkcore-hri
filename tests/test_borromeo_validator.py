from starkcore.validators.borromeo_validator import (
    Hypothesis,
    BorromeoValidator
)


def valid_hypothesis():
    return Hypothesis(
        id="valid",
        L_old=10,
        L_new=5,
        F_old=2,
        F_new=8,
        chain=["root"],
        assumptions_P0={"P0"},
        assumptions_used={"P0"},
        hammers_applied={
            "n=0": True,
            "n=1": True,
            "n=inf": True,
            "fijo": True,
            "inversion": True,
            "limite": True,
        },
    )


def test_borromeo_accepts_valid_hypothesis():
    v = BorromeoValidator()
    result = v.validate(valid_hypothesis())

    assert result["verdict"] == "BORROMEO_TIGHT"


def test_borromeo_rejects_hidden_assumption_CA002():
    v = BorromeoValidator()

    h = valid_hypothesis()
    h.assumptions_used = {"P0", "P1_oculta"}

    result = v.validate(h)

    assert result["verdict"] == "REJECTED"
    assert "CA-002" in result["reason"]


def test_borromeo_rejects_weak_theory():
    v = BorromeoValidator()

    h = valid_hypothesis()
    h.hammers_applied = {}

    result = v.validate(h)

    assert result["verdict"] == "REJECTED"
    assert "TEORIA_DEBIL" in result["reason"]
