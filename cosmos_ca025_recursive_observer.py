"""
===============================================================================
CA-025 RECURSIVE OBSERVER ATTACK

El demonio:
El verificador intenta validarse a sí mismo.

Objeto:
    X

Auditor:
    Ω(X)

Ataque:
    Ω(Ω)

Problema:
¿El juez pertenece al mismo dominio que juzga?
===============================================================================
"""

import hashlib


class CosmosRecursiveAudit:

    def __init__(self):
        self.nodes = {}
        self.counter = 0


    def hash(self, data):

        return hashlib.sha256(
            data.encode()
        ).hexdigest()


    def add(self, kind, value, parent=None):

        node = {
            "kind": kind,
            "value": value,
            "parent": parent
        }

        h = self.hash(str(node))

        self.nodes[self.counter] = {
            "data": node,
            "hash": h
        }

        self.counter += 1

        return self.counter - 1


    def omega(self, node_id):

        node = self.nodes[node_id]["data"]

        if node["kind"] == "AUDITOR":

            raise Exception(
"""
🚨 CA-025:
OBSERVADOR RECURSIVO DETECTADO.

El juez intenta convertirse
en su propio acusado.
"""
            )

        return True



cosmos = CosmosRecursiveAudit()


print("""
=== CA-025 RECURSIVE OBSERVER ATTACK ===
""")


# Objeto normal
entity = cosmos.add(
    "ENTITY",
    "STATE_A"
)


print("Entidad:")
print(entity)


print(
    "Ω(entidad)=",
    cosmos.omega(entity)
)


print("""
--- ATAQUE ---

El adversario inserta al propio auditor
como objeto dentro del universo.
""")


observer = cosmos.add(
    "AUDITOR",
    "OMEGA"
)


try:

    cosmos.omega(observer)


except Exception as e:

    print(e)



print("""
=== VEREDICTO CA-025 ===

Un sistema puede auditar objetos.

Pero necesita separar:

✓ Universo observado
✓ Operador observador
✓ Regla de validación


Si Ω está dentro de Ω:

la medición pierde referencia.

La herramienta se convierte
en parte del experimento.

===
""")

