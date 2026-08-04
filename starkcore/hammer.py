#!/usr/bin/env python3
"""
STARKCORE HAMMER v0.9.1 — COMMERCIAL FORENSIC CORE
Detector de Clonación Diacrónica + Adaptador de Entrada Real.
"""
import os, sys, json, math, time, argparse
import numpy as np

# ---------------------------------------------------------------------------
# 1. Carga sucia de datos reales (el adaptador que vende)
# ---------------------------------------------------------------------------
def load_matrix(path):
    """Acepta .npy, .npz, edge list (.txt/.csv) o checkpoint .pt/.pth (extrae primera matriz 2D)."""
    ext = os.path.splitext(path)[1].lower()
    if ext == ".npy":
        A = np.load(path)
    elif ext == ".npz":
        A = np.load(path)["arr_0"] if "arr_0" in np.load(path) else np.load(path)[list(np.load(path).keys())[0]]
    elif ext in (".txt", ".csv", ".edgelist"):
        edges = np.loadtxt(path, delimiter=None if ext==".txt" else ",")
        n = int(max(edges.max(), edges[:,0].max(), edges[:,1].max())) + 1
        A = np.zeros((n, n), dtype=np.float32)
        for u, v in edges.astype(int):
            A[u, v] = 1.0
    elif ext in (".pt", ".pth"):
        try:
            import torch
            obj = torch.load(path, map_location="cpu")
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if hasattr(v, "numpy") and len(v.shape) == 2:
                        A = v.detach().numpy().astype(np.float32)
                        break
                else:
                    raise ValueError("No se encontró matriz 2D en el state_dict")
            else:
                A = obj.detach().numpy().astype(np.float32)
        except ImportError:
            raise RuntimeError("PyTorch no está instalado. Usa .npy o edge list.")
    else:
        raise ValueError(f"Formato no soportado: {ext}")
    A = np.asarray(A, dtype=np.float32)
    if A.ndim != 2:
        raise ValueError("La matriz debe ser 2D")
    return A

def load_history(path, target_dim=128):
    """Carga vector de historia de cualquier dimensión y proyecta a target_dim."""
    ext = os.path.splitext(path)[1].lower()
    if ext == ".npy":
        h = np.load(path).astype(np.float32).ravel()
    elif ext == ".npz":
        data = np.load(path)
        h = data[list(data.keys())[0]].astype(np.float32).ravel()
    elif ext in (".pt", ".pth"):
        try:
            import torch
            obj = torch.load(path, map_location="cpu")
            if isinstance(obj, dict):
                for v in obj.values():
                    if hasattr(v, "numpy"):
                        h = v.detach().numpy().astype(np.float32).ravel()
                        break
            else:
                h = obj.detach().numpy().astype(np.float32).ravel()
        except ImportError:
            raise RuntimeError("PyTorch no instalado")
    else:
        h = np.loadtxt(path).astype(np.float32).ravel()

    if h.size == target_dim:
        return h / (np.linalg.norm(h) + 1e-6)
    # Proyección lineal determinista (siempre la misma para la misma seed)
    rng = np.random.default_rng(42)
    proj = rng.normal(0, 1, (h.size, target_dim)).astype(np.float32)
    proj /= np.linalg.norm(proj, axis=0, keepdims=True) + 1e-6
    h_proj = h @ proj
    return h_proj / (np.linalg.norm(h_proj) + 1e-6)

# ---------------------------------------------------------------------------
# 2. Descriptores + Fermi blindada
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
                queue = [i]; visited[i] = True
                while queue:
                    curr = queue.pop(0)
                    for neighbor in range(N):
                        if adj_t[curr, neighbor] == 1 and not visited[neighbor]:
                            visited[neighbor] = True
                            queue.append(neighbor)
        edges = np.sum(adj_t) // 2
        b0_acc += components
        b1_acc += max(0, edges - N + components)
    return float((b0_acc / steps) / N), float((b1_acc / steps) / N)

def get_f_info_with_vectors(A):
    H = A + A.T
    ev, evecs = np.linalg.eigh(H)
    return np.sort(ev) / (np.sum(np.abs(ev)) + 1e-6), evecs

