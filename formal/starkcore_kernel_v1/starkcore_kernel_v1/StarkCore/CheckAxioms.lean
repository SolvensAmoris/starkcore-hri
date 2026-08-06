import StarkCore.Kernel.Consistency
import StarkCore.Kernel.CA002
import StarkCore.Kernel.StarkCoreCore
import StarkCore.Evidence.MirrorGate
import StarkCore.Logic.NoContradiction
import StarkCore.Invariants.Conservation

open StarkCore

#print axioms identity_consistent
#print axioms CA002_rejects_mutable_identity
#print axioms CA002_identity_survives
#print axioms StarkCore_kernel_invariant
#print axioms CA002_MirrorGate_composition
#print axioms mirror_gate_preserves_identity
#print axioms no_false_identity
#print axioms identity_conserved
