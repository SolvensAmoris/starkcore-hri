import numpy as np
import networkx as nx

def shannon(arr):
    if len(arr) < 1: return 0.0
    vals, counts = np.unique(np.round(arr, 5), return_counts=True)
    p = counts.astype(float) / counts.sum()
    return -np.sum(p * np.log2(p + 1e-15))

def entropy_rate(arr):
    if len(arr) < 3: return 0.0
    h1 = shannon(arr)
    arr_d = np.round(arr, 4)
    blocks = [tuple(arr_d[i:i+2]) for i in range(len(arr)-1)]
    if not blocks: return 0.0
    _, counts = np.unique(blocks, axis=0, return_counts=True)
    p = counts.astype(float) / counts.sum()
    h2 = -np.sum(p * np.log2(p + 1e-15))
    return max(0.0, h2 - h1)

def gen_trace(mode, target_churn=14, n=120, steps=80, seed=0):
    """mode: 'random' | 'struct'. Mismo target de volumen. Trackea estructura + percolación."""
    rng = np.random.default_rng(seed)
    G = nx.erdos_renyi_graph(n, p=0.035, seed=seed)
    nodes = list(G.nodes())
    hist = {k: [] for k in ['churn','clust','tris','closing_frac','giant','delta_clust','delta_giant']}
    prev_c = nx.average_clustering(G)
    prev_g = max(len(c) for c in nx.connected_components(G)) / n
    for t in range(steps):
        changes = 0
        closing = 0
        attempts = 0
        while changes < target_churn and attempts < target_churn*5:
            attempts += 1
            if mode == 'random':
                edges = list(G.edges())
                if edges:
                    e = edges[rng.integers(len(edges))]
                    G.remove_edge(*e)
                    changes += 1
                non = list(nx.non_edges(G))
                if non:
                    ne = non[rng.integers(len(non))]
                    G.add_edge(*ne)
                    changes += 1
            else:
                node = nodes[rng.integers(n)]
                cands = []
                for nb in list(G.neighbors(node)):
                    for nb2 in G.neighbors(nb):
                        if nb2 != node and not G.has_edge(node, nb2):
                            cands.append(nb2)
                if cands and rng.random() < 0.88:
                    G.add_edge(node, cands[rng.integers(len(cands))])
                    changes += 1
                    closing += 1
                else:
                    if G.degree(node) > 7:
                        neigh = list(G.neighbors(node))
                        if neigh:
                            G.remove_edge(node, neigh[rng.integers(len(neigh))])
                            changes += 1
                    else:
                        non = [x for x in nodes if x!=node and not G.has_edge(node,x)]
                        if non:
                            G.add_edge(node, non[rng.integers(len(non))])
                            changes += 1
        c = nx.average_clustering(G)
        tris = sum(nx.triangles(G).values()) // 3
        giant = max((len(cc) for cc in nx.connected_components(G)), default=1) / n
        hist['churn'].append(changes)
        hist['clust'].append(c)
        hist['tris'].append(tris)
        hist['closing_frac'].append(closing / max(1, changes))
        hist['giant'].append(giant)
        hist['delta_clust'].append(c - prev_c)
        hist['delta_giant'].append(giant - prev_g)
        prev_c, prev_g = c, giant
    return {k: np.array(v, float) for k,v in hist.items()}

print("="*72)
print("v1.9 ESTRUCTURA + PERCOLACIÓN + DETECTOR ONLINE")
print("Firma = organización de los cambios (no volumen)")
print("="*72)

# ---------- 1. Generación controlada ----------
print("\n[1] Generando mundos con churn volumen casi idéntico...")
trs_r = [gen_trace('random', seed=i) for i in range(16)]
trs_s = [gen_trace('struct', seed=100+i) for i in range(16)]
print(f"Churn μ  Random: {np.mean([t['churn'].mean() for t in trs_r]):.2f}")
print(f"Churn μ  Struct: {np.mean([t['churn'].mean() for t in trs_s]):.2f}")
print(f"Closingμ Random: {np.mean([t['closing_frac'].mean() for t in trs_r]):.3f}")
print(f"Closingμ Struct: {np.mean([t['closing_frac'].mean() for t in trs_s]):.3f}")

# ---------- 2. Demostración: la firma es estructural ----------
print("\n[2] DEMOSTRACIÓN: firma refleja ESTRUCTURA de los cambios")
print("   (volumen controlado → si separa, es patrón, no cantidad)")
for frac in [0.35, 0.7]:
    print(f"\n  Ventana final {frac*100:.0f}%")
    for label, key in [('closing_frac','closing_frac'), ('clust','clust'), ('giant (percolación)','giant'), ('delta_clust','delta_clust')]:
        feats, labs = [], []
        for lab, trs in [(0, trs_r), (1, trs_s)]:
            for t in trs:
                k = max(8, int(len(t[key])*frac))
                w = t[key][-k:]
                feats.append([shannon(w), entropy_rate(w), w.mean(), w.std()])
                labs.append(lab)
        feats = np.array(feats)
        labs = np.array(labs)
        c0 = feats[labs==0].mean(0)
        c1 = feats[labs==1].mean(0)
        preds = np.array([0 if np.linalg.norm(f-c0)<np.linalg.norm(f-c1) else 1 for f in feats])
        acc = (preds == labs).mean()
        print(f"  {label:20s} ACC {acc*100:5.1f}% | μ R {feats[labs==0,2].mean():.4f} vs S {feats[labs==1,2].mean():.4f}")

