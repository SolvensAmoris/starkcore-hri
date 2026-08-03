import numpy as np, networkx as nx
def gen_trace_churn(law, n=150, steps=80, seed=0):
    rng=np.random.default_rng(seed)
    G=nx.erdos_renyi_graph(n, p=0.03, seed=seed)
    hist=[]
    for _ in range(steps):
        before=set(G.edges())
        for node in list(G.nodes()):
            if G.degree(node) > law['max_deg']:
                neigh=list(G.neighbors(node))
                scored=sorted([(len(list(nx.common_neighbors(G, node, nb))), nb) for nb in neigh])
                for _,nb in scored[:G.degree(node)-law['max_deg']]:
                    if G.has_edge(node,nb): G.remove_edge(node,nb)
        nodes=list(G.nodes()); rng.shuffle(nodes)
        for node in nodes:
            if G.degree(node)>=law['max_deg']: continue
            two=set()
            for nb in G.neighbors(node):
                for nb2 in G.neighbors(nb):
                    if nb2!=node and not G.has_edge(node,nb2): two.add(nb2)
            for cand in list(two):
                if rng.random()<law['p_tri']: G.add_edge(node,cand)
        after=set(G.edges())
        churn=len(before.symmetric_difference(after))
        hist.append(churn)
    return np.array(hist)

lawA={"max_deg":8,"p_tri":0.85}
lawB={"max_deg":8,"p_tri":0.15}
print("v1.7d ISOSTATICO pero midiendo churn (velocidad de reescritura)")
tracesA=[gen_trace_churn(lawA, seed=i) for i in range(25)]
tracesB=[gen_trace_churn(lawB, seed=100+i) for i in range(25)]

for frac in [0.02,0.05,0.1,0.25,0.5,1.0]:
    feats=[]; labs=[]
    for tr in tracesA:
        k=max(3,int(len(tr)*frac)); w=tr[-k:]
        feats.append([w.mean(), w.std(), w[-1]]); labs.append(0)
    for tr in tracesB:
        k=max(3,int(len(tr)*frac)); w=tr[-k:]
        feats.append([w.mean(), w.std(), w[-1]]); labs.append(1)
    feats=np.array(feats)
    c0=feats[np.array(labs)==0].mean(0); c1=feats[np.array(labs)==1].mean(0)
    acc=sum(1 for f,l in zip(feats,labs) if (0 if np.linalg.norm(f-c0)<np.linalg.norm(f-c1) else 1)==l)/len(labs)
    print(f" {frac*100:4.0f}% -> {acc*100:5.1f}% | churn A {c0[0]:.1f} vs B {c1[0]:.1f}")
