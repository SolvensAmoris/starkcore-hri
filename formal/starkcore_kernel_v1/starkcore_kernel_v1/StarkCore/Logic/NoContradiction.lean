import StarkCore.Kernel.Core
namespace StarkCore

theorem no_false_identity (s : State) : ¬(s.identity ≠ s.identity) := by
  simp

end StarkCore
