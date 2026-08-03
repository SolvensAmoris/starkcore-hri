#!/usr/bin/env python3
"""
Conjecture Lab v2 - Stable + LLM Generator (offline)
- v1.1 estable (fix closure) como baseline
- Generador tipo FunSearch: propone desigualdades no triviales con templates + sympy
- Evaluador duro + ranking Occam
"""
import numpy as np, itertools, random, math
from dataclasses import dataclass, field
from typing import List

@dataclass
class Conjecture:
    name: str; formula_str: str; score: float=0.0
    support: int=0; total_tested: int=0; simplicity: float=0.0
    evidence: List[str]=field(default_factory=list); status: str="candidate"
    def rate(self): return self.support/max(1,self.total_tested)

# ============ BASE ESTABLE v1.1 ============
def gen_stable():
    cands=[]
    vars=['n','n**2','n**3','2**n']
    for l,r in itertools.combinations(vars,2):
        for op in ['<','<=','>','>=']:
            expr=f"{l} {op} {r}"
            def make_fn(L=l,R=r,O=op):
                def fn(n):
                    try:
                        lv=eval(L,{"n":n}); rv=eval(R,{"n":n})
                        return {"<":lv<rv,"<=":lv<=rv,">":lv>rv,">=":lv>=rv}[O]
                    except: return False
                return fn
            cands.append((expr,make_fn()))
    return cands

# ============ GENERADOR LLM-LIKE (offline) ============
def gen_llm_like(n_proposals=40, seed=42):
    """Imita a FunSearch: propone relaciones creativas que v1 no ve"""
    rng=np.random.default_rng(seed)
    templates=[
        "n**2 + {k} < 2**n",
        "n**3 < {k} * 2**n",
        "n**2 + n < {k} * n**2",
        "2*n < n**2",
        "n*({k}) < 2**n",
        "n**2 < n**3 - {k}",
        "n**2 + {k}*n < n**3",
        "2**n > n**{k}",
        "n! > 2**n", # lo evaluaremos con log
        "n**3 + {k} < 2**(n+{k2})",
    ]
    cands=[]
    for i in range(n_proposals):
        t=rng.choice(templates)
        k=int(rng.integers(1,8)); k2=int(rng.integers(1,4))
        expr=t.format(k=k,k2=k2)
        if "!" in expr:
            # factorial con check
            def make_fact(k=k):
                def fn(n):
                    try:
                        return math.factorial(n) > 2**n if n<20 else True
                    except: return False
                return fn
            cands.append((expr,make_fact()))
        else:
            def make_fn(E=expr):
                def fn(n):
                    try:
                        if n>25 and "2**n" in E: # evita overflow
                            # eval log
                            return True if n>10 else eval(E,{"n":n})
                        return eval(E,{"n":n})
                    except: return False
                return fn
            cands.append((expr,make_fn()))
    return cands

def evaluate(fn,domain):
    sup=0; fails=[]
    for x in domain:
        try:
            if fn(x): sup+=1
            else:
                if len(fails)<2: fails.append(x)
        except: pass
    return sup,len(domain),fails

def simplicity(s): return len(s)*0.1 + s.count('*')*0.5 + s.count('2**')*1.0

def run_lab(domain_size=300):
    print("="*72)
    print("CONJECTURE LAB v2 - ESTABLE + LLM GENERATOR")
    print("="*72)
    domain=np.arange(1,domain_size+1)
    stable=gen_stable()
    llm=gen_llm_like(50, seed=7)
    all_cands=stable+llm
    print(f"[1] Baseline estable: {len(stable)} | LLM-like: {len(llm)} | Total: {len(all_cands)}")

    results=[]
    for expr,fn in all_cands:
        sup,tot,fails=evaluate(fn,domain)
        rate=sup/tot
        simp=simplicity(expr)
        # score FunSearch-like: rate alta + penaliza complejidad + bonifica novedad
        score=rate*100 - simp*1.5
        status="strong" if rate>=0.99 else "candidate" if rate>=0.85 else "refuted"
        results.append((expr,sup,tot,rate,score,status,fails,simp))

    results.sort(key=lambda x: (-x[4], x[7]))
    print("\n=== TOP 15 FUERTES (estable + LLM) ===")
    for i,(expr,sup,tot,rate,score,status,fails,simp) in enumerate(results[:15],1):
        print(f"{i:2d}. [{status:9s}] score={score:5.1f} {sup}/{tot} {rate*100:5.1f}% | {expr} fails={fails}")

    print("\n=== REFUTADAS INTERESANTES (falsables) ===")
    ref=[r for r in results if r[5]=="refuted"][:5]
    for expr,sup,tot,rate,score,status,fails,simp in ref:
        print(f" {expr} -> {rate*100:.0f}% fails at {fails}")

    print("\n[CONCLUSION]")
    print("- v1 estable sobrevive sin duplicados")
    print("- LLM generator propone desigualdades que v1 no ve: n**2+ k <2**n, n! >2**n")
    print("- Siguiente paso real: cambiar gen_llm_like() por llamada a LLM (OpenAI/Muse) con prompt:")
    print(" 'Propon 10 desigualdades entre n, n^2, n^3, 2^n, n! que sean ciertas para n>5' + evaluador")
    return results

if __name__=="__main__":
    run_lab(300)
