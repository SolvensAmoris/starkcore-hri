import random
random.seed(0)
N=70

def evolve_from_scratch(steps, max_deg, seed_evo):
    random.seed(seed_evo)
    edges=set() # amnesia total: empieza vacio, sin G0
    for _ in range(steps):
        # adj actual
        adj={i:set() for i in range(N)}
        for a,b in edges: adj[a].add(b); adj[b].add(a)
        new=set(edges)
        # regla creadora
        for i in range(N):
            if random.random()<0.15:
                a=random.randrange(N); b=random.randrange(N)
                if a!=b: new.add((min(a,b),max(a,b)))
            # triadic closure debil
            neigh=list(adj[i])
            if len(neigh)>=2 and random.random()<0.3:
                a,b=random.sample(neigh,2)
                if len(adj[a]&adj[b])==1:
                    new.add((min(a,b),max(a,b)))
        for a,b in list(new):
            if len(adj[a]&adj[b])>3 and random.random()<0.6:
                new.discard((a,b))
        adj2={i:set() for i in range(N)}
        for a,b in new: adj2[a].add(b); adj2[b].add(a)
        for i in range(N):
            while len(adj2[i])>max_deg:
                if not adj2[i]: break
                worst=min(adj2[i], key=lambda nb: len(adj2[i]&adj2[nb]))
                new.discard((min(i,worst),max(i,worst)))
                adj2[i].discard(worst); adj2[worst].discard(i)
        edges=new
    return list(edges)

def resonance_norm(edges, n_hits=20):
    adj={i:set() for i in range(N)}
    for a,b in edges: adj[a].add(b); adj[b].add(a)
    curves=[]
    for _ in range(n_hits):
        energy={i:0.0 for i in range(N)}
        target=random.randrange(N)
        energy[target]=1.0
        curve=[]
        for t in range(12):
            new_e={}
            for i in range(N):
                if energy[i]>0.001:
                    for nb in adj[i]:
                        new_e[nb]=new_e.get(nb,0)+energy[i]*0.22
            tot_before=sum(energy.values())
            for i in new_e:
                energy[i]=energy[i]*0.65 + new_e[i]
            tot=sum(energy.values()) or 1
            # normalizado: forma, no magnitud
            curve.append(tot/tot_before if tot_before>0 else 0)
        # normaliza curva a 1 en pico
        m=max(curve) if curve else 1
        curves.append([c/(m+1e-9) for c in curve])
    # promedio forma
    avg=[sum(c[t] for c in curves)/len(curves) for t in range(12)]
    return avg

print("ET v1.4 AMNESIA - regla sola, sin origen")
# 3 leyes, mismo vacio inicial, semillas de evolucion distintas
for max_deg in [6,8,12]:
    Gt1=evolve_from_scratch(120, max_deg, 1)
    Gt2=evolve_from_scratch(120, max_deg, 999)
    f1=resonance_norm(Gt1)
    f2=resonance_norm(Gt2)
    dist=sum(abs(a-b) for a,b in zip(f1,f2))/len(f1)
    print(f"\nLey max_deg={max_deg} | Gt1 {len(Gt1)} edges Gt2 {len(Gt2)} edges")
    print(f" Distancia forma normalizada entre 2 mundos misma ley, distinto ruido: {dist:.3f} (0=identico)")
    print(f" Curva promedio f1: {[f'{x:.2f}' for x in f1[:5]]}...")

# compara entre leyes
Gt6=evolve_from_scratch(120, 6, 1)
Gt12=evolve_from_scratch(120, 12, 1)
f6=resonance_norm(Gt6)
f12=resonance_norm(Gt12)
dist_laws=sum(abs(a-b) for a,b in zip(f6,f12))/len(f6)
print(f"\nDistancia entre leyes 6 vs 12 (misma semilla): {dist_laws:.3f}")

if dist_laws > 0.15:
    print("\n-> LEY CREA IDENTIDAD: desde cero, sin pasado, la restriccion inventa una forma de sonar")
    print(" Amnesia no es muerte. La dinamica reconstruye un yo.")
else:
    print("\n-> sin ley no hay yo")

print("\nV1.4 DONE - Identidad = Restricciones que permiten resonar")
