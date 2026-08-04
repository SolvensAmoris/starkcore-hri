from dataclasses import dataclass
from typing import Dict, List, Set

@dataclass
class Hypothesis:
    id: str
    L_old: float
    L_new: float
    F_old: int
    F_new: int
    chain: List[str]
    assumptions_P0: Set[str]
    assumptions_used: Set[str]
    hammers_applied: Dict[str, bool]

REQUIRED_HAMMERS = {"n=0","n=1","n=inf","fijo","inversion","limite"}
LAW = r"F(H\X)==F(H) && L(H\X)<L(H) => MAKEUP else STRUCTURE"

class BorromeoValidator:
    def c1_peligrosa(self, h: Hypothesis):
        if h.L_new >= h.L_old:
            return False, f"C1 FAIL: L no bajo {h.L_old}->{h.L_new}"
        if h.F_new <= h.F_old:
            return False, f"C1 FAIL: F no subio {h.F_old}->{h.F_new}"
        return True, "C1 OK"

    def c2_bordes(self, h: Hypothesis):
        if not h.hammers_applied:
            return False, "C2 FAIL: sin martillos -> TEORIA_DEBIL"
        missing = REQUIRED_HAMMERS - set(h.hammers_applied.keys())
        # Si faltan mas de 4, es porque solo testeo en su terreno
        if len(missing) >= 4:
            return False, f"C2 FAIL: faltan {missing} -> TEORIA_DEBIL"
        return True, "C2 OK"

    def c3_inevitabilidad(self, h: Hypothesis):
        if len(h.chain) == 0:
            return False, "C3 FAIL: cadena vacia"
        # convertir a set por si vienen como lista
        p0 = set(h.assumptions_P0)
        used = set(h.assumptions_used)
        hidden = used - p0
        if hidden:
            return False, f"C3 FAIL: ocultas {hidden} -> CA-002"
        return True, "C3 OK"

    def validate(self, h: Hypothesis):
        for check in [self.c1_peligrosa, self.c2_bordes, self.c3_inevitabilidad]:
            ok, msg = check(h)
            if not ok:
                return {"verdict": "REJECTED", "reason": msg}
        return {"verdict": "BORROMEO_TIGHT", "reason": "C1^C2^C3"}
