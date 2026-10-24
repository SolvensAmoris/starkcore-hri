# CORE MANIFEST v1.1 - Inmutable

Hash axioms: 6b018058049567fff174474da3dc4683bdb00f49efa252740babb8309674c381
Commit: b89ba7c
Jobs: 11
Axioms: 0 + propext

## NÚCLEO DURO (7 módulos - Compilan)
1. StarkCore/Kernel/Core.lean [ROOT]
2. StarkCore/Kernel/StarkCoreCore.lean [ROOT]
3. StarkCore/Kernel/Consistency.lean -> Core
4. StarkCore/Logic/NoContradiction.lean -> Core
5. StarkCore/Invariants/Conservation.lean -> Core
6. StarkCore/Kernel/CA002.lean -> Core + StarkCoreCore
7. StarkCore/Evidence/MirrorGate.lean -> StarkCoreCore

## EXTENSIONES FUTURAS (18 módulos - No compilan, fuera del núcleo)
- StarkCore/Evidence/Chain, Integrity, Verification
- StarkCore/Evolution/*
- StarkCore/Identity/*
- StarkCore/Memory/*
- StarkCore/Invariants/FixedPoints
- StarkCore/Logic/Composition
- StarkCore/Kernel/Axioms

Grafo: Core + StarkCoreCore son raíces. CA002 y MirrorGate son las dos invariantes críticas.
