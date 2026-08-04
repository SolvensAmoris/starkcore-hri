#!/usr/bin/env python3
"""
STARKCORE HAMMER · QA v0.5 — BASAL NORMALIZATION & FUNCTOR ABLATION
Ajusta las distancias de los canales usando un baseline estocástico adimensional.
Ejecuta pruebas de ablación sistemática para medir la cooperación real f_info, f_topo y f_mem.
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
# 2. Descriptores de la Firma Functorial Normalizados
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
# 3. Calibración Estocástica de Línea de Base (Anti-Contrabando de Escala)
# ---------------------------------------------------------------------------
def compute_baselines(layers=6, width=15, rho=0.78, samples=5):
    """Calcula la distancia euclidiana esperada ante mutaciones estándar por canal."""
    rng = np.random.default_rng(12345)
    d_infos, d_topos, d_mems = [], [], []
    
    for _ in range(samples):
        A0 = build_adj(layers, width, rho, seed=int(rng.integers(1, 100000)))
        fi0 = get_f_info(A0)
        ft0 = compute_spectral_homology(A0)
        fm0 = rng.standard_normal(128)
        
        # Perturbación estocástica estándar
        A1 = A0 + rng.uniform(-0.02, 0.02, A0.shape).astype(np.float32)
        fi1 = get_f_info(A1)
        ft1 = compute_spectral_homology(A1)
        fm1 = rng.standard_normal(128)
        
        d_infos.append(float(np.linalg.norm(fi0 - fi1)))
        d_topos.append(float(math.sqrt((ft0[0] - ft1[0])**2 + (ft0[1] - ft1[1])**2)))
        d_mems.append(float(np.linalg.norm(fm0 - fm1)))
        
    return np.mean(d_infos) + 1e-6, np.mean(d_topos) + 1e-6, np.mean(d_mems) + 1e-6

# ---------------------------------------------------------------------------
# 4. Evaluación de Canales Con y Sin Ablación
# ---------------------------------------------------------------------------
def evaluate_identity(drifts_norm, mode="full", base_capacity=0.35):
    """
    Evalúa la supervivencia bajo diferentes configuraciones de ablación.
    drifts_norm = [dn_info, dn_topo, dn_mem]
    """
    dn_info, dn_topo, dn_mem = drifts_norm
    
    if mode == "full":
        d_total = dn_info + dn_topo + dn_mem
    elif mode == "no_mem":
        d_total = dn_info + dn_topo
    elif mode == "no_topo":
        d_total = dn_info + dn_mem
    elif mode == "no_info":
        d_total = dn_topo + dn_mem
        
    if d_total < 1e-6: return True
    capacity_eff = base_capacity / (1.0 + math.log1p(d_total))
    return (capacity_eff / d_total) >= 1.0

# ---------------------------------------------------------------------------
# 5. Core Experimental Monte Carlo v0.5
# ---------------------------------------------------------------------------
def run_ablation_matrix(samples=15, layers=6, width=15):
    master_rng = np.random.default_rng(42)
    rho_space = [0.30, 0.55, 0.78, 0.92]
    
    # 1. Pre-calcular baselines globales para el balanceo
    b_info, b_topo, b_mem = compute_baselines(layers, width, 0.78, samples=5)
    
    # Estructura para registrar drifts calibrados globales
    global_weights = {"info": [], "topo": [], "mem": []}
    
    # Estructura de métricas de precisión de ablación frente a ataques adversariales masivos
    # Buscamos medir cuántas veces detectamos la ruptura (True = Detectó rotura, lo correcto en ataque)
    accuracy_report = {mode: {"total": 0, "detected": 0} for mode in ["full", "no_mem", "no_topo", "no_info"]}
    
    for rho in rho_space:
        for s in range(samples):
            seed = int(master_rng.integers(1, 1000000))
            rng = np.random.default_rng(seed)
            
            fm0 = rng.standard_normal(128)
            A0 = build_adj(layers=layers, width=width, rho=rho, seed=seed)
            fi0 = get_f_info(A0)
            ft0 = compute_spectral_homology(A0)
            
            # Simulamos un ataque mixto de confusión radical para estresar el identómetro
            A_att = A0 * rng.uniform(0.7, 1.3, A0.shape).astype(np.float32)
            fi1 = get_f_info(A_att)
            ft1 = compute_spectral_homology(A_att)
            fm1 = rng.standard_normal(128)
            
            # Distancias puras
            d_i = float(np.linalg.norm(fi0 - fi1))
            d_t = float(math.sqrt((ft0[0] - ft1[0])**2 + (ft0[1] - ft1[1])**2))
            d_m = float(np.linalg.norm(fm0 - fm1))
            
            # NORMALIZACIÓN GEOMÉTRICA ADIMENSIONAL
            dn_i = d_i / b_info
            dn_t = d_t / b_topo
            dn_m = d_m / b_mem
            
            global_weights["info"].append(dn_i)
            global_weights["topo"].append(dn_t)
            global_weights["mem"].append(dn_m)
            
            # Pruebas cíclicas de ablación: Comprobar quién ve primero el colapso (Retorna False si cayó)
            for mode in accuracy_report.keys():
                survived = evaluate_identity([dn_i, dn_t, dn_m], mode=mode)
                accuracy_report[mode]["total"] += 1
                if not survived: # Si detectó correctamente la pérdida de identidad
                    accuracy_report[mode]["detected"] += 1
                    
    return global_weights, accuracy_report, (b_info, b_topo, b_mem)

# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
def main():
    print("=" * 64)
    print("  STARKCORE HAMMER v0.5 · LÍNEA DE BASE Y MATRIZ DE ABLACIÓN")
    print("=" * 64)
    t0 = time.time()
    
    LAYERS, WIDTH = 6, 15
    weights, ablation, baselines = run_ablation_matrix(samples=20, layers=LAYERS, width=WIDTH)
    
    # Calcular balance de masa real en el espacio normalizado
    sm = np.mean(weights["info"]) + np.mean(weights["topo"]) + np.mean(weights["mem"]) + 1e-6
    w_info = float(np.mean(weights["info"]) / sm)
    w_topo = float(np.mean(weights["topo"]) / sm)
    w_mem = float(np.mean(weights["mem"]) / sm)
    
    cpu_s = time.time() - t0
    modo = classify_architecture(L_old=86400, L_new=cpu_s, F_old=1, F_new=2400)
    
    print(f"\n⚙️  LÍNEAS DE BASE ESTIMADAS (Escala geométrica interna):")
    print(f"   -> Base f_info: {baselines[0]:.6f}")
    print(f"   -> Base f_topo: {baselines[1]:.6f}")
    print(f"   -> Base f_mem : {baselines[2]:.6f} (¡Las 16 toneladas corregidas!)")
    
    print(f"\n⚖️  BALANZA VECTORIAL CALIBRADA:")
    print(f"   ΔIdentity = {w_topo:.2f}Δtopo + {w_info:.2f}Δinfo + {w_mem:.2f}Δmem")
    
    print(f"\n📊 EFICACIA DE DETECCIÓN BAJO ABLACIÓN (Sensibilidad al ataque):")
    print("-" * 64)
    print(f"{'Configuración del Functor f':<30}{'Precisión de Ruptura (Recall)':<25}")
    print("-" * 64)
    
    for mode, counts in ablation.items():
        accuracy = float(counts["detected"] / counts["total"])
        mode_label = {
            "full": "Firma Completa [topo, info, mem]",
            "no_mem": "Ablación de Memoria [topo, info]",
            "no_topo": "Ablación de Topología [info, mem]",
            "no_info": "Ablación de Información [topo, mem]"
        }[mode]
        print(f"{mode_label:<30}{accuracy * 100:>20.2f}%")
        
    out = {
        "martillo": "QA_v05_basal_normalization_ablation",
        "baselines_utilizados": {"info": baselines[0], "topo": baselines[1], "mem": baselines[2]},
        "pesos_adimensionales": {"w_topo": w_topo, "w_info": w_info, "w_mem": w_mem},
        "rendimiento_ablacion": ablation,
        "cpu_seconds": round(cpu_s, 3),
        "borromeo_clasificacion": modo
    }
    
    os.makedirs("evidence", exist_ok=True)
    path = "evidence/hammer_QA_v05.json"
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
        
    print("-" * 64)
    print(f"💾 Espectrometría libre de sesgo guardada en: {path}")
    print(f"⏱  Tiempo total de yunque: {cpu_s:.2f}s")

if __name__ == "__main__":
    main()
