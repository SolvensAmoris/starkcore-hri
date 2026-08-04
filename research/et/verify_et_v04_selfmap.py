import random, math, collections
random.seed(1337)
N=80
pos_true=[random.random() for _ in range(N)]
edges=set()

def step(pos, thr=0.08):
    global edges
    edges=set()
    for i in range(N):
        for j in range(i+1,N):
            d=min(abs(pos[i]-pos[j]),1-abs(pos[i]-pos[j]))
            if d < thr + random.uniform(-0.02,0.02):
                edges.add((i,j))
    adj={k:[] for k in range(N)}
    for a,b in edges: adj[a].append(b); adj[b].append(a)
    new=list(pos)
    for i in range(N):
        if not adj[i]: continue
        avg=sum(pos[j] for j in adj[i])/len(adj[i])
        diff=(avg-pos[i]+0.5)%1-0.5
        new[i]=(pos[i]+0.05*diff)%1
    return new

for _ in range(30): pos_true=step(pos_true)
edges_final=list(edges)

# OLVIDAMOS pos_true, solo grafo
adj={i:set() for i in range(N)}
for a,b in edges_final:
    adj[a].add(b); adj[b].add(a)

# 1) matriz distancias grafo (Floyd via BFS)
dist=[[0]*N for _ in range(N)]
for s in range(N):
    d={s:0}; q=collections.deque([s])
    while q:
        u=q.popleft()
        for v in adj[u]:
            if v not in d:
                d[v]=d[u]+1; q.append(v)
    for t in range(N):
        dist[s][t]=d.get(t, N)

# 2) MDS 1D clasico: coloca nodos para minimizar stress
# inicial random en [0,1)
random.seed(0)
pos_rec=[random.random() for _ in range(N)]
# gradient descent simple sobre stress = sum ( |rec_i-rec_j|_circ - dist_ij )^2 ponderado
for it in range(300):
    for i in range(N):
        grad=0.0
        for j in range(N):
            if i==j: continue
            dij=dist[i][j]
            if dij>=N: continue
            # distancia circular en rec
            diff=(pos_rec[i]-pos_rec[j]+0.5)%1-0.5
            drec=abs(diff)
            # target proporcional: queremos drec ~ dij / diam * 0.5
            # normaliza
            target=dij/12.0 # diam~9, escala 0.75
            if drec<1e-9: continue
            grad+=2*(drec-target)*(1 if diff>0 else -1)
        pos_rec[i]=(pos_rec[i]-0.001*grad)%1

# 3) correlacion circular entre pos_true y pos_rec (procrustes 1D)
# probamos rotacion + flip que maximiza correlacion
best=-1; best_shift=0; best_flip=False
for flip in [False, True]:
    rec2=[1-x if flip else x for x in pos_rec]
    for shift in [k/20 for k in range(20)]:
        # correlacion como coseno de diferencia angular
        s=0
        for a,b in zip(pos_true, rec2):
            diff = (a - (b+shift)%1 +0.5)%1-0.5
            s+=math.cos(2*math.pi*diff)
        corr=s/N
        if corr>best:
            best=corr; best_shift=shift; best_flip=flip

print(f"ET v0.4 self-map")
print(f"Correlacion reconstruccion vs verdad: {best:.3f}")
print(f" (1.0=perfecta, 0=random, flip={best_flip} shift={best_shift:.2f})")
if best>0.7:
    print("-> GEOMETRIA SOBREVIVIO en relaciones")
elif best>0.4:
    print("-> huella parcial")
else:
    print("-> perdida")

# test control: MDS sobre grafo aleatorio deberia dar ~0
print("\nV0.4 DONE - espacio como memoria relacional")
