#!/usr/bin/env python3

import hashlib
import json


class IdentityError(Exception):
    pass



class CosmosMerkle:

    def __init__(self):
        self.nodes = {}
        self.counter = 0


    def hash(self, payload):

        data=json.dumps(
            payload,
            sort_keys=True
        )

        return hashlib.sha256(
            data.encode()
        ).hexdigest()



    def add(self,state,parent=None):

        node={
            "id":self.counter,
            "state":state,
            "parent":parent
        }

        node_hash=self.hash(node)

        self.nodes[self.counter]={
            **node,
            "hash":node_hash
        }

        self.counter+=1

        return node["id"]



    def history_root(self,node_id,visited=None):

        if visited is None:
            visited=set()


        if node_id in visited:
            raise IdentityError(
                "Ciclo histórico detectado"
            )


        visited.add(node_id)


        if node_id not in self.nodes:
            raise IdentityError(
                f"Ancestro perdido: {node_id}"
            )


        node=self.nodes[node_id]


        if node["parent"] is None:

            return self.hash(
                {
                    "root":node["hash"]
                }
            )


        parent_root=self.history_root(
            node["parent"],
            visited
        )


        return self.hash(
            {
                "node":node["hash"],
                "parent_root":parent_root
            }
        )



def compare(label,a,b):

    print("\n"+label)

    print("A:")
    print(a)

    print("B:")
    print(b)


    if a==b:

        print("""
🚨 FALLA:
Dos genealogías distintas
comparten la misma raíz.
""")

    else:

        print("""
✅ Procedencia separada.
""")



print("""
=== CA-021 ORIGIN BRANCH FORGERY ATTACK ===
""")


cosmos=CosmosMerkle()


# -------------------------
# HISTORIA LEGÍTIMA
# -------------------------

root_A=cosmos.add(
    "GENESIS_A"
)


b=cosmos.add(
    "BUILD",
    root_A
)


c=cosmos.add(
    "COMPILE",
    b
)


final_A=cosmos.add(
    "FINAL",
    c
)



real_root=cosmos.history_root(
    final_A
)


print("Historia legítima:")
print(real_root)



# -------------------------
# ATAQUE
# -------------------------

print("""
=== ATAQUE:
Rama falsa con mismo destino
===
""")


fake_root=cosmos.add(
    "GENESIS_FAKE"
)


fake_b=cosmos.add(
    "BUILD",
    fake_root
)


fake_c=cosmos.add(
    "COMPILE",
    fake_b
)


fake_final=cosmos.add(
    "FINAL",
    fake_c
)



fake_history=cosmos.history_root(
    fake_final
)



compare(
    "Comparación de raíces Merkle",
    real_root,
    fake_history
)



print("""
=== ATAQUE 2:
Intento de reemplazar origen
===
""")


cosmos.nodes[root_A]["state"]="GENESIS_FAKE"



try:

    mutated=cosmos.history_root(
        final_A
    )


    compare(
        "Después de mutación profunda",
        real_root,
        mutated
    )


except IdentityError as e:

    print(
        "✅ Detectado:",
        e
    )



print("""
=== VEREDICTO CA-021 ===

La identidad completa requiere:

✓ Estado actual
✓ Padres válidos
✓ Raíz histórica
✓ Ausencia de ciclos
✓ Integridad de ancestros


Un atacante puede copiar el presente.

Pero no puede copiar
la trayectoria sin poseer
la historia completa.

===
""")


