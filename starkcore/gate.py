from.evidence import EvidenceStore
class Gate:
    def check(self, task: str):
        store = EvidenceStore()
        if "fail" in task:
            store.add("GATE_DENIED", {"task": task})
            return "DENIED"
        store.add("GATE_ALLOWED", {"task": task})
        return "ALLOWED"

# --- integración oráculo ---
from starkcore.oracle.btc_burn_verifier import verify as verify_burn
def is_external_anchored(evidence, gate_rules, did):
    ok, msg = verify_burn(evidence, gate_rules, did)
    return ok
