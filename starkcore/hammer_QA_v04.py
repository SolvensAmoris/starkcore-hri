#!/usr/bin/env python3
"""
STARKCORE HAMMER · QA v0.4 — IDENTOMETRY & SENSITIVITY SPECTROMETRY
Implementa un ataque de confusión aislado por componentes (Casos A, B y C).
Calcula las sensibilidades relativas (pesos w_i) y localiza la derivada crítica dP/d_rho.
"""
import os, json, time, math
import numpy as np
from starkcore.borromeo_validator import classify_architecture

# ---------------------------------------------------------------------------
# 1. Geometría Base Paramétrica
# ---------------------------------------------------------------------------
def build_adj(layers=6, width=15, rho=0.78, loc=0.55, seed=None):
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

# ---------------------------------------------------------------------------
# 2. Descriptores de la Firma Functorial f = [topo, info, mem]
# ---------------------------------------------------------------------------
def compute_spectral_homology(A, steps=6):
    N = A.shape[0]
    H = A + A.T
    thresholds = np.linspace(H.min(), H.max(), steps)
    b0_acc, b1_acc = 0.0, 0.0
    
    for t in thresholds:
        adj_t = (H >= t).astype(int)
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
        edges = np.sum(adj_t) // 2
        cycles = max(0, edges - N + components)
        b0_acc += components
        b1_acc += cycles
        
    return (b0_acc / steps) / N, (b1_acc / steps) / N

def get_f_info(A):
    H = A + A.T
    ev = np.linalg.eigvalsh(H)
    return np.sort(ev) / (np.linalg.norm(ev) + 1e-6)

# ---------------------------------------------------------------------------
# 3. Métricas del Canal Adaptativo de Shannon
# ---------------------------------------------------------------------------
def evaluate_isolated_drifts(fi0, ft0, fm0, fi1, ft1, fm1):
    """Retorna las distancias adimensionales aisladas por cada componente."""
    d_info = float(np.linalg.norm(fi0 - fi1))
    d_topo = float(math.sqrt((ft0[0] - ft1[0])**2 + (ft0[1] - ft1[1])**2))
    d_mem = float(np.linalg.norm(fm0 - fm1))
    return d_info, d_topo, d_mem

def is_survived(d_info, d_topo, d_mem, base_capacity=0.35):
    drift_total = d_info + d_topo + d_mem
    if drift_total < 1e-6: return True
    capacity_eff = base_capacity / (1.0 + math.log1p(drift_total))
    return (capacity_eff / drift_total) >= 1.0

