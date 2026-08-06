namespace StarkCore

structure CoreState where
  identity : Nat
  mutable_value : Nat
  evidence_root : Nat


def IdentityInvariant (s : CoreState) : Prop :=
  s.identity = s.identity


def MirrorPreservesCore
  (before after : CoreState) : Prop :=
  before.identity = after.identity ∧
  before.evidence_root = after.evidence_root


theorem StarkCore_kernel_invariant
  (before after : CoreState)
  (h : MirrorPreservesCore before after) :
  before.identity = after.identity ∧
  before.evidence_root = after.evidence_root := by
  exact h


theorem CA002_MirrorGate_composition
  (before after : CoreState)
  (h : MirrorPreservesCore before after) :
  before.identity = after.identity := by
  exact h.1


end StarkCore
