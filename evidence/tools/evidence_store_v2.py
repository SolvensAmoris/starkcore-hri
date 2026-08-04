# evidence_store_v2.py - EvidenceStore v2: Event Sourcing
import json, time, os
from pathlib import Path

class EvidenceStoreV2:
    def __init__(self, base_dir="evidence"):
        self.base = Path(base_dir)
        self.base.mkdir(exist_ok=True)
        self.log_path = self.base / "events.log"
        self.snapshot_path = self.base / "snapshot.json"
        self.counter = self._load_counter()

    def _load_counter(self):
        if not self.log_path.exists(): return 0
        try:
            return len(open(self.log_path).readlines())
        except: return 0

    def append(self, event_type, node_id, identity_hash, seed_decl, decision="ALLOWED"):
        self.counter += 1
        event = {
            "seq": self.counter,
            "ts": time.time(),
            "type": event_type,
            "node_id": node_id,
            "identity_hash": identity_hash,
            "seed_decl": seed_decl,
            "decision": decision
        }
        with open(self.log_path, "a") as f:
            f.write(json.dumps(event) + "\n")
        if self.counter % 100 == 0:
            self._make_snapshot()
        return event

    def _make_snapshot(self):
        state = {}
        if self.log_path.exists():
            with open(self.log_path, "r") as f:
                for line in f:
                    e = json.loads(line)
                    state[str(e["node_id"])] = e
        with open(self.snapshot_path, "w") as f:
            json.dump(state, f, indent=2)

    def replay(self):
        if not self.log_path.exists(): return []
        with open(self.log_path, "r") as f:
            return [json.loads(line) for line in f]

    def get_history(self, node_id):
        # FIX: comparar como string ambos lados
        target = str(node_id)
        return [e for e in self.replay() if str(e["node_id"])==target]

if __name__ == "__main__":
    import shutil
    if os.path.exists("evidence"): shutil.rmtree("evidence")
    store = EvidenceStoreV2()
    print("Escribiendo 500 eventos...")
    t0=time.time()
    for i in range(500):
        store.append("EXECUTED", i, f"hash_{i}", "SUN,NODE,ROOT,FLOW", "ALLOWED")
    print(f"500 eventos en {time.time()-t0:.3f}s")
    print("\nReplay de los últimos 3:")
    for e in store.replay()[-3:]:
        print(f" {e['seq']:06d} {e['type']} node={e['node_id']} {e['decision']}")
    print("\nAuditoría: ¿existe historia válida para node 42?")
    hist = store.get_history(42)
    print(f" Encontrados {len(hist)} eventos para node 42")
    if hist:
        print(f" {hist[0]}")
    else:
        print(" No hay historia")
