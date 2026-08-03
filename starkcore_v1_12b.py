import numpy as np, networkx as nx, gzip, random
def sample_induced(G,q,rng):
    k=max(20,int(len(G)*q))
    nodes=rng.choice(list(G.nodes()), size=k, replace=False)
    return G.subgraph(nodes).copy()
def metrics(G):
    if len(G)<5: return 0
    return nx.average_clustering(G)

# carga
G_full = nx.read_edgelist(gzip.open("ca-GrQc.txt.gz"), nodetype=int)
G0 = nx.Graph(G_full.subgraph(list(G_full.nodes())[:900]))
print(f"Base {G0.number_of_nodes()} nodos clust {nx.average_clustering(G0):.3f}")

def run_regime(G0, mode, steps=40, rng=None):
    G=G0.copy()
    nodes=list(G.nodes())
    for _ in range(steps):
        # rewire que conserva E
        e1,e2 = rng.choice(list(G.edges()),2, replace=False)
        u,v=e1; x,y=e2
        if len({u,v,x,y})==4 and not G.has_edge(u,x) and not G.has_edge(v,y):
            G.remove_edge(u,v); G.remove_edge(x,y)
            if mode=='triadic':
                # intenta cerrar triangulo: busca par con vecino comun
                commons = list(set(G.neighbors(u)).intersection(set(G.neighbors(x))))
                if commons and rng.random()<0.7:
                    # fuerza triangulo
                    G.add_edge(u,x); G.add_edge(v,y)
                else:
                    G.add_edge(u,x); G.add_edge(v,y)
            else:
                G.add_edge(u,x); G.add_edge(v,y)
    return G

rng=np.random.default_rng(42)
for q in [0.5,0.4,0.3,0.2,0.1,0.05]:
    wins=0
    for s in range(20):
        Gr=run_regime(G0,'random', rng=np.random.default_rng(s))
        Gt=run_regime(G0,'triadic', rng=np.random.default_rng(s+100))
        cr=metrics(sample_induced(Gr,q,np.random.default_rng(s)))
        ct=metrics(sample_induced(Gt,q,np.random.default_rng(s+100)))
        if ct>cr: wins+=1
    print(f"q={q:.2f} -> P(triadic>random | q) {wins/20*100:.0f}% | esperado 100%->50%")
