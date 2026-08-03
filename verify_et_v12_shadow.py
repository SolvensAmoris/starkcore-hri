import random
random.seed(0)
N=70

def make_world(seed):
    random.seed(seed)
    edges=set()
    while len(edges)<N*2:
        a=random.randrange(N); b=random.randrange(N)
        if a!=b: edges.add((min(a,b),max(a,b)))
    return list(edges)

def evolve(edges, steps, seed_evo):
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
            while len(adj2[i])>8:
                worst=min(adj2[i], key=lambda nb: len(adj2[i]&adj2[nb]))
                new.discard((min(i,worst),max(i,worst)))
                adj2[i].discard(worst); adj2[worst].discard(i)
        edges=list(new)
    return edges

def response_fingerprint(edges, trials=20):
    # F(G) = curva de colapso ante eliminacion progresiva
    import collections
    def diameter(edges_cur):
        adj={i:set() for i in range(N)}
        for a,b in edges_cur: adj[a].add(b); adj[b].add(a)
        # bfs desde 0 sample
        seen=set([0]); q=collections.deque([(0,0)]); maxd=0
        while q:
            u,d=q.popleft(); maxd=max(maxd,d)
            for v in adj[u]:
                if v not in seen:
                    seen.add(v); q.append((v,d+1))
        # tamano componente
        return maxd, len(seen)

    fingerprint=[]
    random.seed(99)
    for _ in range(trials):
        cur=list(edges)
        for k in range(6):
            d,s=diameter(cur)
            fingerprint.append((d,s))
            if not cur: break
            # ataca arista con mayor overlap (quitar lo redundante duele menos)
            cur.pop(random.randrange(len(cur)))
    return fingerprint

# Clonacion
G0_A=make_world(100)
G0_B=make_world(999) # origen distinto

Gt_A=evolve(G0_A, 100, 11)
Gt_B=evolve(G0_B, 100, 11) # misma evolucion, distinto origen

Gt_A2=evolve(G0_A, 100, 77) # mismo origen, evolucion distinta

print("ET v1.2 SOMBRA DEL ORIGEN")
print(f"G0_A {len(G0_A)} vs G0_B {len(G0_B)} Jaccard origen: {len(set(G0_A)&set(G0_B))/len(set(G0_A)|set(G0_B)):.3f}")
print(f"Gt_A {len(Gt_A)} Gt_B {len(Gt_B)} Jaccard tras evolucion: {len(set(Gt_A)&set(Gt_B))/len(set(Gt_A)|set(Gt_B)):.3f}")

Fa=response_fingerprint(Gt_A)
Fb=response_fingerprint(Gt_B)
Fa2=response_fingerprint(Gt_A2)

def dist_fp(F1,F2):
    return sum(abs(a[0]-b[0])+abs(a[1]-b[1])*0.1 for a,b in zip(F1,F2))/len(F1)

d_AB=dist_fp(Fa,Fb)
d_AA2=dist_fp(Fa,Fa2)
print(f"\nDistancia huella respuesta:")
print(f" Mismo origen, distinta evolucion (A vs A2): {d_AA2:.3f}")
print(f" Distinto origen, misma evolucion (A vs B): {d_AB:.3f}")

if d_AA2 < d_AB*0.7:
    print("\n-> SOMBRA ENCONTRADA: identidad = historia, no forma")
    print(" Dos universos con mismo pasado responden igual al romperse,")
    print(" aunque ya no se parezcan en aristas.")
else:
    print("\n-> identidad borrada por evolucion")

# Invariante
import collections
def degree_hist(edges):
    c=collections.Counter()
    for a,b in edges: c[a]+=1; c[b]+=1
    return sorted(c.values())

print(f"\nGrado medio Gt_A {sum(degree_hist(Gt_A))/N:.2f} vs Gt_B {sum(degree_hist(Gt_B))/N:.2f}")
print("V1.2 DONE - identidad como funcion de respuesta, no como lista de partes")
