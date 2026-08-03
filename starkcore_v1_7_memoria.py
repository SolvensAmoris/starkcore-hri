"""
v1.7 - Curva de Memoria Causal
Cuanto pasado necesitas para recuperar la Ley?
I(Ley ; Observacion) via clasificador simple
"""
import numpy as np, networkx as nx, random
from itertools import combinations

def gen_world_trace(law, n=150, p0=0.03, steps=60, seed=0):
    rng=np.random.default_rng(seed)
    G=nx.erdos_renyi_graph(n, p=p0, seed=seed)
    trace=[G.copy()] # guarda historia
    for _ in range(steps):
        # mismo evolve que v1.5
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
        trace.append(G.copy())
    return trace

def diffusion_fp(G, t_max=20, n_pert=20, seed=0):
    rng=np.random.default_rng(seed)
    nodes=list(G.nodes()); n=len(nodes)
    if n==0: return np.zeros(t_max)
    A=nx.to_numpy_array(G, nodelist=nodes)
    deg=A.sum(axis=1); deg[deg==0]=1
    P=A/deg[:,None]
    curves=[]
    for _ in range(n_pert):
        p=np.zeros(n); p[rng.integers(0,n)]=1.0
        Hs=[]
        for _ in range(t_max):
            p=p@P
            ps=p[p>1e-12]
            Hs.append(-np.sum(ps*np.log(ps)) if len(ps)>0 else 0)
        curves.append(Hs)
    return np.mean(curves,axis=0)

def accuracy_law(traces_A, traces_B, use_frac=1.0):
    # usa solo ultimos use_frac de la historia promediado
    fps=[]
    labels=[]
    for tr in traces_A:
        k=int(len(tr)*use_frac)
        k=max(1,k)
        # promedia huella de ultimos k grafos
        cur=np.mean([diffusion_fp(g, seed=0) for g in tr[-k:]], axis=0)
        fps.append(cur); labels.append(0)
    for tr in traces_B:
        k=int(len(tr)*use_frac)
        k=max(1,k)
        cur=np.mean([diffusion_fp(g, seed=1) for g in tr[-k:]], axis=0)
        fps.append(cur); labels.append(1)
    fps=np.array(fps)
    # clasificador centroid
    c0=fps[np.array(labels)==0].mean(axis=0)
    c1=fps[np.array(labels)==1].mean(axis=0)
    correct=0
    for fp,l in zip(fps,labels):
        pred=0 if np.linalg.norm(fp-c0)<np.linalg.norm(fp-c1) else 1
        if pred==l: correct+=1
    return correct/len(labels)

if __name__=="__main__":
    lawA={"max_deg":8,"p_tri":0.85,"prune_thr":0.2}
    lawB={"max_deg":8,"p_tri":0.15,"prune_thr":0.9}
    print("=== v1.7 Curva de Memoria Causal ===")
    print(f"Ley A {lawA}\nLey B {lawB}\nGenerando 20 trazas cada una...")
    tracesA=[gen_world_trace(lawA, seed=i) for i in range(20)]
    tracesB=[gen_world_trace(lawB, seed=100+i) for i in range(20)]
    for frac in [0.02, 0.05, 0.1, 0.25, 0.5, 1.0]:
        acc=accuracy_law(tracesA, tracesB, use_frac=frac)
        print(f" Ultimo {frac*100:4.0f}% de historia -> accuracy {acc*100:.1f}% {'(azar)' if acc<0.6 else 'memoria' if acc<0.85 else 'FOSIL FUERTE'}")
