import random, math, collections
random.seed(7)
N=100
edges=set()
while len(edges)<N*3:
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
    diam=max(max(bfs(i).values()) for i in range(0,N,10))
    tri=0
    for i in range(N):
        for j in adj[i]:
            if j>i: tri+=len(adj[i]&adj[j])
    tri//=3
    d0=bfs(0)
    cnt=collections.Counter(d0.values())
    acc=0; curve=[]
    for r in sorted(cnt):
        acc+=cnt[r]; curve.append((r,acc))
    D=None
    if len(curve)>=3 and curve[1][1]>1:
        try:
            D=math.log(curve[2][1]/curve[1][1])/math.log(2)
        except: D=None
    ov=[]
    for a,b in edges[:100]:
        if a>=N or b>=N: continue
        inter=len(adj[a]&adj[b]); union=len(adj[a]|adj[b])
        ov.append(inter/(union+1e-9))
    curv=sum(ov)/len(ov) if ov else 0
    return diam, tri, D, curv, curve

for step in range(60):
    adj={i:set() for i in range(N)}
    for a,b in edges: adj[a].add(b); adj[b].add(a)
    new_edges=set(edges)
    for i in range(N):
        neigh=list(adj[i])
        for j in range(len(neigh)):
            for k in range(j+1,len(neigh)):
                a=neigh[j]; b=neigh[k]
                if (min(a,b),max(a,b)) in new_edges: continue
                if len(adj[a]&adj[b])>=2 and random.random()<0.15:
                    new_edges.add((min(a,b),max(a,b)))
    adj2={i:set() for i in range(N)}
    for a,b in new_edges: adj2[a].add(b); adj2[b].add(a)
    to_remove=set()
    for i in range(N):
        if len(adj2[i])>10:
            worst=None; worst_score=1e9
            for nb in adj2[i]:
                score=len(adj2[i]&adj2[nb])
                if score<worst_score:
                    worst_score=score; worst=nb
            to_remove.add((min(i,worst),max(i,worst)))
    new_edges=new_edges - to_remove
    edges=list(new_edges)

diam, tri, D, curv, curve = analyze(edges)
Dstr = f"{D:.2f}" if D is not None else "NA"
print(f"ET v0.7 - NACIDO SIN ESPACIO")
print(f"N={N} edges={len(edges)}")
print(f"diam={diam} tri={tri} D~{Dstr} curv_overlap={curv:.3f}")
print(f"N(r): {curve[:5]}")

random.seed(99)
rand_edges=set()
while len(rand_edges)<len(edges):
    a=random.randrange(N); b=random.randrange(N)
    if a!=b: rand_edges.add((min(a,b),max(a,b)))
diam_r, tri_r, D_r, curv_r, _ = analyze(list(rand_edges))
Drs = f"{D_r:.2f}" if D_r is not None else "NA"
print(f"\nRandom control: diam={diam_r} tri={tri_r} D~{Drs} curv={curv_r:.3f}")

if tri>tri_r*3 and diam>diam_r and curv>0.3:
    print("\n-> SEÑAL: orden sin espacio sembrado")
else:
    print("\n-> No emergio claro")

import json
with open("edges_v07.json","w") as f: json.dump(edges,f)
print("\nV0.7 DONE")
