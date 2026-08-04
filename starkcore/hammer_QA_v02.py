#!/usr/bin/env python3
"""
STARKCORE HAMMER · QA v0.2 — MONTE CARLO PHASE CARTOGRAPHY
Formalización del espacio de firmas f = [f_topo, f_info, f_mem].
Somete el invariante estructural a un barrido estocástico de densidad (rho) y ruido.
Calcula la probabilidad empírica de preservación de identidad P(Omega > 1 | T).
"""
import os, json, time, math
import numpy as np
from starkcore.borromeo_validator import classify_architecture

# ---------------------------------------------------------------------------
# 1. Geometría Paramétrica StarkCore
# ---------------------------------------------------------------------------
def build_adj(layers=6, width=15, rho=0.78, loc=0.55, seed=None):
    """Construye la matriz de adyacencia dirigida por capas de M2.5."""
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

def shuffle_preserva_grado(A, layers=6, width=15, rng=None):
    """T3: Rompe la localidad |i-j| preservando capas y out-degree exacto."""
    B = np.zeros_like(A)
    def nid(l, w): return l * width + w
    for l in range(layers - 1):
        for w in range(width):
            u = nid(l, w)
            k = int(A[u].sum())
            if k == 0: continue
            pool = [nid(l + 1, w2) for w2 in range(width)]
            B[u, rng.choice(pool, size=k, replace=False)] = 1
    return B

def shuffle_rompe_todo(A, rng=None):
    """T4: Transición de Anderson total (Destrucción macroscópica)."""
    B = A.flatten().copy()
    rng.shuffle(B)
    return B.reshape(A.shape)

# ---------------------------------------------------------------------------
# 2. Complejo de Vietoris-Rips Espectral (H0, H1 Nativos)
# ---------------------------------------------------------------------------
def compute_spectral_homology(A, steps=8):
    """
    Extrae descriptores de homología filtrando el Hamiltoniano H = A + A^T.
    Normaliza las firmas Betti por el orden del sistema para garantizar adimensionalidad.
    """
    N = A.shape[0]
    H = A + A.T
    thresholds = np.linspace(H.min(), H.max(), steps)
    
    b0_acc = 0.0
    b1_acc = 0.0
    
    for t in thresholds:
        adj_t = (H >= t).astype(int)
        
        # Betti 0 (H0): Componentes conectados mediante búsqueda por proximidad
        visited = np.zeros(N, dtype=bool)
        components = 0
        for i in range(N):
            if not visited[i]:
                components += 1
                queue = [i]
                visited[i] = True
                while queue:
                    curr = queue.pop(0)
                    for neighbor in range(N):
                        if adj_t[curr, neighbor] == 1 and not visited[neighbor]:
                            visited[neighbor] = True
                            queue.append(neighbor)
        
        # Betti 1 (H1): Ciclos independientes no triviales (Complejo 1D)
        edges = np.sum(adj_t) // 2
        cycles = max(0, edges - N + components)
        
        b0_acc += components
        b1_acc += cycles
        
    return (b0_acc / steps) / N, (b1_acc / steps) / N

def get_f_info(A):
    """f_info: Espectro de autovalores normalizado por la norma L2."""
    H = A + A.T
    ev = np.linalg.eigvalsh(H)
    norm = np.linalg.norm(ev) + 1e-6
    return np.sort(ev) / norm

# ---------------------------------------------------------------------------
# 3. Métrica de Shannon para Canales de Identidad (Ω)
# ---------------------------------------------------------------------------
def evaluate_channel_omega(f_info_base, f_topo_base, f_info_trans, f_topo_trans, base_capacity=0.35):
    """
    Calcula el Drift compuesto adimensional en el espacio de firmas Sig.
    Aplica la ley de degradación de Shannon para dictaminar si Omega > 1.
    """
    d_info = float(np.linalg.norm(f_info_base - f_info_trans))
    d_topo = float(math.sqrt((f_topo_base[0] - f_topo_trans[0])**2 + (f_topo_base[1] - f_topo_trans[1])**2))
    
    # Drift total combinado (Espacio Métrico de la Firma)
    drift_total = d_info + d_topo
    
    if drift_total < 1e-6:
        return 999.0, drift_total
        
    # Capacidad efectiva penalizada por la entropía del desorden estructural
    capacity_eff = base_capacity / (1.0 + math.log1p(drift_total))
    omega = capacity_eff / drift_total
    return omega, drift_total

