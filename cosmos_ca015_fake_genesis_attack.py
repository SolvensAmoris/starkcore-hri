import hashlib
import json


class GenesisError(Exception):
    pass



class Node:

    def __init__(
        self,
        name,
        value,
        parents=(),
        genesis=False
    ):
        self.name=name
        self.value=value
        self.parents=tuple(parents)
        self.genesis=genesis



class Cosmos:


    def __init__(self):

        self.nodes={}



    def add(self,node):

        self.nodes[node.name]=node



    def hash_node(self,name,visited=None):

        if visited is None:
            visited=set()


        if name in visited:
            raise GenesisError(
                "Ciclo en historia"
            )


        visited.add(name)


        node=self.nodes.get(name)


        if node is None:
            raise GenesisError(
                f"Nodo inexistente: {name}"
            )


        parent_hashes=tuple(
            self.hash_node(
                p,
                visited.copy()
            )
            for p in node.parents
        )


        payload=json.dumps(
            {
                "name":node.name,
                "value":node.value,
                "parents":parent_hashes,
                "genesis":node.genesis
            },
            sort_keys=True
        )


        return hashlib.sha256(
            payload.encode()
        ).hexdigest()



print("""
=== CA-015 FAKE GENESIS ATTACK ===
""")



# Historia legítima

real=Cosmos()


real.add(
    Node(
        "ROOT",
        "inicio",
        (),
        True
    )
)


real.add(
    Node(
        "A",
        "dato",
        ("ROOT",)
    )
)


real.add(
    Node(
        "B",
        "resultado",
        ("A",)
    )
)



real_hash=real.hash_node("B")


print("Historia real:")
print(real_hash)



print("\n=== ATAQUE ===")



fake=Cosmos()


fake.add(
    Node(
        "ROOT",
        "inicio",
        (),
        False
    )
)


fake.add(
    Node(
        "A",
        "dato",
        ("ROOT",)
    )
)


fake.add(
    Node(
        "B",
        "resultado",
        ("A",)
    )
)



fake_hash=fake.hash_node("B")


print("Historia falsa:")
print(fake_hash)



if real_hash==fake_hash:

    print("""
🚨 FALLA:
Un génesis falso creó
la misma identidad.
""")

else:

    print("""
✅ Génesis protegido:
la raíz también pertenece
a la identidad.
""")


print("""
=== VEREDICTO CA-015 ===

Una cadena no solo necesita enlaces.

Necesita un origen verificable.
""")

