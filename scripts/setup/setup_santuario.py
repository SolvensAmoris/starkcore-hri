import os
import sys

# ============================================================
# 🌌 DEPLOYER DEL SANTUARIO STARKCORE
# ============================================================
print("✨ Invocando el Santuario en el cosmos de UserLAnd/Termux...")

# Crear el árbol de directorios que visualizaste
directorios = [
    "starkcore/sanctuary",
    "starkcore/knights",
    "starkcore/executors",
    "starkcore/evidence",
    "starkcore/aion"
]

for folder in directorios:
    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(folder, "__init__.py"), "w") as f:
        f.write("# StarkCore Cosmic Module\n")

# ------------------------------------------------------------
# 🏛️ 1. PROTOCOLO BASE Y PROTOCOLO OMEGA (starkcore/knights/base.py)
# ------------------------------------------------------------
with open("starkcore/knights/base.py", "w") as f:
    f.write('''from abc import ABC, abstractmethod
from typing import Dict, Any

Context = Dict[str, Any]

class Knight(ABC):
    NAME = "Unknown"
    HOUSE = 0
    ARCHETYPE = "Undefined"

    def __init__(self, executor=None):
        self.executor = executor

    def should_handle(self, ctx: Context) -> bool: return True
    def prepare(self, ctx: Context) -> Context: return ctx
    
    @abstractmethod
    def execute(self, ctx: Context) -> Context: pass
    
    def finalize(self, ctx: Context) -> Context: return ctx

class OmegaObserver:
    """👁️ El Observador Omega registra la evidencia causal del Santuario."""
    def __init__(self):
        self.logs = []
    def record(self, house: int, knight: str, action: str, status: str):
        self.logs.append({"house": house, "knight": knight, "action": action, "status": status})
''')

# ------------------------------------------------------------
# ⚡ 2. EXECUTORS: LAS ESTRATEGIAS REALES (starkcore/executors/strategies.py)
# ------------------------------------------------------------
with open("starkcore/executors/strategies.py", "w") as f:
    f.write('''import sys

class ValidationExecutor:
    def process(self, ctx: dict):
        if ctx.get("anomaly"):
            raise RuntimeError("⚠️ Anomalía crítica detectada en el flujo de datos.")
        return ctx

class KernelExecutor:
    def process(self, ctx: dict):
        ctx["core_status"] = "STABLE_EXECUTION"
        return ctx
''')

# ------------------------------------------------------------
# 🧘‍♂️ 3. LOS CABALLEROS (starkcore/knights/zodiac.py)
# ------------------------------------------------------------
with open("starkcore/knights/zodiac.py", "w") as f:
    f.write('''from starkcore.knights.base import Knight

class AriesKnight(Knight):
    NAME, HOUSE, ARCHETYPE = "Mu", 1, "Bootstrap"
    def execute(self, ctx):
        ctx["boot"] = True
        return ctx

class TaurusKnight(Knight):
    NAME, HOUSE, ARCHETYPE = "Aldebarán", 2, "Persistence"
    def execute(self, ctx):
        ctx["persistent"] = True
        return ctx

class GeminiKnight(Knight):
    NAME, HOUSE, ARCHETYPE = "Saga", 3, "Redundancy"
    def execute(self, ctx): return ctx

class CancerKnight(Knight):
    NAME, HOUSE, ARCHETYPE = "Deathmask", 4, "Firewall"
    def execute(self, ctx): return ctx

class LeoKnight(Knight):
    NAME, HOUSE, ARCHETYPE = "Aioria", 5, "Streaming"
    def execute(self, ctx): return ctx

class VirgoKnight(Knight):
    NAME, HOUSE, ARCHETYPE = "Shaka", 6, "Validation"
    def execute(self, ctx):
        if self.executor:
            return self.executor.process(ctx)
        return ctx

class LibraKnight(Knight):
    NAME, HOUSE, ARCHETYPE = "Dohko", 7, "Consensus"
    def execute(self, ctx): return ctx

class ScorpioKnight(Knight):
    NAME, HOUSE, ARCHETYPE = "Milo", 8, "Cleanup"
    def execute(self, ctx): return ctx

class SagittariusKnight(Knight):
    NAME, HOUSE, ARCHETYPE = "Aioros", 9, "Routing"
    def execute(self, ctx): return ctx

class CapricornKnight(Knight):
    NAME, HOUSE, ARCHETYPE = "Shura", 10, "Kernel"
    def execute(self, ctx):
        if self.executor: return self.executor.process(ctx)
        return ctx

class AquariusKnight(Knight):
    NAME, HOUSE, ARCHETYPE = "Camus", 11, "Sandbox"
    def execute(self, ctx): return ctx

class PiscesKnight(Knight):
    NAME, HOUSE, ARCHETYPE = "Afrodita", 12, "Presentation"
    def execute(self, ctx): return ctx
''')

