from enum import Enum
from collections import deque

class Verdict(str, Enum):
    ACCEPT = "ACCEPT"
    REJECT = "REJECT"
    ESCALATE = "ESCALATE"

class Health(str, Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"

def propagate(nodes, dependencies):
    """
    Edges: dependency -> dependent.
    Verdict and operational health are independent.
    REJECT dominates ESCALATE, which dominates ACCEPT.
    """
    indegree = {node: 0 for node in nodes}
    children = {node: [] for node in nodes}

    for source, target in dependencies:
        if source not in nodes or target not in nodes:
            raise ValueError("Unknown node in dependency graph")

        children[source].append(target)
        indegree[target] += 1

    # Deterministic topological traversal.
    ready = deque(sorted(
        node for node in nodes if indegree[node] == 0
    ))

    results = {}

    while ready:
        node = ready.popleft()
        local = nodes[node]

        parent_results = [
            results[parent]
            for parent in sorted(
                source for source, target in dependencies
                if target == node
            )
        ]

        inherited = [r["verdict"] for r in parent_results]

        # Verdict propagation.
        if local["verdict"] == Verdict.REJECT:
            verdict = Verdict.REJECT
        elif Verdict.REJECT in inherited:
            verdict = Verdict.REJECT
        elif (
            local["verdict"] == Verdict.ESCALATE
            or Verdict.ESCALATE in inherited
        ):
            verdict = Verdict.ESCALATE
        else:
            verdict = Verdict.ACCEPT

        # Operational degradation is a separate dimension.
        degraded = (
            local["health"] == Health.DEGRADED
            or any(r["degraded"] for r in parent_results)
        )

        results[node] = {
            "verdict": verdict.value,
            "degraded": degraded
        }

        for child in sorted(children[node]):
            indegree[child] -= 1
            if indegree[child] == 0:
                ready.append(child)

    if len(results) != len(nodes):
        raise ValueError("CYCLE_DETECTED: dependency graph is not a DAG")

    return results

def enforce(results):
    decisions = {}
    for node, result in sorted(results.items()):
        verdict = result["verdict"]
        if verdict == Verdict.ACCEPT.value:
            decision = "ACCEPT"
        elif verdict == Verdict.REJECT.value:
            decision = "REJECT"
        else:
            decision = "ESCALATE"

        decisions[node] = {
            "decision": decision,
            "operational_warning": result["degraded"]
        }
    return decisions

if __name__ == "__main__":
    nodes = {
        "crypto-lib": {
            "verdict": Verdict.REJECT,
            "health": Health.HEALTHY
        },
        "service-api": {
            "verdict": Verdict.ACCEPT,
            "health": Health.DEGRADED
        },
        "application": {
            "verdict": Verdict.ACCEPT,
            "health": Health.HEALTHY
        },
        "reporting": {
            "verdict": Verdict.ACCEPT,
            "health": Health.HEALTHY
        }
    }

    dependencies = [
        ("crypto-lib", "service-api"),
        ("service-api", "application"),
        ("application", "reporting")
    ]

    results = propagate(nodes, dependencies)
    decisions = enforce(results)

    print("STARKCORE GIE-001")
    print("=================")
    for node, result in decisions.items():
        print(
            f"{node:15} "
            f"{result['decision']:8} "
            f"DEGRADED={result['operational_warning']}"
        )
