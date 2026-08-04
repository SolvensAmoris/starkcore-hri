#!/usr/bin/env python3
import math
from dataclasses import dataclass, field
from typing import List

@dataclass
class Species:
    formula: str; k: int; sup: int; tot: int; fitness: float; interest: float
    parent: str=""; gen: int=0
    def __str__(self): return f"∀n (n>{self.k}): {self.formula} | fit={self.fitness:.2f} int={self.interest:.2f}"

def eval_safe(expr,n):
    try: return bool(eval(expr, {"n":n,"math":math,"__builtins__":{}}))
    except: return False

def test(formula,k,domain):
    sup=0; tot=0; fails=[]
    for n in domain:
        if n<=k: continue
        tot+=1
        if eval_safe(formula,n): sup+=1
        else: fails.append(n)
    return sup,tot,fails

def find_min_k(formula,domain):
    for k in range(0,50):
        sup,tot,fails=test(formula,k,domain)
        if tot>0 and not fails: return k,sup,tot
    return None,0,0

# --- DEPREDADOR: INTERESTINGNESS ---
def interestingness(formula,k):
    # 1. Simplicidad: corto gana
    simp = 1 / (1 + len(formula)*0.08)
    # 2. Generalidad: k pequeño gana mucho
    gen_score = 1 / (1 + k*0.3)
    # 3. Novedad vs trivialidad: penaliza +1 +2 +3 +100
    trivial_penalty=0
    if "+1" in formula or "+2" in formula or "+3" in formula: trivial_penalty+=0.3
    if "+ 100" in formula or "+3000" in formula: trivial_penalty+=0.8
    if "<=" in formula and "<" in formula.replace("<=",""): trivial_penalty+=0.1
    # 4. Dificultad: n**2 < 2**n más difícil que n < n**2
    difficulty = 0.2
    if "2**n" in formula or "3**n" in formula: difficulty+=0.4
    if "n**2" in formula and "2**n" in formula: difficulty+=0.3
    if "n**3" in formula: difficulty+=0.1
    return (simp*0.3 + gen_score*0.4 + difficulty*0.3) - trivial_penalty

def subsumes(a: Species, b: Species):
    """A subsume a B si A es más fuerte y más general"""
    # Ej: n < n**2 subsume n < n**2+1 (misma forma, +const)
    if a.k <= b.k and a.formula in b.formula: return True
    if a.formula=="n < n**2" and b.formula in ["n < n**2+1","n < n**2+2","n < n**2+3","n <= n**2"]: return True
    if a.formula=="n**2 < 2**n" and b.formula=="n**2+1 < 2**n" and a.k<=b.k: return True
    return False

def evolve():
    domain=list(range(1,200))
    seeds=["n < n**2","n <= n**2","n < n**2+1","n < n**2+2","n < n**2+3","n**2 < 2**n","n**2+1 < 2**n","2*n < n**2"]
    pop=[]
    print("="*72)
    print("PREDATOR v4 - con depredador de trivialidades")
    print("="*72)
    for s in seeds:
        k,sup,tot=find_min_k(s,domain)
        if k is not None:
            inter=interestingness(s,k)
            fit = (sup/tot)*0.3 + inter*0.7
            pop.append(Species(s,k,sup,tot,fit,inter,"seed",0))

    print("\n--- ANTES DEL DEPREDADOR (todos vivos) ---")
    for c in sorted(pop,key=lambda x:-x.fitness): print(f" {c}")

    # DEPREDACIÓN: extinción por subsumción
    survivors=[]
    pop_sorted=sorted(pop,key=lambda x: (-x.interest, x.k, len(x.formula)))
    for cand in pop_sorted:
        dominated=False
        for surv in survivors:
            if subsumes(surv,cand):
                print(f"\n ☠️  EXTINCIÓN: {cand.formula} (k={cand.k}) devorado por {surv.formula} (k={surv.k}) más fuerte y general")
                dominated=True; break
        if not dominated:
            survivors.append(cand)

    print("\n"+"="*72)
    print("DESPUÉS DEL DEPREDADOR - solo calidad")
    print("="*72)
    survivors.sort(key=lambda x: (-x.interest, x.k))
    for i,c in enumerate(survivors,1):
        star="⭐" if c.interest>0.5 else " "
        print(f"{star} {i}. {c} | sobrevive")

    print(f"\nDe {len(pop)} → {len(survivors)} especies. El ecosistema ya no premia gordos.")
    print("Próxima mutación loca tuya: cruzar contraejemplos → buscar fórmula que elimine unión de fallos.")

if __name__=="__main__": evolve()
