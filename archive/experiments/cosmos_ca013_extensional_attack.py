import hashlib
import json


class NodeKey:

    def __init__(self, op, parents=(), data=None):
        self.op = op
        self.parents = tuple(parents)
        self.data = data


class Cosmos:

    def __init__(self):
        self.nodes = {}
        self.table = {}

    def hash_id(self, node):

        payload = json.dumps(
            {
                "op": node.op,
                "parents": node.parents,
                "data": node.data
            },
            sort_keys=True
        )

        return hashlib.sha256(
            payload.encode()
        ).hexdigest()


    def add(self, node):

        h = self.hash_id(node)

        if h in self.table:
            print("♻️ Nodo reutilizado")
            return self.table[h]

        idx = len(self.nodes)

        self.nodes[idx] = node
        self.table[h] = idx

        print("✨ Nodo nuevo:", idx)

        return idx



print("=== CA-013 EXTENSIONAL VS INTENSIONAL ATTACK ===")


cosmos = Cosmos()


# Camino A
A = cosmos.add(
    NodeKey(
        "ADD",
        data="x+1"
    )
)


# Camino B
B = cosmos.add(
    NodeKey(
        "ADD",
        data="x+2-1"
    )
)


print()

print("Nodo A:", A)
print("Nodo B:", B)


if A == B:

    print("""
🚨 FALLA:
Dos operaciones distintas
colapsaron por resultado equivalente.
""")

else:

    print("""
✅ Identidad preservada:
misma salida no significa mismo proceso.
""")


print("\n=== PRUEBA DE SALIDA ===")

print("""
f(10)=11
g(10)=11

Pero:

f != g

La pregunta:
¿Cosmos protege el camino o solo el destino?
""")


print("\nNodos totales:")
print(len(cosmos.nodes))


for k,v in cosmos.nodes.items():
    print(k, v.op, v.data)

