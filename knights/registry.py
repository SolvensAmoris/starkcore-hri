from typing import Dict, Any
from.ophiuchus import OphiuchusKnight

class TempleRegistry:
    def __init__(self):
        self.knights = {
            13: OphiuchusKnight(),
        }

    def process(self, ctx: Dict[str, Any]) -> Dict[str, Any]:
        if ctx.get("es_anomalia_persistente"):
            return self.knights[13].execute(ctx)
        # Flujo normal por las 12 casas
        return ctx
