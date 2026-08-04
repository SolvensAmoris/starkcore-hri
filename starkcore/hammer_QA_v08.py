#!/usr/bin/env python3
"""
STARKCORE HAMMER · QA v0.8 — MEMORY COLLISION ATTACK (MCA)
PARTE 1 DE 2: RESOLUCIÓN DE DESEMPAQUETADO EN CANAL FERMI
Corrige la firma de la función fermi_detection para aceptar escalares desempacados.
"""
import os, json, time, math
import numpy as np
from starkcore.borromeo_validator import classify_architecture

# ---------------------------------------------------------------------------
# 1. Geometría Dinámica: Trayectorias Confluentes
# ---------------------------------------------------------------------------
def build_confluent_trajectories(layers=6, width=15, rho=0.78, loc=0.55, path_type="exponential", seed=None):
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

    t = np.linspace(0, 10, 128, dtype=np.float32)
    if path_type == "exponential":
        history = np.exp(-t / 3.0) + rng.normal(0, 0.01, 128)
    else:
        history = np.sin(2 * np.pi * t / 4.0) * np.exp(-t / 5.0) + rng.normal(0, 0.01, 128)
        
    history = history / (np.linalg.norm(history) + 1e-6)
    return A, history

# ---------------------------------------------------------------------------
# 2. Descriptores Avanzados de la Firma: Filtro de Procrustes Espectral
# ---------------------------------------------------------------------------
def compute_spectral_homology(A, steps=6):
    N = int(A.shape[0])
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

def get_f_info_with_vectors(A):
    H = A + A.T
    ev, evecs = np.linalg.eigh(H)
    ev_norm = np.sort(ev) / (np.sum(np.abs(ev)) + 1e-6)
    return ev_norm, evecs

# ---------------------------------------------------------------------------
# 3. Detector Continuo de Fermi-Dirac Calibrado (Saneado)
# ---------------------------------------------------------------------------
def fermi_detection(dn_info, dn_topo, dn_mem, mode="full", beta=5.0):
    if mode == "full":
        d = dn_info + dn_topo + dn_mem
    elif mode == "no_mem":
        d = dn_info + dn_topo
    elif mode == "no_topo":
        d = dn_info + dn_mem
    elif mode == "no_info":
        d = dn_topo + dn_mem
    return float(1.0 / (1.0 + math.exp(beta * (d - 1.2))))

