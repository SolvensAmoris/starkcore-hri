class OphiuchusKnight:
    NAME = "Odysseus"
    HOUSE = 13
    LAW = "🐍 Toda anomalía persistente debe tratarse primero como evidencia antes que como error."

    def investigate(self, error: Exception, house_failed: int, ctx: dict, observer) -> dict:
        print(f"\n🐍 \033[1;33m[OFIUCO DESPIERTA]\033[0m -> Interceptando colapso en Casa {house_failed}.")
        
        # Calcular el hash único del ataque
        anomaly_hash = observer.compute_anomaly_hash(error, house_failed)
        
        # Registrar o actualizar el expediente directamente en el disco duro a través de Omega
        expedient = observer.registry.register_encounter(anomaly_hash, type(error).__name__, house_failed)

        if expedient["disposition"] == "PERMANENT_IMMUNITY_PATCH":
            # 💡 PARCHE DE INMUNIDAD ATÓMICA
            print(f"   🛡️ \033[1;32m[INMUNIDAD ABSOLUTA - DISCO]\033[0m Hash: {anomaly_hash} | Avistamientos: {expedient['frequency']}.")
            print(f"   ↳ Ley Ofiuco aplicada: El veneno se transmutó en anticuerpo.")
            ctx["kernel_immunity"] = True
            ctx["anomaly"] = False  # El error es neutralizado en caliente
            observer.record(13, self.NAME, "Apply Disk Patch", "SYSTEM_INMUNIZED")
            return {"status": "REMEDIED_BY_DISK_IMMUNITY", "ctx": ctx}
        else:
            # 🔍 INVESTIGACIÓN ABIERTA
            print(f"   🔍 \033[1;35m[EXPEDIENTE ABIERTA EN DISCO]\033[0m Hash: {anomaly_hash} | Frecuencia: {expedient['frequency']}/3")
            observer.record(13, self.NAME, "Log Evidence to Disk", "EXPEDIENT_SAVED", {"hash": anomaly_hash})
            ctx["evidence"] = {
                "hash": anomaly_hash,
                "exception": type(error).__name__,
                "attempts": expedient["frequency"]
            }
            ctx["learning_mode"] = True
            return {"status": "COLLECTED_AS_PERSISTENT_EVIDENCE", "ctx": ctx}