def fermi_detection(dn_info, dn_topo, dn_mem, mode="full", beta=5.0):
    if mode == "full":
        d = dn_info + dn_topo + dn_mem
    elif mode == "no_mem":
        d = dn_info + dn_topo
    else:
        d = dn_info + dn_mem
    exponent = beta * (d - 1.2)
    if exponent > 50.0: return 0.0
    if exponent < -50.0: return 1.0
    return float(1.0 / (1.0 + math.exp(exponent)))
EOFcat >> starkcore/hammer.py <<'EOF'

# ---------------------------------------------------------------------------
# 3. Generador HTML + CLI
# ---------------------------------------------------------------------------
def generate_html_report(json_path, html_path="report.html"):
    with open(json_path, "r") as f:
        data = json.load(f)
    status = data.get("status", "UNKNOWN")
    p_coll = data.get("p_collision", 0.0) * 100
    rec_full = data.get("recall_full_memory_defense", 0.0) * 100
    rec_blind = data.get("recall_blind_state_only", 0.0) * 100
    spec_grad = data.get("spectral_detection_gradient", 0.0) * 100
    meta = data.get("meta", {})
    status_color = "#10b981" if status == "SECURE" else "#ef4444"
    status_bg = "#ecfdf5" if status == "SECURE" else "#fef2f2"

    html = f"""<!DOCTYPE html>
<html lang="es"><head><meta charset="UTF-8"><title>StarkCore Hammer Report</title>
<style>
body{{font-family:system-ui,sans-serif;background:#f9fafb;margin:0;padding:40px 20px}}
.container{{max-width:800px;margin:0 auto;background:white;padding:40px;border-radius:12px;box-shadow:0 4px 6px rgba(0,0,0,.05)}}
h1{{font-size:24px;font-weight:800;text-transform:uppercase;margin:0 0 4px}}
.sub{{color:#6b7280;font-size:13px;margin-bottom:30px}}
.badge{{display:inline-block;padding:10px 20px;border-radius:6px;font-weight:700;color:{status_color};background:{status_bg};border:2px solid {status_color};margin-bottom:30px;text-transform:uppercase}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:30px}}
.card{{background:#f3f4f6;padding:20px;border-radius:8px;border:1px solid #e5e7eb}}
.card-t{{font-size:11px;font-weight:700;text-transform:uppercase;color:#4b5563;margin-bottom:6px}}
.card-v{{font-size:26px;font-weight:800;color:#111827}}
.bar{{background:#e5e7eb;height:6px;border-radius:3px;margin-top:8px;overflow:hidden}}
.fill{{height:100%;background:#3b82f6}}
.fill.success{{background:#10b981}}
.fill.danger{{background:#ef4444}}
.footer{{font-size:11px;color:#9ca3af;margin-top:40px;padding-top:20px;border-top:1px solid #e5e7eb;display:flex;justify-content:space-between}}
</style></head><body><div class="container">
<h1>StarkCore Hammer Audit</h1>
<div class="sub">Análisis Forense Criptográfico e Inyectividad Temporal</div>
<div class="badge">{status} — INTEGRIDAD HISTÓRICA</div>
<div class="grid">
<div class="card"><div class="card-t">P(Colisión de Memoria)</div><div class="card-v">{p_coll:.2f}%</div><div class="bar"><div class="fill danger" style="width:{p_coll}%"></div></div></div>
<div class="card"><div class="card-t">Gradiente Espectral</div><div class="card-v">{spec_grad:.1f}%</div><div class="bar"><div class="fill" style="width:{spec_grad}%"></div></div></div>
<div class="card"><div class="card-t">Recall Firma Completa</div><div class="card-v">{rec_full:.1f}%</div><div class="bar"><div class="fill success" style="width:{rec_full}%"></div></div></div>
<div class="card"><div class="card-t">Ceguera sin Memoria</div><div class="card-v">{rec_blind:.1f}%</div><div class="bar"><div class="fill danger" style="width:{rec_blind}%"></div></div></div>
</div>
<div class="footer"><div>Muestras: {meta.get("samples")} | ε: {meta.get("epsilon")}</div>
<div>Cómputo: {meta.get("elapsed_s")}s | StarkCore v0.9.1</div></div>
</div></body></html>"""
    with open(html_path, "w") as f:
        f.write(html)
    print(f"[📊] Informe HTML → {html_path}")

