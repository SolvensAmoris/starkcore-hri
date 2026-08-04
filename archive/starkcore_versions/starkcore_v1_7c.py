import numpy as np, networkx as nx

def gen_trace(law, n=150, steps=60, seed=0):
    rng=np.random.default_rng(seed)
    G=nx.erdos_renyi_graph(n, p=0.03, seed=seed)
    hist=[]
    for _ in range(steps):
        # guarda delta antes de evolucionar
        tris = sum(nx.triangles(G).values())//3
        clust = nx.average_clustering(G)
        # evolucion
        edges_before = set(G.edges())
        for node in list(G.nodes()):
            if G.degree(node) > law['max_deg']:
                neigh=list(G.neighbors(node))
                scored=sorted([(len(list(nx.common_neighbors(G, node, nb))), nb) for nb in neigh])
                for _,nb in scored[:G.degree(node)-law['max_deg']]:
                    if G.has_edge(node,nb): G.remove_edge(node,nb)
        nodes=list(G.nodes()); rng.shuffle(nodes)
        for node in nodes:
            if G.degree(node)>=law['max_deg']: continue
            two_hop=set()
            for nb in G.neighbors(node):
                for nb2 in G.neighbors(nb):
                    if nb2!=node and not G.has_edge(node,nb2): two_hop.add(nb2)
            for cand in list(two_hop):
                if G.degree(node)>=law['max_deg']: break
                if rng.random()<law['p_tri']: G.add_edge(node,cand)
        edges_after = set(G.edges())
        churn = len(edges_before.symmetric_difference(edges_after))
        hist.append((clust, tris, churn, G.number_of_edges()))
    return np.array(hist, float)

# abre leyes: una hace mundo denso en triangulos, otra mundo disperso
lawA={"max_deg":12, "p_tri":0.9} # jardin cerrado
lawB={"max_deg":6, "p_tri":0.1} # jardin podado

print("v1.7c leyes separadas + bugfix")
tracesA=[gen_trace(lawA, seed=i) for i in range(20)]
tracesB=[gen_trace(lawB, seed=100+i) for i in range(20)]

for frac in [0.05,0.1,0.25,0.5,1.0]:
    feats=[]; labels=[]
    for tr in tracesA:
        k=max(5,int(len(tr)*frac))
        w=tr[-k:]
        # feature: media clustering, media tris, media churn
        feat=[w[:,0].mean(), w[:,1].mean(), w[:,2].mean(), w[-1,0]-w[0,0]]
        feats.append(feat); labels.append(0)
    for tr in tracesB:
        k=max(5,int(len(tr)*frac))
        w=tr[-k:]
        feat=[w[:,0].mean(), w[:,1].mean(), w[:,2].mean(), w[-1,0]-w[0,0]]
        feats.append(feat); labels.append(1)
    feats=np.array(feats)
    c0=feats[np.array(labels)==0].mean(axis=0)
    c1=feats[np.array(labels)==1].mean(axis=0)
    acc=sum(1 for f,l in zip(feats,labels) if (0 if np.linalg.norm(f-c0)<np.linalg.norm(f-c1) else 1)==l)/len(labels)
    print(f" {frac*100:4.0f}% -> {acc*100:.1f}% | clust {c0[0]:.3f} vs {c1[0]:.3f} | tris {c0[1]:.0f} vs {c1[1]:.0f} | churn {c0[2]:.1f} vs {c1[2]:.1f}")
