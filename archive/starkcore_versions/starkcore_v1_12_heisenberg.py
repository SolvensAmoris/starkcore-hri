import numpy as np, networkx as nx, gzip, os
def sample_induced(G,q,rng):
    k=max(10,int(len(G)*q))
    return G.subgraph(rng.choice(list(G.nodes()), size=k, replace=False)).copy()

def metrics(G):
    if len(G)<3: return 0,0
    try:
        mod=nx.community.modularity(G, nx.community.greedy_modularity_communities(G))
    except: mod=0
    return nx.average_clustering(G), mod

# usa tu G0 de 900 nodos
G0 = nx.Graph(nx.read_edgelist(gzip.open("ca-GrQc.txt.gz"), nodetype=int).subgraph(range(900)))
rng=np.random.default_rng(0)

for q in [0.5,0.4,0.3,0.2,0.1,0.05]:
    accs=[]
    for seed in range(10):
        # simula 2 mundos con rewire random vs triadic sobre G0
        Gr=G0.copy(); Gt=G0.copy()
        for _ in range(20):
            # triadic boost en Gt
            n=list(Gt.nodes())[rng.integers(len(Gt))]
            c=[nb2 for nb in Gt.neighbors(n) for nb2 in Gt.neighbors(nb) if nb2!=n and not Gt.has_edge(n,nb2)]
            if c: Gt.add_edge(n, c[rng.integers(len(c))])
        c_r,_=metrics(sample_induced(Gr,q,rng))
        c_t,_=metrics(sample_induced(Gt,q,rng))
        accs.append(c_t>c_r) # separacion simple
    print(f"q={q:.2f} -> P(triadic > random) {np.mean(accs)*100:.0f}%")
