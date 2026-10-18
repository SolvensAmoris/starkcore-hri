import json
import hashlib

class DAGCanonicalizer:
    def generar_hash_estructural(self, nodos: list, aristas: list) -> str:
        # Canonicalización estricta
        nodos_ordenados = sorted(nodos, key=lambda x: str(x.get("id", "")))
        aristas_ordenadas = sorted(aristas, key=lambda x: (str(x.get("from", "")), str(x.get("to", ""))))
        
        estructura_canonica = {
            "nodos": nodos_ordenados,
            "aristas": aristas_ordenadas
        }
        
        payload_bytes = json.dumps(estructura_canonica, sort_keys=True, separators=(",", ":")).encode('utf-8')
        return hashlib.sha256(payload_bytes).hexdigest()

cosmos = DAGCanonicalizer()

print("============================================================")
print("   STARKCORE :: DAG CANONICALIZER - EDGE CASES")
print("============================================================")

# --- BASE ---
nodos_base = [{"id": "A", "tipo": "core"}, {"id": "B", "tipo": "sec"}]
aristas_base = [{"from": "A", "to": "B"}]
hash_base = cosmos.generar_hash_estructural(nodos_base, aristas_base)
print(f"\n[Base] Hash: {hash_base}")

# --- TEST 1: Ataque de Atributo (Cambiar un dato interno del nodo) ---
# El atacante deja la misma topología, pero altera el rol del nodo B.
nodos_atributo = [{"id": "A", "tipo": "core"}, {"id": "B", "tipo": "malicious_override"}]
hash_atributo = cosmos.generar_hash_estructural(nodos_atributo, aristas_base)
print(f"\n[TEST 1: Atributo Alterado] Hash: {hash_atributo}")
if hash_base != hash_atributo:
    print("✅ PASS: La alteración de metadatos internos fue detectada.")

# --- TEST 2: Inyección de Nodo Fantasma ---
# El atacante añade un nodo no autorizado a la red.
nodos_fantasma = nodos_base + [{"id": "C", "tipo": "backdoor"}]
hash_fantasma = cosmos.generar_hash_estructural(nodos_fantasma, aristas_base)
print(f"\n[TEST 2: Nodo Inyectado] Hash: {hash_fantasma}")
if hash_base != hash_fantasma:
    print("✅ PASS: La inyección de un nodo fantasma rompió el hash.")

# --- TEST 3: Ataque de Tipo de Dato (Type Confusion) ---
# El atacante intenta romper el sorting pasando un ID numérico en lugar de string.
try:
    nodos_type_confusion = [{"id": 123, "tipo": "core"}, {"id": "B", "tipo": "sec"}]
    hash_type = cosmos.generar_hash_estructural(nodos_type_confusion, aristas_base)
    print(f"\n[TEST 3: Type Confusion] Hash: {hash_type}")
    print("✅ PASS: El sistema manejó el ID numérico sin colapsar (gracias al str() en el sort).")
except Exception as e:
    print(f"\n❌ FAIL: El sistema colapsó ante type confusion: {e}")

# --- TEST 4: Grafo Vacío ---
# Un atacante envía un payload vacío para intentar un bypass.
hash_vacio = cosmos.generar_hash_estructural([], [])
print(f"\n[TEST 4: Grafo Vacío] Hash: {hash_vacio}")
if hash_vacio != hash_base:
    print("✅ PASS: El grafo vacío tiene un hash único (no colisiona con la base).")

print("\n============================================================")
