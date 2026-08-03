import random, collections
random.seed(1337)
N=80

# --- red emergente (tu dinamica) ---
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
    adj={k:[] for k in range(N)}
    for a,b in edges:
        adj[a].append(b); adj[b].append(a)
    new_pos=pos[:]
    for i in range(N):
        if not adj[i]: continue
        avg=sum(pos[j] for j in adj[i])/len(adj[i])
        diff=(avg-pos[i]+0.5)%1-0.5
        new_pos[i]=(pos[i]+0.05*diff)%1
    return new_pos

for _ in range(30): pos=step(pos)
emergent_edges=edges.copy()

# --- red aleatoria control, mismo N y M ---
random.seed(999)
control_edges=set()
while len(control_edges)<len(emergent_edges):
    a=random.randrange(N); b=random.randrange(N)
    if a!=b:
        control_edges.add((min(a,b),max(a,b)))

def analyze(edges, label):
    adj={i:set() for i in range(N)}
    for a,b in edges:
        adj[a].add(b); adj[b].add(a)
    # BFS para N(r)
    def bfs(start):
        dist={start:0}; q=collections.deque([start])
        while q:
            u=q.popleft()
            for v in adj[u]:
                if v not in dist:
                    dist[v]=dist[u]+1
                    q.append(v)
        # cuenta por r
        cnt=collections.Counter(dist.values())
        # acumulada
        acc=0; curve=[]
        for r in sorted(cnt):
            acc+=cnt[r]
            curve.append((r,acc))
        return curve

    # promedia sobre 5 origenes
    curves=[]
    for s in [0,10,20,30,40]:
        curves.append(bfs(s))

    print(f"\n=== {label} ===")
    print(f"edges={len(edges)}")
    # N(r) promedio
    avg_r={}
    for cur in curves:
        for r,nr in cur:
            avg_r.setdefault(r, []).append(nr)
    for r in sorted(avg_r):
        m=sum(avg_r[r])/len(avg_r[r])
        print(f" r={r} N(<=r)~{m:.1f}")

    # estima dimension D por log N / log r entre r=1 y r=2
    if 1 in avg_r and 2 in avg_r:
        n1=sum(avg_r[1])/len(avg_r[1])
        n2=sum(avg_r[2])/len(avg_r[2])
        if n1>1:
            import math
            D=math.log(n2/n1)/math.log(2)
            print(f" Dimension efectiva D ~ {D:.2f} (D~1 linea, D~2 plano, D>>random)")
    # clustering
    tri=0
    for i in range(N):
        for j in adj[i]:
            if j>i:
                tri+=len(adj[i]&adj[j])
    tri//=3
    print(f" triangulos={tri}")

analyze(emergent_edges,"RED EMERGENTE v0.1")
analyze(control_edges,"RED ALEATORIA control")
print("\nV0.2 DONE - si D estable 1-3 = geometria, si D explota = random")
