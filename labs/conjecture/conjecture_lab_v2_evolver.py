#!/usr/bin/env python3
import numpy as np, math
from dataclasses import dataclass, field
from typing import List

@dataclass
class Conjecture:
    formula: str; condition: str="n >= 1"; support: int=0; total: int=0
    counterexamples: List[int]=field(default_factory=list); generation: int=0
    parent: str=""; status: str="alive"
    def rate(self): return self.support/max(1,self.total)
    def __str__(self): return f"∀n ({self.condition}): {self.formula} [{self.support}/{self.total} {self.rate()*100:.1f}% gen={self.generation}]"

def safe_eval(expr,n):
    try:
        # evitar overflow: usar log para potencias gigantes
        if "n**n" in expr and n>15:
            # log: n*log n vs n*log2
            if expr=="2**n < n**n": return n*math.log(n) > n*math.log(2) if n>1 else False
            if expr=="2**n <= n**n": return n*math.log(n) >= n*math.log(2) if n>1 else False
        if "n!" in expr or "factorial" in expr:
            if n>20: return True # n! >>2**n para n>4
        return bool(eval(expr, {"n":n,"math":math,"__builtins__":{}}))
    except: return None

def test_conjecture(c, domain):
    sup=0; tot=0; fails=[]
    for n in domain:
        cond=safe_eval(c.condition, n)
        if cond is not True: continue
        tot+=1
        res=safe_eval(c.formula, n)
        if res is True: sup+=1
        elif res is False:
            fails.append(int(n))
    c.support=sup; c.total=tot; c.counterexamples=fails
    if not fails and tot>10: c.status="strong"
    elif fails: c.status="needs_refine"
    else: c.status="weak"
    return c

def refine(c):
    if not c.counterexamples: return []
    max_fail=max(c.counterexamples)
    children=[]
    # E1: subir umbral justo después del último fallo
    for k in [max_fail, max_fail+1]:
        children.append(Conjecture(c.formula, f"n > {k}", generation=c.generation+1, parent=str(c)))
    # E2: debilitar < a <=
    if "<" in c.formula and "<=" not in c.formula:
        children.append(Conjecture(c.formula.replace("<","<="), c.condition, generation=c.generation+1, parent=str(c)))
    return children

def evolve():
    domain=np.arange(1,201)
    seeds=["n < n**2","n**2 < 2**n","2*n < n**2","n**3 < 3**n","n < 2**n","n**2 < n**3","2**n < n**n","n**2 < n**3 - 5"]
    pop=[Conjecture(s,"n >= 1",0,0,[],0,"") for s in seeds]
    archive=[]; seen=set()
    print("="*72); print("EVOLVER v2.1 - FIXED"); print("="*72)
    for gen in range(5):
        print(f"\n--- Gen {gen} pop={len(pop)} ---")
        nxt=[]
        for c in pop:
            key=(c.formula,c.condition)
            if key in seen: continue
            seen.add(key)
            t=test_conjecture(c,domain)
            if t.status=="strong":
                archive.append(t); print(f" ✓ FUERTE: {t}")
            elif t.status=="needs_refine":
                print(f" → refina: {t.formula} en {t.condition} falla {t.counterexamples[:3]}")
                nxt.extend(refine(t))
            else:
                if t.rate()>0.7: nxt.append(t)
        pop=nxt[:40]
        if not pop: break
    print("\n"+"="*72); print("ARCHIVO FUERTES"); print("="*72)
    uniq={}
    for c in archive:
        k=(c.formula,c.condition)
        if k not in uniq or c.rate()>uniq[k].rate(): uniq[k]=c
    for i,c in enumerate(sorted(uniq.values(), key=lambda x: x.condition),1):
        print(f"{i}. {c}")
    print(f"\nTotal fuertes únicas: {len(uniq)}")
    return list(uniq.values())

if __name__=="__main__": evolve()
