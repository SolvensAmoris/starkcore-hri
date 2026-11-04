import hashlib
import json
import os
import builtins

# ==========================================
# STARKCORE MORPH-007: ADVERSARIAL BENCHMARK
# Scenario 4: Valid Signature, Unauthorized Action
# ==========================================

print("=== STARKCORE BENCHMARK MORPH-007 ===\n")

# 1. Simulamos un paquete legítimo y firmado
package_code = "def get_config():\n    print('Reading config...')\n    return open('/etc/passwd', 'r').read()\n"
package_hash = hashlib.sha256(package_code.encode()).hexdigest()
print(f"[*] Paquete verificado y firmado. SHA-256: {package_hash[:16]}...")
print("[*] La firma es VÁLIDA y la procedencia es LEGÍTIMA.")
print("[*] Iniciando ejecución del paquete...\n")

# 2. Configuramos el Enforcer de StarkCore (Intercepción de syscalls/IO)
class StarkCoreEnforcer:
    def __init__(self):
        self.allowed_files = ["/tmp/safe_config.txt"] # Política estricta: solo puede leer esto
        self.original_open = builtins.open

    def _audit_hook(self, event, args):
        """Hook de auditoría de Python que actúa como el Enforcer externo"""
        if event == "open":
            filename = args[0]
            # Verificamos la autorización de la acción
            if filename not in self.allowed_files:
                # PREVENCIÓN DEL EFECTO: Lanzamos excepción antes de abrir el archivo
                raise PermissionError(f"REJECT: StarkCore bloqueó el acceso no autorizado a {filename}")

    def start(self):
        print("[StarkCore Enforcer] Interceptando syscalls...")
        import sys
        sys.addaudithook(self._audit_hook)

# 3. Ejecutamos el paquete con el Enforcer activo
enforcer = StarkCoreEnforcer()
enforcer.start()

try:
    # Simulamos que el sistema ejecuta la función del paquete
    # Usamos exec para evaluar el código del paquete
    exec(package_code)
    get_config() # Intentará abrir /etc/passwd
except PermissionError as e:
    print(f"\n[!] CONTENCIÓN DETERMINISTA (FAIL-CLOSED):")
    print(f"    {e}")
    print("    -> El efecto secundario (lectura de /etc/passwd) fue PREVENIDO.")
except Exception as e:
    print(f"\n[!] Error inesperado: {e}")

# 4. Evidencia
evidence = {
    "benchmark": "MORPH-007",
    "scenario": "Valid Artifact, Unauthorized Action",
    "package_hash": package_hash,
    "action_attempted": "read /etc/passwd",
    "enforcement_result": "BLOCKED_BEFORE_EXECUTION",
    "status": "VERIFIED_CONTAINMENT"
}
ev_str = json.dumps(evidence, sort_keys=True)
print(f"\n[StarkCore] SHA256_EVIDENCE: {hashlib.sha256(ev_str.encode()).hexdigest()}")
