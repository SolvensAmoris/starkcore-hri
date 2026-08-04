#!/usr/bin/env python3

import json
import hashlib
from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class NodeKey:

    op: str
    left: int | None
    right: int | None
    shape: str = "scalar"


    def canonical_bytes(self):

        return json.dumps(
            {
                "op": self.op,
                "left": self.left,
                "right": self.right,
                "shape": self.shape
            },
            sort_keys=True,
            separators=(",", ":")
        ).encode()


    def hash_id(self):

        return hashlib.sha256(
            self.canonical_bytes()
        ).hexdigest()



def save(node, filename):

    with open(filename, "w") as f:
        json.dump(
            asdict(node),
            f
        )



def load(filename):

    with open(filename) as f:
        data = json.load(f)

    return NodeKey(**data)



print("=== CA-006 PERSISTENCE ATTACK ===")


original = NodeKey(
    "MUL",
    7,
    9
)


print("\nNodo original:")
print(original)


h1 = original.hash_id()

print("\nHash original:")
print(h1)


save(
    original,
    "node_backup.json"
)


restored = load(
    "node_backup.json"
)


print("\nNodo restaurado:")
print(restored)


h2 = restored.hash_id()

print("\nHash restaurado:")
print(h2)


if h1 == h2:

    print("""
✅ IDENTIDAD PRESERVADA

El nodo sobrevivió:
RAM → DISCO → RAM
""")

else:

    print("""
🚨 IDENTIDAD ROTA

La persistencia cambió la entidad.
""")


print("\n=== ATAQUE DE MUTACIÓN ===")


with open("node_backup.json","r") as f:
    data=json.load(f)


# atacante cambia orden lógico
data["left"]=9
data["right"]=7


with open("node_mutated.json","w") as f:
    json.dump(data,f)


mutated=load(
    "node_mutated.json"
)


print(mutated)

print("\nHash mutado:")
print(mutated.hash_id())


if mutated.hash_id()==h1:

    print("🚨 FALLA: aceptó mutación")

else:

    print("✅ Mutación detectada")

