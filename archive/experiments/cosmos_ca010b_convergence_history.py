import hashlib
import json
from dataclasses import dataclass


@dataclass(frozen=True)
class NodeKey:
    op: str
    parents: tuple
    data: str = ""


class Cosmos:

    def __init__(self):
        self.table = {}
        self.nodes = {}


    def hash_key(self, key):

        payload = json.dumps(
            {
                "op": key.op,
                "parents": key.parents,
                "data": key.data
            },
            sort_keys=True
        )

        return hashlib.sha256(
            payload.encode()
        ).hexdigest()


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



print("=== CA-010b CONVERGENCE HISTORY ATTACK ===")


cosmos = Cosmos()


# Dos orígenes diferentes

sensor_A = cosmos.intern(
    NodeKey(
        "INPUT",
        (),
        "sensor_A"
    )
)


sensor_B = cosmos.intern(
    NodeKey(
        "INPUT",
        (),
        "sensor_B"
    )
)



# Misma transformación

proc_A = cosmos.intern(
    NodeKey(
        "NORMALIZE",
        (sensor_A,),
        "temperature"
    )
)


proc_B = cosmos.intern(
    NodeKey(
        "NORMALIZE",
        (sensor_B,),
        "temperature"
    )
)



# Mismo resultado aparente

out_A = cosmos.intern(
    NodeKey(
        "OUTPUT",
        (proc_A,),
        "value=25"
    )
)


out_B = cosmos.intern(
    NodeKey(
        "OUTPUT",
        (proc_B,),
        "value=25"
    )
)



print()

print("sensor_A:", sensor_A)
print("sensor_B:", sensor_B)

print("proc_A:", proc_A)
print("proc_B:", proc_B)

print("out_A:", out_A)
print("out_B:", out_B)



if out_A == out_B:

    print("""
🚨 CA-010b:
Dos trayectorias distintas
colapsaron.
""")

else:

    print("""
✅ Procedencia conservada:
mismo resultado ≠ misma historia.
""")


print()

print("Nodos totales:")
print(len(cosmos.nodes))


print("\n=== GRAFO ===")

for k,v in cosmos.nodes.items():
    print(k, v)

