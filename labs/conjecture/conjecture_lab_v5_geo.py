#!/usr/bin/env python3
import math
from dataclasses import dataclass, field
from typing import List, Set

@dataclass
class Species:
    formula: str; k: int; fails: Set[int]; sup: int; tot: int; interest: float; gen: int=0; parent: str=""
    def __str__(self): return f"∀n (n>{self.k}): {self.formula} | fails={sorted(list(self.fails))[:5]} int={self.interest:.2f}"

def eval_safe(e,n):
    try: return bool(eval(e, {"n":n,"math":math,"__builtins__":{}}))
    except: return False

def test(formula,k,domain):
    fails=set()
    for n in domain:
        if n<=k: continue
        if not eval_safe(formula,n): fails.add(n)
    tot=len([n for n in domain if n>k])
    return fails, tot-len(fails), tot

def find_min_k(formula,domain):
    for k in range(0,50):
        fails,sup,tot=test(formula,k,domain)
        if not fails: return k,fails,sup,tot
    return None,set(),0,0

def interestingness(formula,k,fails):
    gen_score=1/(1+k*0.3)
    simp=1/(1+len(formula)*0.07)
    # dificultad: si su fail set es pequeño pero no vacío en k=0, es casi teorema
    diff = 0.5 if len(fails)>0 and len(fails)<10 else 0.2
    if "2**n" in formula: diff+=0.4
    trivial=-0.4 if "+1" in formula or "+2" in formula or "+3" in formula else 0
    return gen_score*0.4 + simp*0.3 + diff*0.3 + trivial

# --- DEPREDADOR LÓGICO REAL ---
def logically_subsumes(a:Species,b:Species,domain):
    """A subsume B si: fails(A) ⊆ fails(B) y A es más general (k_a <= k_b) y fórmula no trivialmente más débil"""
    if not a.fails.issubset(b.fails): return False
    if a.k > b.k: return False
    # si A falla menos y es más general, B es redundante
    if len(a.fails) < len(b.fails): return True
    # misma zona de fallo pero A más simple
    if a.fails==b.fails and len(a.formula) < len(b.formula): return True
    return False

def evolve_geo():
    domain=list(range(1,100))
    seeds=["n < n**2","n <= n**2","2*n < n**2","n**2 < 2**n","n**2+1 < 2**n","n**2+2 < 2**n","n < n**2+1","n < n**2+5"]
    pop=[]
    print("="*72); print("v5 GEOGRAFÍA DE ERRORES - el ADN es dónde falla"); print("="*72)
    for s in seeds:
        k,fails0,sup0,tot0=find_min_k(s,domain) if True else (0,*test(s,0,domain))
        # test base k=0 para ver fails
        fails_base,sup_base,tot_base=test(s,0,domain)
        if k is None:
            k,f,sup,tot=0,fails_base,sup_base,tot_base
        else:
            f=set()
        inter=interestingness(s,k,fails_base)
        pop.append(Species(s,k,fails_base,sup_base,tot_base,inter,0,"seed"))

    print("\n--- MAPA DE FALLOS (k=0) ---")
    for c in pop:
        print(f" {c.formula:15s} falla en {sorted(c.fails)[:8]} -> k_min={find_min_k(c.formula,domain)[0]}")

    # Cruza por contraejemplos: intersección y diferencia
    print("\n--- CRUZA POR ERRORES (tu idea loca) ---")
    a=next(p for p in pop if p.formula=="n < n**2")
    b=next(p for p in pop if p.formula=="2*n < n**2")
    print(f"A {a.formula} fails {sorted(a.fails)}")
    print(f"B {b.formula} fails {sorted(b.fails)}")
    print(f"Intersección fails: {sorted(a.fails & b.fails)}")
    print(f"Unión fails: {sorted(a.fails | b.fails)}")
    print(f"-> pregunta: ¿existe fórmula cuyo fail sea intersección? Esa sería más general que ambas")

    # DEPREDADOR GEOGRÁFICO
    print("\n--- DEPREDADOR GEOGRÁFICO ---")
    survivors=[]
    for cand in sorted(pop,key=lambda x: (len(x.fails), x.k, len(x.formula))):
        dominated=False
        for surv in survivors:
            if logically_subsumes(surv,cand,domain):
                print(f" ☠️ {cand.formula} (fails {sorted(cand.fails)[:3]}) devorado por {surv.formula} (fails {sorted(surv.fails)[:3]}) | fails ⊆")
                dominated=True; break
        if not dominated:
            survivors.append(cand)

    print("\n"+"="*72); print("POKÉDEX v5 - sobreviven por geografía, no por string"); print("="*72)
    for i,c in enumerate(sorted(survivors,key=lambda x: (-x.interest, len(x.fails))),1):
        kmin=find_min_k(c.formula,domain)[0]
        print(f"⭐ {i}. {c.formula} → fuerte desde n>{kmin} | interés {c.interest:.2f}")

    print("\nAhora sí:")
    print("v1: ¿verdadera? | v2: ¿desde cuándo? | v3: muta y cruza | v4: heurística | v5: fails ⊆ fails")
    print("El depredador ya no lee fórmulas, lee territorios de error.")

if __name__=="__main__": evolve_geo()
