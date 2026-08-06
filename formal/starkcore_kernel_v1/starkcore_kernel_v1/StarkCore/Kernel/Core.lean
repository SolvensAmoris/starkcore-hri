namespace StarkCore

structure State where
  identity : Nat
  memory : Nat
  evidence : Nat


structure Transition where
  before : State
  after : State


def validTransition (t : Transition) : Prop :=
  t.after.evidence >= t.before.evidence

end StarkCore
