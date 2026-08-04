import json
import os

class EvidenceRegistry:
    """💾 Almacenamiento Atómico de Anomalías. Mantiene la memoria viva en el disco duro."""
    def __init__(self, filename="starkcore/evidence/immunological_memory.json"):
        self.filename = filename
        self.memory = self._load_from_disk()

    def _load_from_disk(self) -> dict:
        if not os.path.exists(self.filename):
            return {}
        try:
            with open(self.filename, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            print("⚠️ [Alerta de Memoria] Archivo corrupto detectado. Inicializando base de datos vacía.")
            return {}

    def save_to_disk(self):
        # Crear directorios si fueron borrados en caliente
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        try:
            with open(self.filename, "w") as f:
                json.dump(self.memory, f, indent=4)
        except IOError as e:
            print(f"💥 [Error Crítico de Disco] No se pudo guardar la evidencia: {e}")

    def get_expedient(self, anomaly_hash: str) -> dict:
        return self.memory.get(anomaly_hash, None)

    def register_encounter(self, anomaly_hash: str, exception_type: str, house: int) -> dict:
        """Incrementa la frecuencia del ataque y actualiza el expediente en disco."""
        if anomaly_hash not in self.memory:
            self.memory[anomaly_hash] = {
                "exception_type": exception_type,
                "first_seen_house": house,
                "frequency": 0,
                "disposition": "NEW_EXPEDIENT",
                "patched_at_epoch": None
            }
        
        self.memory[anomaly_hash]["frequency"] += 1
        
        # Si llega al umbral de 3 ataques, Ofiuco decreta INMUNIDAD PERMANENTE
        if self.memory[anomaly_hash]["frequency"] >= 3:
            self.memory[anomaly_hash]["disposition"] = "PERMANENT_IMMUNITY_PATCH"
            import time
            self.memory[anomaly_hash]["patched_at_epoch"] = time.time()
            
        self.save_to_disk()
        return self.memory[anomaly_hash]
