import random
N=80
random.seed(1337)
pos=[random.random() for _ in range(N)]
edges=set()

def step(pos, thr=0.08):
    global edges
    edges=set()
    for i in range(N):
        for j in range(i+1,N):
            d=min(abs(pos[i]-pos[j]),1-abs(pos[i]-pos[j]))
            if d < thr + random.uniform(-0.02,0.02):
                edges.add((i,j))
    new_pos=pos[:]
    adj={k:[] for k in range(N)}
    for a,b in edges:
        adj[a].append(b)
        adj[b].append(a)
    for i in range(N):
        neigh=adj[i]
        if not neigh: continue
        avg=sum(pos[j] for j in neigh)/len(neigh)
        diff=(avg-pos[i]+0.5)%1-0.5
        new_pos[i]=(pos[i]+0.05*diff)%1
    return new_pos

for t in range(30):
    pos=step(pos)

deg=[0]*N
for a,b in edges: deg[a]+=1; deg[b]+=1
print(f"edges={len(edges)} mean_deg={sum(deg)/N:.2f}")
adj={i:set() for i in range(N)}
for a,b in edges: adj[a].add(b); adj[b].add(a)
tri=0
for i in range(N):
    for j in adj[i]:
        if j>i:
            tri+=len(adj[i]&adj[j])
tri//=3
print(f"triangulos={tri} (0=random, >0=geometria local)")
print(f"¿espacio emergio? {'SI' if tri>20 and len(edges)>100 else 'aún no'}")
print("\nV0.1 DONE - red -> geometria")
