import json, uuid, time
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric import ed25519
priv = ed25519.Ed25519PrivateKey.generate()
pub = priv.public_key().public_bytes_raw()
Path("public_key.json").write_text(json.dumps({"public_key": pub.hex()}))
def emitir(accion, filename):
    payload = {"device": "YAL-L21", "accion": accion, "ts": time.time(), "nonce": str(uuid.uuid4())}
    canon = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    firma = priv.sign(canon.encode())
    Path(filename).write_text(json.dumps({**payload, "firma": firma.hex()}, indent=2))
emitir("MODO_FAIL_CLOSED", "cert_valido.json")
emitir("MODO_ABIERTO", "cert_invalido.json")
print("✅ Certs ok")
