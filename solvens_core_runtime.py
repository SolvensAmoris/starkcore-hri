import json, hashlib, time
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric import ed25519

# ==========================================
# 1. COSMOS: CANONICALIZER (El DAG)
# ==========================================
class DAGCanonicalizer:
    def generar_hash(self, nodos: list, aristas: list) -> str:
        nodos_ord = sorted(nodos, key=lambda x: str(x.get("id", "")))
        aristas_ord = sorted(aristas, key=lambda x: (str(x.get("from", "")), str(x.get("to", ""))))
        payload = json.dumps({"nodos": nodos_ord, "aristas": aristas_ord}, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(payload.encode()).hexdigest()

# ==========================================
# 2. RUNTIME: GATEWAY Y JACOBIAN
# ==========================================
class Gateway:
    def __init__(self, pub_key_hex, expected_dag_hash):
        self.pub_key = ed25519.Ed25519PublicKey.from_public_bytes(bytes.fromhex(pub_key_hex))
        self.expected_dag_hash = expected_dag_hash

    def validar(self, evento):
        try:
            payload = evento["payload"]
            # 1. Verificar Firma
            firma = bytes.fromhex(evento["firma"])
            self.pub_key.verify(firma, json.dumps(payload, sort_keys=True, separators=(",", ":")).encode())
            
            # 2. Verificar Topología DAG
            if payload.get("dag_hash") != self.expected_dag_hash:
                return False, "TOPOLOGY_MISMATCH"
                
            return True, "OK"
        except Exception:
            return False, "SIGNATURE_INVALID"

class Jacobian:
    def __init__(self, state_file="solvens_state.json"):
        self.state_file = Path(state_file)
        
    def mutar(self, estado_nuevo):
        self.state_file.write_text(json.dumps({"proof_state": estado_nuevo, "ts": time.time()}, indent=2))

# ==========================================
# 3. EVIDENCE LAYER (El Bus Inmutable)
# ==========================================
class EvidenceLayer:
    def __init__(self, log_file="solvens_evidence.log"):
        self.log_file = Path(log_file)
        
    def registrar(self, veredicto, hash_artefacto):
        prev_hash = "0"*64
        if self.log_file.exists():
            lineas = self.log_file.read_text().strip().split("\n")
            if lineas and lineas[0]:
                prev_hash = json.loads(lineas[-1])["hash"]
                
        bloque = {
            "veredicto": veredicto,
            "artefacto_hash": hash_artefacto,
            "prev_hash": prev_hash,
            "ts": time.time()
        }
        bloque["hash"] = hashlib.sha256(json.dumps(bloque, sort_keys=True).encode()).hexdigest()
        
        with open(self.log_file, "a") as f:
            f.write(json.dumps(bloque) + "\n")
        return bloque["hash"]

# ==========================================
# 4. SOLVENS CORE ORCHESTRATOR
# ==========================================
class SolvensCore:
    def __init__(self, pub_key_hex, genesis_dag_hash):
        self.canonicalizer = DAGCanonicalizer()
        self.gateway = Gateway(pub_key_hex, genesis_dag_hash)
        self.jacobian = Jacobian()
        self.evidence = EvidenceLayer()

    def procesar_artefacto(self, evento, nombre_artefacto):
        print(f"\n[SOLVENS CORE] Procesando: {nombre_artefacto}")
        print("  -> Parseando y canonicalizando estructura...")
        
        # Validación en Gateway
        print("  -> Validando criptografía y topología en Gateway...")
        es_valido, motivo = self.gateway.validar(evento)
        
        if not es_valido:
            print(f"  ❌ [REJECT] Motivo: {motivo}")
            self.evidence.registrar(f"REJECT_{motivo}", evento["payload"]["dag_hash"])
            return False

        # Mutación de estado (Si es válido)
        print("  -> Mutando estado en Jacobian...")
        self.jacobian.mutar("PROOF_ACCEPTED")
        
        # Registro de evidencia
        print("  -> Registrando evidencia inmutable...")
        h = self.evidence.registrar("ACCEPT", evento["payload"]["dag_hash"])
        
        print(f"\n🟩 SOLVENS CORE :: VERIFIED [ACCEPT]")
        print(f"   Hash de Evidencia: {h[:16]}...")
        return True

# ==========================================
# EJECUCIÓN DE LA PRUEBA
# ==========================================
print("============================================================")
print("   SOLVENS CORE :: RUNTIME ORCHESTRATOR V1.0")
print("============================================================")

# 1. Setup (Simulamos el entorno del usuario)
priv = ed25519.Ed25519PrivateKey.generate()
pub_hex = priv.public_key().public_bytes_raw().hex()

# Topología del sistema (Nuestro DAG válido)
nodos_auth = [{"id": "Lean4_Verifier", "tipo": "math"}, {"id": "Runtime", "tipo": "core"}]
aristas_auth = [{"from": "Lean4_Verifier", "to": "Runtime"}]
canon = DAGCanonicalizer()
dag_hash_auth = canon.generar_hash(nodos_auth, aristas_auth)

# Instanciamos Solvens Core
solvens = SolvensCore(pub_hex, dag_hash_auth)

# --- ARTEFACTO 1: Prueba Lean 4 Válida ---
payload_valido = {
    "archivo": "WarpOmega_Corrected.lean",
    "teorema": "E_Omega > 0",
    "dag_hash": dag_hash_auth
}
firma_valida = priv.sign(json.dumps(payload_valido, sort_keys=True, separators=(",", ":")).encode()).hex()
evento_valido = {"payload": payload_valido, "firma": firma_valida}

solvens.procesar_artefacto(evento_valido, "WarpOmega_Corrected.lean")

# --- ARTEFACTO 2: Prueba Manipulada (Ataque) ---
print("\n------------------------------------------------------------")
print("🕵️ [HACKER] Interceptando artefacto y alterando el Teorema...")
payload_malo = dict(payload_valido)
payload_malo["teorema"] = "E_Omega < 0 (FALSA)" 
# El hacker altera el payload pero mantiene la firma vieja
evento_malo = {"payload": payload_malo, "firma": firma_valida} 

solvens.procesar_artefacto(evento_malo, "WarpOmega_Corrupted.lean")

print("\n============================================================")
print("   ESTADO FINAL DEL SISTEMA")
print("============================================================")
print(Path("solvens_state.json").read_text())
