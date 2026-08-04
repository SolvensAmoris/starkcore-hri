#!/usr/bin/env python3
import math
from dataclasses import dataclass, field
from typing import List

@dataclass
class Conjecture:
    formula: str; condition: str="n >= 1"; support: int=0; total: int=0
    fails: List[int]=field(default_factory=list); gen: int=0; parent: str=""
    def rate(self): return self.support/max(1,self.total)
    def threshold(self):
        try: return int(self.condition.split(">")[1].strip())
        except: return 0

def eval_strict(expr,n):
    # Evaluador sin escapatoria: True/False SIEMPRE, nunca None
    try:
        if "n**n" in expr:
            # comparar logaritmos para evitar overflow
            if n<=1: lv,rv=False,False
            else:
                # 2**n < n**n <=> n*log2 < n*log n <=> log2 < log n
                if expr=="2**n < n**n": return math.log(n) > math.log(2)
                if expr=="2**n <= n**n": return math.log(n) >= math.log(2)
        if "2**n" in expr and n>60:
            # 2**n es monstruo, pero n < 2**n siempre True para n>=1
            if expr.strip()=="n < 2**n": return True
            if "n**2 < 2**n" in expr: return True # n**2 <<2**n para n>4
            if "n**3 < 3**n" in expr: return True # 3**n domina
        return bool(eval(expr, {"n":n, "math":math, "__builtins__":{}}))
    except Exception as e:
        # Si explota, es fallo del evaluador, no de la conjetura -> contar como False para no mentir
        return False

def test(c, domain):
    sup=0; tot=0; fails=[]
    thr=c.threshold() if ">" in c.condition else 0
    for n in domain:
        if n <= thr: continue
        tot+=1
        if eval_strict(c.formula, n): sup+=1
        else: fails.append(n)
    c.support=sup; c.total=tot; c.fails=fails
    return c

def find_min_threshold(formula, domain):
    # tu idea: buscar el umbral más débil que funciona
    for k in range(1, 30):
        c=Conjecture(formula, f"n > {k}")
        t=test(c, domain)
        if t.total>0 and not t.fails:
            return k, t
    return None,None

def evolve():
    domain=list(range(1,201))
    seeds=["n < n**2","n**2 < 2**n","2*n < n**2","n**3 < 3**n","n < 2**n","2**n < n**n"]
    print("="*72); print("EVOLVER v2.2 DARWIN - sin autoengaño + umbral mínimo"); print("="*72)
    tree={}
    for s in seeds:
        print(f"\n🌱 {s}")
        # test base
        base=Conjecture(s,"n >= 1"); test(base,domain)
        print(f" base: {base.support}/{base.total} fails={base.fails[:5]}")
        k,strong=find_min_threshold(s,domain)
        if k is not None:
            print(f" ✓ fuerte minimal: ∀n (n > {k}): {s} [{strong.support}/{strong.total} 100%]")
            tree[s]=(k,strong)
        else:
            print(f" ✗ muere, no hay umbral <30 que la salve")

    print("\n"+"="*72); print("ÁRBOL DE DESCENDENCIA (ideas únicas, no spam)"); print("="*72)
    for i,(form,(k,_)) in enumerate(tree.items(),1):
        print(f"{i}. {form} => se vuelve fuerte en n > {k}")
    print(f"\nTotal ideas únicas fuertes: {len(tree)} (no 18 primas hermanas)")

if __name__=="__main__": evolve()
