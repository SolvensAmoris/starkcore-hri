from typing import Any, Dict

class OphiuchusKnight:
    NAME = "Odysseus de Ofiuco"
    HOUSE = 13
    ARCHETYPE = "Alquimia de la Excepción"
    SYMBOL = "⛎"

    def validate(self, ctx: Dict[str, Any]) -> bool:
        return True

    def transform(self, ctx: Dict[str, Any]) -> Dict[str, Any]:
        ctx["ofiuco_flag"] = True
        ctx["nota"] = "Anomalia persistente detectada como posible nueva ley"
        return ctx

    def execute(self, anomaly_context: Dict[str, Any]) -> Dict[str, Any]:
        print(f"🔱 {self.SYMBOL} Ofiuco Activado: {anomaly_context.get('error_code')} -> Mutando en conocimiento...")
        anomaly_context["resolucion"] = "TRANSMUTADA"
        anomaly_context["nueva_regla_propuesta"] = f"Ofiuco-Law-{anomaly_context.get('hash_canonico','UNKNOWN')}"
        return anomaly_context
