from typing import List

from starkcore.knights.zodiac import ImmuneKnight


class Sanctuary:
    """
    Templo central de ejecución.
    Coordina Caballeros, sensores y respuesta.
    """

    def __init__(self, observer=None):
        self.knights: List[ImmuneKnight] = []
        self.observer = observer

    def load_constellation(self, name: str, executors=None):
        """
        Carga la constelación dorada.
        """

        executors = executors or {}

        from starkcore.knights.zodiac import (
            AriesKnight,
            TaurusKnight,
            GeminiKnight,
            CancerKnight,
            LeoKnight,
            VirgoKnight,
            LibraKnight,
            ScorpioKnight,
            SagittariusKnight,
            CapricornKnight,
            AquariusKnight,
            PiscesKnight,
        )

        self.knights = [
            AriesKnight(),
            TaurusKnight(),
            GeminiKnight(),
            CancerKnight(),
            LeoKnight(),
            VirgoKnight(
                executors.get("VirgoKnight")
            ),
            LibraKnight(),
            ScorpioKnight(),
            SagittariusKnight(),
            CapricornKnight(
                executors.get("CapricornKnight")
            ),
            AquariusKnight(),
            PiscesKnight(),
        ]

    def invoke(self, ctx: dict):

        for knight in self.knights:

            try:
                if not knight.should_handle(ctx):
                    continue

                if self.observer:
                    self.observer.record(
                        knight.HOUSE,
                        knight.NAME,
                        "ENTER",
                        "PROCEEDING"
                    )

                ctx = knight.prepare(ctx)

                # Primera línea de defensa
                if hasattr(
                    knight,
                    "execute_with_sensor"
                ):
                    ctx = knight.execute_with_sensor(ctx)
                else:
                    ctx = knight.execute(ctx)

                ctx = knight.finalize(ctx)

                if self.observer:
                    self.observer.record(
                        knight.HOUSE,
                        knight.NAME,
                        "EXIT",
                        "SUCCESS"
                    )

            except Exception as exc:

                if self.observer:
                    self.observer.record(
                        knight.HOUSE,
                        knight.NAME,
                        "INTRUSION_BLOCKED",
                        "OPHIUCHUS"
                    )

                ctx["evidence"] = {
                    "house": knight.HOUSE,
                    "knight": knight.NAME,
                    "exception": str(exc)
                }

                ctx["learning_mode"] = True

                return (
                    "OPHIUCHUS_INTERVENTION",
                    ctx
                )

        return (
            "SUCCESSFUL_RUN",
            ctx
        )
