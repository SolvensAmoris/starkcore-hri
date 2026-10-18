import json, time, hashlib
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
STATE_FILE = Path("estado_firewall.json")
LOG_FILE = Path("audit.log")
if not STATE_FILE.exists():
    STATE_FILE.write_text(json.dumps({"modo": "MODO_HSIC", "head_hash": "0"*64, "altura": 0}, indent=2))
def escribir_log(prev, nuevo, resultado, nonce="N/A"):
    prev_hash = "0"*64
    altura = 0
    if LOG_FILE.exists():
        lineas = LOG_FILE.read_text().strip().split("\n")
        if lineas and lineas[0]:
            last = json.loads(lineas[-1])
            prev_hash = last["current_hash"]
            altura = last.get("altura", 0) + 1
    entrada = {"altura": altura, "ts": time.time(), "cert_nonce": nonce, "estado_prev": prev, "estado_nuevo": nuevo, "resultado": resultado, "prev_hash": prev_hash}
    current_hash = hashlib.sha256(json.dumps(entrada, sort_keys=True).encode()).hexdigest()
    entrada["current_hash"] = current_hash
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entrada) + "\n")
    estado = json.loads(STATE_FILE.read_text())
    estado["head_hash"] = current_hash
    estado["altura"] = altura
    if resultado == "EXITOSO":
        estado["modo"] = nuevo
    STATE_FILE.write_text(json.dumps(estado, indent=2))
def intentar_mutacion(cert_path):
    print(f"\n🛡️ [GATEKEEPER v1.3.1] {cert_path}...")
    cert = json.loads(Path(cert_path).read_text())
    pub_data = json.loads(Path("public_key.json").read_text())
    estado_actual = json.loads(STATE_FILE.read_text())["modo"]
    try:
        pub_key = Ed25519PublicKey.from_public_bytes(bytes.fromhex(pub_data["public_key"]))
        payload = {k: v for k, v in cert.items() if k != "firma"}
        pub_key.verify(bytes.fromhex(cert["firma"]), json.dumps(payload, sort_keys=True, separators=(",", ":")).encode())
    except Exception as e:
        print(f"   ❌ Firma inválida: {e}")
        escribir_log(estado_actual, estado_actual, "RECHAZADO_FIRMA", cert.get("nonce", "N/A"))
        return
    if cert["accion"] != "MODO_FAIL_CLOSED":
        print("   ❌ Política bloquea")
        escribir_log(estado_actual, estado_actual, "RECHAZADO_POLITICA", cert["nonce"])
        return
    print("   🔥 MUTACIÓN FÍSICA")
    escribir_log(estado_actual, cert["accion"], "EXITOSO", cert["nonce"])
