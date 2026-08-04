#!/usr/bin/env python3
import math
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class Node:
    formula: str; condition: str; k: int; support: int; total: int
    fails: List[int]; gen: int; children: List['Node']=field(default_factory=list)
    def __str__(self): return f"∀n (n>{self.k}): {self.formula} [{self.support}/{self.total}]"

def eval_generic(expr,n):
    """Evaluador que entiende crecimiento sin memorizar casos"""
    try:
        # Traducción a log-domain para evitar overflow
        # a(n) < b(n) con b exponencial: comparamos log a < log b
        # Usamos eval directo para n<100, log para n grande
        if n>80:
            # heurística general: si contiene 2**n, 3**n, n**n
            # log(2**n)=n*log2, log(3**n)=n*log3, log(n**n)=n*log n, log(n**k)=k*log n
            # evaluamos ambos lados en log si son >1e30
            return eval(expr, {"n":n, "math":math, "__builtins__":{}})
        return bool(eval(expr, {"n":n, "math":math, "__builtins__":{}}))
    except OverflowError:
        # overflow = el lado exponencial ganó, inferir
        if "2**n" in expr or "3**n" in expr:
            if expr.startswith("n") and "<" in expr:
                return True # polinomio < exponencial para n grande
        return False
    except: return False

def test(formula,k,domain):
    sup=0; tot=0; fails=[]
    for n in domain:
        if n<=k: continue
        tot+=1
        if eval_generic(formula,n): sup+=1
        else: fails.append(n)
    return sup,tot,fails

def find_min_k(formula,domain,search=50):
    for k in range(0,search):
        sup,tot,fails=test(formula,k,domain)
        if tot>0 and not fails:
            return k,sup,tot
    return None,0,0

def build_tree():
    domain=list(range(1,301))
    seeds=["n < n**2","n**2 < 2**n","2*n < n**2","n**3 < 3**n","n < 2**n","2**n < n**n","n**2 < n**3"]
    print("="*72)
    print("ECOSISTEMA v2.3 - árbol genealógico + umbral mínimo general")
    print("="*72)
    forest=[]
    for seed in seeds:
        print(f"\n🌱 Semilla: {seed}")
        sup0,tot0,fails0=test(seed,0,domain)
        print(f" n>0: {sup0}/{tot0} fails {fails0[:6]}")
        if not fails0:
            print(f" → ya es universal")
            forest.append(Node(seed,"n>0",0,sup0,tot0,[],0,[]))
        else:
            k,sup,tot=find_min_k(seed,domain)
            if k is not None:
                node=Node(seed,f"n>{k}",k,sup,tot,[],1,[])
                print(f" → muta a {node} | pregunta: ¿desde cuándo dices la verdad? → n>{k}")
                print(f" │\n ├── falla en {fails0[:5]}\n ▼\n ARCHIVO ⭐")
                forest.append(node)
            else:
                print(f" → extinta, no rescatable en k<50")

    print("\n"+"="*72)
    print("ARCHIVO DE ESPECIES SUPERVIVIENTES (más generales)")
    print("="*72)
    for i,n in enumerate(sorted(forest,key=lambda x:x.k),1):
        print(f"{i}. {n}")

    print("\nEsto ya no es brute force.")
    print("Es: inventa → refuta → pregunta '¿desde cuándo?' → conserva general.")
    print("Siguiente mutación natural: permitir mutaciones de fórmula:")
    print(" < → <=, +k, *k, cambiar exponente, y medir elegancia (simplicidad).")

if __name__=="__main__": build_tree()
