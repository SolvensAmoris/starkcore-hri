import json, hashlib, time
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric import ed25519

# ==========================================
# ARQUITECTURA: STARKCORE COSMOS TERMINAL
# ==========================================

class Ingest:
    def procesar(self, raw_data):
        print("  [Ingest] Ingesta de datos y normalización...")
        return json.loads(raw_data)

class Planner:
    def planificar(self, evento):
        print("  [Planner] Planificación de consulta y optimización...")
        evento["plan_id"] = hashlib.sha256(str(time.time()).encode()).hexdigest()[:8]
        return evento

class Gateway:
    def __init__(self, pub_key_hex):
        self.pub_key = ed25519.Ed25519PublicKey.from_public_bytes(bytes.fromhex(pub_key_hex))
    
    def control_acceso(self, evento):
        print("  [Gateway] Control de acceso, API y enrutamiento...")
        try:
            payload = evento["payload"]
            firma = bytes.fromhex(evento["firma"])
            payload_bytes = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
            
            # Validación Criptográfica
            self.pub_key.verify(firma, payload_bytes)
            
            # Validación de Política (Π)
            if payload.get("accion") != "MODO_FAIL_CLOSED":
                print("    ❌ [Gateway] Rechazado: Violación de Política (Π).")
                return False
            
            print("    ✅ [Gateway] Firma válida y política aprobada.")
            return True
        except Exception:
            print("    ❌ [Gateway] Rechazado: Firma inválida o alterada.")
            return False

class Jacobian:
    def mutar_estado(self, evento):
        print("  [Jacobian] Gestión de estado y consistencia...")
        state_file = Path("cosmos_state.json")
        
        estado_actual = "MODO_HSIC"
        if state_file.exists():
            estado_actual = json.loads(state_file.read_text()).get("modo", "MODO_HSIC")
            
        nuevo_estado = evento["payload"]["accion"]
        
        state_file.write_text(json.dumps({"modo": nuevo_estado, "timestamp": time.time()}, indent=2))
        print(f"    -> Matriz mutada: {estado_actual} -> {nuevo_estado}")
        return nuevo_estado

class Bus:
    def emitir_log(self, evento, nuevo_estado):
        print("  [Bus] Streaming y mensajería (Hash-Chain)...")
        log_file = Path("cosmos_bus.log")
        
        prev_hash = "0"*64
        if log_file.exists():
            lineas = log_file.read_text().strip().split("\n")
            if lineas and lineas[0]:
                prev_hash = json.loads(lineas[-1])["hash"]
                
        bloque = {
            "plan_id": evento["plan_id"],
            "estado": nuevo_estado,
            "prev_hash": prev_hash,
            "ts": time.time()
        }
        bloque["hash"] = hashlib.sha256(json.dumps(bloque, sort_keys=True).encode()).hexdigest()
        
        with open(log_file, "a") as f:
            f.write(json.dumps(bloque) + "\n")
        print(f"    -> Evento emitido al bus: {bloque['hash'][:16]}...")

class Query:
    def consultar(self):
        print("  [Query] Ejecución de consulta de estado...")
        state_file = Path("cosmos_state.json")
        if state_file.exists():
            return json.loads(state_file.read_text())
        return {"error": "Estado no encontrado"}

# ==========================================
# SIMULACIÓN DEL RUNTIME
# ==========================================

print("============================================================")
print("   STARKCORE COSMOS TERMINAL :: RUNTIME START")
print("============================================================")

# Setup
priv = ed25519.Ed25519PrivateKey.generate()
pub_hex = priv.public_key().public_bytes_raw().hex()

payload_valido = {"dispositivo": "YAL-L21", "accion": "MODO_FAIL_CLOSED", "nonce": "x1y2z3"}
payload_bytes = json.dumps(payload_valido, sort_keys=True, separators=(",", ":")).encode()
firma_valida = priv.sign(payload_bytes).hex()

evento_raw = json.dumps({"payload": payload_valido, "firma": firma_valida})

# Instanciar nodos
ingest = Ingest()
planner = Planner()
gateway = Gateway(pub_hex)
jacobian = Jacobian()
bus = Bus()
query = Query()

# --- FLUJO A: Evento Legítimo ---
print("\n--- FLUJO A: EVENTO LEGÍTIMO (Firma Correcta) ---")
e1 = ingest.procesar(evento_raw)
e1 = planner.planificar(e1)

if gateway.control_acceso(e1):
    estado_final = jacobian.mutar_estado(e1)
    bus.emitir_log(e1, estado_final)
    print(f"✅ Runtime Status: {query.consultar()}")

# --- FLUJO B: Evento Malicioso ---
print("\n--- FLUJO B: EVENTO MALICIOSO (Tampering) ---")
evento_malo = json.loads(evento_raw)
evento_malo["payload"]["accion"] = "MODO_ABIERTO" 
evento_malo_raw = json.dumps(evento_malo)

e2 = ingest.procesar(evento_malo_raw)
e2 = planner.planificar(e2)

if gateway.control_acceso(e2):
    estado_final = jacobian.mutar_estado(e2)
    bus.emitir_log(e2, estado_final)
else:
    print("🚨 Flujo bloqueado en Gateway. Jacobian y Bus NO se ejecutan.")
    print(f"🛡️  Estado se mantiene seguro: {query.consultar()}")

print("\n============================================================")
