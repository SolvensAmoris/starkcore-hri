#!/usr/bin/env python3
"""
STARKCORE HAMMER · QA v0.6 — ADVERSARIAL ORTHOGONAL ATTACK (AOA)
PARTE 1 DE 2: INFRAESTRUCTURA CORREGIDA DE COMPONENTES BETTI
Corrige el desempaquetado de tuplas en el espacio métrico de f_topo y el indexado NumPy.
"""
import os, json, time, math
import numpy as np
from starkcore.borromeo_validator import classify_architecture

# ---------------------------------------------------------------------------
# 1. Geometría Base Paramétrica StarkCore
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
        
    return float((b0_acc / steps) / N), float((b1_acc / steps) / N)

def get_f_info(A):
    H = A + A.T
    ev = np.linalg.eigvalsh(H)
    return np.sort(ev) / (np.linalg.norm(ev) + 1e-6)

# ---------------------------------------------------------------------------
# 3. Servidor de Calibración de Líneas de Base Estocásticas
# ---------------------------------------------------------------------------
def compute_baselines(layers=6, width=15, rho=0.78):
    rng = np.random.default_rng(999)
    d_infos, d_topos, d_mems = [], [], []
    for _ in range(5):
        A0 = build_adj(layers, width, rho, seed=int(rng.integers(1, 100000)))
        fi0 = get_f_info(A0)
        ft0_b0, ft0_b1 = compute_spectral_homology(A0)
        fm0 = rng.standard_normal(128)
        
        A1 = A0 + rng.uniform(-0.01, 0.01, A0.shape).astype(np.float32)
        fi1 = get_f_info(A1)
        ft1_b0, ft1_b1 = compute_spectral_homology(A1)
        fm1 = rng.standard_normal(128)
        
        d_infos.append(float(np.linalg.norm(fi0 - fi1)))
        d_topos.append(float(math.sqrt((ft0_b0 - ft1_b0)**2 + (ft0_b1 - ft1_b1)**2)))
        d_mems.append(float(np.linalg.norm(fm0 - fm1)))
    return np.mean(d_infos) + 1e-6, np.mean(d_topos) + 1e-6, np.mean(d_mems) + 1e-6

# ---------------------------------------------------------------------------
# 4. Ataques Quirúrgicos Ortogonales (AOA)
# ---------------------------------------------------------------------------
def attack_spectral_only(A, rng):
    H = A + A.T
    evals, evecs = np.linalg.eigh(H)
    evals_fake = evals * (1.0 + 0.15 * np.sin(np.linspace(0, math.pi, len(evals))))
    H_fake = evecs @ np.diag(evals_fake) @ evecs.T
    A_fake = np.clip(np.triu(H_fake, k=1), 0, 1).astype(np.float32)
    return A_fake