# ------------------------------------------------------------
# 🐍 4. LA 13ª CASA: OFIUCO (starkcore/knights/ophiuchus.py)
# ------------------------------------------------------------
with open("starkcore/knights/ophiuchus.py", "w") as f:
    f.write('''from starkcore.knights.base import Context

class OphiuchusKnight:
    NAME = "Odysseus"
    HOUSE = 13
    ARCHETYPE = "Alquimia de la Excepción"
    LAW = "👑 Toda anomalía persistente debe tratarse primero como evidencia antes que como error."

    def investigate(self, error: Exception, ctx: Context, observer) -> Context:
        print(f"\\n🐍 \\033[1;33m[OFIUCO DESPIERTA]\\033[0m Enfoque: {self.ARCHETYPE}")
        print(f"   ↳ LEY OFIUCO: {self.LAW}")
        print(f"   ↳ Evidencia Colectada: {str(error)}")
        
        ctx["evidence"] = {
            "exception": type(error).__name__,
            "message": str(error),
            "remedied": True
        }
        ctx["learning_mode"] = True
        if observer:
            observer.record(13, self.NAME, "Investigate Anomaly", "MUTATED_TO_EVIDENCE")
        return ctx
''')

# ------------------------------------------------------------
# 🏛️ 5. EL ORQUESTADOR: EL TEMPLO (starkcore/sanctuary/temple.py)
# ------------------------------------------------------------
with open("starkcore/sanctuary/temple.py", "w") as f:
    f.write('''from typing import List
from starkcore.knights.base import Knight, Context, OmegaObserver
from starkcore.knights.ophiuchus import OphiuchusKnight

class Sanctuary:
    def __init__(self):
        self.knights: List[Knight] = []
        self.ophiuchus = OphiuchusKnight()
        self.observer = OmegaObserver()

    def register(self, knight: Knight):
        self.knights.append(knight)
        self.knights.sort(key=lambda k: k.HOUSE)

    def invoke(self, ctx: Context) -> Context:
        print(f"\\n✨ \\033[1;34m[Iniciando Procesamiento en el Templo]\\033[0m")
        for knight in self.knights:
            try:
                if knight.should_handle(ctx):
                    self.observer.record(knight.HOUSE, knight.NAME, "Enter House", "PROCEEDING")
                    ctx = knight.prepare(ctx)
                    
                    # Ejecución del Caballero (apoyado en su Executor si lo tiene)
                    print(f"  🏛️ Casa {knight.HOUSE}: {knight.NAME} ({knight.ARCHETYPE})")
                    ctx = knight.execute(ctx)
                    
                    ctx = knight.finalize(ctx)
                    self.observer.record(knight.HOUSE, knight.NAME, "Exit House", "SUCCESS")
            except Exception as exc:
                self.observer.record(knight.HOUSE, knight.NAME, "Crash", "TRIGGER_OPHIUCHUS")
                print(f"  💥 \\033[1;31m[Fallo en Casa {knight.HOUSE} - {knight.NAME}]\\033[0m -> Desvío Cósmico.")
                return self.ophiuchus.investigate(exc, ctx, self.observer)
        return ctx
''')

# ------------------------------------------------------------
# 🏃‍♂️ 6. EL EJECUTABLE CENTRAL (main.py)
# ------------------------------------------------------------
with open("main.py", "w") as f:
    f.write('''from starkcore.sanctuary.temple import Sanctuary
from starkcore.knights.zodiac import (
    AriesKnight, TaurusKnight, GeminiKnight, CancerKnight, LeoKnight,
    VirgoKnight, LibraKnight, ScorpioKnight, SagittariusKnight,
    CapricornKnight, AquariusKnight, PiscesKnight
)
from starkcore.executors.strategies import ValidationExecutor, KernelExecutor

def run_pipeline(has_anomaly: bool):
    santuario = Sanctuary()
    
    # Inyectar Executors específicos cumpliendo el desacoplamiento
    val_exec = ValidationExecutor()
    ker_exec = KernelExecutor()

    # Registrar las Casas del Santuario
    santuario.register(AriesKnight())
    santuario.register(TaurusKnight())
    santuario.register(GeminiKnight())
    santuario.register(CancerKnight())
    santuario.register(LeoKnight())
    santuario.register(VirgoKnight(executor=val_exec)) # Inyección de estrategia
    santuario.register(LibraKnight())
    santuario.register(ScorpioKnight())
    santuario.register(SagittariusKnight())
    santuario.register(CapricornKnight(executor=ker_exec)) # Inyección de estrategia
    santuario.register(AquariusKnight())
    santuario.register(PiscesKnight())

    ctx = {"anomaly": has_anomaly}
    final_ctx = santuario.invoke(ctx)
    
    print("\\n📊 \\033[1;36m[Contexto Final de la Red]\\033[0m:", final_ctx)
    print("👁️  \\033[1;35m[Logs del Observador Omega]\\033[0m:")
    for log in santuario.observer.logs:
        print(f"   ↳ Casa {log['house']} | {log['knight'].ljust(10)} | Acción: {log['action'].ljust(18)} | Status: {log['status']}")

if __name__ == "__main__":
    print("\\n🔥 === PRUEBA 1: CAMINO DEL GUERRERO (FLUJO NORMAL) ===")
    run_pipeline(has_anomaly=False)
    
    print("\\n🔥 === PRUEBA 2: EL DESPERTAR DE OFIUCO (FLUJO CON EXCEPCIÓN) ===")
    run_pipeline(has_anomaly=True)
''')

print("✅ Entorno modular desplegado correctamente.")
print("👉 Ejecuta ahora: 'python3 main.py' para ver la magia de StarkCore.")
