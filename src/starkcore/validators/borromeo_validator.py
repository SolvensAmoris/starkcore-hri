from dataclasses import dataclass
from enum import Enum


class Verdict(Enum):
    BORROMEO_TIGHT = "BORROMEO_TIGHT"
    COMPRESION_SOLO = "COMPRESION_SOLO"
    TEORIA_DEBIL = "TEORIA_DEBIL"
    HALLAZGO_AZAROSO = "HALLAZGO_AZAROSO"


@dataclass
class Hypothesis:
    name: str
    L: int
    F: int
    hammers: set
    assumptions: set
    chain: list


@dataclass
class ValidationReport:
    verdict: Verdict
    broken_ring: str | None
    reason: str
    evidence: list


REQUIRED_HAMMERS = {
    "n=0",
    "n=1",
    "n=infinito",
    "punto_fijo",
    "inversion",
    "limite"
}


def check_C1(previous, current):

    if current.L < previous.L and current.F > previous.F:
        return True

    return False


def check_C2(applied):

    return REQUIRED_HAMMERS.issubset(applied)


def missing_hammers(applied):

    return list(REQUIRED_HAMMERS - applied)


def check_C3(chain, declared):

    for step in chain:
        if step not in declared:
            return False

    return True


def borromeo_validator(previous, current, declared):

    if not check_C1(previous, current):
        return ValidationReport(
            Verdict.COMPRESION_SOLO,
            "C1",
            "La compresion redujo longitud pero no aumentó falsabilidad",
            [
                f"L viejo={previous.L}",
                f"L nuevo={current.L}",
                f"F viejo={previous.F}",
                f"F nuevo={current.F}"
            ]
        )


    if not check_C2(current.hammers):

        return ValidationReport(
            Verdict.TEORIA_DEBIL,
            "C2",
            "No sobrevivio todos los martillos epistemicos",
            missing_hammers(current.hammers)
        )


    if not check_C3(current.chain, declared):

        return ValidationReport(
            Verdict.HALLAZGO_AZAROSO,
            "C3",
            "Existe un paso no declarado en la cadena",
            [
                step for step in current.chain
                if step not in declared
            ]
        )


    return ValidationReport(
        Verdict.BORROMEO_TIGHT,
        None,
        "Los tres anillos sobreviven",
        []
    )


def self_test():
    """
    Prueba minima de identidad:
    el validador debe rechazar
    compresiones que pierden falsabilidad.
    """

    weak_old = Hypothesis(
        "old",
        L=100,
        F=10,
        hammers=REQUIRED_HAMMERS,
        assumptions=set(),
        chain=[]
    )

    weak_new = Hypothesis(
        "fake",
        L=10,
        F=0,
        hammers=REQUIRED_HAMMERS,
        assumptions=set(),
        chain=[]
    )

    report = borromeo_validator(
        weak_old,
        weak_new,
        set()
    )

    return report.verdict != Verdict.BORROMEO_TIGHT
