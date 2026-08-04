import random, math, collections
random.seed(1337)
N=80
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
    for a,b in edges: adj[a].append(b); adj[b].append(a)
    new=[p for p in pos]
    for i in range(N):
        if not adj[i]: continue
        avg=sum(pos[j] for j in adj[i])/len(adj[i])
        diff=(avg-pos[i]+0.5)%1-0.5
        new[i]=(pos[i]+0.05*diff)%1
    return new

for _ in range(30): pos=step(pos)
emergent=list(edges)

print("ET v0.3 - olvida pos, solo queda grafo")

# 1) Laplaciano y Fiedler (algebraic connectivity)
# L = D - A, segundo eigenvalor >0 = conexo, chico = cuello de botella tipo linea
def laplacian_spectrum(edges):
    # power iteration simple para estimar 2o eigenvalor chico usando numpy? sin numpy usamos heuristica
    # hacemos BFS diameter + spectral gap aproximado via adj
    adj={i:set() for i in range(N)}
    for a,b in edges: adj[a].add(b); adj[b].add(a)
    # diametro
    def bfs_dist(s):
        d={s:0}; q=collections.deque([s])
        while q:
            u=q.popleft()
            for v in adj[u]:
                if v not in d:
                    d[v]=d[u]+1; q.append(v)
        return d
    diam=max(max(bfs_dist(i).values()) for i in range(N))
    # clustering medio
    tri=0
    for i in range(N):
        for j in adj[i]:
            if j>i: tri+=len(adj[i]&adj[j])
    tri//=3
    return diam, tri

diam_em, tri_em = laplacian_spectrum(emergent)
print(f"Emergente: diam={diam_em} tri={tri_em}")

# control aleatoria
random.seed(999)
control=set()
while len(control)<len(emergent):
    a=random.randrange(N); b=random.randrange(N)
    if a!=b: control.add((min(a,b),max(a,b)))
diam_rd, tri_rd = laplacian_spectrum(control)
print(f"Aleatoria: diam={diam_rd} tri={tri_rd}")

# 2) Curvatura Ollivier simplificada: compara vecindarios
def ollivier_curvature(edges, samples=20):
    adj={i:set() for i in range(N)}
    for a,b in edges: adj[a].add(b); adj[b].add(a)
    curvs=[]
    for _ in range(samples):
        a,b=random.choice(list(edges))
        # distancia Wasserstein aproximada = overlap de vecinos
        na=adj[a]; nb=adj[b]
        inter=len(na&nb)
        union=len(na|nb)
        # curvatura ~ inter/union - base
        curvs.append(inter/(union+1e-9))
    return sum(curvs)/len(curvs)

random.seed(0)
print(f"\nCurvatura local (overlap vecinos):")
print(f" Emergente {ollivier_curvature(emergent):.3f} (alto=plano/curvo positivo)")
print(f" Aleatoria {ollivier_curvature(control):.3f} (bajo=hiperbolico/random)")

# 3) Perturbacion reina
def perturb_test(edges, p=0.15):
    E=list(edges)
    random.seed(1)
    keep=[e for e in E if random.random()>p]
    diam,_=laplacian_spectrum(keep)
    return len(keep), diam

keep, diam2 = perturb_test(emergent,0.15)
print(f"\nPerturbacion 15% removido: quedan {keep} aristas diam {diam_em}->{diam2}")
print("Si diam no explota, la geometria es estable")

print("\nV0.3 DONE - sin pos, solo topologia")
