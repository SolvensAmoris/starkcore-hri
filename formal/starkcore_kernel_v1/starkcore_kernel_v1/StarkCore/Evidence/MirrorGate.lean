namespace StarkCore

structure Evidence where
  root : Nat
  hash : Nat


structure MirrorProof where
  before : Evidence
  after : Evidence
  preserved : before.root = after.root


def MirrorValid (p : MirrorProof) : Prop :=
  p.before.root = p.after.root


theorem mirror_gate_preserves_identity
(p : MirrorProof)
(h : MirrorValid p) :
p.before.root = p.after.root := by
  exact h


end StarkCore
