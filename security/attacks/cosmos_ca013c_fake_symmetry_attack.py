import hashlib
import json


class Operator:

    def __init__(self,name,commutative):
        self.name=name
        self.commutative=commutative



class NodeKey:

    def __init__(self,op,left,right):
        self.op=op
        self.left=left
        self.right=right



class Cosmos:


    def hash_id(self,node,operator):

        args=[
            node.left,
            node.right
        ]

        if operator.commutative:
            args=sorted(args)


        payload=json.dumps(
            {
                "op":operator.name,
                "args":args
            },
            sort_keys=True
        )


        return hashlib.sha256(
            payload.encode()
        ).hexdigest()



print("=== CA-013c FAKE SYMMETRY ATTACK ===")


cosmos=Cosmos()


# Operador realmente NO conmutativo

sub=Operator(
    "SUB",
    True   # atacante falsifica
)


A=NodeKey(
    "SUB",
    10,
    3
)


B=NodeKey(
    "SUB",
    3,
    10
)



ha=cosmos.hash_id(A,sub)
hb=cosmos.hash_id(B,sub)


print("A:",ha)
print("B:",hb)


if ha==hb:

    print("""
🚨 FALLA:
Una propiedad matemática falsa
alteró la identidad.
""")

else:

    print("""
✅ Propiedad rechazada.
""")

