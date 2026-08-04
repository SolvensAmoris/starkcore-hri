from starkcore.immunity.sensor import ThreatSensor


class ImmuneKnight:
    """
    Caballero Dorado con capa inmune integrada.
    """

    NAME = "Unknown"
    HOUSE = 0
    ARCHETYPE = "Undefined"

    def __init__(self, executor=None):
        self.executor = executor
        self.sensor = ThreatSensor()

    def prepare(self, ctx):
        return ctx

    def finalize(self, ctx):
        return ctx

    def should_handle(self, ctx):
        return True

    def execute_with_sensor(self, ctx):
        self.sensor.scan(
            ctx,
            self.HOUSE,
            self.NAME
        )

        return self.execute(ctx)

    def execute(self, ctx):
        return ctx


class AriesKnight(ImmuneKnight):
    NAME = "Mu"
    HOUSE = 1
    ARCHETYPE = "Bootstrap"

    def execute(self, ctx):
        ctx["boot"] = True
        return ctx


class TaurusKnight(ImmuneKnight):
    NAME = "Aldebaran"
    HOUSE = 2
    ARCHETYPE = "Persistence"

    def execute(self, ctx):
        ctx["persistent"] = True
        return ctx


class GeminiKnight(ImmuneKnight):
    NAME = "Saga"
    HOUSE = 3
    ARCHETYPE = "Redundancy"


class CancerKnight(ImmuneKnight):
    NAME = "Deathmask"
    HOUSE = 4
    ARCHETYPE = "Firewall"


class LeoKnight(ImmuneKnight):
    NAME = "Aioria"
    HOUSE = 5
    ARCHETYPE = "Streaming"


class VirgoKnight(ImmuneKnight):
    NAME = "Shaka"
    HOUSE = 6
    ARCHETYPE = "Validation"

    def execute(self, ctx):
        if self.executor:
            return self.executor.process(ctx)

        if ctx.get("anomaly"):
            raise RuntimeError(
                "Anomalía detectada por Virgo"
            )

        return ctx


class LibraKnight(ImmuneKnight):
    NAME = "Dohko"
    HOUSE = 7
    ARCHETYPE = "Consensus"


class ScorpioKnight(ImmuneKnight):
    NAME = "Milo"
    HOUSE = 8
    ARCHETYPE = "Cleanup"


class SagittariusKnight(ImmuneKnight):
    NAME = "Aioros"
    HOUSE = 9
    ARCHETYPE = "Routing"


class CapricornKnight(ImmuneKnight):
    NAME = "Shura"
    HOUSE = 10
    ARCHETYPE = "Kernel"

    def execute(self, ctx):
        if self.executor:
            return self.executor.process(ctx)

        return ctx


class AquariusKnight(ImmuneKnight):
    NAME = "Camus"
    HOUSE = 11
    ARCHETYPE = "Sandbox"


class PiscesKnight(ImmuneKnight):
    NAME = "Afrodita"
    HOUSE = 12
    ARCHETYPE = "Presentation"
