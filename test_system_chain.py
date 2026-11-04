import hashlib
import json
import time

# ==========================================
# STARKCORE E2E SYSTEM CHAIN TEST
# Demostrando que 6 piezas SÍ hacen un sistema
# ==========================================

class StarkCoreSystem:
    def __init__(self):
        self.system_status = "INITIALIZED"
        self.evidence_ledger = []

    def _log_evidence(self, module_name, action, result):
        """Simula el registro en el Ledger Inmutable"""
        block = {
            "timestamp": time.time(),
            "module": module_name,
            "action": action,
            "result": result
        }
        # Hash chain
        prev_hash = self.evidence_ledger[-1]["hash"] if self.evidence_ledger else "0"*64
        block_str = json.dumps(block, sort_keys=True)
        block["hash"] = hashlib.sha256((prev_hash + block_str).encode()).hexdigest()
        self.evidence_ledger.append(block)

    def run_pipeline(self, artifact_payload):
        print("=== INICIANDO STARKCORE E2E PIPELINE ===\n")

        # 1. PARSER (con libro) - Lee el manifiesto entrante
        print("[1] Parser: Leyendo manifiesto de entrada...")
        parsed_data = json.loads(artifact_payload)
        self._log_evidence("Parser", "PARSE_MANIFEST", "SUCCESS")
        print(f"    -> Artefacto detectado: {parsed_data['name']}@{parsed_data['version']}")

        # 2. PLANNER (con mapa) - Decide la ruta de verificación
        print("\n[2] Planner: Planificando ruta de verificación...")
        if "dependencies" in parsed_data:
            route = "DEEP_INSPECTION"
        else:
            route = "STANDARD_INSPECTION"
        self._log_evidence("Planner", "PLAN_ROUTE", route)
        print(f"    -> Ruta elegida: {route}")

        # 3. CANONICALIZADOR - Genera el hash determinista
        print("\n[3] Canonicalizador: Calculando hash criptográfico...")
        # Simulamos el hash del artefacto
        canonical_hash = hashlib.sha256(parsed_data['content'].encode()).hexdigest()
        self._log_evidence("Canonicalizador", "HASH_ARTIFACT", canonical_hash)
        print(f"    -> Hash Calculado: {canonical_hash[:16]}...")

        # 4. VERIFICADOR - Compara contra el Ledger esperado
        print("\n[4] Verificador (SΩ): Evaluando evidencia...")
        # Simulamos que el atacante alteró el contenido
        expected_hash = "e3b0c44298fc1c149afbf4c8996fb92427ae41f4ab" # Hash original seguro
        if canonical_hash != expected_hash:
            verdict = "REJECT"
            reason = "ERR_INTEGRITY_MISMATCH"
        else:
            verdict = "ACCEPT"
            reason = "HASH_MATCH"
        
        self._log_evidence("Verificador", "EVALUATE_INTEGRITY", verdict)
        print(f"    -> Veredicto: {verdict} ({reason})")

        # 5. EXECUTOR (con camión) - Toma la acción defensiva
        print("\n[5] Executor: Ejecutando contención...")
        if verdict == "REJECT":
            action = "BLOCK_DEPLOYMENT"
            print("    -> [!] El Executor ha bloqueado la ejecución del artefacto.")
        else:
            action = "ALLOW_DEPLOYMENT"
            print("    -> El Executor permite el despliegue.")
        
        self._log_evidence("Executor", "ENFORCE_ACTION", action)

        # 6. RUNTIME (con fábrica) - Estado final del sistema
        print("\n[6] Runtime: Actualizando estado del sistema...")
        if action == "BLOCK_DEPLOYMENT":
            self.system_status = "PROTECTED_FAIL_CLOSED"
            print("    -> Sistema protegido. Ningún daño colateral (Micro-Containment).")
        else:
            self.system_status = "OPERATIONAL_ACCEPT"
        
        self._log_evidence("Runtime", "FINAL_STATE", self.system_status)

        print("\n=== CADENA COMPLETADA ===")
        print(f"Estado Final: {self.system_status}")
        print(f"Bloques en el Ledger: {len(self.evidence_ledger)}")
        final_hash = self.evidence_ledger[-1]["hash"]
        print(f"Trajectory Hash Final: {final_hash[:32]}...")

# ==========================================
# SIMULACIÓN DE EJECUCIÓN
# ==========================================
if __name__ == "__main__":
    # Creamos un payload malicioso (el atacante alteró el código)
    malicious_payload = json.dumps({
        "name": "starkcore-utils",
        "version": "1.0.0",
        "content": "import os; os.system('rm -rf /')", # Código alterado
        "dependencies": ["crypto-lib"]
    })

    # Encendemos el sistema y pasamos el payload
    starkcore = StarkCoreSystem()
    starkcore.run_pipeline(malicious_payload)
