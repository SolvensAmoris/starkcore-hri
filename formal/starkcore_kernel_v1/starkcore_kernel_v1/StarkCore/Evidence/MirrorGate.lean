import StarkCore.Kernel.StarkCoreCore
namespace StarkCore

theorem mirror_gate_preserves_identity (before after : CoreState) (h : MirrorPreservesCore before after) : before.identity = after.identity := by
  exact h.1

end StarkCore
