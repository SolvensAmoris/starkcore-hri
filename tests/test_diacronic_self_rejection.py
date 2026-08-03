from src.starkcore.validators.diacronic_identity_validator import (
    EntityState,
    IdentityVerdict,
    diacronic_validator
)


def test_diacronic_rechaza_su_propia_perdida_de_historia():

    validator_v1 = EntityState(
        name="DiacronicValidator",
        state={"state", "history", "constraints"},
        history=["genesis", "v0.1"],
        constraints={"history"}
    )

    validator_v2 = EntityState(
        name="DiacronicValidator",
        state={"state", "constraints"},
        history=[],
        constraints={"history"}
    )

    result = diacronic_validator(
        validator_v1,
        validator_v2
    )

    assert result == IdentityVerdict.HISTORY_BROKEN
