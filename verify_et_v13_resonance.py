import random, collections
random.seed(0)
N=70

def make_world(seed):
    random.seed(seed)
    edges=set()
    while len(edges)<N*2:
        a=random.randrange(N); b=random.randrange(N)
        if a!=b: edges.add((min(a,b),max(a,b)))
    return list(edges)

def evolve(edges, steps, seed_evo, max_deg):
    random.seed(seed_evo)
    edges=list(edges)
    for _ in range(steps):
        adj={i:set() for i in range(N)}
        for a,b in edges: adj[a].add(b); adj[b].add(a)
        new=set(edges)
        for i in range(N):
            neigh=list(adj[i])
            if len(neigh)>=2 and random.random()<0.4:
                a,b=random.sample(neigh,2)
                if len(adj[a]&adj[b])==1 and random.random()<0.1:
                    new.add((min(a,b),max(a,b)))
        for a,b in list(new):
            if len(adj[a]&adj[b])>3 and random.random()<0.5:
                new.discard((a,b))
        adj2={i:set() for i in range(N)}
        for a,b in new: adj2[a].add(b); adj2[b].add(a)
        for i in range(N):
            while len(adj2[i])>max_deg: # <-- RESTRICCION variable
                worst=min(adj2[i], key=lambda nb: len(adj2[i]&adj2[nb]))
                new.discard((min(i,worst),max(i,worst)))
                adj2[i].discard(worst); adj2[worst].discard(i)
        edges=list(new)
    return edges

def resonance_fingerprint(edges, n_hits=15):
    # golpea nodo random con energia y ve como se propaga
    adj={i:set() for i in range(N)}
    for a,b in edges: adj[a].add(b); adj[b].add(a)
    signature=[]
    for hit in range(n_hits):
        energy={i:0.0 for i in range(N)}
        target=random.randrange(N)
        energy[target]=1.0
        curve=[]
        for t in range(10): # propagacion
            new_e={}
            for i in range(N):
                if energy[i]>0.01:
                    for nb in adj[i]:
                        new_e[nb]=new_e.get(nb,0)+energy[i]*0.25
            for i in new_e:
                energy[i]=energy[i]*0.7 + new_e[i]
            curve.append(sum(energy.values()))
        # features: pico, tiempo al pico, decaimiento
        peak=max(curve) if curve else 0
        t_peak=curve.index(peak) if curve else 0
        decay=curve[-1]/(peak+1e-9)
        signature.extend([peak,t_peak,decay])
    return signature

print("ET v1.3 RESONANCIA - Prueba del gemelo")
G0_A=make_world(100)
G0_B=make_world(999)

# Experimento 1: mismo origen, leyes distintas (max_deg)
Gt_sameOrigin_diffLaw1=evolve(G0_A, 100, 11, max_deg=6)
Gt_sameOrigin_diffLaw2=evolve(G0_A, 100, 11, max_deg=12)

# Experimento 2: distinto origen, mismas leyes
Gt_diffOrigin_sameLaw_A=evolve(G0_A, 100, 11, max_deg=8)
Gt_diffOrigin_sameLaw_B=evolve(G0_B, 100, 11, max_deg=8)

def dist(a,b):
    return sum(abs(x-y) for x,y in zip(a,b))/len(a)

Fa1=resonance_fingerprint(Gt_sameOrigin_diffLaw1)
Fa2=resonance_fingerprint(Gt_sameOrigin_diffLaw2)
FbA=resonance_fingerprint(Gt_diffOrigin_sameLaw_A)
FbB=resonance_fingerprint(Gt_diffOrigin_sameLaw_B)

d_sameOrigin = dist(Fa1,Fa2)
d_sameLaw = dist(FbA,FbB)

print(f"Distancia resonancia:")
print(f" Mismo origen, leyes distintas (6 vs 12): {d_sameOrigin:.3f}")
print(f" Distinto origen, mismas leyes (8 vs 8): {d_sameLaw:.3f}")

if d_sameLaw < d_sameOrigin:
    print("\n-> LEYES > ORIGEN: la identidad viene de las restricciones, no del nacimiento")
    print(" Igual que biologia: mismo ADN en distinto ambiente = diferente")
else:
    print("\n-> ORIGEN > LEYES: la historia inicial sobrevive a leyes distintas")
    print(" Sombra del nacimiento resiste")

print(f"\nFirma A (ley 6): pico medio {sum(Fa1[0::3])/len(Fa1[0::3]):.2f}")
print(f"Firma B (ley 12): pico medio {sum(Fa2[0::3])/len(Fa2[0::3]):.2f}")
print("\nEsto ya es Identidad = Estado + Historia + Restricciones, medido.")
print("V1.3 DONE")
