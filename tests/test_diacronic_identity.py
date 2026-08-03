from src.starkcore.validators.diacronic_identity_validator import (
    EntityState,
    IdentityVerdict,
    diacronic_validator
)


def test_identidad_sin_historia_es_rechazada():

    viejo = EntityState(
        "X",
        {"a"},
        ["genesis"],
        {"a"}
    )

    nuevo = EntityState(
        "X",
        {"a"},
        [],
        {"a"}
    )

    assert diacronic_validator(
        viejo,
        nuevo
    ) == IdentityVerdict.HISTORY_BROKEN


def test_identidad_persistente():

    viejo = EntityState(
        "X",
        {"a"},
        ["genesis"],
        {"a"}
    )

    nuevo = EntityState(
        "X",
        {"a", "b"},
        ["genesis", "mutation"],
        {"a"}
    )

    assert diacronic_validator(
        viejo,
        nuevo
    ) == IdentityVerdict.IDENTITY_PERSISTENT


def test_etiqueta_sin_continuidad():

    viejo = EntityState(
        "X",
        {"a"},
        ["genesis"],
        {"a"}
    )

    nuevo = EntityState(
        "Y",
        {"a"},
        ["fake"],
        {"a"}
    )

    assert diacronic_validator(
        viejo,
        nuevo
    ) == IdentityVerdict.LABEL_ONLY
