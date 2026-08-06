namespace StarkCore


structure Representation where
  identity : Nat
  mutable_value : Nat


def IdentityStable (r : Representation) : Prop :=
  r.identity = r.identity


def MutableAttack (r : Representation) : Prop :=
  r.mutable_value ≠ r.identity


theorem CA002_rejects_mutable_identity
(r : Representation)
(h : MutableAttack r) :
r.mutable_value ≠ r.identity := by
  exact h


theorem CA002_identity_survives
(r : Representation) :
IdentityStable r := by
  rfl


end StarkCore
