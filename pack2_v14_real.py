#!/usr/bin/env python3
import math
from conjecture_lab_v14_final import fails_of as fails_v14

# Dominio oficial v14
DOMAIN = list(range(1, 30))

# Pack 2 basado en ARBOL FILOGENÉTICO v14 válido (solo ramas con proof)
# No inventamos, usamos lo que tu motor ya probó que evoluciona
pack2_real = [
    # nombre, expresion, operador origen, lore, rareza
    ("001-cubo-voraz", "n**3 < 3**n", "EXP2->3[implies]", "El cubo intentó comer exponencial", "Uncommon"),
    ("002-factorial-devorador", "2**n < math.factorial(n)", "WEAKEN_<[implies]+EXP", "Exponencial devorada por factorial", "Rare"),
    ("003-cuadrado-tragado", "n**2 < math.factorial(n)", "WEAKEN_<[implies]", "Cuadrado tragado por factorial", "Uncommon"),
    ("004-exponente-minimal", "n < 2**n", "ROOT", "Axioma verdadero desde n=1", "Common"),
    ("005-lineal-aplastado", "2*n < n**2", "WEAKEN_<[implies]", "La línea se dobló en n=2", "Common"),
    ("006-cuarta-dimension", "n**4 < 4**n", "EXP2->3[implies] x2", "4D no alcanzó a 4^n", "Ultra Rare"),
    ("007-torre-dominante", "2**n < n**n", "EXP2->3 + n^n", "Torre n^n aplasta 2^n", "Rare"),
    ("008-log-raiz", "math.log(n+1) < n**0.5", "LOG_BOTH[equiv]", "Log vs Raíz, batalla lenta", "Secret"),
    ("009-goodhart-trap", "n**2 < 2**n", "DIV_LEFT_ONLY_TRAMPA", "Trampa Goodhart curada v14", "Secret Trap"),
]

print("╔════════════════════════════════════════════════════════════╗")
print("🧪 PACK 2 REAL - BASADO EN MOTOR v14 CON PROOF")
print("╚════════════════════════════════════════════════════════════╝\n")

for fname, expr, op, lore, rareza in pack2_real:
    try:
        fails = fails_v14(expr, DOMAIN)
    except:
        # fallback si fails_of firma distinta
        fails = set(x for x in DOMAIN if not eval(expr, {"n": x, "math": math, "__builtins__": {}}))

    bar = "".join("█" if i in fails else "░" for i in range(1, 31))
    print(f"{fname}.jpg | {rareza} | {op}")
    print(f" expr: {expr}")
    print(f" fails: {sorted(fails)} len={len(fails)}")
    print(f" {bar}")
    print(f" lore: {lore}")
    print()

# Generar prompts de imagen 1066x1599 uniformes
print("\n=== PROMPTS FAKEMON TCG 1066x1599 ===\n")
for fname, expr, op, lore, rareza in pack2_real:
    print(f"{fname}:")
    print(f"Prompt: Fakemon TCG card, {lore}, mathematical creature, dark tech background #0e0e12, full art, highly detailed, 1066x1599, no border, no text, evolution aura, StarkCore style")
    print()