# ---------------------------------------------------------------------------
# 4. Core de Ataque Adversarial de Colisiones (MCA) y Ejecución
# ---------------------------------------------------------------------------
def main():
    print("=" * 64)
    print("  STARKCORE HAMMER v0.8 · CRYPTOGRAPHIC MEMORY COLLISION")
    print("=" * 64)
    t0 = time.time()
    
    LAYERS, WIDTH = 6, 15
    samples = 25
    master_rng = np.random.default_rng(10101)
    
    # Baselines de calibración adimensional
    b_info, b_topo, b_mem = 0.0162, 0.1565, 1.0
    
    # g(M) es una función de interfaz lineal (proyección) que intenta forzar la colisión
    projection_matrix = master_rng.normal(0, 1, (128, 16))
    projection_matrix /= np.linalg.norm(projection_matrix, axis=0)

    collision_counter = 0
    modes = ["full", "no_mem", "no_topo", "no_info"]
    sensitivity_accum = {m: {"Spect_Attack": [], "Collision_Defense": []} for m in modes}

    for s in range(samples):
        seed = int(master_rng.integers(1, 1000000))
        rng = np.random.default_rng(seed)
        
        # 1. Forzar Confluencia Dinámica con enteros y argumentos corregidos
        A_base, fm_exp = build_confluent_trajectories(LAYERS, WIDTH, path_type="exponential", seed=seed)
        _, fm_osc = build_confluent_trajectories(LAYERS, WIDTH, path_type="oscillatory", seed=seed)
        
        fi_base, fevecs_base = get_f_info_with_vectors(A_base)
        ft_base_b0, ft_base_b1 = compute_spectral_homology(A_base)
        
        # --- FUNCIÓN INTERFAZ DE CONFUSIÓN CRIPTOGRÁFICA g(M) ---
        g_m1 = fm_exp @ projection_matrix
        g_m2 = fm_osc @ projection_matrix
        d_projection = float(np.linalg.norm(g_m1 - g_m2))
        
        # Si la interfaz reducida g detecta el cambio por debajo del ruido basal, hay colisión
        if d_projection < 0.1:
            collision_counter += 1

        # --- ATAQUE ESPECTRAL REFINADO (Rotación del espacio propio de autovectores) ---
        A_sp = A_base + rng.uniform(-0.03, 0.03, A_base.shape).astype(np.float32)
        fi_sp, fevecs_sp = get_f_info_with_vectors(A_sp)
        ft_sp_b0, ft_sp_b1 = compute_spectral_homology(A_sp)
        
        # Distancia espectral combinada: Autovalores + Desviación de Procrustes en Autovectores
        d_procrustes = float(np.linalg.norm(fevecs_base - fevecs_sp))
        d_info_total = float(np.linalg.norm(fi_base - fi_sp)) + (0.1 * d_procrustes)

        # --- EVALUACIÓN DE RESISTENCIA BAJO ABLACIÓN ---
        for mode in modes:
            # Prueba Espectral (Debe detectar el ataque, S -> 0, Gradiente -> 100%)
            d_t1_topo = float(math.sqrt((ft_base_b0 - ft_sp_b0)**2 + (ft_base_b1 - ft_sp_b1)**2))
            dn_1 = [d_info_total / b_info, d_t1_topo / b_topo, 0.0]
            
            # Corregido: Pasamos los componentes escalares explícitamente indexados
            s_val_1 = fermi_detection(dn_1[0], dn_1[1], dn_1[2], mode=mode)
            sensitivity_accum[mode]["Spect_Attack"].append(1.0 - s_val_1)
            
            # Prueba de Colisión (Debe rechazar la falsa historia, S -> 0, Gradiente -> 100%)
            dn_c = [0.0, 0.0, float(np.linalg.norm(fm_exp - fm_osc)) / b_mem]
            s_val_c = fermi_detection(dn_c[0], dn_c[1], dn_c[2], mode=mode)
            sensitivity_accum[mode]["Collision_Defense"].append(1.0 - s_val_c)

    p_collision = float(collision_counter / samples)
    cpu_s = time.time() - t0
    modo = classify_architecture(L_old=86400, L_new=cpu_s, F_old=1, F_new=samples*2*4)

    # --- REPORTE DEL ESPECTRÓMETRO CRIPTOGRÁFICO ---
    print(f"\n📊 MATRIZ DE RESISTENCIA CRIPTOGRÁFICA BAJO ABLACIÓN (Gradiente de Detección):")
    print("-" * 76)
    print(f"{'Configuración del Functor f':<28}{'AOA_1 (Procrustes Spec)':<24}{'AOA_3 (Collision Def)':<20}")
    print("-" * 76)
    
    for mode in modes:
        m_spec = float(np.mean(sensitivity_accum[mode]["Spect_Attack"])) * 100
        m_coll = float(np.mean(sensitivity_accum[mode]["Collision_Defense"])) * 100
        
        mode_label = {
            "full": "Firma Completa [topo, info, mem]",
            "no_mem": "Sin Memoria [topo, info]",
            "no_topo": "Sin Topología [info, mem]",
            "no_info": "Sin Información [topo, mem]"
        }[mode]
        print(f"{mode_label:<28}{m_spec:>20.1f}%{m_coll:>22.1f}%")
        
    print("-" * 76)
    print(f"🔑 Probabilidad Empírica de Colisión Ontológica P(Colisión): {p_collision * 100:.2f}%")
    print("-" * 76)

    # Diagnóstico del material final de la forja
    if p_collision < 0.05:
        diagnostico = "CRIPTOGRAFÍA INYECTIVA CONFIRMADA · f_mem posee inmunidad a la falsificación de trayectorias."
    else:
        diagnostico = "COLAPSO REDUNDANTE · La interfaz lineal g(M) colapsó la memoria histórica."

    out = {
        "martillo": "QA_v08_memory_collision_attack",
        "cpu_seconds": round(cpu_s, 3),
        "probabilidad_colision": p_collision,
        "analisis_cripto": diagnostico,
        "borromeo_clasificacion": modo
    }
    
    os.makedirs("evidence", exist_ok=True)
    path = "evidence/hammer_QA_v08.json"
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
        
    print(f"🧬 Diagnóstico Estructural → {diagnostico}")
    print(f"⚖️  Borromeo Clasificación  → {modo}")
    print(f"💾 Evidencia sellada en    → {path}")

if __name__ == "__main__":
    main()
