#!/usr/bin/env python3
import math
from dataclasses import dataclass
from typing import Set, List

@dataclass
class Species:
    formula: str; fails: Set[int]; k: int; niche: str; sig: dict; interest: float

def eval_safe(e,n):
    try: return bool(eval(e, {"n":n,"math":math,"__builtins__":{}}))
    except: return False

def test(formula,domain):
    fails=set(n for n in domain if not eval_safe(formula,n))
    return fails

def niche_of(formula):
    if "!" in formula or "factorial" in formula: return "FACTORIAL"
    if "2**n" in formula or "3**n" in formula: return "EXP vs POLY"
    if "n**3" in formula and "n**2" in formula: return "POLY vs POLY"
    if "2*n" in formula or "n < n" in formula: return "LINEAL vs POLY"
    return "POLY"

def failure_signature(fails):
    if not fails: return {"size":0,"max":0,"continuous":True,"density":0,"type":"universal"}
    s=sorted(fails)
    size=len(s); mx=max(s)
    continuous = s==list(range(min(s),max(s)+1))
    # ¿falla al inicio y luego despierta? vs falla tardía
    ftype="early" if mx<10 else "late" if min(s)>20 else "scattered"
    return {"size":size,"max":mx,"continuous":continuous,"type":ftype,"set":s}

def interestingness(formula,sig):
    base=0.5
    if sig["type"]=="early" and sig["size"]<5 and sig["continuous"]: base+=0.3 # n**2<2**n que despierta en 4
    if sig["type"]=="universal": base-=0.2 # n<=n**2 verdadero pero trivial
    if "2**n" in formula: base+=0.3
    if "+1" in formula or "+2" in formula: base-=0.3
    return base

def evolves():
    domain=list(range(1,80))
    seeds=["n <= n**2","n < n**2","2*n < n**2","n < n**2+1","n**2 < 2**n","n**2+1 < 2**n","n**3 < 3**n"]
    pop=[]
    for f in seeds:
        fails=test(f,domain)
        # k min
        k=0
        for kk in range(0,30):
            if not any(n>kk and not eval_safe(f,n) for n in domain): k=kk; break
        sig=failure_signature(fails)
        niche=niche_of(f)
        pop.append(Species(f,fails,k,niche,sig,interestingness(f,sig)))

    print("="*72); print("v6 NICHOS - {} ya no mata a todos"); print("="*72)
    for c in pop:
        print(f"{c.niche:15s} {c.formula:15s} fails={sorted(c.fails)[:6]} sig={c.sig} k={c.k}")

    # DEPREDADOR POR NICHO
    print("\n--- DEPREDADOR POR NICHO (no global) ---")
    niches={}
    for c in pop: niches.setdefault(c.niche,[]).append(c)

    survivors=[]
    for niche, group in niches.items():
        print(f"\n🌿 NICHO {niche}:")
        # ordenar por interés + generalidad
        group_sorted=sorted(group, key=lambda x: (-x.interest, x.k, len(x.formula)))
        local_surv=[]
        for cand in group_sorted:
            dominated=False
            for surv in local_surv:
                # solo si mismo nicho y fails surv ⊆ fails cand y k surv <= k cand y no es universal devorando todo
                if surv.fails==set() and cand.fails!=set(): continue # FIX: universal no mata a otros nichos ni a no-universales
                if surv.fails.issubset(cand.fails) and surv.k <= cand.k and surv.formula!=cand.formula:
                    if surv.fails!=cand.fails or len(surv.formula)<len(cand.formula):
                        print(f" ☠️ {cand.formula} (fails {sorted(cand.fails)[:3]}) devorado por {surv.formula}")
                        dominated=True; break
            if not dominated:
                print(f" ⭐ sobrevive {cand.formula} sig={cand.sig['type']} int={cand.interest:.2f}")
                local_surv.append(cand)
        survivors.extend(local_surv)

    print("\n"+"="*72); print("POKÉDEX FINAL v6 - biodiversidad preservada"); print("="*72)
    for c in sorted(survivors,key=lambda x: -x.interest):
        print(f"{c.niche:15s} ∀n (n>{c.k}): {c.formula} | sig={c.sig} | int={c.interest:.2f}")

    print("\nBug filosófico resuelto:")
    print("{} ⊆ todo ya no causa extinción porque depredador solo caza en su nicho")
    print("y universales no depredan no-universales.")
    print("Firma del error: {2,3,4} early continuo ≠ {50,51,52} late → historias distintas")

if __name__=="__main__": evolves()
