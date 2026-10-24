# StarkCore Kernel v1.1 - Dependency Graph

Commit: b89ba7c12cc406673aa01daab3020b5a2262a1f1 - v1.1: 11 jobs zero-axiom - CA002+MirrorGate verified - propext only
Axioms hash: 6b018058049567fff174474da3dc4683bdb00f49efa252740babb8309674c381

## Módulos físicos
- StarkCore/CheckAxioms.lean
- StarkCore/Evidence.lean
- StarkCore/Evidence/Chain.lean
- StarkCore/Evidence/Integrity.lean
- StarkCore/Evidence/MirrorGate.lean
- StarkCore/Evidence/Verification.lean
- StarkCore/Evolution.lean
- StarkCore/Evolution/Causality.lean
- StarkCore/Evolution/Invariant.lean
- StarkCore/Evolution/Transition.lean
- StarkCore/Identity.lean
- StarkCore/Identity/Canonical.lean
- StarkCore/Identity/Identity.lean
- StarkCore/Identity/Observer.lean
- StarkCore/Invariants/Conservation.lean
- StarkCore/Invariants/FixedPoints.lean
- StarkCore/Kernel.lean
- StarkCore/Kernel/Axioms.lean
- StarkCore/Kernel/CA002.lean
- StarkCore/Kernel/Consistency.lean
- StarkCore/Kernel/Core.lean
- StarkCore/Kernel/StarkCoreCore.lean
- StarkCore/Logic/Composition.lean
- StarkCore/Logic/NoContradiction.lean
- StarkCore/Memory.lean
- StarkCore/Memory/History.lean
- StarkCore/Memory/Persistence.lean

## Imports por módulo

### StarkCore/CheckAxioms.lean
 - import StarkCore.Kernel.Consistency
 - import StarkCore.Kernel.CA002
 - import StarkCore.Kernel.StarkCoreCore
 - import StarkCore.Evidence.MirrorGate
 - import StarkCore.Logic.NoContradiction
 - import StarkCore.Invariants.Conservation

### StarkCore/Evidence.lean

### StarkCore/Evidence/Chain.lean

### StarkCore/Evidence/Integrity.lean

### StarkCore/Evidence/MirrorGate.lean
 - import StarkCore.Kernel.StarkCoreCore

### StarkCore/Evidence/Verification.lean

### StarkCore/Evolution.lean

### StarkCore/Evolution/Causality.lean

### StarkCore/Evolution/Invariant.lean

### StarkCore/Evolution/Transition.lean

### StarkCore/Identity.lean

### StarkCore/Identity/Canonical.lean

### StarkCore/Identity/Identity.lean

### StarkCore/Identity/Observer.lean

### StarkCore/Invariants/Conservation.lean
 - import StarkCore.Kernel.Core

### StarkCore/Invariants/FixedPoints.lean

### StarkCore/Kernel.lean
 - import StarkCore.Kernel.Core
 - import StarkCore.Kernel.Axioms
 - import StarkCore.Kernel.Consistency
 - import StarkCore.Kernel.CA002
 - import StarkCore.Kernel.StarkCoreCore

### StarkCore/Kernel/Axioms.lean

### StarkCore/Kernel/CA002.lean
 - import StarkCore.Kernel.Core
 - import StarkCore.Kernel.StarkCoreCore

### StarkCore/Kernel/Consistency.lean
 - import StarkCore.Kernel.Core

### StarkCore/Kernel/Core.lean

### StarkCore/Kernel/StarkCoreCore.lean

### StarkCore/Logic/Composition.lean

### StarkCore/Logic/NoContradiction.lean
 - import StarkCore.Kernel.Core

### StarkCore/Memory.lean

### StarkCore/Memory/History.lean

### StarkCore/Memory/Persistence.lean

## .olean generados (11 jobs)
- .lake/build/lib/lean/StarkCore/Evidence/MirrorGate.olean
- .lake/build/lib/lean/StarkCore/Invariants/Conservation.olean
- .lake/build/lib/lean/StarkCore/Kernel/CA002.olean
- .lake/build/lib/lean/StarkCore/Kernel/Consistency.olean
- .lake/build/lib/lean/StarkCore/Kernel/Core.olean
- .lake/build/lib/lean/StarkCore/Kernel/StarkCoreCore.olean
- .lake/build/lib/lean/StarkCore/Logic/NoContradiction.olean