# ---------- 3. Detector ONLINE basado en estructura ----------
print("\n[3] DETECTOR ONLINE (basado en closing_frac + clust, no en volumen)")
print("   Simula cambio de régimen: random → struct en t=35")
print("-"*72)

def gen_switching(n=120, steps=80, switch=35, seed=0):
    rng = np.random.default_rng(seed)
    G = nx.erdos_renyi_graph(n, p=0.035, seed=seed)
    nodes = list(G.nodes())
    hist = []
    for t in range(steps):
        mode = 'random' if t < switch else 'struct'
        changes = closing = attempts = 0
        target = 14
        while changes < target and attempts < target*5:
            attempts += 1
            if mode == 'random':
                edges = list(G.edges())
                if edges:
                    e = edges[rng.integers(len(edges))]
                    G.remove_edge(*e); changes += 1
                non = list(nx.non_edges(G))
                if non:
                    ne = non[rng.integers(len(non))]
                    G.add_edge(*ne); changes += 1
            else:
                node = nodes[rng.integers(n)]
                cands = [nb2 for nb in list(G.neighbors(node)) for nb2 in G.neighbors(nb) if nb2!=node and not G.has_edge(node,nb2)]
                if cands and rng.random() < 0.88:
                    G.add_edge(node, cands[rng.integers(len(cands))])
                    changes += 1; closing += 1
                else:
                    if G.degree(node) > 7:
                        neigh = list(G.neighbors(node))
                        if neigh: G.remove_edge(node, neigh[rng.integers(len(neigh))]); changes += 1
                    else:
                        non = [x for x in nodes if x!=node and not G.has_edge(node,x)]
                        if non: G.add_edge(node, non[rng.integers(len(non))]); changes += 1
        c = nx.average_clustering(G)
        giant = max((len(cc) for cc in nx.connected_components(G)), default=1) / n
        hist.append((closing/max(1,changes), c, giant))
    return np.array(hist)

def online_structural_detector(trace, win=10, close_thresh=0.45, clust_jump=0.08):
    """Detecta entrada en régimen estructurado. trace columns: closing_frac, clust, giant"""
    flags = []
    for t in range(win, len(trace)):
        w = trace[t-win:t]
        mean_close = w[:,0].mean()
        mean_clust = w[:,1].mean()
        if t < win + 8:
            flag = False
        else:
            baseline_close = trace[max(0,t-25):t-win, 0].mean() if t > win+5 else 0.0
            flag = (mean_close > close_thresh) and (mean_clust > baseline_close + 0.03 or mean_clust > 0.12)
        flags.append((t, mean_close, mean_clust, flag))
    return flags

lags = []
success = 0
for s in range(14):
    tr = gen_switching(seed=300+s)
    dets = online_structural_detector(tr)
    det = next((t for t,c,cl,f in dets if t >= 35 and f), None)
    if det is not None:
        success += 1
        lags.append(det - 35)

print(f"Detecciones: {success}/14")
if lags:
    print(f"Lag medio: {np.mean(lags):.1f} ± {np.std(lags):.1f}  (min {min(lags)}, max {max(lags)})")

print("\nEjemplo seed=0 (t | closeμ | clustμ | FLAG):")
tr0 = gen_switching(seed=300)
for t, c, cl, f in online_structural_detector(tr0):
    if t % 4 == 0 or f:
        mark = "  <<<< RÉGIMEN ESTRUCTURADO" if f else ""
        print(f"{t:3d} | {c:.3f} | {cl:.4f} | {str(f):5s}{mark}")

# ---------- 4. Percolación ----------
print("\n[4] PERCOLACIÓN (tamaño componente gigante)")
print("   Random mantiene/rompe conectividad de forma distinta a Structured")
gR = np.mean([t['giant'][-20:].mean() for t in trs_r])
gS = np.mean([t['giant'][-20:].mean() for t in trs_s])
print(f"Giant final μ  Random: {gR:.3f} | Struct: {gS:.3f}")

print("\n" + "="*72)
print("VEREDICTO v1.9:")
print("- Volumen de churn controlado → separación por closing_frac y clustering = firma de ESTRUCTURA")
print("- Percolación (giant) también diverge según el régimen de reescritura")
print("- Detector online basado en señales estructurales captura el cambio de régimen")
print("- La firma informacional refleja la organización de los cambios, no solo su cantidad")
print("="*72)
