import os
import hashlib
import time

print("🔱 Forjando la Armadura Divina de StarkCore V2: El Templo de la Inmunidad Causal...")

# Crear estructura si no existe
os.makedirs("starkcore/sanctuary", exist_ok=True)
os.makedirs("starkcore/knights", exist_ok=True)

# ------------------------------------------------------------
# 👁️ OMEGA MEMORY & EVENT STREAM (starkcore/sanctuary/omega.py)
# ------------------------------------------------------------
with open("starkcore/sanctuary/omega.py", "w") as f:
    f.write('''import hashlib
import time

class OmegaObserver:
    """👁️ El Observador Omega es un Event Stream con Memoria Inmunológica."""
    def __init__(self):
        self.stream = []
        self.anomaly_memory = {} # Hash -> {"frequency": int, "disposition": str}

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
        """Genera una firma única para la anomalía basada en su tipo, mensaje y lugar de origen."""
        raw_string = f"{type(exception).__name__}:{str(exception)}:House_{house}"
        return hashlib.sha256(raw_string.encode('utf-8')).hexdigest()[:12]

    def query_memory(self, anomaly_hash: str) -> dict:
        """Pregunta a la memoria si ya ha visto este patrón."""
        return self.anomaly_memory.get(anomaly_hash, None)

    def learn_anomaly(self, anomaly_hash: str, disposition: str):
        """Registra el patrón en la memoria permanente del sistema."""
        if anomaly_hash not in self.anomaly_memory:
            self.anomaly_memory[anomaly_hash] = {"frequency": 0, "disposition": "NEW_EXPEDIENT"}
        self.anomaly_memory[anomaly_hash]["frequency"] += 1
        self.anomaly_memory[anomaly_hash]["disposition"] = disposition
''')

# ------------------------------------------------------------
# 🌌 STARMAP: EL CARGADOR DE CONSTELACIONES (starkcore/sanctuary/starmap.py)
# ------------------------------------------------------------
with open("starkcore/sanctuary/starmap.py", "w") as f:
    f.write('''from starkcore.knights.zodiac import (
    AriesKnight, TaurusKnight, GeminiKnight, CancerKnight, LeoKnight,
    VirgoKnight, LibraKnight, ScorpioKnight, SagittariusKnight,
    CapricornKnight, AquariusKnight, PiscesKnight
)

class StarMap:
    """🌌 El Mapa Estelar define qué constelación de oleadas (pipelines) cargar."""
    TEMPLATES = {
        "gold_sanctuary": [
            AriesKnight, TaurusKnight, GeminiKnight, CancerKnight, LeoKnight,
            VirgoKnight, LibraKnight, ScorpioKnight, SagittariusKnight,
            CapricornKnight, AquariusKnight, PiscesKnight
        ],
        "silver_sanctuary": [
            AriesKnight, GeminiKnight, VirgoKnight, SagittariusKnight, CapricornKnight
        ],
        "bronze_sanctuary": [
            AriesKnight, TaurusKnight, PiscesKnight # Versión embebida ligera
        ]
    }

    @classmethod
    def load(cls, template_name: str, executors: dict = None) -> list:
        if template_name not in cls.TEMPLATES:
            raise ValueError(f"La constelación {template_name} no existe en los cielos.")
        
        knights_classes = cls.TEMPLATES[template_name]
        instances = []
        executors = executors or {}

        for kc in knights_classes:
            # Si el caballero requiere un executor específico (ej. Virgo o Capricornio), se inyecta
            exec_instance = executors.get(kc.__name__)
            instances.append(kc(executor=exec_instance))
            
        return instances
''')

