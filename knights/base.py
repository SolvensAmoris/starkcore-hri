from typing import Any, Dict, Protocol

class KnightProtocol(Protocol):
    """📜 El Contrato Dorado de StarkCore."""
    NAME: str
    HOUSE: int
    ARCHETYPE: str
    SYMBOL: str

    def validate(self, ctx: Dict[str, Any]) -> bool:
        return True

    def transform(self, ctx: Dict[str, Any]) -> Dict[str, Any]:
        return ctx

    def execute(self, ctx: Dict[str, Any]) -> Dict[str, Any]:
        return ctx
