import json, hashlib, time
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric import ed25519

# ==========================================
# 1. EL CANONICALIZER (Tu código blindado)
# ==========================================
class DAGCanonicalizer:
    def generar_hash_estructural(self, nodos: list, aristas: list) -> str:
        nodos_ordenados = sorted(nodos, key=lambda x: str(x.get("id", "")))
        aristas_ordenadas = sorted(aristas, key=lambda x: (str(x.get("from", "")), str(x.get("to", ""))))
        estructura_canonica = {"nodos": nodos_ordenados, "aristas": aristas_ordenadas}
        payload_bytes = json.dumps(estructura_canonica, sort_keys=True, separators=(",", ":")).encode('utf-8')
        return hashlib.sha256(payload_bytes).hexdigest()

# ==========================================
# 2. EL GATEWAY (Ahora con Validación de Topología)
# ==========================================
class Gateway:
    def __init__(self, pub_key_hex, expected_dag_hash):
        self.pub_key = ed25519.Ed25519PublicKey.from_public_bytes(bytes.fromhex(pub_key_hex))
        self.expected_dag_hash = expected_dag_hash # Hash de la topología autorizada

    def control_acceso(self, evento):
        print("  [Gateway] Validando firma criptográfica...")
        try:
            payload = evento["payload"]
            firma = bytes.fromhex(evento["firma"])
            payload_bytes = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
            self.pub_key.verify(firma, payload_bytes)
            print("    ✅ Firma Ed25519 válida.")
        except Exception:
            print("    ❌ [RECHAZADO] Firma inválida.")
            return False

        print("  [Gateway] Validando topología del sistema (DAG Hash)...")
        if payload.get("dag_hash") != self.expected_dag_hash:
            print(f"    ❌ [RECHAZADO] ¡Ataque de Topología! El DAG Hash no coincide.")
            print(f"       Esperado: {self.expected_dag_hash[:16]}...")
            print(f"       Recibido: {str(payload.get('dag_hash'))[:16]}...")
            return False
        
        print("    ✅ Topología validada. Coincide con el estado génesis.")
        
        if payload.get("accion") != "MODO_FAIL_CLOSED":
            print("    ❌ [RECHAZADO] Violación de Política (Π).")
            return False
            
        return True

# ==========================================
# 3. SIMULACIÓN
# ==========================================
print("============================================================")
print("   STARKCORE :: DAG INTEGRATION TEST")
print("============================================================")

cosmos = DAGCanonicalizer()

# Topología Autorizada (Génesis)
nodos_auth = [{"id": "runtime", "tipo": "core"}, {"id": "gateway", "tipo": "sec"}]
aristas_auth = [{"from": "runtime", "to": "gateway"}]
hash_auth = cosmos.generar_hash_estructural(nodos_auth, aristas_auth)

# Setup
priv = ed25519.Ed25519PrivateKey.generate()
pub_hex = priv.public_key().public_bytes_raw().hex()
gateway = Gateway(pub_hex, hash_auth)

# --- FLUJO 1: Evento Válido y Topología Correcta ---
payload_ok = {"dispositivo": "YAL-L21", "accion": "MODO_FAIL_CLOSED", "dag_hash": hash_auth}
firma_ok = priv.sign(json.dumps(payload_ok, sort_keys=True, separators=(",", ":")).encode()).hex()
evento_ok = {"payload": payload_ok, "firma": firma_ok}

print("\n--- FLUJO 1: EVENTO LEGÍTIMO (Topología Intacta) ---")
if gateway.control_acceso(evento_ok):
    print("🔥 [MUTACIÓN FÍSICA] Autorizada. El Jacobian procede.")

# --- FLUJO 2: Ataque de Topología (El hacker inyecta un nodo) ---
# El hacker modifica la topología pero mantiene la firma original (porque tiene la llave)
nodos_hack = nodos_auth + [{"id": "backdoor", "tipo": "malicious"}]
hash_hack = cosmos.generar_hash_estructural(nodos_hack, aristas_auth)

payload_hack = {"dispositivo": "YAL-L21", "accion": "MODO_FAIL_CLOSED", "dag_hash": hash_hack} # Inyecta el nuevo hash
firma_hack = priv.sign(json.dumps(payload_hack, sort_keys=True, separators=(",", ":")).encode()).hex()
evento_hack = {"payload": payload_hack, "firma": firma_hack}

print("\n--- FLUJO 2: EVENTO MALICIOSO (Inyección de Nodo Fantasma) ---")
if gateway.control_acceso(evento_hack):
    print("🔥 [MUTACIÓN FÍSICA] Autorizada.")
else:
    print("🚨 Flujo bloqueado. La topología del sistema no fue alterada.")

print("\n============================================================")
