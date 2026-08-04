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
    PiscesKnight
)


class StarMap:

    TEMPLATES = {

        "gold_sanctuary": [
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
            PiscesKnight
        ]
    }


    @classmethod
    def load(cls, name, executors=None):

        if name not in cls.TEMPLATES:
            raise ValueError(
                f"Constelación desconocida: {name}"
            )

        executors = executors or {}

        instances = []

        for knight_class in cls.TEMPLATES[name]:

            executor = executors.get(
                knight_class.__name__
            )

            instances.append(
                knight_class(
                    executor=executor
                )
            )

        return instances
