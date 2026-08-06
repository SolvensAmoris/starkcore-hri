structure Hypothesis where
  L_old : Nat
  L_new : Nat
  F_old : Nat
  F_new : Nat
  chain_nonempty : Bool
  no_hidden : Bool


def C1 (h : Hypothesis) : Prop :=
  h.L_new < h.L_old ∧
  h.F_old < h.F_new


def C2 (h : Hypothesis) : Prop :=
  True


def C3 (h : Hypothesis) : Prop :=
  h.chain_nonempty = true ∧
  h.no_hidden = true


def BorromeoTight (h : Hypothesis) : Prop :=
  C1 h ∧ C2 h ∧ C3 h


theorem borromeo_sound
  (h : Hypothesis)
  (proof : BorromeoTight h) :
  h.L_new < h.L_old :=
by
  exact proof.1.1
