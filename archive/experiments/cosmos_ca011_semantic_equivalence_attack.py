import hashlib
import json


class NodeKey:

    def __init__(self, op, parents=(), data=None):
        self.op = op
        self.parents = tuple(parents)
        self.data = data


class Cosmos:

    def __init__(self):
        self.nodes={}
        self.table={}

    def hash_node(self,node):

        parent_hashes=[
            self.hash_node(self.nodes[p])
            for p in node.parents
        ]

        payload=json.dumps(
            {
                "op":node.op,
                "parents":parent_hashes,
                "data":node.data
            },
            sort_keys=True
        )

        return hashlib.sha256(
            payload.encode()
        ).hexdigest()


    def add(self,node):

        h=self.hash_node(node)

        if h in self.table:
            return self.table[h]

        idx=len(self.nodes)

        self.nodes[idx]=node
        self.table[h]=idx

        return idx



print("=== CA-011 SEMANTIC EQUIVALENCE ATTACK ===")


cosmos=Cosmos()


# Camino A
a0=cosmos.add(
    NodeKey(
        "INPUT",
        data="25_C"
    )
)

a1=cosmos.add(
    NodeKey(
        "CELSIUS_TO_KELVIN",
        (a0,)
    )
)

out_A=cosmos.add(
    NodeKey(
        "OUTPUT",
        (a1,),
        "298.15"
    )
)



# Camino B

b0=cosmos.add(
    NodeKey(
        "INPUT",
        data="298.15_K"
    )
)


b1=cosmos.add(
    NodeKey(
        "NORMALIZE",
        (b0,)
    )
)


out_B=cosmos.add(
    NodeKey(
        "OUTPUT",
        (b1,),
        "298.15"
    )
)



print("out_A:",out_A)
print("out_B:",out_B)


if out_A==out_B:

    print("""
🚨 FALLA:
Dos operaciones distintas
colapsaron en una identidad.
""")

else:

    print("""
✅ Procedencia conservada.
Mismo resultado no implica mismo origen.
""")


print("\nNodos:")
for k,v in cosmos.nodes.items():
    print(k,v.op,v.parents,v.data)

