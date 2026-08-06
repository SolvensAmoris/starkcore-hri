namespace StarkCore

theorem identity_consistent
  (α : Type)
  [HasIdentity α]
  (x : α) :
  HasIdentity.identity x = x :=
by
  exact HasIdentity.identity_preserves x


end StarkCore
