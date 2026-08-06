import StarkCore.Kernel.Core
import StarkCore.Kernel.StarkCoreCore
namespace StarkCore

theorem CA002_rejects_mutable_identity (before after : CoreState) (h : before.identity ≠ after.identity) : ¬ MirrorPreservesCore before after := by
  intro hm
  exact h hm.1

theorem CA002_identity_survives (before after : CoreState) (h : MirrorPreservesCore before after) : before.identity = after.identity := by
  exact h.1

end StarkCore
