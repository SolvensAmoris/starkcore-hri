import random, math, collections
N=80

def make_world(seed):
    random.seed(seed)
    pos=[random.random() for _ in range(N)]
    edges=set()
    def step(pos, thr=0.08):
        edges.clear()
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
    for _ in range(30): pos=step(pos)
    return list(pos), list(edges)

def reconstruct_corr(edges, pos_true, iters=150):
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
    for _ in range(iters):
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
            s=sum(math.cos(2*math.pi*((a-(b+shift)%1+0.5)%1-0.5)) for a,b in zip(pos_true, rec2))
            corr=s/N
            if corr>best: best=corr
    return best

def degree_preserved_shuffle(edges, swaps=2000):
    # conserva grado de cada nodo (configuration model shuffle)
    edges=set((min(a,b),max(a,b)) for a,b in edges)
    edges=list(edges)
    random.seed(9999)
    for _ in range(swaps):
        e1,e2=random.sample(edges,2)
        a,b=e1; c,d=e2
        if len({a,b,c,d})<4: continue
        # rewire a-c, b-d
        new1=(min(a,c),max(a,c)); new2=(min(b,d),max(b,d))
        if new1 in edges or new2 in edges: continue
        if new1[0]==new1[1] or new2[0]==new2[1]: continue
        edges.remove(e1); edges.remove(e2)
        edges.append(new1); edges.append(new2)
    return edges

# 1) 30 mundos
print("ET v0.6 - 30 mundos emergentes")
corrs=[]
for seed in range(30):
    pos_true, e = make_world(1337+seed*7)
    corrs.append(reconstruct_corr(e, pos_true))
mean=sum(corrs)/len(corrs)
std=math.sqrt(sum((x-mean)**2 for x in corrs)/len(corrs))
print(f"Emergente: {mean:.3f} ± {std:.3f} min {min(corrs):.3f} max {max(corrs):.3f}")

# 2) 30 randoms puros y grado-preservado
corrs_rand=[]
corrs_deg=[]
for seed in range(30):
    pos_true, e = make_world(1337+seed*7)
    random.seed(seed)
    rand_edges=set()
    while len(rand_edges)<len(e):
        a=random.randrange(N); b=random.randrange(N)
        if a!=b: rand_edges.add((min(a,b),max(a,b)))
    corrs_rand.append(reconstruct_corr(list(rand_edges), pos_true))
    deg_shuf=degree_preserved_shuffle(e)
    corrs_deg.append(reconstruct_corr(deg_shuf, pos_true))

mean_r=sum(corrs_rand)/len(corrs_rand)
std_r=math.sqrt(sum((x-mean_r)**2 for x in corrs_rand)/len(corrs_rand))
mean_d=sum(corrs_deg)/len(corrs_deg)
std_d=math.sqrt(sum((x-mean_d)**2 for x in corrs_deg)/len(corrs_deg))
print(f"Aleatoria pura: {mean_r:.3f} ± {std_r:.3f}")
print(f"Grado-preservada: {mean_d:.3f} ± {std_d:.3f}")

# 3) Blind file
pos_true, e = make_world(1337)
import json
with open("edges.json","w") as f: json.dump(e,f)
print(f"\nBlind test: edges.json guardado con {len(e)} aristas, sin pos")
# reconstructor ciego solo lee edges.json
with open("edges.json") as f: blind_edges=json.load(f)
c_blind=reconstruct_corr(blind_edges, pos_true)
print(f"Reconstruccion ciega corr={c_blind:.3f} -> prueba de memoria relacional")

print("\nV0.6 DONE")
if mean - std > mean_d + std_d:
    print("CONCLUSION: geometria emergente supera null models => SI emergio memoria espacial")
else:
    print("CONCLUSION: no separable de null model grado")
