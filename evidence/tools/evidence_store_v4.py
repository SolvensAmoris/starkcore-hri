# evidence_store_v4.py - EvidenceStore v4: Merkle Root
# Un solo hash que resume toda la historia
import json, time, os, hashlib
from pathlib import Path

def sha256(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()

def merkle_root(hashes):
    """Calcula root de lista de hashes. Si impar, duplica el ultimo"""
    if not hashes: return "EMPTY"
    level = hashes[:]
    while len(level) > 1:
        next_level = []
        for i in range(0, len(level), 2):
            left = level[i]
            right = level[i+1] if i+1 < len(level) else left
            next_level.append(sha256(left + right))
        level = next_level
    return level[0]

def merkle_proof(hashes, index):
    """Prueba de inclusión: hermanos necesarios para llegar al root"""
    proof = []
    level = hashes[:]
    idx = index
    while len(level) > 1:
        is_right = idx % 2 == 1
        sibling_idx = idx - 1 if is_right else idx + 1
        if sibling_idx < len(level):
            proof.append((level[sibling_idx], is_right))
        else:
            proof.append((level[idx], is_right)) # duplicado
        # subir nivel
        next_level = []
        for i in range(0, len(level), 2):
            l = level[i]
            r = level[i+1] if i+1 < len(level) else l
            next_level.append(sha256(l + r))
        level = next_level
        idx //= 2
    return proof

def verify_proof(leaf_hash, proof, root):
    h = leaf_hash
    for sibling_hash, is_right in proof:
        if is_right:
            h = sha256(sibling_hash + h)
        else:
            h = sha256(h + sibling_hash)
    return h == root

class EvidenceStoreV4:
    def __init__(self, base_dir="evidence_v4"):
        self.base = Path(base_dir)
        self.base.mkdir(exist_ok=True)
        self.log_path = self.base / "events.log"
        self.counter = 0
        self.last_hash = "GENESIS"
        self.event_hashes = []
        self._load()

    def _load(self):
        if not self.log_path.exists(): return
        for line in open(self.log_path):
            e = json.loads(line)
            self.counter = e["seq"]
            self.last_hash = e["event_hash"]
            self.event_hashes.append(e["event_hash"])

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
        event_hash = sha256(json.dumps(payload, sort_keys=True))
        payload["event_hash"] = event_hash
        self.last_hash = event_hash
        self.event_hashes.append(event_hash)

        with open(self.log_path, "a") as f:
            f.write(json.dumps(payload) + "\n")
        return payload

    def root(self):
        return merkle_root(self.event_hashes)

    def get_proof(self, seq):
        # seq 1-indexed
        idx = seq - 1
        return merkle_proof(self.event_hashes, idx)

if __name__ == "__main__":
    import shutil
    if os.path.exists("evidence_v4"): shutil.rmtree("evidence_v4")
    store = EvidenceStoreV4()

    print("COSMOS EVIDENCE STORE v4 - Merkle Root\n")
    t0=time.time()
    for i in range(500):
        store.append("EXECUTED", i, f"hash_{i}", "SUN,NODE,ROOT,FLOW", "ALLOWED")
    print(f"500 eventos en {time.time()-t0:.3f}s")

    root = store.root()
    print(f"\nMerkle Root (resumen de 500 eventos):\n {root}")
    print(f" Longitud: {len(root)} chars, 32 bytes. Eso es todo para verificar 500.")

    # Probar inclusion de evento 42
    seq_target = 42
    proof = store.get_proof(seq_target)
    leaf = store.event_hashes[seq_target-1]
    print(f"\nPrueba de inclusión para seq {seq_target}:")
    print(f" Leaf hash: {leaf[:16]}...")
    print(f" Proof length: {len(proof)} hermanos (log2(500) ~ 9)")

    ok = verify_proof(leaf, proof, root)
    print(f" Verificación contra root: {'✅ VALIDA' if ok else '❌ INVALIDA'}")

    print("\n--- Magia ---")
    print("Ahora puedes publicar solo este root en otro lado (otro archivo, otro server).")
    print("Si alguien te entrega los 500 eventos, calculas el root y si coincide,")
    print("sabes que nadie tocó NADA. Un hash para gobernarlos a todos.")

    # Simular manipulación
    print("\n--- Ataque: modifico evento 42 ---")
    lines = open(store.log_path).readlines()
    e = json.loads(lines[41])
    e["decision"] = "HACKEADO"
    # recalcular su hash pero no el resto de la cadena
    e_copy = {k:v for k,v in e.items() if k!="event_hash"}
    e["event_hash"] = sha256(json.dumps(e_copy, sort_keys=True))
    lines[41] = json.dumps(e) + "\n"
    open(store.log_path,"w").writelines(lines)

    # Recalcular root malicioso
    from evidence_store_v4 import merkle_root as mr
    new_hashes = [json.loads(l)["event_hash"] for l in lines]
    new_root = mr(new_hashes)
    print(f" Root original: {root[:16]}...")
    print(f" Root atacado: {new_root[:16]}...")
    print(f" ¿Coinciden? {'SI' if root==new_root else 'NO - DETECTADO ✅'}")
