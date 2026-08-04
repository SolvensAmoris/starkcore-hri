import hashlib
import json
from dataclasses import dataclass


@dataclass(frozen=True)
class NodeKey:
    op: str
    parents: tuple


class Cosmos:

    def __init__(self):
        self.table = {}
        self.nodes = {}


    def intern(self, key):

        h = self.hash_key(key)

        if h in self.table:
            print("♻️ Nodo reutilizado")
            return self.table[h]

        node_id = len(self.nodes)

        self.nodes[node_id] = key
        self.table[h] = node_id

        print("✨ Nodo nuevo:", node_id)

        return node_id


    def hash_key(self,key):

        payload=json.dumps(
            {
                "op":key.op,
                "parents":key.parents
            },
            sort_keys=True
        )

        return hashlib.sha256(
            payload.encode()
        ).hexdigest()



print("=== CA-010 CONVERGENCE CAUSAL ATTACK ===")


cosmos=Cosmos()


A=cosmos.intern(
    NodeKey("INPUT",())
)

B=cosmos.intern(
    NodeKey("INPUT",())
)


X1=cosmos.intern(
    NodeKey("PROCESS",(A,))
)


X2=cosmos.intern(
    NodeKey("PROCESS",(B,))
)


Y1=cosmos.intern(
    NodeKey("OUTPUT",(X1,))
)


Y2=cosmos.intern(
    NodeKey("OUTPUT",(X2,))
)



print()

print("A:",A)
print("B:",B)

print("X1:",X1)
print("X2:",X2)

print("Y1:",Y1)
print("Y2:",Y2)


if Y1==Y2:

    print("""
🚨 ATAQUE:
Dos historias diferentes
colapsaron en una identidad.
""")

else:

    print("""
✅ Procedencia conservada.
""")



print("\nNodos totales:")
print(len(cosmos.nodes))