# ------------------------------------------------------------
# 🐍 OFIUCO ADAPTATIVO (starkcore/knights/ophiuchus.py)
# ------------------------------------------------------------
with open("starkcore/knights/ophiuchus.py", "w") as f:
    f.write('''class OphiuchusKnight:
    NAME = "Odysseus"
    HOUSE = 13
    LAW = "🐍 Toda anomalía persistente debe tratarse primero como evidencia antes que como error."

    def investigate(self, error: Exception, house_failed: int, ctx: dict, observer) -> dict:
        print(f"\\n🐍 \\033[1;33m[OFIUCO DESPIERTA]\\033[0m -> Interceptando colapso en Casa {house_failed}.")
        
        # 1. Consultar la memoria inmunológica de Omega
        anomaly_hash = observer.compute_anomaly_hash(error, house_failed)
        expedient = observer.query_memory(anomaly_hash)

        if expedient and expedient["frequency"] >= 3:
            # 💡 MUTACIÓN EN CALIENTE DEL KERNEL (Inmunidad del Sistema)
            print(f"   🛡️ \\033[1;32m[MEMORIA ACTIVA - HASH: {anomaly_hash}]\\033[0m Frecuencia: {expedient['frequency']}. Mutando el Kernel...")
            print(f"   ↳ Inmunizando contexto. Forzando curación automática.")
            
            ctx["kernel_immunity"] = True
            ctx["anomaly"] = False # Disuelve el veneno, lo vuelve medicina
            observer.learn_anomaly(anomaly_hash, "MUTATED_TO_IMMUNITY")
            observer.record(13, self.NAME, "Apply Kernel Patch", "IMMUNITY_VERIFIED")
            return {"status": "REMEDIED_BY_IMMUNITY", "ctx": ctx}
        
        else:
            # 🕵️ INVESTIGACIÓN INICIAL (Abrir expediente)
            print(f"   🔍 \\033[1;35m[NUEVA ANOMALÍA - HASH: {anomaly_hash}]\\033[0m Abriendo expediente de evidencia.")
            observer.learn_anomaly(anomaly_hash, "UNDER_INVESTIGATION")
            observer.record(13, self.NAME, "Investigate Anomaly", "EXPEDIENT_OPENED", {"hash": anomaly_hash})
            
            ctx["evidence"] = {
                "hash": anomaly_hash,
                "exception": type(error).__name__,
                "house": house_failed
            }
            ctx["learning_mode"] = True
            return {"status": "COLLECTED_AS_EVIDENCE", "ctx": ctx}
''')

# ------------------------------------------------------------
# 🏛️ EL MOTOR ACTUALIZADO (starkcore/sanctuary/temple.py)
# ------------------------------------------------------------
with open("starkcore/sanctuary/temple.py", "w") as f:
    f.write('''from typing import List
from starkcore.knights.base import Knight, Context
from starkcore.sanctuary.omega import OmegaObserver
from starkcore.knights.ophiuchus import OphiuchusKnight
from starkcore.sanctuary.starmap import StarMap

class Sanctuary:
    def __init__(self, observer=None):
        self.knights: List[Knight] = []
        self.ophiuchus = OphiuchusKnight()
        self.observer = observer or OmegaObserver()

    def load_constellation(self, name: str, executors: dict = None):
        """Carga automáticamente la tubería de Caballeros usando el StarMap."""
        self.knights = StarMap.load(name, executors)

    def invoke(self, ctx: Context) -> tuple:
        print(f"\\n✨ \\033[1;34m[Iniciando Invocación del Templo]\\033[0m")
        for knight in self.knights:
            try:
                if knight.should_handle(ctx):
                    self.observer.record(knight.HOUSE, knight.NAME, "Enter House", "PROCEEDING")
                    ctx = knight.prepare(ctx)
                    ctx = knight.execute(ctx)
                    ctx = knight.finalize(ctx)
                    self.observer.record(knight.HOUSE, knight.NAME, "Exit House", "SUCCESS")
            except Exception as exc:
                self.observer.record(knight.HOUSE, knight.NAME, "Crash", "TRIGGER_OPHIUCHUS")
                print(f"  💥 \\033[1;31m[Fallo en Casa {knight.HOUSE}]\\033[0m -> Transmutando en la 13ª Casa.")
                
                ophiuchus_outcome = self.ophiuchus.investigate(exc, knight.HOUSE, ctx, self.observer)
                return ophiuchus_outcome["status"], ophiuchus_outcome["ctx"]
                
        return "SUCCESSFUL_RUN", ctx
''')

