from src.starkcore.validators.borromeo_validator import (
    Hypothesis,
    Verdict,
    borromeo_validator,
    check_C2,
    check_C3,
    REQUIRED_HAMMERS
)


def test_rechaza_falso_C1_compresion_cobarde():

    viejo = Hypothesis(
        "modelo viejo",
        L=100,
        F=10,
        hammers=set(),
        assumptions=set(),
        chain=[]
    )

    falso = Hypothesis(
        "yo digo",
        L=10,
        F=0,
        hammers=REQUIRED_HAMMERS,
        assumptions=set(),
        chain=[]
    )

    resultado = borromeo_validator(
        viejo,
        falso,
        set()
    )

    assert resultado != Verdict.BORROMEO_TIGHT


def test_rechaza_falso_C2_terreno_propio():

    teoria = Hypothesis(
        "teoria bonita",
        L=20,
        F=20,
        hammers={"n=1"},
        assumptions=set(),
        chain=[]
    )

    assert check_C2(teoria.hammers) is False


def test_rechaza_falso_C3_premisa_oculta():

    cadena = [
        "tag",
        "commit",
        "firma"
    ]

    declaradas = {
        "tag",
        "commit"
    }

    assert check_C3(
        cadena,
        declaradas
    ) is False
def test_reporte_explica_C3():

    viejo = Hypothesis(
        "modelo viejo",
        L=100,
        F=10,
        hammers=REQUIRED_HAMMERS,
        assumptions=set(),
        chain=[]
    )

    nuevo = Hypothesis(
        "cadena con fantasma",
        L=50,
        F=20,
        hammers=REQUIRED_HAMMERS,
        assumptions=set(),
        chain=[
            "tag",
            "commit",
            "supuesto_oculto",
            "firma"
        ]
    )

    reporte = borromeo_validator(
        viejo,
        nuevo,
        {
            "tag",
            "commit",
            "firma"
        }
    )

    assert reporte.verdict == Verdict.HALLAZGO_AZAROSO
    assert reporte.broken_ring == "C3"
    assert "supuesto_oculto" in reporte.evidence


from src.starkcore.validators.borromeo_validator import self_test


def test_el_validador_se_rechaza_si_mismo():

    assert self_test() is True
