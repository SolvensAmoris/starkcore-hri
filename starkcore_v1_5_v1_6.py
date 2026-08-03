"""
StarkCore v1.5 - v1.6
Identidad = Estado + Historia + Restricciones

v1.5: Huella por entropia de difusion + ratio intra/inter
v1.6: Adversario Isostatico (mismo Estado final, distinta Ley)
"""

import numpy as np
import networkx as nx
from itertools import combinations
import random

def generate_world(law, n=200, p0=0.02, steps=50, seed=0):
    rng = np.random.default_rng(seed)
    random.seed(seed)
    G = nx.erdos_renyi_graph(n, p=p0, seed=seed)
    for _ in range(steps):
        G = evolve_step(G, law, rng)
    return G

def evolve_step(G, law, rng):
    max_deg = law['max_deg']
    p_tri = law['p_tri']
    prune_thr = law['prune_thr']

    for node in list(G.nodes()):
        deg = G.degree(node)
        if deg > max_deg:
            neigh = list(G.neighbors(node))
            scored = []
            for nb in neigh:
                try:
                    cn = len(list(nx.common_neighbors(G, node, nb)))
                except:
                    cn = 0
                scored.append((cn, nb))
            scored.sort(key=lambda x: x[0])
            n_prune = deg - max_deg
            for i in range(n_prune):
                if i >= len(scored): break
                _, nb = scored[i]
                if G.has_edge(node, nb):
                    G.remove_edge(node, nb)

    nodes = list(G.nodes())
    rng.shuffle(nodes)
    for node in nodes:
        if G.degree(node) >= max_deg: continue
        two_hop = set()
        for nb in G.neighbors(node):
            for nb2 in G.neighbors(nb):
                if nb2!= node and not G.has_edge(node, nb2):
                    two_hop.add(nb2)
        for cand in list(two_hop):
            if G.degree(node) >= max_deg: break
            if G.degree(cand) >= max_deg: continue
            if rng.random() < p_tri:
                G.add_edge(node, cand)
    return G

def diffusion_fingerprint(G, t_max=25, n_perturb=30, seed=0):
    rng = np.random.default_rng(seed)
    nodes = list(G.nodes())
    n = len(nodes)
    if n == 0:
        return np.zeros(t_max), np.zeros(t_max), np.zeros((1,t_max))
    A = nx.to_numpy_array(G, nodelist=nodes)
    deg = A.sum(axis=1)
    deg[deg == 0] = 1
    P = A / deg[:, None]
    curves = []
    for _ in range(n_perturb):
        start = rng.integers(0, n)
        p = np.zeros(n)
        p[start] = 1.0
        Hs = []
        for t in range(t_max):
            p = p @ P
            p_safe = p[p > 1e-12]
            H = -np.sum(p_safe * np.log(p_safe)) if len(p_safe)>0 else 0.0
            Hs.append(H)
        curves.append(Hs)
    curves = np.array(curves)
    return curves.mean(axis=0), curves.std(axis=0), curves

def fingerprint_distance(fp1, fp2):
    return np.linalg.norm(fp1 - fp2)

