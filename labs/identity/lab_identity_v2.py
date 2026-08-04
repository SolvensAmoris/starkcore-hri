# lab_identity_v2.py - COSMOS IDENTITY STRESS TEST v0.2
import hashlib, time, random, asyncio
from dataclasses import dataclass
from typing import List

@dataclass
class Node:
    id: int
    seed_decl: str
    parent_hash: str
    identity_hash: str
    mutated: bool = False

def compute_identity(seed: str, parent: str, nid: int) -> str:
    return hashlib.sha256(f"{seed}|{parent}|{nid}".encode()).hexdigest()[:12]

def gen_seed():
    verbs = ["SUN","MOON","STAR"]
    nouns = ["NODE","FLOW","ROOT","LEAF"]
    return f"{random.choice(verbs)},{random.choice(nouns)},ROOT,FLOW"

def test_collisions(n=20000):
    seen = {}
    collisions = 0
    for i in range(n):
        seed = gen_seed()
        seed_canonical = ",".join([s.strip().upper() for s in seed.split(",")])
        h = compute_identity(seed_canonical, "00000", i)
        if h in seen and seen[h]!= seed_canonical:
            collisions += 1
        seen[h] = seed_canonical
    print(f"[1] Colisiones de identidad: {collisions}/{n} -> {'FAIL' if collisions else 'OK'}")

def gen_chain(n):
    prev="00000"
    chain=[]
    for i in range(n):
        h=compute_identity("SUN,NODE,ROOT,FLOW", prev, i)
        chain.append(Node(i, "SUN,NODE,ROOT,FLOW", prev, h))
        prev=h
    return chain

def gen_star(n):
    center_h = compute_identity("SUN,NODE,ROOT,FLOW", "00000", 0)
    nodes=[Node(0,"SUN,NODE,ROOT,FLOW","00000",center_h)]
    for i in range(1,n):
        h=compute_identity("SUN,NODE,ROOT,FLOW", center_h, i)
        nodes.append(Node(i,"SUN,NODE,ROOT,FLOW",center_h,h))
    return nodes

def gen_deep_tree(n):
    nodes=[]
    for i in range(n):
        parent = nodes[random.randint(max(0,i-10), i-1)].identity_hash if i>0 and nodes else "00000"
        h=compute_identity("SUN,NODE,ROOT,FLOW", parent, i)
        nodes.append(Node(i,"SUN,NODE,ROOT,FLOW",parent,h))
    return nodes

def test_topologies():
    for name, gen in [("Cadena", gen_chain), ("Estrella", gen_star), ("Arbol Profundo", gen_deep_tree)]:
        dag = gen(5000)
        uniq = len(set(n.identity_hash for n in dag))
        print(f"[2] Topologia {name}: {len(dag)} nodos, unicos {uniq} -> {'OK' if uniq==len(dag) else 'FAIL'}")

async def fake_evidence_write(store: dict, node: Node, lock: asyncio.Lock):
    async with lock:
        if node.identity_hash in store:
            return False
        store[node.identity_hash] = node.seed_decl
        await asyncio.sleep(0)
        return True

async def test_concurrency(n=5000):
    dag = gen_chain(n)
    store = {}
    lock = asyncio.Lock()
    results = await asyncio.gather(*[fake_evidence_write(store, node, lock) for node in dag])

    store_nolock = {}
    async def write_nolock(s, node):
        if node.identity_hash in s: return False
        s[node.identity_hash] = node.seed_decl
        await asyncio.sleep(0)
        return True
    results_nolock = await asyncio.gather(*[write_nolock(store_nolock, node) for node in dag])

    print(f"[3] Concurrencia con lock: {sum(results)}/{n} OK")
    print(f"[3] Concurrencia sin lock: {sum(results_nolock)}/{n} -> {'RACE CONDITION DETECTADA' if sum(results_nolock)!=n else 'OK'}")

def test_corruption():
    cases = [None, "", " ", "SUN,NODE,ROOT,FLOW\n", b"SUN,NODE", 12345]
    blocked = 0
    for seed in cases:
        try:
            if not isinstance(seed, str) or not seed.strip():
                blocked += 1
                continue
            canonical = ",".join([s.strip().upper() for s in seed.split(",")])
            if len(canonical.split(","))!= 4:
                blocked += 1
                continue
            compute_identity(canonical, "00000", 0)
        except:
            blocked += 1
    print(f"[4] Corrupcion deliberada: {blocked}/{len(cases)} bloqueadas -> {'OK' if blocked==len(cases) else 'GRIETA'}")

async def main():
    print("COSMOS IDENTITY STRESS TEST v0.2 - MODO ROMPER\n")
    t0=time.time()
    test_collisions()
    test_topologies()
    await test_concurrency()
    test_corruption()
    print(f"\nTiempo total: {time.time()-t0:.3f}s")

if __name__ == "__main__":
    asyncio.run(main())
