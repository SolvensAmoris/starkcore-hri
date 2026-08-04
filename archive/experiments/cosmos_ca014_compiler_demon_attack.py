import hashlib
import json


class Artifact:

    def __init__(self, source, compiler, binary):
        self.source = source
        self.compiler = compiler
        self.binary = binary



class Cosmos:


    def artifact_hash(self, artifact):

        payload = json.dumps(
            {
                "source": artifact.source,
                "compiler": artifact.compiler,
                "binary": artifact.binary
            },
            sort_keys=True
        )

        return hashlib.sha256(
            payload.encode()
        ).hexdigest()



    def binary_only_hash(self, artifact):

        # versión vulnerable:
        # solo mira el resultado final

        return hashlib.sha256(
            artifact.binary.encode()
        ).hexdigest()



print("=== CA-014 COMPILER DEMON ATTACK ===")


cosmos = Cosmos()



# Historia A

A = Artifact(
    source="return a+b;",
    compiler="gcc-1",
    binary="0101010101"
)



# Historia B

B = Artifact(
    source="return b+a;",
    compiler="gcc-2",
    binary="0101010101"
)



print("\n=== HASH DEL BINARIO ===")


ha = cosmos.binary_only_hash(A)
hb = cosmos.binary_only_hash(B)


print("A:",ha)
print("B:",hb)


if ha == hb:

    print("""
🚨 ATAQUE:
Dos historias distintas
parecen la misma entidad.
""")

else:

    print("""
✅ Separadas.
""")



print("\n=== HASH DE PROCEDENCIA ===")


ha = cosmos.artifact_hash(A)
hb = cosmos.artifact_hash(B)


print("A:",ha)
print("B:",hb)


if ha == hb:

    print("""
🚨 FALLA:
La procedencia colapsó.
""")

else:

    print("""
✅ Historia conservada.
Mismo binario ≠ mismo origen.
""")