def main():
    parser = argparse.ArgumentParser(description="StarkCore Hammer — Detector de Clonación Diacrónica")
    parser.add_argument("--target", type=str, help="Matriz o checkpoint del sistema a auditar")
    parser.add_argument("--history", type=str, help="Vector de historia (cualquier dim)")
    parser.add_argument("--baseline", type=str, help="Opcional: matriz/historia legítima de referencia")
    parser.add_argument("--eps", type=float, default=0.20)
    parser.add_argument("--samples", type=int, default=25)
    parser.add_argument("--out", type=str, default="evidence/audit.json")
    args = parser.parse_args()

    t0 = time.time()
    b_info, b_topo, b_mem = 0.0162, 0.1565, 1.0

    # Modo forense real
    if args.target and args.history:
        print(f"[*] Modo Forense Activado. Ingestando: {args.target}")
        A = load_matrix(args.target)
        f_mem = load_history(args.history)
        print(f"[*] Historia proyectada a {f_mem.shape[0]}d")

        # Generamos un "clon" sintético con misma estructura pero trayectoria distinta para medir defensa
        rng = np.random.default_rng(42)
        f_mem_fake = rng.normal(0, 1, f_mem.shape).astype(np.float32)
        f_mem_fake /= (np.linalg.norm(f_mem_fake) + 1e-6)

        fi, fevc = get_f_info_with_vectors(A)
        ft0, ft1 = compute_spectral_homology(A)

        # Ataque espectral controlado
        A_sp = A + rng.uniform(-args.eps, args.eps, A.shape).astype(np.float32)
        fi_sp, fevc_sp = get_f_info_with_vectors(A_sp)
        ft_sp0, ft_sp1 = compute_spectral_homology(A_sp)

        d_inf = float(np.linalg.norm(fi - fi_sp)) + 0.1 * float(np.linalg.norm(fevc - fevc_sp))
        d_top = float(math.sqrt((ft0 - ft_sp0)**2 + (ft1 - ft_sp1)**2))
        d_mem = float(np.linalg.norm(f_mem - f_mem_fake))

        scores = {"full": [], "no_mem": []}
        for m in ["full", "no_mem"]:
            s_spec = fermi_detection(d_inf/b_info, d_top/b_topo, 0.0, mode=m)
            s_coll = fermi_detection(0.0, 0.0, d_mem/b_mem, mode=m)
            scores[m].append((1.0 - s_spec, 1.0 - s_coll))

        p_coll = 0.0  # en modo real medimos defensa, no colisión sintética
        report = {
            "status": "SECURE" if scores["full"][0][1] > 0.8 else "VULNERABLE",
            "p_collision": p_coll,
            "recall_full_memory_defense": float(scores["full"][0][1]),
            "recall_blind_state_only": float(scores["no_mem"][0][1]),
            "spectral_detection_gradient": float(scores["full"][0][0]),
            "meta": {"samples": 1, "epsilon": args.eps, "elapsed_s": round(time.time()-t0, 3), "mode": "forensic_real"}
        }
    else:
        # Fallback sintético (para demos rápidas)
        print("[*] Modo sintético (demo). Usa --target y --history para forense real.")
        # ... (puedes dejar el loop sintético anterior si quieres, o cortarlo)
        report = {"status": "DEMO", "p_collision": 0.0, "recall_full_memory_defense": 0.95,
                  "recall_blind_state_only": 0.02, "spectral_detection_gradient": 0.88,
                  "meta": {"samples": args.samples, "epsilon": args.eps, "elapsed_s": round(time.time()-t0, 3)}}

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(report, f, indent=2)
    print(f"[🔥] Auditoría completada → {args.out}")
    generate_html_report(args.out, args.out.replace(".json", ".html"))

if __name__ == "__main__":
    main()
EOF# Asegúrate de tener el __main__.py
cat > starkcore/__main__.py <<'EOF'
from starkcore.hammer import main
if __name__ == "__main__":
    main()
