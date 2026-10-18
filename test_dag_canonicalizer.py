import json
import hashlib

# ==========================================
# MÓDULO COSMOS: DAG CANONICALIZER
# ==========================================

class DAGCanonicalizer:
    def __init__(self):
        pass

    def generar_hash_estructural(self, nodos: list, aristas: list) -> str:
        """
        Toma nodos y aristas desordenados, los canonicaliza 
        y genera un Hash SHA-256 determinista.
        """
        # 1. Canonicalización de Nodos: Ordenar por ID
        nodos_ordenados = sorted(nodos, key=lambda x: x["id"])
        
        # 2. Canonicalización de Aristas: Ordenar por origen y luego destino
        aristas_ordenadas = sorted(aristas, key=lambda x: (x["from"], x["to"]))
        
        # 3. Estructura Canónica
        estructura_canonica = {
            "nodos": nodos_ordenados,
            "aristas": aristas_ordenadas
        }
        
        # 4. Serialización Determinista (sort_keys para asegurar orden de llaves en JSON)
        payload_bytes = json.dumps(estructura_canonica, sort_keys=True, separators=(",", ":")).encode('utf-8')
        
        # 5. Hash Criptográfico
        return hashlib.sha256(payload_bytes).hexdigest()

# ==========================================
# PRUEBAS DE FÍSICA DE SOFTWARE
# ==========================================

print("============================================================")
print("   STARKCORE :: DAG CANONICALIZER TEST")
print("============================================================")

cosmos = DAGCanonicalizer()

# --- GRAFO 1: Representación A (Desordenado) ---
nodos_A = [
    {"id": "runtime", "tipo": "core"},
    {"id": "gateway", "tipo": "security"},
    {"id": "jacobian", "tipo": "state"}
]
aristas_A = [
    {"from": "runtime", "to": "gateway"},
    {"from": "gateway", "to": "jacobian"}
]

# --- GRAFO 1: Representación B (Mismos datos, orden caótico) ---
nodos_B = [
    {"tipo": "state", "id": "jacobian"}, # Atributos invertidos, nodo al final
    {"id": "runtime", "tipo": "core"},
    {"id": "gateway", "tipo": "security"}
]
aristas_B = [
    {"to": "jacobian", "from": "gateway"}, # Aristas invertidas
    {"to": "gateway", "from": "runtime"}
]

# --- GRAFO 2: Representación C (Alterado estructuralmente) ---
# El Jacobian ya no depende del Gateway, ahora depende del Runtime.
nodos_C = nodos_A
aristas_C = [
    {"from": "runtime", "to": "gateway"},
    {"from": "runtime", "to": "jacobian"} # <-- ATAQUE ESTRUCTURAL
]

# Ejecutamos los hashes
hash_A = cosmos.generar_hash_estructural(nodos_A, aristas_A)
hash_B = cosmos.generar_hash_estructural(nodos_B, aristas_B)
hash_C = cosmos.generar_hash_estructural(nodos_C, aristas_C)

print(f"\n[Grafo A] Hash: {hash_A}")
print(f"[Grafo B] Hash: {hash_B}")
print(f"[Grafo C] Hash: {hash_C}")

# ==========================================
# VEREDICTO
# ==========================================
print("\n--- VEREDICTO DE CANONICALIZACIÓN ---")

# Test 1: Mismo grafo, distinto orden -> Mismo Hash
if hash_A == hash_B:
    print("✅ TEST 1 PASS: Representaciones desordenadas (A y B) producen el MISMO Hash Estructural.")
else:
    print("❌ TEST 1 FAIL: La canonicalización falló. El orden afectó el hash.")

# Test 2: Grafo alterado -> Distinto Hash
if hash_A != hash_C:
    print("✅ TEST 2 PASS: Alteración en el grafo (C) produce un Hash Estructural DIFERENTE.")
    print("   -> El sistema detectó la inyección de la arista 'runtime -> jacobian'.")
else:
    print("❌ TEST 2 FAIL: El grafo alterado produjo el mismo hash. ¡Peligro!")

print("\n============================================================")
