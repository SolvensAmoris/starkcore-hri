import os

print("🏛️ Forjando las Paredes de Piedra del Santuario: Inyectando starkcore/evidence/learning.py...")

# Asegurar que existan los directorios
os.makedirs("starkcore/evidence", exist_ok=True)
os.makedirs("starkcore/sanctuary", exist_ok=True)

# ------------------------------------------------------------
# 💾 EL MOTOR DE MEMORIA PERSISTENTE (starkcore/evidence/learning.py)
# ------------------------------------------------------------
with open("starkcore/evidence/learning.py", "w") as f:
    f.write('''import json
import os

class EvidenceRegistry:
    """💾 Almacenamiento Atómico de Anomalías. Mantiene la memoria viva en el disco duro."""
    def __init__(self, filename="starkcore/evidence/immunological_memory.json"):
        self.filename = filename
        self.memory = self._load_from_disk()

    def _load_from_disk(self) -> dict:
        if not os.path.exists(self.filename):
            return {}
        try:
            with open(self.filename, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            print("⚠️ [Alerta de Memoria] Archivo corrupto detectado. Inicializando base de datos vacía.")
            return {}

    def save_to_disk(self):
        # Crear directorios si fueron borrados en caliente
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        try:
            with open(self.filename, "w") as f:
                json.dump(self.memory, f, indent=4)
        except IOError as e:
            print(f"💥 [Error Crítico de Disco] No se pudo guardar la evidencia: {e}")

    def get_expedient(self, anomaly_hash: str) -> dict:
        return self.memory.get(anomaly_hash, None)

    def register_encounter(self, anomaly_hash: str, exception_type: str, house: int) -> dict:
        """Incrementa la frecuencia del ataque y actualiza el expediente en disco."""
        if anomaly_hash not in self.memory:
            self.memory[anomaly_hash] = {
                "exception_type": exception_type,
                "first_seen_house": house,
                "frequency": 0,
                "disposition": "NEW_EXPEDIENT",
                "patched_at_epoch": None
            }
        
        self.memory[anomaly_hash]["frequency"] += 1
        
        # Si llega al umbral de 3 ataques, Ofiuco decreta INMUNIDAD PERMANENTE
        if self.memory[anomaly_hash]["frequency"] >= 3:
            self.memory[anomaly_hash]["disposition"] = "PERMANENT_IMMUNITY_PATCH"
            import time
            self.memory[anomaly_hash]["patched_at_epoch"] = time.time()
            
        self.save_to_disk()
        return self.memory[anomaly_hash]
''')

# ------------------------------------------------------------
# 👁️ ACTUALIZACIÓN DEL OBSERVADOR OMEGA (starkcore/sanctuary/omega.py)
# ------------------------------------------------------------
with open("starkcore/sanctuary/omega.py", "w") as f:
    f.write('''import hashlib
import time
from starkcore.evidence.learning import EvidenceRegistry

class OmegaObserver:
    """👁️ El Observador Omega ahora se apoya en el EvidenceRegistry para persistencia."""
    def __init__(self):
        self.stream = []
        self.registry = EvidenceRegistry()

    def record(self, house: int, knight: str, action: str, status: str, meta: dict = None):
        event = {
            "timestamp": time.time(),
            "house": house,
            "knight": knight,
            "action": action,
            "status": status,
            "meta": meta or {}
        }
        self.stream.append(event)

    def compute_anomaly_hash(self, exception: Exception, house: int) -> str:
        raw_string = f"{type(exception).__name__}:{str(exception)}:House_{house}"
        return hashlib.sha256(raw_string.encode('utf-8')).hexdigest()[:12]
''')

