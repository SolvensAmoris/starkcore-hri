import hashlib
import json


class CompilerError(Exception):
    pass



class Artifact:

    def __init__(
        self,
        source,
        transforms,
        binary
    ):

        self.source = source
        self.transforms = tuple(transforms)
        self.binary = binary



class CosmosCompiler:


    def hash(self,obj):

        payload=json.dumps(
            obj,
            sort_keys=True
        )

        return hashlib.sha256(
            payload.encode()
        ).hexdigest()



    def source_hash(self,a):

        return self.hash({
            "source":a.source
        })



    def artifact_hash(self,a):

        return self.hash({
            "binary":a.binary
        })



    def provenance_hash(self,a):

        return self.hash({
            "source":self.source_hash(a),
            "transforms":a.transforms,
            "binary":self.artifact_hash(a)
        })



print("""
=== CA-014b COMPILER DEMON:
FALSE PROVENANCE ATTACK
===
""")


cosmos=CosmosCompiler()



# Historia legítima

good=Artifact(
    source="program_v1",
    transforms=[
        "parse",
        "optimize",
        "compile"
    ],
    binary="101010"
)



# Historia atacante:
# mismo binario final,
# intenta cambiar el camino

evil=Artifact(
    source="program_v1",
    transforms=[
        "parse",
        "inject",
        "compile"
    ],
    binary="101010"
)



print("=== BINARIO ===")

hg=cosmos.artifact_hash(good)
he=cosmos.artifact_hash(evil)


print("GOOD:",hg)
print("EVIL:",he)



if hg==he:
    print("""
⚠️ Correcto:
el binario no revela la historia.
""")



print("\n=== PROCEDENCIA ===")


pg=cosmos.provenance_hash(good)
pe=cosmos.provenance_hash(evil)


print("GOOD:")
print(pg)

print("\nEVIL:")
print(pe)



if pg==pe:

    print("""
🚨 FALLA:
El compilador borró la trayectoria.
""")

else:

    print("""
✅ Defensa correcta:
mismo resultado,
distinta geodésica.
""")


print("""
=== VEREDICTO CA-014b ===

El destino puede coincidir.

La trayectoria no.

Cosmos no protege solamente
lo que existe.

Protege cómo llegó a existir.
""")

