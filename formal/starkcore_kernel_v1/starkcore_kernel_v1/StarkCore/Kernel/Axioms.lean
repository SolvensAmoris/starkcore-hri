namespace StarkCore

axiom identity_persistence :
  ∀ s : State, s.identity = s.identity


axiom evidence_monotonic :
  ∀ t : Transition,
  validTransition t

end StarkCore
