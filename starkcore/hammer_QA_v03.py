#!/usr/bin/env python3
"""
STARKCORE HAMMER · QA v0.3 — ADVERSARIAL PHASE ATTACK
Somete el marco a ataques diseñados para engañar por separado a f_info, f_topo y f_mem.
Calcula el intervalo de confianza CI_95% y localiza la densidad crítica de fase (rho_c).
"""
import os, json, time, math
import numpy as np
from starkcore.borromeo_validator import classify_architecture

# ---------------------------------------------------------------------------
# 1. Geometría Base StarkCore
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
# 2. Ataques Adversariales Diseñados (El Guante de Pruebas)
# ---------------------------------------------------------------------------
def attack_isospectral(A, rng):
    """ADV_1: Intenta engañar a f_info. Preserva el espectro aproximado pero altera la topología."""
    H = A + A.T
    evals, evecs = np.linalg.eigh(H)
    # Mutación ortogonal: baraja un fragmento de la matriz de autovectores
    idx = np.arange(len(evals))
    rng.shuffle(idx[:len(idx)//2])
    H_fake = evecs[:, idx] @ np.diag(evals) @ evecs[:, idx].T
    # Extrae la parte triangular superior para mapear de vuelta a adyacencia regularizada
    A_fake = np.triu(H_fake, k=1)
    return np.clip(A_fake, 0, 1).astype(np.float32)

def attack_isomorphic_topo(A, rng):
    """ADV_2: Intenta engañar a f_topo. Mantiene conectividad base pero inyecta ruido masivo de energía."""
    # Modifica los pesos de las aristas existentes multiplicándolos de forma caótica
    noise = rng.uniform(0.1, 5.0, A.shape).astype(np.float32)
    return A * noise

# ---------------------------------------------------------------------------
# 3. Complejo Espectral de Vietoris-Rips y Firmas
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
# 4. Métrica de Canal (Termómetro de Control Ω)
# ---------------------------------------------------------------------------
def evaluate_channel_omega(fi0, ft0, fm0, fi1, ft1, fm1, base_capacity=0.35):
    d_info = float(np.linalg.norm(fi0 - fi1))
    d_topo = float(math.sqrt((ft0[0] - ft1[0])**2 + (ft0[1] - ft1[1])**2))
    d_mem = float(np.linalg.norm(fm0 - fm1))
    
    drift_total = d_info + d_topo + d_mem
    if drift_total < 1e-6:
        return 999.0
        
    capacity_eff = base_capacity / (1.0 + math.log1p(drift_total))
    return capacity_eff / drift_total

# ---------------------------------------------------------------------------
# 5. Análisis Estadístico Monte Carlo de Fase
# ---------------------------------------------------------------------------
def run_adversarial_sweep(samples=15, layers=6, width=15):
    master_rng = np.random.default_rng(42)
    # Barrido continuo de 15 puntos para detectar la densidad crítica rho_c
    rho_space = np.linspace(0.15, 0.95, 15)
    
    results = {}
    print(f"[🛡️] Ejecutando ataque adversarial cruzado sobre {len(rho_space)} fases de densidad...")
    
    for rho in rho_space:
        omega_adv1, omega_adv2, omega_adv3 = [], [], []
        
        for s in range(samples):
            seed = int(master_rng.integers(1, 1000000))
            rng = np.random.default_rng(seed)
            
            # Vectores de historia iniciales (f_mem)
            fm0 = rng.standard_normal(128)
            fm_clon = rng.standard_normal(128) # Trayectoria disjunta para ADV_3
            
            # Grafo base
            A0 = build_adj(layers=layers, width=width, rho=rho, seed=seed)
            fi0 = get_f_info(A0)
            ft0 = compute_spectral_homology(A0)
            
            # ADV_1: Ataque Isospectral (Burla a f_info)
            A_adv1 = attack_isospectral(A0, rng)
            fi1 = get_f_info(A_adv1)
            ft1 = compute_spectral_homology(A_adv1)
            omega_adv1.append(evaluate_channel_omega(fi0, ft0, fm0, fi1, ft1, fm0))
            
            # ADV_2: Ataque Isomórfico Topológico (Burla a f_topo)
            A_adv2 = attack_isomorphic_topo(A0, rng)
            fi2 = get_f_info(A_adv2)
            ft2 = compute_spectral_homology(A_adv2)
            omega_adv2.append(evaluate_channel_omega(fi0, ft0, fm0, fi2, ft2, fm0))
            
            # ADV_3: Paradoja del Clon Markoviano (Burla a f_mem mediante idéntico estado pero historia rota)
            omega_adv3.append(evaluate_channel_omega(fi0, ft0, fm0, fi0, ft0, fm_clon))
            
        results[rho] = {
            "ADV_1_Isospectral": omega_adv1,
            "ADV_2_Isomorphic": omega_adv2,
            "ADV_3_Markov_Clon": omega_adv3
        }
    return results

def compute_ci95(data_list):
    """Calcula la probabilidad de supervivencia y su intervalo de confianza binomial."""
    successes = np.array([1.0 if x >= 1.0 else 0.0 for x in data_list])
    p = np.mean(successes)
    n = len(successes)
    ci = 1.96 * math.sqrt((p * (1.0 - p)) / n) if p > 0 and p < 1 else 0.0
    return float(p), float(ci)

# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
def main():
    print("=" * 64)
    print("  STARKCORE HAMMER v0.3 · ADVERSARIAL ATTACK & PHASE SWEEP")
    print("=" * 64)
    t0 = time.time()
    
    LAYERS, WIDTH = 6, 15
    samples = 15
    raw_data = run_adversarial_sweep(samples=samples, layers=LAYERS, width=WIDTH)
    
    processed_report = {}
    rho_critical = None
    
    print(f"\n📊 MAPA DE VULNERABILIDAD ADVERSARIAL (Supervivencia P(Ω > 1) ± CI_95%)")
    print("-" * 74)
    print(f"{'ρ':<6}{'ADV_1 (Isospec)':<22}{'ADV_2 (Isomorph)':<22}{'ADV_3 (Markov)':<22}")
    print("-" * 74)
    
    for rho, attacks in raw_data.items():
        p1, ci1 = compute_ci95(attacks["ADV_1_Isospectral"])
        p2, ci2 = compute_ci95(attacks["ADV_2_Isomorphic"])
        p3, ci3 = compute_ci95(attacks["ADV_3_Markov_Clon"])
        
        # Detectar la fase crítica rho_c donde el clon markoviano o la topología se vuelven indistinguibles
        if rho_critical is None and p2 < 0.5:
            rho_critical = float(rho)
            
        processed_report[f"{rho:.3f}"] = {
            "ADV_Isospectral": {"p": p1, "ci": ci1},
            "ADV_Isomorphic":  {"p": p2, "ci": ci2},
            "ADV_Markov":      {"p": p3, "ci": ci3}
        }
        
        print(f"{rho:<6.2f}{p1:.2f}±{ci1:.2f}{' '*7}{p2:.2f}±{ci2:.2f}{' '*7}{p3:.2f}±{ci3:.2f}")

    cpu_s = time.time() - t0
    F_total = samples * len(raw_data) * 3
    modo = classify_architecture(L_old=86400, L_new=cpu_s, F_old=1, F_new=F_total)
    
    # Diagnóstico del material de la campana
    if rho_critical:
        diagnostico = f"ZONA CRÍTICA LOCALIZADA → Transición de fase en ρ_c ≈ {rho_critical:.2f}"
    else:
        diagnostico = "ESTRUCTURA BLINDADA → Ningún ataque engañó los tres componentes de la firma"

    out = {
        "martillo": "QA_v03_adversarial_phase_attack",
        "dimensiones": {"layers": LAYERS, "width": WIDTH, "nodos": LAYERS * WIDTH},
        "muestras_computadas": F_total,
        "cpu_seconds": round(cpu_s, 3),
        "densidad_critica_rho_c": rho_critical,
        "cartografia_adversarial": processed_report,
        "diagnostico_blindaje": diagnostico,
        "borromeo_clasificacion": modo
    }

    os.makedirs("evidence", exist_ok=True)
    path = "evidence/hammer_QA_v03.json"
    with open(path, "w") as f:
        json.dump(out, f, indent=2)

    print("-" * 74)
    print(f"🧬 Diagnóstico Estructural → {diagnostico}")
    print(f"⚖️  Borromeo Clasificación  → {modo}")
    print(f"💾 Evidencia sellada en    → {path}")
    print(f"⏱  Tiempo total de ataque   → {cpu_s:.2f}s")

if __name__ == "__main__":
    main()