# ------------------------------------------------------------
# 🚀 EL NUEVO CORAZÓN DE PRUEBA (main_v2.py)
# ------------------------------------------------------------
with open("main_v2.py", "w") as f:
    f.write('''from starkcore.sanctuary.temple import Sanctuary
from starkcore.sanctuary.omega import OmegaObserver
from starkcore.executors.strategies import ValidationExecutor, KernelExecutor

if __name__ == "__main__":
    # Compartimos un único Observador Omega global para mantener la memoria viva entre ejecuciones
    omega_global = OmegaObserver()
    
    executors_map = {
        "VirgoKnight": ValidationExecutor(),
        "CapricornKnight": KernelExecutor()
    }

    # ----------------------------------------------------------------
    # ESCENARIO: El ataque repetido de una anomalía (Simulación de estrés)
    # ----------------------------------------------------------------
    print("\\n🚀 === INICIANDO SIMULACIÓN DE RITUAL CÓSMICO (4 ATAQUES CONSECUTIVOS) ===")
    
    for i in range(1, 5):
        print(f"\\n\\033[1;37m[⚡ OLEADA DE RED INTRUSA NÚMERO {i}]\\033[0m")
        
        santuario = Sanctuary(observer=omega_global)
        
        # 🌌 ¡Llamada Limpia! Cargando un StarMap preconfigurado
        santuario.load_constellation("gold_sanctuary", executors=executors_map)
        
        # Enviamos la misma anomalía para estresar el discernimiento de Virgo
        status, ctx_final = santuario.invoke({"anomaly": True})
        
        print(f"📋 \\033[1;36mResultado Final de la Oleada {i}:\\033[0m {status}")
        print(f"📦 Contexto de Datos resultante:", ctx_final)

    # 👁️ Ver los logs del Event Stream Final
    print("\\n📊 \\033[1;35m[HISTORIAL GLOBAL DEL EVENT STREAM DE OMEGA]\\033[0m")
    for log in omega_global.stream:
        print(f"  👁️  Casa {str(log['house']).zfill(2)} | {log['knight'].ljust(10)} | Acción: {log['action'].ljust(20)} -> Status: {log['status']}")
''')

print("✅ Versión V2 inyectada en el Santuario.")

print("👉 Ejecuta ahora: 'python3 main_v2.py'")EOFpython3 setup_santuario_v2.py
cat << 'EOF' > setup_santuario_v2.py
import os
import hashlib
import time

print("🔱 Forjando la Armadura Divina de StarkCore V2: El Templo de la Inmunidad Causal...")

# Crear estructura si no existe
os.makedirs("starkcore/sanctuary", exist_ok=True)
os.makedirs("starkcore/knights", exist_ok=True)

# ------------------------------------------------------------
# 👁️ OMEGA MEMORY & EVENT STREAM (starkcore/sanctuary/omega.py)
# ------------------------------------------------------------
with open("starkcore/sanctuary/omega.py", "w") as f:
    f.write('''import hashlib
import time

class OmegaObserver:
    """👁️ El Observador Omega es un Event Stream con Memoria Inmunológica."""
    def __init__(self):
        self.stream = []
        self.anomaly_memory = {} # Hash -> {"frequency": int, "disposition": str}

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
        """Genera una firma única para la anomalía basada en su tipo, mensaje y lugar de origen."""
        raw_string = f"{type(exception).__name__}:{str(exception)}:House_{house}"
        return hashlib.sha256(raw_string.encode('utf-8')).hexdigest()[:12]

    def query_memory(self, anomaly_hash: str) -> dict:
        """Pregunta a la memoria si ya ha visto este patrón."""
        return self.anomaly_memory.get(anomaly_hash, None)

    def learn_anomaly(self, anomaly_hash: str, disposition: str):
        """Registra el patrón en la memoria permanente del sistema."""
        if anomaly_hash not in self.anomaly_memory:
            self.anomaly_memory[anomaly_hash] = {"frequency": 0, "disposition": "NEW_EXPEDIENT"}
        self.anomaly_memory[anomaly_hash]["frequency"] += 1
        self.anomaly_memory[anomaly_hash]["disposition"] = disposition
''')

