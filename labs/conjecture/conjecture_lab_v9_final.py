#!/usr/bin/env python3
import math, random
from collections import defaultdict
import numpy as np

def eval_safe(e,n):
    try: return bool(eval(e, {"n":n,"math":math,"__builtins__":{}}))
    except: return False

def fails_of(f,domain): return set(n for n in domain if not eval_safe(f,n))

def kmin_of(f,domain):
    for k in range(0,60):
        if not any(n>k and not eval_safe(f,n) for n in domain): return k
    return 60

def landscape_bar(fails,m=30):
    return "".join("█" if n in fails else "░" for n in range(1,m+1))

# OPERADORES = GENES
OPERATORS = [
    ("< → <=", lambda f: f.replace("<","<=",1) if "<" in f and "<=" not in f else None),
    ("2**n → 3**n", lambda f: f.replace("2**n","3**n") if "2**n" in f else None),
    ("2**n → 2*2**n", lambda f: f.replace("2**n","2*2**n") if "2**n" in f else None),
    ("n**2 → n**2//2", lambda f: f.replace("n**2","n**2//2") if "n**2" in f else None),
    ("n**2 → n*log", lambda f: f.replace("n**2","n*math.log(n+2)") if "n**2" in f else None),
]

mem = {name:{"usos":0,"exitos":0} for name,_ in OPERATORS}

def surgery_search(formula, fails, domain):
    best=[]
    for name,mut in OPERATORS:
        mem[name]["usos"]+=1
        cand = mut(formula)
        if not cand or cand==formula: continue
        nfails = fails_of(cand,domain)
        if len(nfails) < len(fails):
            mem[name]["exitos"]+=1
            best.append((cand, nfails, name))
    return sorted(best, key=lambda x: len(x[1]))

def print_tree(root, domain, depth=0, maxd=3):
    fails=fails_of(root,domain)
    prefix=" "*depth + ("├── " if depth>0 else "🌱 ")
    print(f"{prefix}{root} {landscape_bar(fails,20)} {sorted(fails)[:3]}")
    if depth>=maxd: return
    children=surgery_search(root, fails, domain)[:2]
    for cand, nfails, opname in children:
        print(f"{' '*depth} │ └─[{opname}]")
        print_tree(cand, domain, depth+1, maxd)

def run():
    domain=list(range(1,50))
    print("╔════════════════════════════════════════════════════════════╗")
    print("🧪 STARKCORE v9 - OPERADORES COMO GENES 🧬")
    print("╚════════════════════════════════════════════════════════════╝")

    f="n**2 < 2**n"
    fails=fails_of(f,domain)
    print(f"\n🔴 CIRUGÍA CORREGIDA (solo reduce paisaje)")
    print(f"🦠 Paciente: {f} fails={sorted(fails)} {landscape_bar(fails,30)}")
    for cand,nfails,op in surgery_search(f,fails,domain):
        red=(len(fails)-len(nfails))/len(fails)*100
        print(f" 🔪 {op}: → {cand} | {sorted(fails)}→{sorted(nfails)} -{red:.0f}%")

    print(f"\n🟢 ÁRBOL FILOGENÉTICO")
    print_tree("n**2 < 2**n", domain, maxd=3)

    print(f"\n🔵 PAISAJE 2D ENCOGIÉNDOSE")
    history=[]; cur="n**2 < 2**n"; cf=fails_of(cur,domain); history.append((cur,cf))
    for _ in range(4):
        nxt=surgery_search(cur,cf,domain)
        if not nxt: break
        cur,cf,_=nxt[0]; history.append((cur,cf))
    print("n→")
    for i,(ff,fl) in enumerate(history):
        print(f"{i} {landscape_bar(fl,40)} {ff}")

    print(f"\n🟣 MEMORIA DE OPERADORES")
    print(f"{'Mutación':<15} {'Usos':<5} {'Éxitos':<6} P(éxito)")
    for name,d in sorted(mem.items(), key=lambda x: -x[1]['exitos']/max(1,x[1]['usos'])):
        p=d["exitos"]/max(1,d["usos"])
        print(f"{name:<15} {d['usos']:<5} {d['exitos']:<6} {p:.2f}")

    print(f"\n🟡 NICHOS EMERGENTES (k-means sobre [k_min,size,max,growth])")
    seeds=["n < n**2","2*n < n**2","n**2 < 2**n","n**3 < 3**n"]
    vecs=[]
    for s in seeds:
        fl=fails_of(s,domain); k=kmin_of(s,domain)
        growth=2 if "2**n" in s or "3**n" in s else 0
        vecs.append(np.array([k,len(fl),max(fl) if fl else 0,growth],float))
    # k-means k=2
    vecs_np=np.array(vecs); c1,c2=vecs_np[0],vecs_np[2]
    for _ in range(5):
        g1=[v for v in vecs if np.linalg.norm(v-c1)<np.linalg.norm(v-c2)]
        g2=[v for v in vecs if v not in g1]
        if g1: c1=np.mean(g1,axis=0)
        if g2: c2=np.mean(g2,axis=0)
    for s,v in zip(seeds,vecs):
        cl=0 if np.linalg.norm(v-c1)<np.linalg.norm(v-c2) else 1
        print(f" Ecosistema {cl} ({'EXP' if cl==0 else 'POLY'}): {s} vec={v}")

    print(f"\n> 🌄 Las conjeturas viven sobre un paisaje de errores.")
    print(f"> v9: Evolucionan Φ: conjetura → mejor conjetura. Genes=operadores")

if __name__=="__main__": run()
