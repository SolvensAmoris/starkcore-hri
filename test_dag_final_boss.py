import json, hashlib
from pathlib import Path

class DAGCanonicalizer:
    def generar_hash_estructural(self, nodos: list, aristas: list) -> str:
        nodos_ordenados = sorted(nodos, key=lambda x: str(x.get("id", "")))
        aristas_ordenadas = sorted(aristas, key=lambda x: (str(x.get("from", "")), str(x.get("to", ""))))
        estructura_canonica = {"nodos": nodos_ordenados, "aristas": aristas_ordenadas}
        payload_bytes = json.dumps(estructura_canonica, sort_keys=True, separators=(",", ":")).encode('utf-8')
        return hashlib.sha256(payload_bytes).hexdigest()

cosmos = DAGCanonicalizer()
GENESIS_FILE = Path("cosmos_genesis.json")

print("============================================================")
print("   STARKCORE :: DAG - THE FINAL BOSS TEST")
print("============================================================")

# 1. Setup del Génesis Original
nodos_originales = [{"id": "runtime", "tipo": "core"}, {"id": "gateway", "tipo": "sec"}]
aristas_originales = [{"from": "runtime", "to": "gateway"}]
hash_original = cosmos.generar_hash_estructural(nodos_originales, aristas_originales)

GENESIS_FILE.write_text(json.dumps({
    "nodos": nodos_originales,
    "aristas": aristas_originales,
    "dag_hash": hash_original
}, indent=2))
print(f"✅ [GÉNESIS] Archivo creado. Hash: {hash_original[:16]}...")

# 2. El Ataque del "Root Access"
print("\n🕵️ [HACKER] El atacante entra en la terminal, lee el génesis y añade un nodo malicioso...")
# El hacker lee el génesis
genesis_comprometido = json.loads(GENESIS_FILE.read_text())

# Añade su nodo y RECALCULA el hash, luego guarda el archivo falso
genesis_comprometido["nodos"].append({"id": "backdoor", "tipo": "malicious"})
hash_falso = cosmos.generar_hash_estructural(genesis_comprometido["nodos"], genesis_comprometido["aristas"])
genesis_comprometido["dag_hash"] = hash_falso

# Sobrescribe el archivo (El atacante tiene root)
GENESIS_FILE.write_text(json.dumps(genesis_comprometido, indent=2))
print(f"   ❌ [HACKER] Génesis sobrescrito. Nuevo hash en disco: {hash_falso[:16]}...")

# 3. El Sistema Arranca y hace una Auditoría Forense
print("\n🛡️ [SYSTEM BOOT] Iniciando proceso de arranque y verificación...")

# El sistema tiene su hash esperado grabado en el código (o en un chip TPM separado)
HASH_ESPERADO_EN_ROM = hash_original

# Lee el archivo en disco
disco_actual = json.loads(GENESIS_FILE.read_text())
hash_en_disco = cosmos.generar_hash_estructural(disco_actual["nodos"], disco_actual["aristas"])

print(f"   [AUDITOR] Hash en ROM (Esperado): {HASH_ESPERADO_EN_ROM[:16]}...")
print(f"   [AUDITOR] Hash en Disco (Real):   {hash_en_disco[:16]}...")

if hash_en_disco == HASH_ESPERADO_EN_ROM:
    print("✅ [PASS] El sistema arranca. La topología es la original.")
else:
    print("🚨 [CRITICAL FAILURE] ¡EL GÉNESIS HA SIDO ALTERADO EN DISCO!")
    print("   -> El atacante intentó reescribir la historia del sistema.")
    print("   -> Entrando en MODO_FAIL_CLOSED por compromiso de integridad estructural.")
    
print("\n============================================================")
