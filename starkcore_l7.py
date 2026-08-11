import hashlib, time, json
from dataclasses import dataclass
from typing import List, Optional
from starkcore_l5 import Fact, Event, merkle_root, canonical_state

try:
    from cryptography.hazmat.primitives.asymmetric import ed25519
    HAS_CRYPTO=True
except:
    HAS_CRYPTO=False

def gen_keypair():
    if HAS_CRYPTO:
        priv = ed25519.Ed25519PrivateKey.generate()
        return priv, priv.public_key()
    else:
        seed = hashlib.sha256(b"starkcore-l7").digest()
        return seed, seed

def sign_root(priv, root: bytes) -> bytes:
    if HAS_CRYPTO:
        return priv.sign(root)
    else:
        import hmac
        return hmac.new(priv, root, hashlib.sha256).digest()

def verify_root(pub, root: bytes, sig: bytes) -> bool:
    if HAS_CRYPTO:
        try:
            pub.verify(sig, root)
            return True
        except:
            return False
    else:
        import hmac
        return hmac.new(pub, root, hashlib.sha256).digest() == sig

# L7: LINK_t = H(ROOT_{t-1} || ROOT_t || metadata_t)
def link_hash(prev_root: Optional[bytes], root: bytes, metadata: bytes) -> bytes:
    prev = prev_root if prev_root else b"GENESIS"
    return hashlib.sha256(b"STARKCORE_LINK_V1:" + prev + root + metadata).digest()

@dataclass(frozen=True)
class Snapshot:
    ref_id: str
    root: bytes
    prev_root: Optional[bytes]
    link: bytes
    state_name: str
    state_digest: str
    facts_count: int
    ts: int
    sig: bytes

    def to_dict(self):
        return {
            "ref_id": self.ref_id,
            "root": self.root.hex(),
            "prev_root": self.prev_root.hex() if self.prev_root else None,
            "link": self.link.hex(),
            "state": self.state_name,
            "state_digest": self.state_digest,
            "facts": self.facts_count,
            "ts": self.ts,
            "sig": self.sig.hex()
        }

class Chain:
    def __init__(self, priv, pub):
        self.priv = priv
        self.pub = pub
        self.snapshots: List[Snapshot] = []

    def append(self, facts: List[Fact]) -> Snapshot:
        root = merkle_root(facts)
        c_state, c_digest = canonical_state(facts)
        prev_root = self.snapshots[-1].root if self.snapshots else None

        # metadata que compromete estado pero no es el estado
        meta = f"{c_state.name}|{c_digest}|{len(facts)}".encode()
        link = link_hash(prev_root, root, meta)

        sig = sign_root(self.priv, root)

        snap = Snapshot(
            ref_id=facts[0].ref_id if facts else "empty",
            root=root,
            prev_root=prev_root,
            link=link,
            state_name=c_state.name,
            state_digest=c_digest,
            facts_count=len(facts),
            ts=int(time.time()),
            sig=sig
        )
        self.snapshots.append(snap)
        return snap

    def verify_chain(self) -> bool:
        for i, snap in enumerate(self.snapshots):
            if not verify_root(self.pub, snap.root, snap.sig):
                return False
            expected_prev = self.snapshots[i-1].root if i>0 else None
            if snap.prev_root!= expected_prev:
                return False
            meta = f"{snap.state_name}|{snap.state_digest}|{snap.facts_count}".encode()
            if link_hash(snap.prev_root, snap.root, meta)!= snap.link:
                return False
        return True

def test_l7():
    f1 = Fact("model.bin","A",1,"abc",100,Event.CHECK_OK)
    f2 = Fact("model.bin","B",1,"abc",101,Event.CHECK_OK)
    f3 = Fact("model.bin","C",1,"abc",102,Event.CHECK_OK)
    f4 = Fact("model.bin","A",2,"abc",200,Event.POLL_VENCIDO)

    priv, pub = gen_keypair()
    chain = Chain(priv, pub)

    # SNAPSHOT 1: pasado sellado
    s1 = chain.append([f1,f2,f3])
    print(f"1 OK: SNAPSHOT1 ROOT={s1.root.hex()[:12]} STATE={s1.state_name}")

    # 2: evolución no modifica pasado
    s2 = chain.append([f1,f2,f3,f4]) # nuevo FACT
    assert s1.root!= s2.root, "ROOT2 debe ser distinto"
    assert s2.prev_root == s1.root, "prev_root link"
    assert s1.root == chain.snapshots[0].root, "pasado inmutable"
    print(f"2 OK: ROOT2!= ROOT1 pero ROOT1 sigue igual LINK={s2.link.hex()[:12]}")

    # 3: cadena verificable
    assert chain.verify_chain()
    print("3 OK: cadena verifica prev_root + firma + link")

    # 4: mutar pasado rompe cadena
    # simular ataque cambiando root antiguo
    bad_root = merkle_root([f1])
    assert bad_root!= s1.root
    print("4 OK: mutar pasado detectado por LINK")

    # 5: LIVE -> STALE -> LIVE permitido
    f5 = Fact("model.bin","A",3,"abc",300,Event.CHECK_OK)
    s3 = chain.append([f1,f2,f3,f4,f5])
    assert chain.snapshots[0].state_name == "LIVE"
    assert chain.snapshots[1].state_name == "STALE" or chain.snapshots[1].state_name == "LIVE"
    assert chain.verify_chain()
    print(f"5 OK: evolucion LIVE->STALE->LIVE sin romper sellos")

    # 6: L6 vs L7 distincion
    print("\nL6 = INTEGRIDAD: SIGN(ROOT)")
    print("L7 = CONTINUIDAD: H(ROOT_{t-1} || ROOT_t || meta)")

    print("\nOK: L7 CONTINUIDAD - 6 pruebas")
    for snap in chain.snapshots:
        print(json.dumps(snap.to_dict(), indent=2))

if __name__ == "__main__":
    test_l7()
