import hashlib
import json


class NodeKey:

    def __init__(self, op, left, right):
        self.op=op
        self.left=left
        self.right=right


class Cosmos:

    def bad_hash(self,node):

        # ATAQUE:
        # normalización aplicada a todo

        values=sorted(
            [
                str(node.left),
                str(node.right)
            ]
        )

        payload=json.dumps(
            {
                "op":node.op,
                "args":values
            },
            sort_keys=True
        )

        return hashlib.sha256(
            payload.encode()
        ).hexdigest()



c=Cosmos()


A=NodeKey(
    "SUB",
    5,
    3
)


B=NodeKey(
    "SUB",
    3,
    5
)


ha=c.bad_hash(A)
hb=c.bad_hash(B)


print("=== CA-013b BAD CANONICALIZATION ===")

print("A:",ha)
print("B:",hb)


if ha==hb:
    print("""
🚨 FALLA:
La normalización destruyó
la dirección de la operación.
""")
else:
    print("""
✅ Orden preservado.
""")

