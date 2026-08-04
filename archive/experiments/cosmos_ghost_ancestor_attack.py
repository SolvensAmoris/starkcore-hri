import hashlib
import json
from dataclasses import dataclass


class CausalError(Exception):
    pass


@dataclass(frozen=True)
class Node:
    name: str
    parents: tuple


class Cosmos:

    def __init__(self):
        self.nodes = {}

    def add(self, node):
        if self.detect_cycle(node.name, node.parents):
            raise CausalError(
                f"Ciclo causal detectado en {node.name}"
            )

        self.nodes[node.name] = node

    def detect_cycle(self, name, parents, visited=None):

        if visited is None:
            visited = set()

        if name in visited:
            return True

        visited.add(name)

        if name not in self.nodes:
            return False

        for p in self.nodes[name].parents:
            if self.detect_cycle(p, (), visited):
                return True

        return False


    def identity(self, name, stack=None):

        if stack is None:
            stack = set()

        if name in stack:
            raise CausalError(
                "Identidad infinita: ciclo detectado"
            )

        stack.add(name)

        node = self.nodes[name]

        parent_ids = tuple(
            self.identity(p, stack.copy())
            for p in node.parents
        )

        payload = json.dumps(
            {
                "name": node.name,
                "parents": parent_ids
            },
            sort_keys=True
        )

        return hashlib.sha256(
            payload.encode()
        ).hexdigest()



print("=== CA-009b GHOST ANCESTOR ATTACK ===")


cosmos = Cosmos()


print("\n=== HISTORIA NORMAL ===")


cosmos.add(Node("A", ()))
cosmos.add(Node("B", ("A",)))
cosmos.add(Node("C", ("B",)))


good = cosmos.identity("C")

print("Hash C legítimo:")
print(good)


print("\n=== ATAQUE: ANCESTRO FANTASMA ===")


# Intentamos insertar una historia imposible:
#
# C depende de B
# B depende de A
# A depende de C
#
# La serpiente intenta comerse su propia cola.


try:

    cosmos.nodes["A"] = Node(
        "A",
        ("C",)
    )

    bad = cosmos.identity("C")

    print(
        "🚨 FALLA: ciclo aceptado"
    )

    print(bad)


except CausalError as e:

    print(
        "✅ ATAQUE DETENIDO"
    )

    print(e)


print("\n=== VEREDICTO ===")

print("""
Si un nodo puede existir sin historia verificable:
la identidad causal está rota.

Si toda identidad necesita ancestros válidos:
la procedencia está protegida.
""")

