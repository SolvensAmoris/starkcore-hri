#!/usr/bin/env python3
import math, random, itertools
from dataclasses import dataclass, field
from typing import List

@dataclass
class Species:
    formula: str; k: int; support: int; total: int
    fails: List[int]; fitness: float; parent: str=""; gen: int=0
    def __str__(self): return f"∀n (n>{self.k}): {self.formula} | fit={self.fitness:.3f} [{self.support}/{self.total}]"

def eval_safe(expr,n):
    try:
        if n>100 and "2**n" in expr: # polinomio vs exp, exp gana
            if expr.split("<")[0].strip() in ["n","n**2","n**3","2*n","n**2+n","n**2+1","2*n**2","n**3"]:
                return "<" in expr
        return bool(eval(expr, {"n":n,"math":math,"__builtins__":{}}))
    except: return False

def test(formula,k,domain):
    sup=0; tot=0; fails=[]
    for n in domain:
        if n<=k: continue
        tot+=1
        if eval_safe(formula,n): sup+=1
        else: fails.append(n)
    return sup,tot,fails

def fitness_score(sup,tot,k,formula,fails):
    if tot==0: return 0
    truth = sup/tot
    generality = 1 - (k/100) # k pequeño = más general
    simplicity = 1 / (1 + len(formula)*0.05 + formula.count("*")*0.1)
    penalty = len(fails)*0.05
    return truth*0.6 + generality*0.25 + simplicity*0.15 - penalty

def find_min_k(formula,domain):
    for k in range(0,50):
        sup,tot,fails=test(formula,k,domain)
        if tot>0 and not fails:
            fit=fitness_score(sup,tot,k,formula,fails)
            return k,sup,tot,fit
    return None,0,0,0

# --- MUTACIONES ESTRUCTURALES ---
def mutate_formula(f):
    mutants=set()
    # < ↔ <=
    if "<" in f and "<=" not in f: mutants.add(f.replace("<","<="))
    # + constantes
    for c in [1,2,3]:
        if "n**2" in f: mutants.add(f.replace("n**2",f"n**2+{c}")); mutants.add(f.replace("n**2",f"n**2+{c}*n"))
    # * constantes
    if "n**2" in f and "2*" not in f: mutants.add(f.replace("n**2",f"2*n**2"))
    # cambiar exponente / base
    mutants.add(f.replace("2**n","3**n")); mutants.add(f.replace("n**2","n**3"))
    mutants.add(f.replace("2**n","n**n",1) if "2**n" in f else f)
    return list(mutants)[:8]

def crossover(f1,f2):
    # n**2 < 2**n x 2**n < n**n => n**2 < n**n
    try:
        left1=f1.split("<")[0].strip(); right2=f2.split("<")[1].strip() if "<" in f2 else f2.split("<=")[1].strip()
        if "<=" in f1 or "<=" in f2: return f"{left1} <= {right2}"
        return f"{left1} < {right2}"
    except: return None

# --- LOOP EVOLUTIVO ---
def evolve():
    domain=list(range(1,250))
    seeds=["n**2 < 2**n","n < n**2","2*n < n**2"]
    population=[]
    print("="*72)
    print("DARWIN v3 - mutación + cruza + fitness")
    print("="*72)
    for s in seeds:
        k,sup,tot,fit=find_min_k(s,domain)
        if k is not None:
            population.append(Species(s,k,sup,tot,[],fit,f"semilla:{s}",0))

    for gen in range(3):
        print(f"\n--- GEN {gen} | {len(population)} especies ---")
        next_gen=[]
        # mutación
        for sp in population[:10]:
            for mf in mutate_formula(sp.formula):
                k,sup,tot,fit=find_min_k(mf,domain)
                if k is not None:
                    child=Species(mf,k,sup,tot,[],fit,sp.formula,sp.gen+1)
                    next_gen.append(child)
        # cruza
        for a,b in itertools.combinations(population[:6],2):
            cf=crossover(a.formula,b.formula)
            if cf:
                k,sup,tot,fit=find_min_k(cf,domain)
                if k is not None:
                    child=Species(cf,k,sup,tot,[],fit,f"{a.formula} x {b.formula}",a.gen+1)
                    next_gen.append(child)
        # selección: top 12 por fitness
        all_cands=population+next_gen
        all_cands.sort(key=lambda x: -x.fitness)
        # deduplicar formula+k
        seen=set(); filtered=[]
        for c in all_cands:
            key=(c.formula,c.k)
            if key not in seen:
                seen.add(key); filtered.append(c)
        population=filtered[:12]
        for i,c in enumerate(population[:5],1):
            print(f" {i}. {c} ← {c.parent[:25]}")

    print("\n"+"="*72)
    print("POKÉDEX FINAL - supervivientes más generales")
    print("="*72)
    for i,c in enumerate(sorted(population,key=lambda x: (-x.fitness, x.k))[:10],1):
        star="⭐" if c.fitness>0.8 else " "
        print(f"{star} {i}. {c}")
        if c.gen>0: print(f" linaje: {c.parent}")

if __name__=="__main__": evolve()