def attack_topo_only(A, rng):
    B = A.copy()
    idx = np.where(B == 1)
    # idx[0] son filas, idx[1] son columnas. Desempaquetado real del grafo binario
    num_edges = len(idx[0])
    if num_edges > 4:
        p_idx = rng.permutation(num_edges)
        for i in range(min(15, num_edges // 2 - 1)):
            u1, v1 = idx[0][p_idx[i]], idx[1][p_idx[i]]
            u2, v2 = idx[0][p_idx[i+1]], idx[1][p_idx[i+1]]
            B[u1, v1], B[u2, v2] = 0, 0
            B[u1, v2], B[u2, v1] = 1, 1
    return B

def evaluate_ablation(drifts_norm, mode="full", threshold=1.0):
    dn_info, dn_topo, dn_mem = drifts_norm
    if mode == "full":
        d = dn_info + dn_topo + dn_mem
    elif mode == "no_mem":
        d = dn_info + dn_topo
    elif mode == "no_topo":
        d = dn_info + dn_mem
    elif mode == "no_info":
        d = dn_topo + dn_mem
    return d < threshold

# ---------------------------------------------------------------------------
# 6. Simulación de Matriz Ortogonal y Reporte
# ---------------------------------------------------------------------------
def main():
    print("=" * 64)
    print("  STARKCORE HAMMER v0.6 · ADVERSARIAL ORTHOGONAL ATTACK")
    print("=" * 64)
    t0 = time.time()
    
    LAYERS, WIDTH = 6, 15
    samples = 20
    master_rng = np.random.default_rng(888)
    
    b_info, b_topo, b_mem = compute_baselines(LAYERS, WIDTH, 0.78)
    
    matrix_report = {
        mode: {"AOA_1_Spectral": 0, "AOA_2_Topo": 0, "AOA_3_History": 0, "total": 0}
        for mode in ["full", "no_mem", "no_topo", "no_info"]
    }
    
    for s in range(samples):
        seed = int(master_rng.integers(1, 1000000))
        rng = np.random.default_rng(seed)
        
        fm0 = rng.standard_normal(128)
        A0 = build_adj(LAYERS, WIDTH, rho=0.75, seed=seed)
        fi0 = get_f_info(A0)
        ft0_b0, ft0_b1 = compute_spectral_homology(A0)
        
        # --- EJECUCIÓN DE ATAQUES FILTRADOS ---
        A_sp = attack_spectral_only(A0, rng)
        fi_sp = get_f_info(A_sp)
        ft_sp_b0, ft_sp_b1 = compute_spectral_homology(A_sp)
        
        A_tp = attack_topo_only(A0, rng)
        fi_tp = get_f_info(A_tp)
        ft_tp_b0, ft_tp_b1 = compute_spectral_homology(A_tp)
        
        fm_fake = rng.standard_normal(128)
        
        # --- MATRIZ DE COMPROBACIÓN DE ABLACIÓN ---
        for mode in matrix_report.keys():
            matrix_report[mode]["total"] += 1
            
            # Evaluación ante AOA_1 (Spectral)
            d_t1_topo = float(math.sqrt((ft0_b0 - ft_sp_b0)**2 + (ft0_b1 - ft_sp_b1)**2))
            dn_1 = [float(np.linalg.norm(fi0 - fi_sp)) / b_info, d_t1_topo / b_topo, 0.0]
            if not evaluate_ablation(dn_1, mode=mode):
                matrix_report[mode]["AOA_1_Spectral"] += 1
                
            # Evaluación ante AOA_2 (Topo)
            d_t2_topo = float(math.sqrt((ft0_b0 - ft_tp_b0)**2 + (ft0_b1 - ft_tp_b1)**2))
            dn_2 = [float(np.linalg.norm(fi0 - fi_tp)) / b_info, d_t2_topo / b_topo, 0.0]
            if not evaluate_ablation(dn_2, mode=mode):
                matrix_report[mode]["AOA_2_Topo"] += 1
                
            # Evaluación ante AOA_3 (History)
            dn_3 = [0.0, 0.0, float(np.linalg.norm(fm0 - fm_fake)) / b_mem]
            if not evaluate_ablation(dn_3, mode=mode):
                matrix_report[mode]["AOA_3_History"] += 1

    cpu_s = time.time() - t0
    modo = classify_architecture(L_old=86400, L_new=cpu_s, F_old=1, F_new=samples*3*4)

    # --- IMPRESIÓN DE RESULTADOS ---
    print(f"\n📊 MATRIZ DE DETECCIÓN ORTOGONAL DE LA RUPTURA (Recall de Seguridad):")
    print("-" * 76)
    print(f"{'Configuración del Functor f':<28}{'AOA_1 (Spect)':<15}{'AOA_2 (Topo)':<15}{'AOA_3 (Hist)':<15}")
    print("-" * 76)
    
    summary_data = {}
    for mode in ["full", "no_mem", "no_topo", "no_info"]:
        tot = matrix_report[mode]["total"]
        r1 = (matrix_report[mode]["AOA_1_Spectral"] / tot) * 100
        r2 = (matrix_report[mode]["AOA_2_Topo"] / tot) * 100
        r3 = (matrix_report[mode]["AOA_3_History"] / tot) * 100
        summary_data[mode] = {"spectral": r1, "topo": r2, "history": r3}
        
        mode_label = {
            "full": "Firma [topo, info, mem]",
            "no_mem": "Sin Memoria [topo, info]",
            "no_topo": "Sin Topología [info, mem]",
            "no_info": "Sin Información [topo, mem]"
        }[mode]
        print(f"{mode_label:<28}{r1:>11.1f}%{r2:>14.1f}%{r3:>14.1f}%")

    print("-" * 76)
    if summary_data["no_mem"]["history"] == 0.0 and summary_data["full"]["history"] == 100.0:
        diagnostico = "SINERGIA CONFIRMADA · Los componentes miden dimensiones independientes. f_mem es inmune a la foto de estado."
    else:
        diagnostico = "ANALISIS COMPLETADO · Revisar firmas parciales de blindaje."

    out = {
        "martillo": "QA_v06_adversarial_orthogonal_attack",
        "muestras": samples,
        "cpu_seconds": round(cpu_s, 3),
        "matriz_sensibilidad": summary_data,
        "diagnostico_laboratorio": diagnostico,
        "borromeo_clasificacion": modo
    }
    
    os.makedirs("evidence", exist_ok=True)
    path = "evidence/hammer_QA_v06.json"
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
        
    print(f"🧬 Diagnóstico Estructural → {diagnostico}")
    print(f"⚖️  Borromeo Clasificación  → {modo}")
    print(f"💾 Evidencia sellada en    → {path}")

if __name__ == "__main__":
    main()
