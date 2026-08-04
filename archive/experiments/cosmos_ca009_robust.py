import hashlib
import json
from dataclasses import dataclass


class IdentityError(Exception):
    pass


@dataclass(frozen=True)
class Node:
    name: str
    parents: tuple


class Cosmos:

    def __init__(self):
        self.nodes = {}

    def add(self, node):
        self.nodes[node.name] = node


    def identity(self, name, stack=None):

        if stack is None:
            stack = set()

        if name in stack:
            raise IdentityError(
                "Ciclo causal detectado"
            )

        stack.add(name)


        if name not in self.nodes:
            raise IdentityError(
                f"Ancestro inexistente: {name}"
            )


        node = self.nodes[name]


        parent_ids = tuple(
            self.identity(
                p,
                stack.copy()
            )
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



def compare(title, a, b):

    print("\n" + title)

    print("A:")
    print(a)

    print("B:")
    print(b)

    if a == b:
        print("🚨 COLISIÓN")
    else:
        print("✅ Identidades separadas")



print("""
=== CA-009 ROBUST TEMPORAL IDENTITY ATTACK ===
""")


# -------------------------
# HISTORIA ORIGINAL
# -------------------------

cosmos = Cosmos()


cosmos.add(Node("A", ()))
cosmos.add(Node("B", ("A",)))
cosmos.add(Node("C", ("B",)))


hash_C_original = cosmos.identity("C")


print("Historia original:")
print("C =", hash_C_original)



# -------------------------
# ATAQUE 1
# MISMO PADRE DIRECTO
# DISTINTO ABUELO
# -------------------------

fake = Cosmos()


fake.add(Node("A", ("X",)))
fake.add(Node("B", ("A",)))
fake.add(Node("C", ("B",)))


try:

    hash_C_fake = fake.identity("C")


    compare(
        "ATAQUE 1: abuelo fantasma",
        hash_C_original,
        hash_C_fake
    )


except IdentityError as e:

    print(
        "✅ Detectado:",
        e
    )



# -------------------------
# ATAQUE 2
# MUTACIÓN PROFUNDA
# -------------------------

mut = Cosmos()


mut.add(Node("A", ()))
mut.add(Node("B", ("A",)))
mut.add(Node("C", ("B",)))


before = mut.identity("C")


mut.nodes["A"] = Node(
    "A",
    ("MUTATED",)
)


try:

    after = mut.identity("C")

    compare(
        "ATAQUE 2: mutación de ancestro",
        before,
        after
    )


except IdentityError as e:

    print(
        "✅ Mutación detectada:",
        e
    )



# -------------------------
# ATAQUE 3
# CICLO TEMPORAL
# -------------------------

cycle = Cosmos()

cycle.add(Node("A", ("C",)))
cycle.add(Node("B", ("A",)))
cycle.add(Node("C", ("B",)))


try:

    cycle.identity("C")

    print(
        "🚨 FALLA: ciclo aceptado"
    )


except IdentityError as e:

    print(
        "\nATAQUE 3: ciclo"
    )

    print(
        "✅ Detenido:",
        e
    )



print("""
=== VEREDICTO CA-009 ===

La identidad debe conservar:

✓ nodo
✓ padres
✓ ancestros
✓ orden causal
✓ ausencia de ciclos

Si una modificación histórica cambia la identidad:
la procedencia está protegida.

""")