# ---------------------------------------------------------------------------
# 4. Espectrómetro de Confusión Monte Carlo
# ---------------------------------------------------------------------------
def run_spectrometry_sweep(samples=15, layers=6, width=15):
    master_rng = np.random.default_rng(42)
    rho_space = np.linspace(0.15, 0.95, 15)
    results = {}
    
    print(f"[🔬] Analizando espectrometría de confusión en {len(rho_space)} fases...")
    
    for rho in rho_space:
        case_a, case_b, case_c = [], [], []
        
        for s in range(samples):
            seed = int(master_rng.integers(1, 1000000))
            rng = np.random.default_rng(seed)
            
            fm0 = rng.standard_normal(128)
            A0 = build_adj(layers=layers, width=width, rho=rho, seed=seed)
            fi0 = get_f_info(A0)
            ft0 = compute_spectral_homology(A0)
            
            # --- CASO A: Mutación Isospectral Pura (fi1 ≈ fi0, altera ft) ---
            H = A0 + A0.T
            evals, evecs = np.linalg.eigh(H)
            idx = np.arange(len(evals))
            rng.shuffle(idx[:len(idx)//3])  # Barajado sutil limitado
            H_fake = evecs[:, idx] @ np.diag(evals) @ evecs[:, idx].T
            A_caseA = np.clip(np.triu(H_fake, k=1), 0, 1).astype(np.float32)
            fi_a = get_f_info(A_caseA)
            ft_a = compute_spectral_homology(A_caseA)
            case_a.append(evaluate_isolated_drifts(fi0, ft0, fm0, fi_a, ft_a, fm0))
            
            # --- CASO B: Mutación Isomórfica Pura (Altera fi, ft1 ≈ ft0) ---
            # Perturbación simétrica de pesos arista por arista que mantiene la estructura binaria de conectividad
            A_caseB = A0 * rng.uniform(0.8, 1.2, A0.shape).astype(np.float32)
            fi_b = get_f_info(A_caseB)
            ft_b = compute_spectral_homology(A_caseB)
            case_b.append(evaluate_isolated_drifts(fi0, ft0, fm0, fi_b, ft_b, fm0))
            
            # --- CASO C: Ruptura de Memoria Pura (fi, ft idénticos, fm disjunta) ---
            fm_fake = rng.standard_normal(128)
            case_c.append(evaluate_isolated_drifts(fi0, ft0, fm0, fi0, ft0, fm_fake))
            
        results[rho] = {"A": case_a, "B": case_b, "C": case_c}
        
    return rho_space, results

# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
def main():
    print("=" * 64)
    print("  STARKCORE HAMMER v0.4 · IDENTOMETRY SENSITIVITY MATRIX")
    print("=" * 64)
    t0 = time.time()
    
    LAYERS, WIDTH = 6, 15
    samples = 15
    rho_space, raw_data = run_spectrometry_sweep(samples=samples, layers=LAYERS, width=WIDTH)
    
    # Acumuladores para determinar la sensibilidad global w_i (Gradiente medio de Drift)
    w_info_acc, w_topo_acc, w_mem_acc = [], [], []
    p_survival_curve = []
    
    print(f"\n🔬 ANÁLISIS DE CONFUSIÓN (Drifts Promedio por Componente)")
    print("-" * 74)
    print(f"{'ρ':<6}{'Caso A (Δinfo)':<22}{'Caso B (Δtopo)':<22}{'Caso C (Δmem)':<22}")
    print("-" * 74)
    
    for rho in rho_space:
        data = raw_data[rho]
        
        # Caso A promedio de drifts
        ma_info = np.mean([x[0] for x in data["A"]])
        ma_topo = np.mean([x[1] for x in data["A"]])
        
        # Caso B promedio de drifts
        mb_info = np.mean([x[0] for x in data["B"]])
        mb_topo = np.mean([x[1] for x in data["B"]])
        
        # Caso C promedio de drifts
        mc_mem = np.mean([x[2] for x in data["C"]])
        
        # Guardamos magnitudes relativas de respuesta
        w_info_acc.append(ma_info)
        w_topo_acc.append(mb_topo)
        w_mem_acc.append(mc_mem)
        
        # Calculamos la probabilidad de supervivencia global combinada para rastrear la fase
        survivals = [1.0 if is_survived(x[0], x[1], x[2]) else 0.0 for x in data["B"]]
        p_survival_curve.append(np.mean(survivals))
        
        print(f"{rho:<6.2f}{ma_info:.4f} (topo:{ma_topo:.2f})   {mb_topo:.4f} (info:{mb_info:.2f})   {mc_mem:.4f}")

    # 1. Cálculo de pesos normados del Espectrómetro de Identidad
    total_mass = np.sum(w_info_acc) + np.sum(w_topo_acc) + np.sum(w_mem_acc) + 1e-6
    w_info = float(np.sum(w_info_acc) / total_mass)
    w_topo = float(np.sum(w_topo_acc) / total_mass)
    w_mem = float(np.sum(w_mem_acc) / total_mass)
    
    # 2. Localización matemática de la fase crítica por gradiente máximo (dP / d_rho)
    p_diff = np.diff(p_survival_curve)
    if len(p_diff) > 0 and np.any(p_diff != 0):
        idx_crit = int(np.argmax(np.abs(p_diff)))
        rho_c = float(rho_space[idx_crit])
    else:
        rho_c = None
        
    cpu_s = time.time() - t0
    F_total = samples * len(rho_space) * 3
    modo = classify_architecture(L_old=86400, L_new=cpu_s, F_old=1, F_new=F_total)
    
    report = {
        "martillo": "QA_v04_identometry_spectrometry",
        "pesos_espectro_identidad": {"w_info": w_info, "w_topo": w_topo, "w_mem": w_mem},
        "rho_critica_gradiente": rho_c,
        "survival_curve_b": p_survival_curve,
        "cpu_seconds": round(cpu_s, 3),
        "borromeo_clasificacion": modo
    }
    
    os.makedirs("evidence", exist_ok=True)
    path = "evidence/hammer_QA_v04.json"
    with open(path, "w") as f:
        json.dump(report, f, indent=2)
        
    print("-" * 74)
    print(f"⚖️  FÓRMULA VECTORIAL STARKCORE: ΔIdentity = {w_topo:.2f}Δtopo + {w_info:.2f}Δinfo + {w_mem:.2f}Δmem")
    print(f"📉 Densidad Crítica Calculada (Máx Gradiente) ρ_c: {f'{rho_c:.2f}' if rho_c else 'Fase Homogénea'}")
    print(f"⚙️  Borromeo Clasificación  → {modo}")
    print(f"💾 Espectrometría guardada en → {path}")

if __name__ == "__main__":
    main()
