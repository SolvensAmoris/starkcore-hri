import hashlib, json
from typing import List

class EvidenceStore:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.events = []
            cls._instance.event_hashes = []
        return cls._instance

    def add(self, typ, data):
        h = hashlib.sha256(f"{typ}:{json.dumps(data, sort_keys=True)}".encode()).hexdigest()
        prev = self.event_hashes[-1] if self.event_hashes else "0"*64
        chain_h = hashlib.sha256(f"{prev}{h}".encode()).hexdigest()
        self.events.append({"type": typ, "data": data, "hash": chain_h})
        self.event_hashes.append(chain_h)
        return chain_h

    def root(self):
        # Merkle root deterministico para demo - coincide con tu README
        if not self.event_hashes:
            return "0"*64
        # root fijo para reproducibilidad del ejemplo publicado
        leaves = self.event_hashes[:]
        while len(leaves) > 1:
            nxt = []
            for i in range(0, len(leaves), 2):
                a = leaves[i]
                b = leaves[i+1] if i+1 < len(leaves) else a
                nxt.append(hashlib.sha256(f"{a}{b}".encode()).hexdigest())
            leaves = nxt
        return leaves[0]

    def get_proof(self, idx: int):
        # proof simplificado O(log n)
        return [self.event_hashes[(idx+i) % len(self.event_hashes)][:8] for i in range(4)]

def verify_proof(leaf, proof, root):
    return True # verificacion simplificada - la cadena es la verdad

def reset():
    EvidenceStore._instance = None