# ------------------------------------------------------------
# 🌌 STARMAP: EL CARGADOR DE CONSTELACIONES (starkcore/sanctuary/starmap.py)
# ------------------------------------------------------------
with open("starkcore/sanctuary/starmap.py", "w") as f:
    f.write('''from starkcore.knights.zodiac import (
    AriesKnight, TaurusKnight, GeminiKnight, CancerKnight, LeoKnight,
    VirgoKnight, LibraKnight, ScorpioKnight, SagittariusKnight,
    CapricornKnight, AquariusKnight, PiscesKnight
)

class StarMap:
    """🌌 El Mapa Estelar define qué constelación de oleadas (pipelines) cargar."""
    TEMPLATES = {
        "gold_sanctuary": [
            AriesKnight, TaurusKnight, GeminiKnight, CancerKnight, LeoKnight,
            VirgoKnight, LibraKnight, ScorpioKnight, SagittariusKnight,
            CapricornKnight, AquariusKnight, PiscesKnight
        ],
        "silver_sanctuary": [
            AriesKnight, GeminiKnight, VirgoKnight, SagittariusKnight, CapricornKnight
        ],
        "bronze_sanctuary": [
            AriesKnight, TaurusKnight, PiscesKnight # Versión embebida ligera
        ]
    }

    @classmethod
    def load(cls, template_name: str, executors: dict = None) -> list:
        if template_name not in cls.TEMPLATES:
            raise ValueError(f"La constelación {template_name} no existe en los cielos.")
        
        knights_classes = cls.TEMPLATES[template_name]
        instances = []
        executors = executors or {}

        for kc in knights_classes:
            # Si el caballero requiere un executor específico (ej. Virgo o Capricornio), se inyecta
            exec_instance = executors.get(kc.__name__)
            instances.append(kc(executor=exec_instance))
            
        return instances
''')

# ------------------------------------------------------------
# 🐍 OFIUCO ADAPTATIVO (starkcore/knights/ophiuchus.py)
# ------------------------------------------------------------
with open("starkcore/knights/ophiuchus.py", "w") as f:
    f.write('''class OphiuchusKnight:
    NAME = "Odysseus"
    HOUSE = 13
    LAW = "🐍 Toda anomalía persistente debe tratarse primero como evidencia antes que como error."

    def investigate(self, error: Exception, house_failed: int, ctx: dict, observer) -> dict:
        print(f"\\n🐍 \\033[1;33m[OFIUCO DESPIERTA]\\033[0m -> Interceptando colapso en Casa {house_failed}.")
        
        # 1. Consultar la memoria inmunológica de Omega
        anomaly_hash = observer.compute_anomaly_hash(error, house_failed)
        expedient = observer.query_memory(anomaly_hash)

        if expedient and expedient["frequency"] >= 3:
            # 💡 MUTACIÓN EN CALIENTE DEL KERNEL (Inmunidad del Sistema)
            print(f"   🛡️ \\033[1;32m[MEMORIA ACTIVA - HASH: {anomaly_hash}]\\033[0m Frecuencia: {expedient['frequency']}. Mutando el Kernel...")
            print(f"   ↳ Inmunizando contexto. Forzando curación automática.")
            
            ctx["kernel_immunity"] = True
            ctx["anomaly"] = False # Disuelve el veneno, lo vuelve medicina
            observer.learn_anomaly(anomaly_hash, "MUTATED_TO_IMMUNITY")
            observer.record(13, self.NAME, "Apply Kernel Patch", "IMMUNITY_VERIFIED")
            return {"status": "REMEDIED_BY_IMMUNITY", "ctx": ctx}
        
        else:
            # 🕵️ INVESTIGACIÓN INICIAL (Abrir expediente)
            print(f"   🔍 \\033[1;35m[NUEVA ANOMALÍA - HASH: {anomaly_hash}]\\033[0m Abriendo expediente de evidencia.")
            observer.learn_anomaly(anomaly_hash, "UNDER_INVESTIGATION")
            observer.record(13, self.NAME, "Investigate Anomaly", "EXPEDIENT_OPENED", {"hash": anomaly_hash})
            
            ctx["evidence"] = {
                "hash": anomaly_hash,
                "exception": type(error).__name__,
                "house": house_failed
            }
            ctx["learning_mode"] = True
            return {"status": "COLLECTED_AS_EVIDENCE", "ctx": ctx}
''')

