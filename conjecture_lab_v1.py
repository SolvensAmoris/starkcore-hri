#!/usr/bin/env python3
"""
Conjecture Discovery Lab v1
Laboratorio de descubrimiento automatizado de conjeturas matemáticas.
Genera → filtra → prueba numéricamente → rankea candidatos fuertes.

Referencias reales (no inventadas):
[1] Raayoni et al. "Generating conjectures on fundamental constants with the Ramanujan Machine"
    Nature 590, 67–73 (2021). https://doi.org/10.1038/s41586-021-03229-4
[2] Romera-Paredes et al. / DeepMind. FunSearch: Making new discoveries in mathematical sciences
    using Large Language Models. Nature (2023/2024). https://deepmind.google/blog/funsearch...
[3] Davila et al. / TxGraffiti lineage. Automated conjecturing frameworks in graph theory
    (building on Fajtlowicz's GRAFFITI). See arXiv:2306.12917 and related.
[4] Recent LLM-based conjecture generation: LeanConjecturer (arXiv:2506.22005),
    FunSearch re-implementations, and neuro-symbolic lemma discovery.

Principio: emparejar generación creativa (o búsqueda sistemática) con evaluador automático
estricto, como en FunSearch y Ramanujan Machine.
"""

import numpy as np
from itertools import combinations, product
from dataclasses import dataclass, field
from typing import List, Callable, Tuple, Dict, Any
import math

# ============================================================
# 1. Representación de una conjetura candidata
# ============================================================
@dataclass
class Conjecture:
    name: str
    formula_str: str
    score: float = 0.0
    support: int = 0          # cuántos ejemplos la cumplen
    total_tested: int = 0
    simplicity: float = 0.0   # menor = más simple (Occam)
    evidence: List[str] = field(default_factory=list)
    status: str = "candidate" # candidate | strong | refuted | known

    def success_rate(self) -> float:
        return self.support / max(1, self.total_tested)

# ============================================================
# 2. Generadores de hipótesis (dominios de ejemplo)
# ============================================================
def generate_polynomial_relations(max_deg=2, max_coeff=3) -> List[Tuple[str, Callable]]:
    """Genera relaciones polinomiales simples del tipo LHS ≈ RHS o desigualdad."""
    candidates = []
    # Ejemplo clásico de búsqueda: relaciones entre n, n^2, sumas, etc.
    vars = ['n', 'n**2', 'n**3', '2**n']
    for left, right in combinations(vars, 2):
        for op in ['<', '<=', '>', '>=', '==']:
            expr = f"{left} {op} {right}"
            # Creamos función evaluable de forma segura
            def make_fn(l=left, r=right, o=op):
                def fn(n):
                    try:
                        lv = eval(l, {"n": n, "np": np})
                        rv = eval(r, {"n": n, "np": np})
                        if o == '<': return lv < rv
                        if o == '<=': return lv <= rv
                        if o == '>': return lv > rv
                        if o == '>=': return lv >= rv
                        if o == '==': return abs(lv - rv) < 1e-9
                    except:
                        return False
                return fn
            candidates.append((expr, make_fn()))
    return candidates

def generate_sequence_patterns(seq: np.ndarray, window=5) -> List[Conjecture]:
    """Busca patrones simples en una secuencia numérica (estilo Ramanujan Machine light)."""
    conjectures = []
    n = len(seq)
    # Diferencias
    diffs = np.diff(seq)
    if np.all(diffs > 0):
        c = Conjecture(
            name="strictly_increasing",
            formula_str="a_{n+1} > a_n for all tested n",
            support=n-1, total_tested=n-1,
            simplicity=1.0
        )
        conjectures.append(c)
    # Ratio
    if np.all(seq[:-1] != 0):
        ratios = seq[1:] / seq[:-1]
        if np.allclose(ratios, ratios[0], rtol=1e-3):
            c = Conjecture(
                name="geometric",
                formula_str=f"a_{{n+1}} / a_n ≈ {ratios[0]:.6f}",
                support=n-1, total_tested=n-1,
                simplicity=2.0,
                evidence=[f"ratio mean={ratios.mean():.6f}, std={ratios.std():.6f}"]
            )
            conjectures.append(c)
    return conjectures