# ------------------------------------------------------------
# 🐍 ACTUALIZACIÓN DE OFIUCO PERSISTENTE (starkcore/knights/ophiuchus.py)
# ------------------------------------------------------------
with open("starkcore/knights/ophiuchus.py", "w") as f:
    f.write('''class OphiuchusKnight:
    NAME = "Odysseus"
    HOUSE = 13
    LAW = "🐍 Toda anomalía persistente debe tratarse primero como evidencia antes que como error."

    def investigate(self, error: Exception, house_failed: int, ctx: dict, observer) -> dict:
        print(f"\\n🐍 \\033[1;33m[OFIUCO DESPIERTA]\\033[0m -> Interceptando colapso en Casa {house_failed}.")
        
        # Calcular el hash único del ataque
        anomaly_hash = observer.compute_anomaly_hash(error, house_failed)
        
        # Registrar o actualizar el expediente directamente en el disco duro a través de Omega
        expedient = observer.registry.register_encounter(anomaly_hash, type(error).__name__, house_failed)

        if expedient["disposition"] == "PERMANENT_IMMUNITY_PATCH":
            # 💡 PARCHE DE INMUNIDAD ATÓMICA
            print(f"   🛡️ \\033[1;32m[INMUNIDAD ABSOLUTA - DISCO]\\033[0m Hash: {anomaly_hash} | Avistamientos: {expedient['frequency']}.")
            print(f"   ↳ Ley Ofiuco aplicada: El veneno se transmutó en anticuerpo.")
            ctx["kernel_immunity"] = True
            ctx["anomaly"] = False  # El error es neutralizado en caliente
            observer.record(13, self.NAME, "Apply Disk Patch", "SYSTEM_INMUNIZED")
            return {"status": "REMEDIED_BY_DISK_IMMUNITY", "ctx": ctx}
        else:
            # 🔍 INVESTIGACIÓN ABIERTA
            print(f"   🔍 \\033[1;35m[EXPEDIENTE ABIERTA EN DISCO]\\033[0m Hash: {anomaly_hash} | Frecuencia: {expedient['frequency']}/3")
            observer.record(13, self.NAME, "Log Evidence to Disk", "EXPEDIENT_SAVED", {"hash": anomaly_hash})
            ctx["evidence"] = {
                "hash": anomaly_hash,
                "exception": type(error).__name__,
                "attempts": expedient["frequency"]
            }
            ctx["learning_mode"] = True
            return {"status": "COLLECTED_AS_PERSISTENT_EVIDENCE", "ctx": ctx}
''')

# ------------------------------------------------------------
# 🏃‍♂️ PROBANDO LA RIGIDEZ DEL TEMPLO (main_v3.py)
# ------------------------------------------------------------
with open("main_v3.py", "w") as f:
    f.write('''from starkcore.sanctuary.temple import Sanctuary
from starkcore.sanctuary.omega import OmegaObserver
from starkcore.executors.strategies import ValidationExecutor, KernelExecutor
import os

if __name__ == "__main__":
    # Importante: Instanciamos un observador fresco. 
    # Al simular ejecuciones separadas, la única forma de recordar es leyendo el DISCO DURO.
    omega_fresco = OmegaObserver()
    
    executors_map = {
        "VirgoKnight": ValidationExecutor(),
        "CapricornKnight": KernelExecutor()
    }

    # Verificar si ya había memoria en el disco para mostrar persistencia real
    db_path = "starkcore/evidence/immunological_memory.json"
    if os.path.exists(db_path):
        print(f"\\n💾 [Detección de Sistema] Se encontró un bloque de memoria previa en disco con {os.path.getsize(db_path)} bytes.")
    else:
        print("\\n🆕 [Detección de Sistema] Iniciando el Santuario sin memoria previa en disco.")

    print("\\n🛡️ === INICIANDO UNA SOLA INVOCACIÓN DE ENTORNO EN PRODUCCIÓN ===")
    santuario = Sanctuary(observer=omega_fresco)
    santuario.load_constellation("gold_sanctuary", executors=executors_map)
    
    # Lanzar petición con anomalía
    status, ctx_final = santuario.invoke({"anomaly": True})
    
    print(f"\\n📋 \\033[1;36mEstatus de Salida:\\033[0m {status}")
    print(f"📦 Contexto de Datos resultante:", ctx_final)
''')

print("✅ Capa de robustez inyectada correctamente.")
print("👉 Ejecuta varias veces: 'python3 main_v3.py' para ver cómo el sistema aprende entre ejecuciones independientes.")
