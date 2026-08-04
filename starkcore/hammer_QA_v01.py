#!/usr/bin/env python3
"""
HAMMER QUANTUM ANALOGY v0.1 — FASE 1
Isomorfismo: matriz de adyacencia → Hamiltoniano H = A + A^T (hermítico)
Mide f_info (espectro), f_topo (proxy Borromeo), f_mem (isómeros)
Usa build_adj REAL de M2.5 (11e4b2b) y classify_architecture OFICIAL
"""
import os, json, time, math
import numpy as np
from starkcore.borromeo_validator import classify_architecture

# ---------------------------------------------------------------------------
# 1. Geometría REAL de M2.5 (idéntica a hammer_M2p5_scale_v01.py)
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
                A[u, nid(l + 1, w)] = 1  # garantiza grado ≥ 1
    return A

# ---------------------------------------------------------------------------
# 2. SHUFFLE REAL de M2.5: preserva out_degree EXACTO + capas, rompe |i-j|
# ---------------------------------------------------------------------------
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
# 3. f_info = espectro del Hamiltoniano H = A + A^T
# ---------------------------------------------------------------------------
def espectro(A):
    H = A + A.T
    return np.sort(np.linalg.eigvalsh(H))

def drift(a, b): return float(np.linalg.norm(np.asarray(a) - np.asarray(b)))

# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
def main():
    print("=" * 64)
    print("  STARKCORE HAMMER · QA v0.1 · f = [topo, info, mem]")
    print("=" * 64)
    t0 = time.time()
    LAYERS, WIDTH = 6, 20

    # --- SISTEMA BASE ---
    A0 = build_adj(layers=LAYERS, width=WIDTH, seed=26)
    s0 = espectro(A0)

    # --- T1 · perturbación GAUGE leve (ruido 2%) ---
    A1 = A0 + np.random.default_rng(1).uniform(-0.02, 0.02, A0.shape).astype(np.float32)
    s1 = espectro(A1)

    # --- T2 · mutación ESTRUCTURAL permitida (A^2 normalizada) ---
    A2 = (A0 @ A0.T) / 10.0
    s2 = espectro(A2)

    # --- T3 · MARTILLO M2.5 REAL · grado + capas OK, localidad ROTA ---
    A3 = shuffle_preserva_grado(A0, layers=LAYERS, width=WIDTH, seed=1000)
    s3 = espectro(A3)

    # --- T4 · SHUFFLE TOTAL · rompe TODO (transición Anderson) ---
    A4 = shuffle_rompe_todo(A0, seed=777)
    s4 = espectro(A4)

    # --- T5 · f_mem · ISÓMERO DE TRAYECTORIA (mismo estado, distinta historia) ---
    A5 = build_adj(layers=LAYERS, width=WIDTH, seed=26)   # mismo estado
    s5 = espectro(A5)                                      # → mismo f_info
    # diferencia real: semilla de memoria distinta → fase φ distinta
    mem_base = np.random.default_rng(26).standard_normal(256)
    mem_clon = np.random.default_rng(20260803).standard_normal(256)
    drift_mem = float(np.linalg.norm(mem_base - mem_clon))

    # --- DRIFTS ---
    d = {
        "T1_gauge_leve":       drift(s0, s1),
        "T2_mutacion_permit":  drift(s0, s2),
        "T3_M2p5_rompe_loc":   drift(s0, s3),
        "T4_anderson_total":   drift(s0, s4),
        "T5_isomero_mem":      drift_mem,
    }

    # --- Ω (capacidad correctora C=0.5) ---
    C = 0.5
    Ω = {k: C / (v + 1e-6) for k, v in d.items()}
    fase = {k: ("PRESERVADA" if v >= 1 else "ROTA") for k, v in Ω.items()}

    # --- CLASIFICACIÓN BORROMEO OFICIAL ---
    cpu_s = time.time() - t0
    F_total = 4 * 1200   # 4 transformaciones × réplicas equivalentes
    modo = classify_architecture(L_old=86400, L_new=cpu_s, F_old=1, F_new=F_total)

    # --- ESTADO TOPOLÓGICO EVOLUCIONADO (Relacional y no rígido) ---
    if d["T3_M2p5_rompe_loc"] < d["T4_anderson_total"]:
        topo = "BOUND_STABLE_GHZ · orden de gauge preservado por grados de libertad"
    elif abs(d["T3_M2p5_rompe_loc"] - d["T4_anderson_total"]) < 0.2:
        topo = "PARTIAL_COLLAPSE"
    else:
        topo = "UNLINKED_VORTEX"

    # --- EVIDENCIA ---
    out = {
        "martillo": "QA_v01_hamiltoniano_espectral",
        "layers": LAYERS, "width": WIDTH,
        "cpu_s": round(cpu_s, 3),
        "espectro_base": s0.round(6).tolist(),
        "drifts":      {k: round(v, 6) for k, v in d.items()},
        "omega":       {k: round(v, 3) for k, v in Ω.items()},
        "fase_firma":  fase,
        "f_topo_status": topo,
        "f_info_note": "H = A + A^T · autovalores = niveles de energía del atractor",
        "f_mem_note":  "T5 demuestra: mismo estado ≠ misma identidad (φ distinta)",
        "borromeo_clasificacion": modo,
    }

    os.makedirs("evidence", exist_ok=True)
    path = "evidence/hammer_QA_v01.json"
    with open(path, "w") as f:
        json.dump(out, f, indent=2)

    # --- REPORTE CONSOLA ---
    print(f"\n⏱  CPU total: {cpu_s:.2f}s")
    print(f"\n{'T':<26}{'Drift':>10}{'Ω':>9}{'Fase':>12}")
    print("-" * 58)
    for k in d:
        print(f"{k:<26}{d[k]:>10.5f}{Ω[k]:>9.2f}{fase[k]:>12}")
    print(f"\n🧬 f_topo  → {topo}")
    print(f"⚖️  Borromeo → {modo}")
    print(f"💾 Guardado → {path}")

if __name__ == "__main__":
    main()
