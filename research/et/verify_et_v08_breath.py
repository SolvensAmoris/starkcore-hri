import random, math, collections
random.seed(7)
N=120
# start random sparse
edges=set()
while len(edges)<N*2:
    a=random.randrange(N); b=random.randrange(N)
    if a!=b: edges.add((min(a,b),max(a,b)))
edges=list(edges)

def analyze(edges):
    adj={i:set() for i in range(N)}
    for a,b in edges: adj[a].add(b); adj[b].add(a)
    def bfs(s):
        d={s:0}; q=collections.deque([s])
        while q:
            u=q.popleft()
            for v in adj[u]:
                if v not in d:
                    d[v]=d[u]+1; q.append(v)
        return d
    # diam + hist dist
    all_dists=[]
    for i in range(0,N,10):
        d=bfs(i)
        all_dists.extend(d.values())
    cnt=collections.Counter(all_dists)
    diam=max(cnt.keys()) if cnt else 0
    tri=0
    for i in range(N):
        for j in adj[i]:
            if j>i: tri+=len(adj[i]&adj[j])
    tri//=3
    # entropia distancias
    tot=sum(cnt.values())
    ent=-sum((c/tot)*math.log(c/tot+1e-9) for c in cnt.values())
    return diam, tri, cnt, ent

# v0.8: respiracion
for step in range(80):
    adj={i:set() for i in range(N)}
    for a,b in edges: adj[a].add(b); adj[b].add(a)
    new_edges=set(edges)

    # 1) atraccion: triadic closure débil, solo si no muy redundante
    for i in range(N):
        neigh=list(adj[i])
        if len(neigh)<2: continue
        for _ in range(2): # intentos limitados
            a,b=random.sample(neigh,2)
            if (min(a,b),max(a,b)) in new_edges: continue
            overlap=len(adj[a]&adj[b])
            if overlap==1 and random.random()<0.08: # solo si justo 1 en comun, no mas
                new_edges.add((min(a,b),max(a,b)))

    # 2) repulsion: si dos nodos comparten >3 vecinos, son demasiado redundantes, corta uno
    # esto es la anti-gravedad local
    for a,b in list(new_edges):
        if a>=N or b>=N: continue
        # recalcula adj rapido
        # usa adj anterior approx
        if len(adj[a]&adj[b])>3 and random.random()<0.5:
            new_edges.discard((a,b))

    # 3) homeostasis + long range decay: si grado>8 corta el de menor overlap
    adj2={i:set() for i in range(N)}
    for a,b in new_edges: adj2[a].add(b); adj2[b].add(a)
    for i in range(N):
        while len(adj2[i])>8:
            worst=min(adj2[i], key=lambda nb: len(adj2[i]&adj2[nb]))
            new_edges.discard((min(i,worst),max(i,worst)))
            adj2[i].discard(worst)
            adj2[worst].discard(i)

    # 4) ruido: crea 1 arista random lejana por paso para mantener exploracion
    if random.random()<0.3:
        a=random.randrange(N); b=random.randrange(N)
        if a!=b: new_edges.add((min(a,b),max(a,b)))

    edges=list(new_edges)

diam, tri, cnt, ent = analyze(edges)
print(f"ET v0.8 BREATH - integracion vs separacion")
print(f"N={N} edges={len(edges)} diam={diam} tri={tri} ent_dist={ent:.2f}")
print(f"distrib dist: {dict(sorted(cnt.items())[:7])}")

# random control mismo M
random.seed(99)
rand_edges=set()
while len(rand_edges)<len(edges):
    a=random.randrange(N); b=random.randrange(N)
    if a!=b: rand_edges.add((min(a,b),max(a,b)))
diam_r, tri_r, cnt_r, ent_r = analyze(list(rand_edges))
print(f"\nRandom: diam={diam_r} tri={tri_r} ent={ent_r:.2f} dist={dict(sorted(cnt_r.items())[:7])}")

# criterio espacio sano: diam 3-8, ent media, tri moderado no 1000
if 3<=diam<=9 and 0.5<ent<2.0 and 50<tri<400:
    print("\n-> POSIBLE ESPACIO: barrios + distancia + no colapso")
else:
    print("\n-> aun no, pero mejor que v0.7" if diam>1 else "-> colapso otra vez")

