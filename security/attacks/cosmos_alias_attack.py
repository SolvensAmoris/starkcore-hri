#!/usr/bin/env python3

import hashlib
from dataclasses import dataclass


@dataclass(frozen=True)
class NodeKey:

    op: str
    left: int | None
    right: int | None
    shape: str = "scalar"


    def hash_id(self):

        data = repr(
            (
                self.op,
                self.left,
                self.right,
                self.shape
            )
        )

        return hashlib.sha256(
            data.encode()
        ).hexdigest()



class CosmosDAG:


    def __init__(self):

        self.nodes = {}
        self.intern = {}


    def create(self, key):

        h = key.hash_id()

        if h in self.intern:

            print("♻️ Nodo reutilizado")

            return self.intern[h]


        node_id = len(self.nodes)

        self.nodes[node_id] = key
        self.intern[h] = node_id

        print("✨ Nodo nuevo:", node_id)

        return node_id



    def identity(self,node_id):

        return self.nodes[node_id].hash_id()



print("=== CA-007 ALIAS IDENTITY ATTACK ===")


cosmos = CosmosDAG()


# Nodo base compartido

A = cosmos.create(
    NodeKey(
        "INPUT",
        None,
        None
    )
)


# Dos ramas usan la misma identidad

B1 = cosmos.create(
    NodeKey(
        "ADD",
        A,
        10
    )
)


B2 = cosmos.create(
    NodeKey(
        "ADD",
        A,
        10
    )
)


print()

print("B1:", B1)
print("B2:", B2)


if B1 == B2:

    print("""
✅ ALIAS CONTROLADO

Dos caminos apuntan
a la misma identidad.
""")

else:

    print("""
🚨 DUPLICACIÓN

La misma estructura creó
dos entidades.
""")


print("\n=== ATAQUE DE MUTACIÓN ===")


original_hash = cosmos.identity(B1)


print("Hash antes:")
print(original_hash)


# Intento de modificar internamente
fake = NodeKey(
    "ADD",
    A,
    99
)


fake_hash = fake.hash_id()


print("\nHash atacante:")
print(fake_hash)


if fake_hash == original_hash:

    print("🚨 FALLA: mutación invisible")

else:

    print("✅ Mutación separada")


print("\nNodos totales:")
print(len(cosmos.nodes))

