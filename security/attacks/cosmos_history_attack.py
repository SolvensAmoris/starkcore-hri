#!/usr/bin/env python3

import hashlib
import json
from dataclasses import dataclass


@dataclass(frozen=True)
class Node:

    name: str
    parents: tuple


    def identity(self):

        payload = json.dumps(
            {
                "name": self.name,
                "parents": self.parents
            },
            sort_keys=True
        )

        return hashlib.sha256(
            payload.encode()
        ).hexdigest()



def show(label,node):

    print(label)
    print(node)
    print(node.identity())
    print()



print("=== CA-009 TEMPORAL ORDER ATTACK ===")


# Historia normal

A = Node(
    "A",
    ()
)

B = Node(
    "B",
    ("A",)
)

C = Node(
    "C",
    ("B",)
)


show(
    "Historia correcta C:",
    C
)



# Ataque:
# mismo nombre final,
# distinto origen

fake_A = Node(
    "A",
    ("C",)
)


fake_B = Node(
    "B",
    ("A",)
)


fake_C = Node(
    "C",
    ("B",)
)


show(
    "Historia atacante C:",
    fake_C
)



if C.identity() == fake_C.identity():

    print(
        "🚨 FALLA: dos historias parecen una"
    )

else:

    print(
        "✅ Procedencia conservada"
    )