# ============================================================
# 3. Evaluador / filtro (el "evaluator" de FunSearch)
# ============================================================
def evaluate_conjecture(conj_fn: Callable, domain: np.ndarray, tol=1e-8) -> Tuple[int, int, List]:
    support = 0
    evidence = []
    for x in domain:
        try:
            if conj_fn(x):
                support += 1
            else:
                evidence.append(f"fails at {x}")
                if len(evidence) > 5:
                    break
        except Exception:
            continue
    return support, len(domain), evidence

def simplicity_score(formula: str) -> float:
    """Proxy de complejidad: longitud + número de operadores."""
    ops = formula.count('+') + formula.count('*') + formula.count('**') + formula.count('/')
    return len(formula) * 0.1 + ops * 1.5

def rank_conjectures(conjectures: List[Conjecture], min_support_rate=0.95) -> List[Conjecture]:
    ranked = []
    for c in conjectures:
        rate = c.success_rate()
        if rate >= min_support_rate and c.total_tested >= 20:
            # Score compuesto: alto soporte + baja complejidad
            c.score = rate * 100 - c.simplicity * 2
            c.status = "strong" if rate >= 0.99 else "candidate"
            ranked.append(c)
        elif rate < 0.5:
            c.status = "refuted"
    ranked.sort(key=lambda x: -x.score)
    return ranked

# ============================================================
# 4. Laboratorio principal
# ============================================================
def run_lab(domain_size=500, seed=42):
    rng = np.random.default_rng(seed)
    print("=" * 70)
    print("CONJECTURE DISCOVERY LAB v1")
    print("Generación → Evaluación numérica → Ranking por evidencia + simplicidad")
    print("Inspirado en Ramanujan Machine [1] y FunSearch [2]")
    print("=" * 70)

    # --- Dominio de prueba: enteros positivos ---
    domain = np.arange(1, domain_size + 1)

    # --- Generar candidatos polinomiales / relacionales ---
    print("\n[1] Generando candidatos de relaciones...")
    raw_candidates = generate_polynomial_relations()
    print(f"    {len(raw_candidates)} expresiones candidatas generadas")

    conjectures = []
    for expr, fn in raw_candidates:
        support, total, evid = evaluate_conjecture(fn, domain)
        c = Conjecture(
            name=expr.replace(" ", "_"),
            formula_str=expr,
            support=support,
            total_tested=total,
            simplicity=simplicity_score(expr),
            evidence=evid[:3]
        )
        conjectures.append(c)

    # --- Secuencias clásicas para patrón ---
    print("\n[2] Buscando patrones en secuencias clásicas...")
    primes = np.array([2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71])
    fib = np.array([1,1,2,3,5,8,13,21,34,55,89,144,233,377,610])
    for name, seq in [("primes_head", primes), ("fibonacci", fib)]:
        pats = generate_sequence_patterns(seq)
        for p in pats:
            p.name = f"{name}_{p.name}"
            conjectures.append(p)

    # --- Ranking ---
    print("\n[3] Filtrando y rankeando...")
    strong = rank_conjectures(conjectures, min_support_rate=0.90)

    print(f"\n=== TOP CANDIDATOS FUERTES (de {len(conjectures)} totales) ===")
    for i, c in enumerate(strong[:12], 1):
        print(f"{i:2d}. [{c.status:8s}] score={c.score:6.1f}  "
              f"support={c.support}/{c.total_tested} ({c.success_rate()*100:.1f}%)")
        print(f"    {c.formula_str}")
        if c.evidence:
            print(f"    evidence: {c.evidence[0]}")
        print()

    # --- Resumen de robustez ---
    print("=" * 70)
    print("ROBUSTEZ DEL LAB:")
    print("- Separación clara entre candidatos fuertes / débiles / refutados")
    print("- Score combina tasa de acierto + penalización por complejidad (Occam)")
    print("- Fácil de extender: añadir nuevos generadores de hipótesis o dominios")
    print("- Próximo salto natural: conectar LLM (estilo FunSearch) para proponer")
    print("  fórmulas más creativas y usar este evaluador como filtro duro")
    print("=" * 70)
    print("\nCitas clave:")
    print("[1] Ramanujan Machine – Nature 2021")
    print("[2] FunSearch (DeepMind) – Nature 2023/24")
    print("[3] Automated conjecturing (TxGraffiti / GRAFFITI lineage)")
    print("[4] LeanConjecturer & LLM conjecture pipelines (2025)")
    return strong

if __name__ == "__main__":
    run_lab(domain_size=300)
