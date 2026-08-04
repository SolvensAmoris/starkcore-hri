#!/usr/bin/env python3
"""
FUNCTOR f_TOPO & ERROR CORRECTION v0.1 — FASE 1 (EVOLUCIONADO)
Calcula la firma tripartita real f = [topo, info, mem].
Implementa homología persistente nativa (Betti 0 y Betti 1) para grafos dirigidos por capas.
Refina la métrica Omega (Ω) usando capacidad de Shannon adaptativa según entropía de ruido.
"""
import os, json, time, math
import numpy as np
from starkcore.borromeo_validator import classify_architecture

# ---------------------------------------------------------------------------
# 1. Geometría REAL de M2.5 (Estable y determinista)
# ---------------------------------------------------------------------------
def build_adj(layers=6, width=20, rho=0.78, loc=0.55, seed=26):
    N = layers * width
    A = np.zeros((N, N), dtype=np.float32)
    rng = np.random.default_rng(seed)
    def nid(l, w): return l * width + w
    for l in range(layers - 1):
        for w in range(width):
            u = nid(l, w)
            for w2 in range(width):
                if rng.random() < rho * math.exp(-(abs(w - w2) ** 2) / (2 * loc * loc)):
                    A[u, nid(l + 1, w2)] = 1
            if A[u].sum() == 0:
                A[u, nid(l + 1, w)] = 1
    return A

def shuffle_preserva_grado(A, layers=6, width=20, seed=1000):
    B = np.zeros_like(A)
    rng = np.random.default_rng(seed)
    def nid(l, w): return l * width + w
    for l in range(layers - 1):
        for w in range(width):
            u = nid(l, w)
            k = int(A[u].sum())
            if k == 0: continue
            pool = [nid(l + 1, w2) for w2 in range(width)]
            B[u, rng.choice(pool, size=k, replace=False)] = 1
    return B

def shuffle_rompe_todo(A, seed=777):
    rng = np.random.default_rng(seed)
    B = A.flatten().copy()
    rng.shuffle(B)
    return B.reshape(A.shape)

# ---------------------------------------------------------------------------
# 2. Motor de Homología Persistente Nativa (f_topo)
# ---------------------------------------------------------------------------
def compute_persistence_betti(A, steps=10):
    """
    Calcula un proxy de homología persistente filtrando el grafo por umbrales de peso.
    Retorna la persistencia de Betti_0 (componentes) y Betti_1 (ciclos/bucles inducidos).
    """
    N = A.shape[0]
    # Usamos el Hamiltoniano simetrizado como mapa de distancias informacionales
    H = A + A.T
    min_w, max_w = H.min(), H.max()
    thresholds = np.linspace(min_w, max_w, steps)
    
    b0_persistence = 0
    b1_persistence = 0
    
    for t in thresholds:
        # Grafo de adyacencia binario filtrado en el nivel de energía t
        adj_t = (H >= t).astype(int)
        
        # Betti 0: Encontrar componentes conectados usando BFS/DFS simplificado
        visited = np.zeros(N, dtype=bool)
        components = 0
        for i in range(N):
            if not visited[i]:
                components += 1
                # Mini BFS
                queue = [i]
                visited[i] = True
                while queue:
                    curr = queue.pop(0)
                    for neighbor in range(N):
                        if adj_t[curr, neighbor] == 1 and not visited[neighbor]:
                            visited[neighbor] = True
                            queue.append(neighbor)
        
        # Betti 1: Aristas activas - Nodos + Componentes (Fórmula de Euler en grafos)
        edges = np.sum(adj_t) // 2
        cycles = max(0, edges - N + components)
        
        b0_persistence += components
        b1_persistence += cycles

    return float(b0_persistence / steps), float(b1_persistence / steps)

# ---------------------------------------------------------------------------
# 3. f_info = Espectro del Hamiltoniano
# ---------------------------------------------------------------------------
def espectro(A):
    H = A + A.T
    return np.sort(np.linalg.eigvalsh(H))

def drift(a, b): return float(np.linalg.norm(np.asarray(a) - np.asarray(b)))

# ---------------------------------------------------------------------------
# 4. Código Corrector de Errores Dinámico (Métrica Omega Refinada)
# ---------------------------------------------------------------------------
def compute_adaptive_omega(drift_val, base_capacity=0.5):
    """
    Refina la ley de Shannon. La capacidad disminuye logarítmicamente 
    a medida que la entropía del drift (ruido ortogonal) satura los canales.
    """
    if drift_val < 1e-6:
        return float('inf')
    # Penalización por entropía de deformación estructural
    entropy_penalty = math.log1p(drift_val)
    effective_capacity = base_capacity / (1.0 + entropy_penalty)
    return float(effective_capacity / drift_val)

# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
def main():
    print("=" * 64)
    print("  STARKCORE HAMMER · f_topo PERSISTENTE + SHANNON REFINADO")
    print("=" * 64)
    t0 = time.time()
    LAYERS, WIDTH = 6, 20

    # --- SISTEMA BASE ---
    A0 = build_adj(layers=LAYERS, width=WIDTH, seed=26)
    s0 = espectro(A0)
    b0_base, b1_base = compute_persistence_betti(A0)

    # --- SIMULACIÓN DE TRANSFORMACIONES ---
    A1 = A0 + np.random.default_rng(1).uniform(-0.02, 0.02, A0.shape).astype(np.float32)
    s1 = espectro(A1)
    b0_t1, b1_t1 = compute_persistence_betti(A1)

    A2 = (A0 @ A0.T) / 10.0
    s2 = espectro(A2)
    b0_t2, b1_t2 = compute_persistence_betti(A2)

    A3 = shuffle_preserva_grado(A0, layers=LAYERS, width=WIDTH, seed=1000)
    s3 = espectro(A3)
    b0_t3, b1_t3 = compute_persistence_betti(A3)

    A4 = shuffle_rompe_todo(A0, seed=777)
    s4 = espectro(A4)
    b0_t4, b1_t4 = compute_persistence_betti(A4)

    # --- EVALUACIÓN DE ISÓMEROS DE MEMORIA (T5) ---
    mem_base = np.random.default_rng(26).standard_normal(256)
    mem_clon = np.random.default_rng(20260803).standard_normal(256)
    drift_mem = float(np.linalg.norm(mem_base - mem_clon))

    # --- CÁLCULO DE DRIFTS (Espectral e Histórico) ---
    drifts = {
        "T1_gauge_leve":       drift(s0, s1),
        "T2_mutacion_permit":  drift(s0, s2),
        "T3_M2p5_rompe_loc":   drift(s0, s3),
        "T4_anderson_total":   drift(s0, s4),
        "T5_isomero_mem":      drift_mem,
    }

    # --- DRIFT TOPOLÓGICO INDEPENDIENTE (Espacio Betti) ---
    drift_topo_t3 = float(math.sqrt((b0_base - b0_t3)**2 + (b1_base - b1_t3)**2))
    drift_topo_t4 = float(math.sqrt((b0_base - b0_t4)**2 + (b1_base - b1_t4)**2))

    # --- CÁLCULO DE OMEGA DINÁMICO (Corrección de Errores) ---
    Ω = {k: compute_adaptive_omega(v, base_capacity=0.5) for k, v in drifts.items()}
    fase = {k: ("PRESERVADA" if v >= 1.0 else "ROTA") for k, v in Ω.items()}

    # --- CLASIFICACIÓN BORROMEO OFICIAL ---
    cpu_s = time.time() - t0
    F_total = 5 * 1200
    modo = classify_architecture(L_old=86400, L_new=cpu_s, F_old=1, F_new=F_total)

    # --- ESTADO TOPOLÓGICO INTEGRADO ---
    # Compara si la estructura de bucles (ciclos de homología) sobrevive al colapso de localidad
    if drift_topo_t3 < drift_topo_t4 and drifts["T3_M2p5_rompe_loc"] < drifts["T4_anderson_total"]:
        topo = "BOUND_STABLE_GHZ · Homología persistente blindada contra desorden local"
    else:
        topo = "UNLINKED_VORTEX · Colapso topológico completo"

    # --- CONSTRUCCIÓN DEL OBJETO DE EVIDENCIA CORREGIDO ---
    out = {
        "martillo": "functor_f_topo_v01_shannon_refinement",
        "layers": LAYERS, "width": WIDTH,
        "cpu_s": round(cpu_s, 3),
        "f_info": {
            "espectro_base_len": len(s0),
            "drifts_espectrales": drifts
        },
        "f_topo": {
            "betti_base": [b0_base, b1_base],
            "betti_t3_shuffled_loc": [b0_t3, b1_t3],
            "drift_topo_t3_M2p5": drift_topo_t3,
            "drift_topo_t4_anderson": drift_topo_t4,
            "status": topo
        },
        "omega_adaptive": {k: round(v, 4) for k, v in Ω.items()},
        "fase_firma": fase,
        "borromeo_clasificacion": modo
    }

    os.makedirs("evidence", exist_ok=True)
    path = "evidence/functor_f_topo_v01.json"
    with open(path, "w") as f:
        json.dump(out, f, indent=2)

    # --- IMPRESIÓN DE REPORTE ---
    print(f"\n⏱  CPU total de cálculo: {cpu_s:.4f}s")
    print(f"\n{'Transformación':<26}{'Drift':>10}{'Ω (Adapt)':>11}{'Fase':>12}")
    print("-" * 62)
    for k in drifts:
        print(f"{k:<26}{drifts[k]:>10.5f}{Ω[k]:>11.3f}{fase[k]:>12}")
    print(f"\n📊 Homología Betti Base  [B0={b0_base:.2f}, B1={b1_base:.2f}]")
    print(f"📉 Drift Topológico T3  [{drift_topo_t3:.4f}] vs T4 Anderson [{drift_topo_t4:.4f}]")
    print(f"\n🧬 f_topo  → {topo}")
    print(f"⚖️  Borromeo → {modo}")
    print(f"💾 Guardado → {path}")

if __name__ == "__main__":
    main()
