#!/usr/bin/env python3
import math, random
from collections import defaultdict
import numpy as np

def eval_safe(e,n):
    try: return bool(eval(e, {"n":n,"math":math,"__builtins__":{}}))
    except: return False
def fails_of(f,d): return set(x for x in d if not eval_safe(f,x))
def landscape_bar(fails,m=30): return "".join("█" if n in fails else "░" for n in range(1,m+1))
def kmin_of(f,d):
    for k in range(0,60):
        if not any(n>k and not eval_safe(f,n) for n in d): return k
    return 60

# === GENES BASE ===
BASE_OPS = {
    "WEAKEN_<": lambda f: f.replace("<","<=",1) if "<" in f and "<=" not in f else None,
    "EXP2->3": lambda f: f.replace("2**n","3**n") if "2**n" in f else None,
    "EXP2->2*EXP2": lambda f: f.replace("2**n","2*2**n") if "2**n" in f else None,
    "POLY//2": lambda f: f.replace("n**2","n**2//2") if "n**2" in f else None,
    "POLY->nlogn": lambda f: f.replace("n**2","n*math.log(n+2)") if "n**2" in f else None,
}

class Operator:
    def __init__(self, chain):
        self.chain = chain # lista de nombres de BASE_OPS ej ["WEAKEN_<","EXP2->3"]
        self.usos=0; self.exitos=0
    def apply(self,f):
        cur=f
        for name in self.chain:
            fn=BASE_OPS.get(name)
            if not fn: return None
            nxt=fn(cur)
            if not nxt: return None
            cur=nxt
        return cur
    def fitness(self): return self.exitos/max(1,self.usos)
    def __str__(self): return "→".join(self.chain)

def mutate_operator(op):
    # 3 mutaciones de operador: añadir gen, quitar gen, reemplazar gen
    new_chain = op.chain[:]
    choice = random.choice(["add","del","swap"])
    keys=list(BASE_OPS.keys())
    if choice=="add" and len(new_chain)<3:
        new_chain.append(random.choice(keys))
    elif choice=="del" and len(new_chain)>1:
        new_chain.pop(random.randrange(len(new_chain)))
    elif choice=="swap":
        if new_chain:
            new_chain[random.randrange(len(new_chain))]=random.choice(keys)
    return Operator(new_chain)

def run():
    domain=list(range(1,50))
    print("╔════════════════════════════════════════════════════════════╗")
    print("🧪 STARKCORE v10 - META: EL OPERADOR MUTA 🧬🧬")
    print("╚════════════════════════════════════════════════════════════╝")

    # Población inicial de operadores
    ops=[Operator([k]) for k in BASE_OPS.keys()]
    # conjeturas
    conjectures=["n**2 < 2**n","2*n < n**2","n < n**2"]

    print("\n🌱 GENES INICIALES")
    for op in ops: print(f" Φ {op}")

    # Evolución META
    history_ops=[]
    for gen in range(5):
        print(f"\n━━━ GENERACIÓN {gen} ━━━")
        # probar todos ops sobre todas conjeturas
        for conj in conjectures:
            fails=fails_of(conj,domain)
            for op in ops:
                op.usos+=1
                cand=op.apply(conj)
                if not cand or cand==conj: continue
                nfails=fails_of(cand,domain)
                if len(nfails)<len(fails):
                    op.exitos+=1
                    print(f" 🏥 {conj} {sorted(fails)[:3]} --[{op}]--> {cand} {sorted(nfails)[:3]} 🌄 -{len(fails)-len(nfails)}")

        # selección de operadores
        ops_sorted=sorted(ops, key=lambda o: -o.fitness())
        print(f"\n📊 FITNESS OPERADORES gen {gen}")
        for o in ops_sorted[:5]:
            print(f" Φ {str(o):<25} usos={o.usos} exitos={o.exitos} P={o.fitness():.2f}")
        # reproducir mejores, mutar
        survivors=ops_sorted[:3]
        children=[mutate_operator(random.choice(survivors)) for _ in range(3)]
        ops=survivors+children
        history_ops.append((gen, survivors[0]))

    print(f"\n🔬 ÁRBOL FILOGENÉTICO DE OPERADORES")
    for gen, op in history_ops:
        print(f" gen{gen}: Φ {op} P={op.fitness():.2f}")

    print(f"\n🌄 PAISAJE 2D - META CIRUGÍA")
    cur="n**2 < 2**n"; cur_f=fails_of(cur,domain)
    print(f"0 {landscape_bar(cur_f,40)} {cur}")
    for i in range(5):
        best=None; best_op=None
        for op in ops:
            cand=op.apply(cur)
            if not cand: continue
            nf=fails_of(cand,domain)
            if len(nf)<len(cur_f):
                if best is None or len(nf)<len(best[1]):
                    best=(cand,nf); best_op=op
        if not best: break
        cur,cur_f=best
        print(f"{i+1} {landscape_bar(cur_f,40)} {cur} vía Φ {best_op}")

    print(f"\n> 🌄 v10: Ya no evolucionan conjeturas. Evolucionan Φ que curan paisajes.")
    print(f"> Los genes son operadores. Los operadores también mutan. Meta-evolución.")

if __name__=="__main__": run()
