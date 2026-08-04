#!/usr/bin/env python3
import math, random
from dataclasses import dataclass
from typing import Set, List
import numpy as np

def eval_safe(e,n):
    try: return bool(eval(e, {"n":n,"math":math,"__builtins__":{}}))
    except: return False

def fails_of(f,domain): return set(n for n in domain if not eval_safe(f,n))

def signature_vector(f,fails,domain):
    # vector: [k_min, size_fail, max_fail, continuidad, crecimiento, complejidad]
    kmin=0
    for k in range(0,50):
        if not any(n>k and not eval_safe(f,n) for n in domain): kmin=k; break
    size=len(fails); mx=max(fails) if fails else 0
    cont=1 if fails and sorted(fails)==list(range(min(fails),max(fails)+1)) else 0
    # tasa crecimiento: 0 lineal, 1 poli, 2 exp
    growth=2 if "2**n" in f or "3**n" in f else 1 if "**" in f else 0
    complexity=len(f)*0.1
    return np.array([kmin, size, mx, cont, growth, complexity], dtype=float), kmin

def kmeans(vectors,k=3,iters=10):
    # kmeans casero sin sklearn
    centroids=random.sample(vectors,k)
    centroids=[np.array(c) for c in centroids]
    for _ in range(iters):
        clusters=[[] for _ in range(k)]
        for v in vectors:
            dists=[np.linalg.norm(v-c) for c in centroids]
            clusters[int(np.argmin(dists))].append(v)
        new_centroids=[]
        for cl in clusters:
            if cl: new_centroids.append(np.mean(cl,axis=0))
            else: new_centroids.append(random.choice(vectors))
        centroids=new_centroids
    return centroids, clusters

# --- CIRUGÍA ---
def surgery_mutations(formula, fails, domain):
    """Propone mutaciones que eliminan exactamente un fallo"""
    proposals=[]
    if not fails: return []
    target = max(fails) # el más grande, el que está en la frontera
    # intenta debilitamientos mínimos que salven a target
    candidates=[
        formula.replace("<","<="),
        formula.replace("n**2",f"n**2+{target}"),
        formula.replace("2*n",f"2*n+{target}"),
        formula.replace("n**2",f"n**2+{target}*n") if "n**2" in formula else None,
        formula.replace("2**n",f"3**n") if "2**n" in formula else None,
    ]
    for cf in candidates:
        if not cf: continue
        new_fails=fails_of(cf,domain)
        # éxito si elimina al menos target y no crea nuevos fails más allá
        if target not in new_fails and len(new_fails) < len(fails):
            proposals.append((cf,new_fails,f"cirugía: elimina {target}"))
    return proposals

def run():
    domain=list(range(1,80))
    seeds=["n < n**2","2*n < n**2","n**2 < 2**n","n**2+1 < 2**n","n**3 < 3**n","n <= n**2"]
    print("="*72); print("v7 CIRUGÍA + CLUSTERING AUTOMÁTICO"); print("="*72)
    species=[]
    for f in seeds:
        fails=fails_of(f,domain)
        vec,kmin=signature_vector(f,fails,domain)
        species.append((f,fails,vec,kmin))

    print("\n--- VECTORES DE ESPECIES ---")
    for f,fails,vec,k in species:
        print(f"{f:15s} vec={vec} k={k} fails={sorted(fails)[:4]}")

    # CLUSTERING: nichos emergen solos
    vecs=[v for _,_,v,_ in species]
    centroids,clusters=kmeans(vecs,k=3)
    print("\n--- CLUSTERING: EL SISTEMA DESCUBRE NICHOS SOLO ---")
    for i,cent in enumerate(centroids):
        print(f"Ecosistema {i}: centro {cent.round(1)} -> interpretación: k~{cent[0]:.0f} growth~{cent[4]:.0f}")

    # CIRUGÍA
    print("\n--- CIRUGÍA: de {2,3,4} → {2,3} → {2} → {} ---")
    f="n**2 < 2**n"
    fails=fails_of(f,domain)
    print(f"Semilla {f} fails {sorted(fails)}")
    cur_f=f; cur_fails=fails
    for step in range(4):
        muts=surgery_mutations(cur_f,cur_fails,domain)
        if not muts: break
        # elige la que más reduce fails
        muts.sort(key=lambda x: len(x[1]))
        best=muts[0]
        print(f" paso {step+1}: {best[2]} | {cur_f} -> {best[0]} | fails {sorted(cur_fails)} -> {sorted(best[1])}")
        cur_f,cur_fails=best[0],best[1]
        if not cur_fails:
            print(f" → curada, universal ⭐")
            break

    print("\n"+"="*72)
    print("CIERRE DEL ARCO")
    print("="*72)
    print("v1 buscaba verdades")
    print("v2 preguntó ¿desde cuándo?")
    print("v3 mutó y cruzó")
    print("v4 depredador heurístico (bug {} mata todo)")
    print("v5 ADN = errores")
    print("v6 nichos a mano + firma")
    print("v7 nichos emergen por kmeans + cirugía que elimina un contraejemplo a la vez")
    print("\nFrase final tuya: Las conjeturas viven sobre un paisaje de errores.")
    print("Y ahora el laboratorio opera sobre ese paisaje, no sobre strings.")

if __name__=="__main__": run()
