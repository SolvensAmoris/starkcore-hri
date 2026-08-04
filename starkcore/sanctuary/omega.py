import hashlib
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
