from.evidence import EvidenceStore
class Executor:
    def execute(self, task: str):
        store = EvidenceStore()
        if "fail_api" in task:
            store.add("EXEC_FAILED", {"task": task, "err": "task fail_api failed"})
            return False
        store.add("EXECUTED", {"task": task})
        return True