def run_v15(laws, n_worlds=8, n=200, steps=40, t_max=25, n_perturb=20):
    print(f"\n=== v1.5: Ratio Intra/Inter con Entropia ===")
    fingerprints = {name: [] for name in laws}
    graphs = {name: [] for name in laws}
    for law_name, law in laws.items():
        print(f"\nGenerando {n_worlds} mundos con {law_name}: {law}")
        for i in range(n_worlds):
            seed = hash((law_name, i)) % 10000
            G = generate_world(law, n=n, steps=steps, seed=seed)
            mean_curve, _, _ = diffusion_fingerprint(G, t_max=t_max, n_perturb=n_perturb, seed=seed)
            fingerprints[law_name].append(mean_curve)
            graphs[law_name].append(G)
            print(f" mundo {i}: E={G.number_of_edges()} avg_deg={np.mean([d for _,d in G.degree()]):.2f}")
    results = {}
    for law_name in laws:
        fps = fingerprints[law_name]
        intra_dists = []
        for a,b in combinations(range(len(fps)), 2):
            intra_dists.append(fingerprint_distance(fps[a], fps[b]))
        results[law_name] = {"intra": intra_dists}
        print(f"\n{law_name} intra: mean={np.mean(intra_dists):.4f} std={np.std(intra_dists):.4f}")
    law_names = list(laws.keys())
    for i in range(len(law_names)):
        for j in range(i+1, len(law_names)):
            n1, n2 = law_names[i], law_names[j]
            inter_dists = []
            for fp1 in fingerprints[n1]:
                for fp2 in fingerprints[n2]:
                    inter_dists.append(fingerprint_distance(fp1, fp2))
            intra_mean = (np.mean(results[n1]["intra"]) + np.mean(results[n2]["intra"])) / 2
            inter_mean = np.mean(inter_dists)
            ratio = inter_mean / (intra_mean + 1e-9)
            print(f"\nINTER {n1} vs {n2}: mean={inter_mean:.4f} std={np.std(inter_dists):.4f}")
            print(f" intra_mean={intra_mean:.4f} => RATIO inter/intra = {ratio:.2f} -> {'PASA' if ratio>3 else 'NO SEPARA'}")
    return fingerprints, graphs

def get_static_stats(G):
    n = G.number_of_nodes()
    e = G.number_of_edges()
    avg_deg = (2*e / n) if n>0 else 0
    dens = nx.density(G)
    try:
        clust = nx.average_clustering(G)
    except:
        clust = 0
    return {"n": n, "e": e, "avg_deg": avg_deg, "dens": dens, "clust": clust}

def static_distance(s1, s2):
    return np.sqrt(((s1["e"]-s2["e"])/100)**2 + (s1["avg_deg"]-s2["avg_deg"])**2 + ((s1["dens"]-s2["dens"])*100)**2 + ((s1["clust"]-s2["clust"])*5)**2)

def run_v16_adversario():
    print(f"\n\n=== v1.6: ADVERSARIO ISOSTATICO ===")
    law_A = {"max_deg": 8, "p_tri": 0.85, "prune_thr": 0.2}
    law_B = {"max_deg": 8, "p_tri": 0.15, "prune_thr": 0.9}
    print(f"Ley A (cluster): {law_A}")
    print(f"Ley B (pruner): {law_B}")
    pool_A, pool_B = [], []
    for i in range(30):
        G_A = generate_world(law_A, n=200, p0=0.03, steps=60, seed=i)
        G_B = generate_world(law_B, n=200, p0=0.05, steps=60, seed=100+i)
        pool_A.append(G_A)
        pool_B.append(G_B)
    best = None
    best_pair = None
    for Ga in pool_A:
        for Gb in pool_B:
            sa, sb = get_static_stats(Ga), get_static_stats(Gb)
            d_static = static_distance(sa, sb)
            if best is None or d_static < best:
                best = d_static
                best_pair = (Ga, Gb, sa, sb)
    Ga, Gb, sa, sb = best_pair
    print(f"\nMejor par isostatico: d_static={best:.4f}")
    print(f" Ga stats: {sa}")
    print(f" Gb stats: {sb}")
    mean_A, _, curves_A = diffusion_fingerprint(Ga, t_max=30, n_perturb=40, seed=0)
    mean_B, _, curves_B = diffusion_fingerprint(Gb, t_max=30, n_perturb=40, seed=1)
    d_dynamic = fingerprint_distance(mean_A, mean_B)
    print(f"\nDistancia DINAMICA A vs B: {d_dynamic:.4f}")
    return Ga, Gb, mean_A, mean_B

if __name__ == "__main__":
    laws_v15 = {
        "LEY_6_cluster": {"max_deg": 6, "p_tri": 0.8, "prune_thr": 0.3},
        "LEY_8_mixta": {"max_deg": 8, "p_tri": 0.5, "prune_thr": 0.5},
        "LEY_12_pruner": {"max_deg": 12, "p_tri": 0.2, "prune_thr": 0.8},
    }
    fps, graphs = run_v15(laws_v15, n_worlds=6, n=200, steps=50, t_max=25, n_perturb=20)
    Ga, Gb, mean_A, mean_B = run_v16_adversario()
