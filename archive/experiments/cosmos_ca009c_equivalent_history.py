import hashlib
import json
from dataclasses import dataclass


@dataclass(frozen=True)
class Node:
    name: str
    value: str
    parents: tuple


class Cosmos:

    def __init__(self):
        self.nodes={}


    def add(self,node):
        self.nodes[node.name]=node


    def identity(self,name):

        node=self.nodes[name]

        parents=tuple(
            self.identity(p)
            for p in node.parents
        )

        payload=json.dumps(
            {
                "name":node.name,
                "value":node.value,
                "parents":parents
            },
            sort_keys=True
        )

        return hashlib.sha256(
            payload.encode()
        ).hexdigest()



print("=== CA-009c EQUIVALENT HISTORY ATTACK ===")


a=Cosmos()

a.add(Node("A1","10",()))
a.add(Node("B1","20",("A1",)))
a.add(Node("RESULT","30",("B1",)))


b=Cosmos()

b.add(Node("A2","10",()))
b.add(Node("B2","20",("A2",)))
b.add(Node("RESULT","30",("B2",)))


ha=a.identity("RESULT")
hb=b.identity("RESULT")


print("Historia A:")
print(ha)

print("\nHistoria B:")
print(hb)


if ha==hb:
    print("\n🚨 FALLA: dos procedencias colapsaron")
else:
    print("\n✅ Procedencias separadas")

