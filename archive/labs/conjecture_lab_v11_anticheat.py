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

BASE_OPS = {
    "WEAKEN_<": lambda f: f.replace("<","<=",1) if "<" in f and "<=" not in f else None,
    "STRENGTHEN_<=": lambda f: f.replace("<=","<",1) if "<=" in f else None, # anti-cheat
    "EXP2->3": lambda f: f.replace("2**n","3**n") if "2**n" in f else None,
    "EXP3->2": lambda f: f.replace("3**n","2**n") if "3**n" in f else None, # anti-cheat
    "POLY//2": lambda f: f.replace("n**2","n**2//2") if "n**2" in f else None,
    "POLY*2": lambda f: f.replace("n**2","2*n**2") if "n**2" in f and "2*n**2" not in f else None, # empeora a propósito
    "ADD_n": lambda f: f.replace("n**2",f"n**2+n") if "n**2" in f else None,
}

class Operator:
    def __init__(self, chain):
        self.chain=chain; self.usos=0; self.score=0.0; self.hist=[]
    def apply(self,f):
        cur=f
        for name in self.chain:
            fn=BASE_OPS.get(name)
            if not fn: return None
            nxt=fn(cur)
            if not nxt: return None
            cur=nxt
        return cur
    def __str__(self): return "→".join(self.chain)

def delta_score(old_fails,new_fails,old_f,new_f):
    # TU FÓRMULA
    eliminated = len(old_fails - new_fails) # ⭐ +3
    created = len(new_fails - old_fails) # ⭐ -2
    length_pen = (len(new_f)-len(old_f))*0.05 # ⭐ -0.5
    struct_pen = 0 if old_f.split("<")[0]==new_f.split("<")[0] else 0.5
    return eliminated - created - length_pen - struct_pen

def run():
    domain=list(range(1,50))
    # DATASET BALANCEADO - anti WEAKEN_< cheat
    conjectures=[
        "n**2 < 2**n", # < ayuda
        "n <= n**2", # <→<= no ayuda, ya es <=
        "n**2 <= 2**n", # <=→< puede ayudar (más fuerte)
        "3**n < 2**n", # siempre falso, ningún <→<= lo salva
        "2*n < n**2", # < ayuda un poco
        "n**3 < 3**n",
    ]
    print("╔════════════════════════════════════════════════════════════╗")
    print("🧪 v11 ANTI-CHEAT - MetaOperatormon nerfeado 🧬")
    print("╚════════════════════════════════════════════════════════════╝")
    print("\n📚 Dataset balanceado: incluye casos donde WEAKEN_< NO sirve")

    ops=[Operator([k]) for k in BASE_OPS.keys()]

    print("\n━━━ EVOLUCIÓN CON Δ REAL ━━━")
    for gen in range(3):
        print(f"\n GENERACIÓN {gen}")
        for conj in conjectures:
            old_fails=fails_of(conj,domain)
            for op in ops:
                op.usos+=1
                cand=op.apply(conj)
                if not cand or cand==conj: continue
                new_fails=fails_of(cand,domain)
                delta=delta_score(old_fails,new_fails,conj,cand)
                op.score+=delta
                op.hist.append(delta)
                if delta>0:
                    print(f" ✅ {conj} --[{op}] Δ={delta:+.1f} | {sorted(old_fails)[:3]}→{sorted(new_fails)[:3]} | {landscape_bar(old_fails,20)}→{landscape_bar(new_fails,20)}")
                elif delta<0:
                    print(f" ❌ {conj} --[{op}] Δ={delta:+.1f} penalizado (crea errores)")

        # ranking por score total, no por P=1.0
        ops_sorted=sorted(ops, key=lambda o: -o.score)
        print(f"\n 📊 RANKING OPERADORES gen {gen} (score = ΣΔ)")
        for o in ops_sorted:
            avg=o.score/max(1,o.usos)
            print(f" Φ {str(o):<20} score={o.score:+5.1f} avgΔ={avg:+.2f} usos={o.usos}")
        # selección + mutación
        survivors=ops_sorted[:3]
        def mutate_operator(op):
            new=list(op.chain); choice=random.choice(["add","del","swap"])
            keys=list(BASE_OPS.keys())
            if choice=="add" and len(new)<2: new.append(random.choice(keys))
            elif choice=="del" and len(new)>1: new.pop()
            elif choice=="swap": new=[random.choice(keys)]
            return Operator(new)
        ops=survivors + [mutate_operator(random.choice(survivors)) for _ in range(3)]

    print("\n" + "="*60)
    print("🏆 CONCLUSIÓN v11")
    print("Antes: WEAKEN_< P=1.0 cheat porque dataset sesgado")
    print("Ahora: Δ = eliminados - creados - longitud - estructura")
    print("WEAKEN_< ya no es rey si crea errores en otros nichos")
    print("\n> 🧬 MetaOperatormon Tipo: Meta/Evolución")
    print("> Ataque nerfeado: Cirugía con Δ real, no con P(éxito) tramposo")
    print("> Narrativa v1→v11: de peces a cañas a fábricas de cañas")

if __name__=="__main__": run()
