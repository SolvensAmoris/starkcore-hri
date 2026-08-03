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
emergent_edges=list(edges)

def reconstruct_corr(edges, pos_true):
    adj={i:set() for i in range(N)}
    for a,b in edges: adj[a].add(b); adj[b].add(a)
    dist=[[N]*N for _ in range(N)]
    for s in range(N):
        d={s:0}; q=collections.deque([s])
        while q:
            u=q.popleft()
            for v in adj[u]:
                if v not in d:
                    d[v]=d[u]+1; q.append(v)
        for t in range(N): dist[s][t]=d.get(t,N)
    random.seed(0)
    pos_rec=[random.random() for _ in range(N)]
    for it in range(200):
        for i in range(N):
            grad=0.0
            for j in range(N):
                if i==j or dist[i][j]>=N: continue
                diff=(pos_rec[i]-pos_rec[j]+0.5)%1-0.5
                drec=abs(diff)
                target=dist[i][j]/12.0
                if drec<1e-9: continue
                grad+=2*(drec-target)*(1 if diff>0 else -1)
            pos_rec[i]=(pos_rec[i]-0.0015*grad)%1
    best=-1
    for flip in [False,True]:
        rec2=[1-x if flip else x for x in pos_rec]
        for shift in [k/20 for k in range(20)]:
            s=0
            for a,b in zip(pos_true, rec2):
                diff=(a-(b+shift)%1+0.5)%1-0.5
                s+=math.cos(2*math.pi*diff)
            corr=s/N
            if corr>best: best=corr
    return best

# control aleatorio con mismo N,M
random.seed(999)
control_edges=set()
while len(control_edges)<len(emergent_edges):
    a=random.randrange(N); b=random.randrange(N)
    if a!=b: control_edges.add((min(a,b),max(a,b)))
control_edges=list(control_edges)

corr_em=reconstruct_corr(emergent_edges, pos_true)
corr_rd=reconstruct_corr(control_edges, pos_true)

print(f"ET v0.5 PROOF")
print(f"Emergente corr = {corr_em:.3f}")
print(f"Aleatoria corr = {corr_rd:.3f}")
print(f"Delta = {corr_em-corr_rd:.3f} -> {'GEOMETRIA REAL' if corr_em-corr_rd>0.3 else 'ruido'}")

print("\nCurva de destruccion emergente:")
for p in [0,0.05,0.1,0.2,0.3,0.5]:
    random.seed(2)
    kept=[e for e in emergent_edges if random.random()>p]
    c=reconstruct_corr(kept, pos_true)
    print(f" {int(p*100)}% borrado -> corr {c:.3f} edges {len(kept)}")

print("\nV0.5 DONE")
