import hashlib, time, random, asyncio
from dataclasses import dataclass

@dataclass
class Node:
    id: int
    seed_decl: str
    parent_hash: str
    identity_hash: str

def compute_identity(seed, parent, nid):
    return hashlib.sha256(f"{seed}|{parent}|{nid}".encode()).hexdigest()[:12]

def test_corruption_detailed():
    cases = [
        (None, True, "None debe bloquearse"),
        ("", True, "vacio debe bloquearse"),
        (" ", True, "espacio debe bloquearse"),
        ("SUN,NODE,ROOT,FLOW\n", False, "con \\n debe CANONICALIZAR y pasar"),
        (b"SUN,NODE", True, "bytes debe bloquearse"),
        (12345, True, "int debe bloquearse"),
        ("SUN,NODE", True, "3 partes debe bloquearse"),
    ]
    print("[4] Corrupcion detallada:")
    for seed, should_block, reason in cases:
        try:
            if not isinstance(seed, str) or not seed.strip():
                blocked=True
            else:
                canonical = ",".join([s.strip().upper() for s in seed.split(",")])
                blocked = len(canonical.split(","))!=4
                if not blocked:
                    compute_identity(canonical, "00000", 0)
                    print(f" ALLOW -> {repr(seed)} | {reason} | canonical={canonical}")
                    continue
            print(f" {'BLOCK' if blocked else 'ALLOW'} -> {repr(seed)} | {reason} | {'OK' if blocked==should_block else '>>> GRIETA'}")
        except Exception as e:
            print(f" BLOCK (exception) -> {repr(seed)} | {e}")

if __name__ == "__main__":
    test_corruption_detailed()