# ------------------------------------------------------------
# 🏛️ EL MOTOR ACTUALIZADO (starkcore/sanctuary/temple.py)
# ------------------------------------------------------------
with open("starkcore/sanctuary/temple.py", "w") as f:
    f.write('''from typing import List
from starkcore.knights.base import Knight, Context
from starkcore.sanctuary.omega import OmegaObserver
from starkcore.knights.ophiuchus import OphiuchusKnight
from starkcore.sanctuary.starmap import StarMap

class Sanctuary:
    def __init__(self, observer=None):
        self.knights: List[Knight] = []
        self.ophiuchus = OphiuchusKnight()
        self.observer = observer or OmegaObserver()

    def load_constellation(self, name: str, executors: dict = None):
        """Carga automáticamente la tubería de Caballeros usando el StarMap."""
        self.knights = StarMap.load(name, executors)

    def invoke(self, ctx: Context) -> tuple:
        print(f"\\n✨ \\033[1;34m[Iniciando Invocación del Templo]\\033[0m")
        for knight in self.knights:
            try:
                if knight.should_handle(ctx):
                    self.observer.record(knight.HOUSE, knight.NAME, "Enter House", "PROCEEDING")
                    ctx = knight.prepare(ctx)
                    ctx = knight.execute(ctx)
                    ctx = knight.finalize(ctx)
                    self.observer.record(knight.HOUSE, knight.NAME, "Exit House", "SUCCESS")
            except Exception as exc:
                self.observer.record(knight.HOUSE, knight.NAME, "Crash", "TRIGGER_OPHIUCHUS")
                print(f"  💥 \\033[1;31m[Fallo en Casa {knight.HOUSE}]\\033[0m -> Transmutando en la 13ª Casa.")
                
                ophiuchus_outcome = self.ophiuchus.investigate(exc, knight.HOUSE, ctx, self.observer)
                return ophiuchus_outcome["status"], ophiuchus_outcome["ctx"]
                
        return "SUCCESSFUL_RUN", ctx
''')

# ------------------------------------------------------------
# 🚀 EL NUEVO CORAZÓN DE PRUEBA (main_v2.py)
# ------------------------------------------------------------
with open("main_v2.py", "w") as f:
    f.write('''from starkcore.sanctuary.temple import Sanctuary
from starkcore.sanctuary.omega import OmegaObserver
from starkcore.executors.strategies import ValidationExecutor, KernelExecutor

if __name__ == "__main__":
    # Compartimos un único Observador Omega global para mantener la memoria viva entre ejecuciones
    omega_global = OmegaObserver()
    
    executors_map = {
        "VirgoKnight": ValidationExecutor(),
        "CapricornKnight": KernelExecutor()
    }

    # ----------------------------------------------------------------
    # ESCENARIO: El ataque repetido de una anomalía (Simulación de estrés)
    # ----------------------------------------------------------------
    print("\\n🚀 === INICIANDO SIMULACIÓN DE RITUAL CÓSMICO (4 ATAQUES CONSECUTIVOS) ===")
    
    for i in range(1, 5):
        print(f"\\n\\033[1;37m[⚡ OLEADA DE RED INTRUSA NÚMERO {i}]\\033[0m")
        
        santuario = Sanctuary(observer=omega_global)
        
        # 🌌 ¡Llamada Limpia! Cargando un StarMap preconfigurado
        santuario.load_constellation("gold_sanctuary", executors=executors_map)
        
        # Enviamos la misma anomalía para estresar el discernimiento de Virgo
        status, ctx_final = santuario.invoke({"anomaly": True})
        
        print(f"📋 \\033[1;36mResultado Final de la Oleada {i}:\\033[0m {status}")
        print(f"📦 Contexto de Datos resultante:", ctx_final)

    # 👁️ Ver los logs del Event Stream Final
    print("\\n📊 \\033[1;35m[HISTORIAL GLOBAL DEL EVENT STREAM DE OMEGA]\\033[0m")
    for log in omega_global.stream:
        print(f"  👁️  Casa {str(log['house']).zfill(2)} | {log['knight'].ljust(10)} | Acción: {log['action'].ljust(20)} -> Status: {log['status']}")
''')

print("✅ Versión V2 inyectada en el Santuary

