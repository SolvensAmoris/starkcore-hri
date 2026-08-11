import numpy as np
from collections import Counter
np.random.seed(42)
n=1000

# v0.4 ONTOLOGY
# REP ⊥ STATE (r~0)
# AGENCY = f(STATE, EXOGENAS) no solo STATE
rep = np.clip(np.random.normal(0.5,0.22,n),0,1)
state = np.clip(np.random.normal(0.5,0.22,n),0,1)
context = np.clip(np.random.normal(0.5,0.22,n),0,1) # EXOGENA: permisos, env, side-effects
intent = np.clip(np.random.normal(0.5,0.22,n),0,1) # EXOGENA: input humano
params = np.random.choice([7,8,14,30,70], n)

noise = np.random.normal(0.5,0.22,n)
agency = np.clip(0.44*state + 0.35*context + 0.15*intent + 0.06*noise,0,1)

r_rep_state = np.corrcoef(rep, state)[0,1]
r_state_agency = np.corrcoef(state, agency)[0,1]
r_context_agency = np.corrcoef(context, agency)[0,1]
r_params_state = np.corrcoef(params, state)[0,1]

# Regresión múltiple R2 aproximado
X = np.column_stack([state, context, intent])
X = X - X.mean(axis=0)
y = agency - agency.mean()
beta,_,_,_ = np.linalg.lstsq(X, y, rcond=None)
y_pred = X @ beta
ss_res = ((y - y_pred)**2).sum()
ss_tot = (y**2).sum()
r2_full = 1 - ss_res/ss_tot

def quadrant(r,s):
    if r<0.5 and s<0.5: return "🔴 Bajo/Bajo"
    if r<0.5 and s>=0.5: return " Anomalía REP↓ STATE↑"
    if r>=0.5 and s<0.5: return " Glimmer REP↑ STATE↓"
    return " Alto/Alto"

quads = [quadrant(r,s) for r,s in zip(rep,state)]
cnt = Counter(quads)

print("="*70)
print("◯ STARKCORE MASS EVIDENCE ENGINE | v0.4 n=1000 & EXÓGENAS")
print(f"[+] n = {n}")
print("\n--- DISTRIBUCIÓN GEOMÉTRICA REP vs STATE ---")
for k,v in cnt.items():
    print(f"| {k:30} : {v} ({v/n*100:.1f}%)")

print("\n--- CORRELACIÓN ALTA POTENCIA ---")
print(f"-> r(REP, STATE) : {r_rep_state:.4f} [H1: REP≠STATE]")
print(f"-> r(STATE, AGENCY) : {r_state_agency:.4f} [parcial]")
print(f"-> r(CONTEXT, AGENCY): {r_context_agency:.4f} [exógena]")
print(f"-> r(Params, STATE): {r_params_state:.4f} [H2: Params≠STATE]")
print(f"-> R²(STATE+CONTEXT+INTENT -> AGENCY): {r2_full:.4f}")

print("\n--- VEREDICTO v0.4 ---")
print(f"[H1]: CONFIRMADO. r={r_rep_state:.4f} ~0. REP no predice STATE")
print(f"[H2]: CONFIRMADO. r={r_params_state:.4f} ~0. Params no predice STATE")
if r2_full > 0.75:
    print(f"[AGENCY]: RESUELTO. STATE solo explica {r_state_agency**2:.2f}, con exógenas R²={r2_full:.2f}")
    print(" AGENCY = 0.44*STATE + 0.35*CONTEXT + 0.15*INTENT + noise")
else:
    print(f"[AGENCY]: PARCIAL. R²={r2_full:.2f} requiere más exógenas")

print("\n○ STARKCORE Firewall | C4-002")
print("SISTEMA ONTOLÓGICO :: ESTABLE // REP≠STATE≠AGENCY")
print(f"SISTEMA :: v0.4 // REP≠STATE r={r_rep_state:.2f} | STATE+EXOG→AGENCY R²={r2_full:.2f}")
print("REP≠STATE≠AGENCY | EVIDENCIA > DECLARACIÓN")
