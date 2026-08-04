# evidence_store_v3.py - EvidenceStore v3: Hash Chain
# Si alteras el pasado, el futuro ya no coincide
import json, time, os, hashlib
from pathlib import Path

def sha256(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()

class EvidenceStoreV3:
    def __init__(self, base_dir="evidence_v3"):
        self.base = Path(base_dir)
        self.base.mkdir(exist_ok=True)
        self.log_path = self.base / "events.log"
        self.snapshot_path = self.base / "snapshot.json"
        self.counter = 0
        self.last_hash = "GENESIS"
        self._load_state()

    def _load_state(self):
        if not self.log_path.exists(): return
        try:
            lines = open(self.log_path).readlines()
            if not lines: return
            last = json.loads(lines[-1])
            self.counter = last["seq"]
            self.last_hash = last["event_hash"]
        except: pass

    def append(self, event_type, node_id, identity_hash, seed_decl, decision="ALLOWED"):
        self.counter += 1
        payload = {
            "seq": self.counter,
            "ts": time.time(),
            "type": event_type,
            "node_id": node_id,
            "identity_hash": identity_hash,
            "seed_decl": seed_decl,
            "decision": decision,
            "prev_hash": self.last_hash
        }
        # Hash encadenado: hash actual = hash(prev_hash + resto del evento)
        event_hash = sha256(json.dumps(payload, sort_keys=True))
        payload["event_hash"] = event_hash
        self.last_hash = event_hash

        with open(self.log_path, "a") as f:
            f.write(json.dumps(payload) + "\n")

        if self.counter % 100 == 0:
            self._make_snapshot()
        return payload

    def _make_snapshot(self):
        state={}
        if self.log_path.exists():
            with open(self.log_path) as f:
                for line in f:
                    e=json.loads(line)
                    state[str(e["node_id"])]=e
        with open(self.snapshot_path, "w") as f:
            json.dump({"last_hash": self.last_hash, "state": state}, f, indent=2)

    def replay(self):
        if not self.log_path.exists(): return []
        return [json.loads(l) for l in open(self.log_path)]

    def verify_chain(self):
        """Verifica que nadie tocó el log a mano"""
        prev = "GENESIS"
        for i, e in enumerate(self.replay(), 1):
            # Recalcular hash
            copy = {k:v for k,v in e.items() if k!= "event_hash"}
            expected_prev = copy["prev_hash"]
            if expected_prev!= prev:
                return False, f"Ruptura en seq {e['seq']}: prev_hash no coincide. Esperado {prev[:8]}, encontrado {expected_prev[:8]}"
            recalc = sha256(json.dumps(copy, sort_keys=True))
            if recalc!= e["event_hash"]:
                return False, f"Ruptura en seq {e['seq']}: event_hash manipulado"
            prev = e["event_hash"]
        return True, f"Cadena OK: {len(self.replay())} eventos verificados, ultimo hash {prev[:12]}..."

    def get_history(self, node_id):
        target=str(node_id)
        return [e for e in self.replay() if str(e["node_id"])==target]

if __name__ == "__main__":
    import shutil
    if os.path.exists("evidence_v3"): shutil.rmtree("evidence_v3")
    store = EvidenceStoreV3()

    print("COSMOS EVIDENCE STORE v3 - Hash Chain\n")
    print("Escribiendo 500 eventos...")
    t0=time.time()
    for i in range(500):
        store.append("EXECUTED", i, f"hash_{i}", "SUN,NODE,ROOT,FLOW", "ALLOWED")
    print(f"500 eventos en {time.time()-t0:.3f}s")

    ok, msg = store.verify_chain()
    print(f"\nVerificación: {msg}")

    print("\n--- Simulando manipulación ---")
    print("Alterando evento 42 en el archivo a mano...")
    lines = open(store.log_path).readlines()
    e42 = json.loads(lines[41])
    e42["decision"] = "DENIED_FAKE" # atacante edita
    lines[41] = json.dumps(e42) + "\n"
    open(store.log_path,"w").writelines(lines)

    ok2, msg2 = store.verify_chain()
    print(f"Verificación después del ataque: {msg2}")
    print(f"\n{'✅ DETECTADO' if not ok2 else '❌ NO DETECTADO'}: El sistema detectó la manipulación")

    print("\nHistoria de node 42 (aunque fue alterada, queda trazada):")
    print(store.get_history(42)[0])
