# lab_identity.py - COSMOS IDENTITY STRESS TEST v0.1
import hashlib, json, time, random
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Node:
    id: int
    seed_decl: str
    parent: int = None
    identity_hash: str = ""
    mutated: bool = False

def compute_identity(seed_decl: str, parent_hash: str = "00000", node_id: int = 0) -> str:
    raw = f"{seed_decl}|{parent_hash}|{node_id}".encode()
    return hashlib.sha256(raw).hexdigest()[:12]

def generate_dag(n: int, seed="SUN,NODE,ROOT,FLOW") -> List[Node]:
    nodes = []
    for i in range(n):
        parent = random.choice(nodes).identity_hash if nodes else "00000"
        h = compute_identity(seed, parent, i)
        nodes.append(Node(id=i, seed_decl=seed, identity_hash=h))
    return nodes

def mutate_node(node: Node, mutation="SUN,NODE,ROOT,FLOW_MUTATED") -> Node:
    node.seed_decl = mutation
    node.mutated = True
    return node

def test_gate(node: Node) -> str:
    if node.mutated:
        return "DENIED_CA002"
    return "ALLOWED"

def test_evidence_integrity(nodes: List[Node]) -> bool:
    seen = set()
    for n in nodes:
        if n.identity_hash in seen:
            return False
        seen.add(n.identity_hash)
    return True

def run_scale_test(n_nodes: int, mutation_rate: float) -> Dict:
    start = time.time()
    dag = generate_dag(n_nodes)
    k = int(n_nodes * mutation_rate)
    mutated_ids = random.sample(range(n_nodes), k) if k>0 else []
    for i in mutated_ids:
        mutate_node(dag[i])
    preserved = 0
    detected = 0
    for n in dag:
        decision = test_gate(n)
        if not n.mutated:
            preserved += 1
        if n.mutated and decision == "DENIED_CA002":
            detected += 1
    elapsed = time.time() - start
    return {
        "nodes": n_nodes,
        "mut_rate": mutation_rate,
        "identity_preserved": preserved / (n_nodes - k) if n_nodes-k else 1,
        "mutations_introduced": k,
        "mutations_detected": detected,
        "detection_rate": detected / k if k else 1,
        "evidence_consistency": test_evidence_integrity(dag),
        "time_s": round(elapsed, 3),
        "first_failure": None if detected==k else f"Node {mutated_ids[0] if mutated_ids else 0}"
    }

def generate_report():
    configs = [(100, 0.01), (1000, 0.05), (10000, 0.05), (50000, 0.10)]
    print("COSMOS IDENTITY STRESS TEST v0.1\n")
    for nodes, rate in configs:
        r = run_scale_test(nodes, rate)
        print(f"--- {nodes} nodos | mut {rate*100}% ---")
        print(f" identity_preserved: {r['identity_preserved']*100:.1f}%")
        print(f" mutations: {r['mutations_detected']}/{r['mutations_introduced']} -> {r['detection_rate']*100:.1f}%")
        print(f" evidence_consistency: {'OK' if r['evidence_consistency'] else 'FAIL'}")
        print(f" time: {r['time_s']}s")
        if r['first_failure']:
            print(f" FIRST FAILURE: {r['first_failure']}")
        print()

if __name__ == "__main__":
    generate_report()
