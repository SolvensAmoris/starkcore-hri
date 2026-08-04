import numpy as np, networkx as nx, random

def gen_trace(law, n=150, steps=60, seed=0):
    rng=np.random.default_rng(seed)
    G=nx.erdos_renyi_graph(n, p=0.03, seed=seed)
    trace=[(G.number_of_edges(), nx.average_clustering(G), sum(1 for _ in nx.triangles(G).values())//3)]
    for _ in range(steps):
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
        trace.append((G.number_of_edges(), nx.average_clustering(G), sum(1 for _ in nx.triangles(G).values())//3))
    return np.array(trace) # shape steps x 3

lawA={"max_deg":8,"p_tri":0.85}
lawB={"max_deg":8,"p_tri":0.15}

print("v1.7b curva con traza de triangulos")
tracesA=[gen_trace(lawA, seed=i) for i in range(20)]
tracesB=[gen_trace(lawB, seed=100+i) for i in range(20)]

for frac in [0.02,0.05,0.1,0.25,0.5,1.0]:
    feats=[]
    labels=[]
    for tr in tracesA:
        k=max(1,int(len(tr)*frac))
        # feature = pendiente y varianza en ventana
        window=tr[-k:]
        # usa clustering y triangulos
        feat=[window[:,1].mean(), window[:,2].mean(), window[:,1].std(), window[:,2].std(), window[-1,1]-window[0,1]]
        feats.append(feat); labels.append(0)
    for tr in tracesB:
        k=max(1,int(len(tr)*frac))
        window=tr[-k:]
        feat=[window[:,1].mean(), window[:,2].mean(), window[:,1].std(), window[:,2].std(), window[-1,1]-window[0,1]]
        feats.append(feat); labels.append(1)
    feats=np.array(feats)
    c0=feats[np.array(labels)==0].mean(axis=0)
    c1=feats[np.array(labels)==1].mean(axis=0)
    correct=sum(1 for f,l in zip(feats,labels) if (0 if np.linalg.norm(f-c0)<np.linalg.norm(f-c1) else 1)==l)
    print(f" {frac*100:4.0f}% -> {correct/len(labels)*100:.1f}% | c0_clust {c0[0]:.3f} vs c1 {c1[0]:.3f} | tri {c0[1]:.0f} vs {c1[1]:.0f}")
