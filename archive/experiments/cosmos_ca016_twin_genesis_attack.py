import hashlib
import json


class Node:

    def __init__(
        self,
        name,
        value,
        parents=()
    ):
        self.name=name
        self.value=value
        self.parents=tuple(parents)



class Cosmos:


    def __init__(self, universe):

        self.universe=universe
        self.nodes={}



    def add(self,node):

        self.nodes[node.name]=node



    def identity(self,name):

        node=self.nodes[name]


        parent_hashes=tuple(
            self.identity(p)
            for p in node.parents
        )


        payload=json.dumps(
            {
                "name":node.name,
                "value":node.value,
                "parents":parent_hashes
            },
            sort_keys=True
        )


        return hashlib.sha256(
            payload.encode()
        ).hexdigest()



    def universe_identity(self,name):

        node_hash=self.identity(name)

        payload=json.dumps(
            {
                "universe":self.universe,
                "root":node_hash
            },
            sort_keys=True
        )


        return hashlib.sha256(
            payload.encode()
        ).hexdigest()



print("""
=== CA-016 TWIN GENESIS ATTACK ===
""")


# Universo A

A=Cosmos("UNIVERSE_A")


A.add(
    Node(
        "ROOT",
        "genesis"
    )
)

A.add(
    Node(
        "DATA",
        "42",
        ("ROOT",)
    )
)



# Universo B

B=Cosmos("UNIVERSE_B")


B.add(
    Node(
        "ROOT",
        "genesis"
    )
)

B.add(
    Node(
        "DATA",
        "42",
        ("ROOT",)
    )
)



print("=== IDENTIDAD INTERNA ===")


ha=A.identity("DATA")
hb=B.identity("DATA")


print("A:")
print(ha)

print("\nB:")
print(hb)



if ha==hb:

    print("""
⚠️ Mismo estado interno.
""")

else:

    print("""
Estados diferentes.
""")


print("\n=== IDENTIDAD DE UNIVERSO ===")


ua=A.universe_identity("DATA")
ub=B.universe_identity("DATA")


print("Universo A:")
print(ua)

print("\nUniverso B:")
print(ub)



if ua==ub:

    print("""
🚨 FALLA:
Dos universos colapsaron.
""")

else:

    print("""
✅ Separación conservada.
Mismo estado ≠ mismo origen.
""")


print("""
=== VEREDICTO CA-016 ===

Una entidad puede tener
la misma estructura interna,

pero pertenecer a una historia
de nacimiento distinta.
""")

