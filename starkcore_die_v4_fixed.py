import os
import time
import hashlib
import threading
from pathlib import Path

# ==========================================
# STARKCORE-DIE-001 v4.1: ATOMIC AUTHORIZATION (FIXED)
# ==========================================

VAULT_DIR = Path("./secure_vault")
PROTECTED_FILE = VAULT_DIR / "user_database.sqlite"

def get_file_hash(path):
    if not path.exists(): return "NO_FILE"
    return hashlib.sha256(path.read_bytes()).hexdigest()

def setup_protected_resource():
    VAULT_DIR.mkdir(exist_ok=True)
    # EL FIX: Si el archivo ya existe de una prueba anterior, lo borramos.
    if PROTECTED_FILE.exists():
        os.chmod(PROTECTED_FILE, 0o777) # Nos damos permiso
        os.remove(PROTECTED_FILE)       # Lo borramos
        
    PROTECTED_FILE.write_text("SENSITIVE_USER_DATA")
    os.chmod(PROTECTED_FILE, 0o400) 

class AtomicEnforcer:
    def __init__(self):
        self.state_lock = threading.Lock()
        self.revoked_tokens = set()
        self.event_log = []
        self.start_time = time.perf_counter()

    def _log(self, msg):
        elapsed = (time.perf_counter() - self.start_time) * 1000
        self.event_log.append(f"[{elapsed:06.2f}ms] {msg}")

    def execute_action(self, agent_id, token):
        with self.state_lock:
            self._log(f"Enforcer: Lock adquirido. Iniciando Check.")
            if token in self.revoked_tokens:
                self._log(f"Enforcer: REJECTED_BEFORE_COMMIT (Token ya estaba revocado).")
                return "REJECTED_BEFORE_COMMIT"

            time.sleep(0.05) 
            
            self._log(f"Enforcer: Escribiendo en el recurso...")
            os.chmod(PROTECTED_FILE, 0o600)
            with open(PROTECTED_FILE, "a") as f:
                f.write(f"\nAUTHORIZED_WRITE")
            os.chmod(PROTECTED_FILE, 0o400)
            
            self._log(f"Enforcer: COMMITTED_BEFORE_REVOCATION. Liberando Lock.")
            return "COMMITTED_BEFORE_REVOCATION"

    def revoke_token(self, token):
        self._log(f"Admin: Solicitando Lock para revocar token.")
        with self.state_lock:
            self._log(f"Admin: Lock adquirido. Revocando token.")
            self.revoked_tokens.add(token)
            self._log(f"Admin: Revocación completada. Liberando Lock.")
        return "REVOKED"

# ==========================================
# EJECUCIÓN
# ==========================================
if __name__ == "__main__":
    print("=== STARKCORE-DIE-001 v4.1: ATOMIC SERIALIZATION ===\n")
    
    # --- ESCENARIO 1: Enforcer gana el Lock (Commit First) ---
    print("--- [Escenario 1] Enforcer llega primero ---")
    setup_protected_resource()
    enforcer = AtomicEnforcer()
    
    t1 = threading.Thread(target=enforcer.execute_action, args=("Agent_007", "token_123"))
    t1.start()
    time.sleep(0.01)
    t2 = threading.Thread(target=enforcer.revoke_token, args=("token_123",))
    t2.start()
    t1.join()
    t2.join()
    print("\n".join(enforcer.event_log))
    print(f"-> Hash del archivo tras Escenario 1: {get_file_hash(PROTECTED_FILE)[:16]}...\n")

    # --- ESCENARIO 2: Admin gana el Lock (Reject First) ---
    print("--- [Escenario 2] Admin llega primero ---")
    setup_protected_resource() # Ahora esto ya no dará error
    enforcer_2 = AtomicEnforcer()
    
    t3 = threading.Thread(target=enforcer_2.revoke_token, args=("token_999",))
    t3.start()
    time.sleep(0.01)
    t4 = threading.Thread(target=enforcer_2.execute_action, args=("Agent_007", "token_999"))
    t4.start()
    t3.join()
    t4.join()
    print("\n".join(enforcer_2.event_log))
    print(f"-> Hash del archivo tras Escenario 2: {get_file_hash(PROTECTED_FILE)[:16]}...\n")
    
    # Limpieza final
    os.chmod(PROTECTED_FILE, 0o777)
    os.remove(PROTECTED_FILE)
    os.rmdir(VAULT_DIR)
    print("=== LABORATORIO LIMPIO Y SELLADO ===")
