import json, hashlib
from pathlib import Path
def verificar():
    print("\n🔍 [AUDITOR FORENSE v1.3.1]")
    log = Path("audit.log")
    state = json.loads(Path("estado_firewall.json").read_text()) if Path("estado_firewall.json").exists() else {"head_hash": "0"*64, "altura": -1}
    if not log.exists():
        print("   ⚠️ Sin log")
        return True
    lineas = log.read_text().strip().split("\n")
    expected = "0"*64
    for i, linea in enumerate(lineas):
        data = json.loads(linea)
        if data["prev_hash"] != expected:
            print(f"   🚨 Ruptura en bloque {i} - borraron el pasado")
            return False
        payload = {k: v for k, v in data.items() if k != "current_hash"}
        if hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest() != data["current_hash"]:
            print(f"   🚨 Hash alterado bloque {i}")
            return False
        expected = data["current_hash"]
    if expected != state.get("head_hash"):
        print(f"   🚨 [ALERTA TAIL-DELETION] Log altura {len(lineas)-1} hash {expected[:8]}...")
        print(f"      Estado ancla altura {state.get('altura')} hash {state.get('head_hash','')[:8]}... ¡Borraron cola!")
        return False
    print(f"   ✅ Cadena {len(lineas)} bloques + ancla verificada. Inmutable.")
    return True
if __name__ == "__main__":
    verificar()
