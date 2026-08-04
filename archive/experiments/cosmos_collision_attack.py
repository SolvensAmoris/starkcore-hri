#!/usr/bin/env python3

import hashlib
from dataclasses import dataclass


@dataclass(frozen=True)
class NodeKey:

    op: str
    left: int | None
    right: int | None
    shape: str = "scalar"


    def vulnerable_hash(self):

        # misma lógica original
        data = (
            self.op +
            str(self.left) +
            str(self.right) +
            self.shape
        )

        return hashlib.sha256(
            data.encode()
        ).hexdigest()



    def hardened_hash(self):

        # versión blindada
        data = repr(
            (
                self.op,
                self.left,
                self.right,
                self.shape
            )
        )

        return hashlib.sha256(
            data.encode()
        ).hexdigest()



attack_a = NodeKey(
    "ADD",
    1,
    23
)

attack_b = NodeKey(
    "ADD",
    12,
    3
)


print("=== CAOSMOS ADVERSARIAL TEST ===")

print()

print("Nodo A:")
print(attack_a)

print()

print("Nodo B:")
print(attack_b)


print("\nHASH VULNERABLE")

ha = attack_a.vulnerable_hash()
hb = attack_b.vulnerable_hash()

print("A:", ha)
print("B:", hb)

if ha == hb:
    print("🚨 COLISIÓN ENCONTRADA")
else:
    print("✅ No colisionó")


print("\nHASH HARDENED")

ha = attack_a.hardened_hash()
hb = attack_b.hardened_hash()

print("A:", ha)
print("B:", hb)

if ha == hb:
    print("🚨 FALLA")
else:
    print("✅ Defensa correcta")


print("\nVEREDICTO")

print("""
Si vulnerable falla:
La identidad dependía de una representación ambigua.

Si hardened pasa:
La identidad depende de estructura real.
""")

