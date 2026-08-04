"""
╔══════════════════════════════════════════════════════════════╗
║                   STARKCORE SANCTUARY                       ║
║        AION Protocol - Temple of the Thirteen Houses        ║
╚══════════════════════════════════════════════════════════════╝

Ley Ofiuco
-----------
"Toda anomalía persistente debe tratarse primero como evidencia
antes que como error."

Este archivo es un prototipo conceptual del Santuario.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, Any, List


# ============================================================
# Contexto
# ============================================================

Context = Dict[str, Any]


# ============================================================
# Caballero Base
# ============================================================

class Knight(ABC):

    NAME = "Unknown"
    HOUSE = 0
    ARCHETYPE = "Undefined"

    def should_handle(self, ctx: Context) -> bool:
        return True

    def prepare(self, ctx: Context) -> Context:
        return ctx

    @abstractmethod
    def execute(self, ctx: Context) -> Context:
        pass

    def finalize(self, ctx: Context) -> Context:
        return ctx


# ============================================================
# Casas del Santuario
# ============================================================

class AriesKnight(Knight):

    NAME = "Mu"
    HOUSE = 1
    ARCHETYPE = "Bootstrap"

    def execute(self, ctx):

        print("♈ Aries :: Inicializando contexto")

        ctx.setdefault("boot", True)

        return ctx


class TaurusKnight(Knight):

    NAME = "Aldebarán"
    HOUSE = 2
    ARCHETYPE = "Persistence"

    def execute(self, ctx):

        print("♉ Tauro :: Persistencia validada")

        ctx["persistent"] = True

        return ctx


class GeminiKnight(Knight):

    NAME = "Saga"

    HOUSE = 3

    ARCHETYPE = "Redundancy"

    def execute(self, ctx):

        print("♊ Géminis :: Preparando redundancia")

        return ctx


class CancerKnight(Knight):

    NAME = "Deathmask"

    HOUSE = 4

    ARCHETYPE = "Firewall"

    def execute(self, ctx):

        print("♋ Cáncer :: Revisando amenazas")

        return ctx


class LeoKnight(Knight):

    NAME = "Aioria"

    HOUSE = 5

    ARCHETYPE = "Streaming"

    def execute(self, ctx):

        print("♌ Leo :: Flujo acelerado")

        return ctx


class VirgoKnight(Knight):

    NAME = "Shaka"

    HOUSE = 6

    ARCHETYPE = "Validation"

    def execute(self, ctx):

        print("♍ Virgo :: Discernimiento")

        if ctx.get("anomaly"):

            raise RuntimeError("Patrón desconocido")

        return ctx


class LibraKnight(Knight):

    NAME = "Dohko"

    HOUSE = 7

    ARCHETYPE = "Consensus"

    def execute(self, ctx):

        print("♎ Libra :: Consenso logrado")

        return ctx


class ScorpioKnight(Knight):

    NAME = "Milo"

    HOUSE = 8

    ARCHETYPE = "Cleanup"

    def execute(self, ctx):

        print("♏ Escorpio :: Eliminando residuos")

        return ctx


class SagittariusKnight(Knight):

    NAME = "Aioros"

    HOUSE = 9

    ARCHETYPE = "Routing"

    def execute(self, ctx):

        print("♐ Sagitario :: Ruta establecida")

        return ctx


class CapricornKnight(Knight):

    NAME = "Shura"

    HOUSE = 10

    ARCHETYPE = "Kernel"

    def execute(self, ctx):

        print("♑ Capricornio :: Núcleo estable")

        return ctx


class AquariusKnight(Knight):

    NAME = "Camus"

    HOUSE = 11

    ARCHETYPE = "Sandbox"

    def execute(self, ctx):

        print("♒ Acuario :: Aislamiento activo")

        return ctx


class PiscesKnight(Knight):

    NAME = "Afrodita"

    HOUSE = 12

    ARCHETYPE = "Presentation"

    def execute(self, ctx):

        print("♓ Piscis :: Preparando salida")

        return ctx


# ============================================================
# OFIUCO
# ============================================================

class OphiuchusKnight:

    NAME = "Odysseus"

    TITLE = "The Hidden House"

    LAW = (
        "Toda anomalía persistente debe tratarse primero "
        "como evidencia antes que como error."
    )

    def investigate(self, error: Exception, ctx: Context):

        print()
        print("🐍 OFIUCO DESPIERTA")
        print("-------------------")
        print(self.LAW)
        print()

        ctx["evidence"] = {
            "exception": str(error),
            "captured": True,
        }

        ctx["learning"] = True

        return ctx


# ============================================================
# SANTUARIO
# ============================================================

class Sanctuary:

    def __init__(self):

        self.knights: List[Knight] = []

        self.ophiuchus = OphiuchusKnight()

    def register(self, knight: Knight):

        self.knights.append(knight)

        self.knights.sort(key=lambda k: k.HOUSE)

    def invoke(self, ctx: Context):

        for knight in self.knights:

            try:

                if knight.should_handle(ctx):

                    ctx = knight.prepare(ctx)

                    ctx = knight.execute(ctx)

                    ctx = knight.finalize(ctx)

            except Exception as exc:

                return self.ophiuchus.investigate(exc, ctx)

        return ctx


# ============================================================
# DEMO
# ============================================================

if __name__ == "__main__":

    sanctuary = Sanctuary()

    sanctuary.register(AriesKnight())
    sanctuary.register(TaurusKnight())
    sanctuary.register(GeminiKnight())
    sanctuary.register(CancerKnight())
    sanctuary.register(LeoKnight())
    sanctuary.register(VirgoKnight())
    sanctuary.register(LibraKnight())
    sanctuary.register(ScorpioKnight())
    sanctuary.register(SagittariusKnight())
    sanctuary.register(CapricornKnight())
    sanctuary.register(AquariusKnight())
    sanctuary.register(PiscesKnight())

    print("\n===== EJECUCIÓN NORMAL =====\n")

    result = sanctuary.invoke({})

    print("\nResultado:")
    print(result)

    print("\n===== EJECUCIÓN CON ANOMALÍA =====\n")

    result = sanctuary.invoke({
        "anomaly": True
    })

    print("\nResultado:")
    print(result)