# ---------------------------------------------------------------------------
# 4. Núcleo del Barrido Estocástico (Monte Carlo)
# ---------------------------------------------------------------------------
def run_monte_carlo(samples=20, layers=6, width=15):
    print(f"[⚙️] Iniciando simulación de n={samples} muestras sobre espacio paramétrico...")
    master_rng = np.random.default_rng(42)
    
    # Rangos de fase para la densidad de acoplamiento (rho)
    rho_space = [0.30, 0.55, 0.78, 0.92]
    
    results_map = {rho: {"T1": [], "T3": [], "T4": []} for rho in rho_space}
    
    for rho in rho_space:
        for s in range(samples):
            # Inicializar semilla única por simulación histórica
            seed = int(master_rng.integers(1, 1000000))
            rng = np.random.default_rng(seed)
            
            # 1. Estado Base e Invariantes
            A0 = build_adj(layers=layers, width=width, rho=rho, seed=seed)
            fi0 = get_f_info(A0)
            ft0 = compute_spectral_homology(A0)
            
            # --- Transformación T1 (Ruido de Gauge Leve 2%) ---
            A1 = A0 + rng.uniform(-0.02, 0.02, A0.shape).astype(np.float32)
            fi1 = get_f_info(A1)
            ft1 = compute_spectral_homology(A1)
            o1, _ = evaluate_channel_omega(fi0, ft0, fi1, ft1)
            results_map[rho]["T1"].append(o1)
            
            # --- Transformación T3 (Martillo M2.5: Preserva grados, rompe localidad) ---
            A3 = shuffle_preserva_grado(A0, layers=layers, width=width, rng=rng)
            fi3 = get_f_info(A3)
            ft3 = compute_spectral_homology(A3)
            o3, _ = evaluate_channel_omega(fi0, ft0, fi3, ft3)
            results_map[rho]["T3"].append(o3)
            
            # --- Transformación T4 (Anderson Total: Ruptura macroscópica) ---
            A4 = shuffle_rompe_todo(A0, rng=rng)
            fi4 = get_f_info(A4)
            ft4 = compute_spectral_homology(A4)
            o4, _ = evaluate_channel_omega(fi0, ft0, fi4, ft4)
            results_map[rho]["T4"].append(o4)

    return results_map

# ---------------------------------------------------------------------------
# MAIN & Generación de Evidencia
# ---------------------------------------------------------------------------
def main():
    print("=" * 64)
    print("  STARKCORE HAMMER · QA v0.2 · CARTOGRAFÍA MONTE CARLO")
    print("=" * 64)
    t0 = time.time()
    
    # Ejecutamos un barrido controlado óptimo para UserLAnd (20 muestras por fase x 4 densidades)
    LAYERS, WIDTH = 6, 15
    samples_per_phase = 20
    data = run_monte_carlo(samples=samples_per_phase, layers=LAYERS, width=WIDTH)
    
    # Procesamiento estadístico de probabilidades P(Omega > 1)
    report = {}
    print(f"\n📊 MATRIZ DE PRESERVACIÓN DE IDENTIDAD: P(Ω > 1 | ρ)")
    print("-" * 64)
    print(f"{'ρ (Densidad)':<14}{'P(Ω>1 | T1)':<16}{'P(Ω>1 | T3)':<16}{'P(Ω>1 | T4)':<16}")
    print("-" * 64)
    
    for rho, transforms in data.items():
        p_t1 = float(np.mean([1.0 if x >= 1.0 else 0.0 for x in transforms["T1"]]))
        p_t3 = float(np.mean([1.0 if x >= 1.0 else 0.0 for x in transforms["T3"]]))
        p_t4 = float(np.mean([1.0 if x >= 1.0 else 0.0 for x in transforms["T4"]]))
        
        report[str(rho)] = {"P_T1": p_t1, "P_T3": p_t3, "P_T4": p_t4}
        print(f"{rho:<14.2f}{p_t1:<16.2f}{p_t3:<16.2f}{p_t4:<16.2f}")
        
    cpu_s = time.time() - t0
    F_total = samples_per_phase * len(data) * 3
    modo = classify_architecture(L_old=86400, L_new=cpu_s, F_old=1, F_new=F_total)
    
    # Determinar rigidez de la campana basándose en la brecha entre T3 y T4
    mean_p_t3 = np.mean([r["P_T3"] for r in report.values()])
    mean_p_t4 = np.mean([r["P_T4"] for r in report.values()])
    
    if mean_p_t3 > mean_p_t4:
        status_string = "ACERO CALIBRADO · Firma functorial inmune a desorden local difuso"
    else:
        status_string = "CRISTAL FRÁGIL · La interfaz colapsa de forma no lineal"
        
    out = {
        "martillo": "QA_v02_monte_carlo_cartography",
        "dimensiones": {"layers": LAYERS, "width": WIDTH, "total_nodos": LAYERS * WIDTH},
        "muestras_totales_computadas": F_total,
        "execution_cpu_seconds": round(cpu_s, 3),
        "cartografia_fases": report,
        "analisis_material": status_string,
        "borromeo_clasificacion": modo
    }
    
    os.makedirs("evidence", exist_ok=True)
    path = "evidence/hammer_QA_v02.json"
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
        
    print("-" * 64)
    print(f"🧬 Diagnóstico Estructural → {status_string}")
    print(f"⚖️  Borromeo Clasificación  → {modo}")
    print(f"💾 Cartografía salvada en  → {path}")
    print(f"⏱  Tiempo total de golpeo  → {cpu_s:.2f}s")

if __name__ == "__main__":
    main()
