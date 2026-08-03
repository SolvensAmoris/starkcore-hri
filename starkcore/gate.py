from.evidence import EvidenceStore
class Gate:
    def check(self, task: str):
        store = EvidenceStore()
        if "fail" in task:
            store.add("GATE_DENIED", {"task": task})
            return "DENIED"
        store.add("GATE_ALLOWED", {"task": task})
        return "ALLOWED"
