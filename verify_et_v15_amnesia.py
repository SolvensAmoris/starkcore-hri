import random, math
from collections import defaultdict
N=70

def evolve(steps, max_deg, seed_evo, p_tri, prune_thr):
    random.seed(seed_evo)
    edges=set() # amnesia total
    for _ in range(steps):
        adj={i:set() for i in range(N)}
        for a,b in edges: adj[a].add(b); adj[b].add(a)
        new=set(edges)
        for i in range(N):
            if random.random()<0.15:
                a=random.randrange(N); b=random.randrange(N)
                if a!=b: new.add((min(a,b),max(a,b)))
            neigh=list(adj[i])
            if len(neigh)>=2 and random.random()<p_tri:
                a,b=random.sample(neigh,2)
                if len(adj[a]&adj[b])==max(0,prune_thr-2):
                    new.add((min(a,b),max(a,b)))
        for a,b in list(new):
            if len(adj[a]&adj[b])>prune_thr and random.random()<0.6:
                new.discard((a,b))
        adj2={i:set() for i in range(N)}
        for a,b in new: adj2[a].add(b); adj2[b].add(a)
        for i in range(N):
            while len(adj2[i])>max_deg:
                worst=min(adj2[i], key=lambda nb: len(adj2[i]&adj2[nb]))
                new.discard((min(i,worst),max(i,worst)))
                adj2[i].discard(worst); adj2[worst].discard(i)
        edges=new
    return list(edges)

def fingerprint(edges, seed=0, n_hits=30):
    random.seed(seed) # fija para reproducibilidad
    adj={i:set() for i in range(N)}
    for a,b in edges: adj[a].add(b); adj[b].add(a)
    curves=[]
    for _ in range(n_hits):
        target=random.randrange(N)
        energy={i:0.0 for i in range(N)}
        energy[target]=1.0
        curve=[]
        for t in range(15):
            new_e=defaultdict(float)
            for i in range(N):
                if energy[i]>1e-5:
                    for nb in adj[i]: new_e[nb]+=energy[i]*0.25
            for i in new_e: energy[i]=energy[i]*0.6 + new_e[i]
            tot=sum(energy.values()) or 1
            probs=[v/tot for v in energy.values() if v>1e-6]
            ent=-sum(p*math.log(p+1e-12) for p in probs)
            curve.append(ent)
        m=max(curve) or 1
        curves.append([c/m for c in curve])
    return [sum(c[t] for c in curves)/len(curves) for t in range(15)]

def dist(a,b): return sum(abs(x-y) for x,y in zip(a,b))/len(a)

# test amnesia + identidad
for law in [(6,0.5,1),(12,0.1,5)]:
    max_deg,p_tri,thr=law
    G1=evolve(120,max_deg,1,p_tri,thr)
    G2=evolve(120,max_deg,999,p_tri,thr)
    print(f"Ley {law} intra-dist {dist(fingerprint(G1),fingerprint(G2)):.4f} edges {len(G1)}/{len(G2)}")

G6=evolve(120,6,1,0.5,1)
G12=evolve(120,12,1,0.1,5)
print(f"\nInter 6 vs 12 dist {dist(fingerprint(G6),fingerprint(G12)):.4f}")
print("-> LEY CREA IDENTIDAD si ratio inter/intra >3")
