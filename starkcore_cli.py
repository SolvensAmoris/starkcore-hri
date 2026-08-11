#!/usr/bin/env python3
import argparse, json, os, sys, hashlib, time
from pathlib import Path
from starkcore_l5 import Fact, Event, merkle_root, canonical_state
from starkcore_l7 import gen_keypair, sign_root, verify_root, link_hash, Chain, Snapshot

CHAIN_FILE = Path("starkcore_chain.json")
KEY_FILE = Path("starkcore_key.json")

def load_or_create_keys():
    if KEY_FILE.exists():
        data = json.loads(KEY_FILE.read_text())
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
        priv = Ed25519PrivateKey.from_private_bytes(bytes.fromhex(data["priv"]))
        pub = Ed25519PublicKey.from_public_bytes(bytes.fromhex(data["pub"]))
        return priv, pub, data
    else:
        priv, pub = gen_keypair()
        # guardar raw
        if hasattr(priv, 'private_bytes'):
            from cryptography.hazmat.primitives import serialization
            priv_hex = priv.private_bytes(serialization.Encoding.Raw, serialization.PrivateFormat.Raw, serialization.NoEncryption()).hex()
            pub_hex = pub.public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw).hex()
        else:
            priv_hex = pub_hex = priv.hex() if isinstance(priv, bytes) else "fallback"
        KEY_FILE.write_text(json.dumps({"priv": priv_hex, "pub": pub_hex, "pub_hex": pub_hex}, indent=2))
        print(f"[KEY] generada -> {KEY_FILE} pub={pub_hex[:16]}...")
        return priv, pub, {"pub_hex": pub_hex}

def load_chain(priv, pub):
    chain = Chain(priv, pub)
    if CHAIN_FILE.exists():
        data = json.loads(CHAIN_FILE.read_text())
        # reconstruir snapshots
        for d in data.get("snapshots", []):
            snap = Snapshot(
                ref_id=d["ref_id"],
                root=bytes.fromhex(d["root"]),
                prev_root=bytes.fromhex(d["prev_root"]) if d["prev_root"] else None,
                link=bytes.fromhex(d["link"]),
                state_name=d["state"],
                state_digest=d["state_digest"],
                facts_count=d["facts"],
                ts=d["ts"],
                sig=bytes.fromhex(d["sig"])
            )
            chain.snapshots.append(snap)
    return chain

def save_chain(chain):
    out = {"snapshots": [s.to_dict() for s in chain.snapshots]}
    CHAIN_FILE.write_text(json.dumps(out, indent=2))
    print(f"[CHAIN] guardada {len(chain.snapshots)} snapshots -> {CHAIN_FILE}")

def cmd_snapshot(args):
    priv, pub, keydata = load_or_create_keys()
    chain = load_chain(priv, pub)

    # demo FACTS desde args o default
    # en prod vendrian de tu observer real
    facts = []
    for i, dig in enumerate(args.digests):
        facts.append(Fact(args.ref, f"OBS{i}", i+1, dig, int(time.time())+i, Event.CHECK_OK))

    snap = chain.append(facts)
    save_chain(chain)

    print(f"\nOK: SNAPSHOT {len(chain.snapshots)}")
    print(f"REFERENCE={snap.ref_id}")
    print(f"FACTS={snap.facts_count}")
    print(f"ROOT={snap.root.hex()}")
    print(f"PREV={snap.prev_root.hex()[:16] if snap.prev_root else 'GENESIS'}")
    print(f"LINK={snap.link.hex()}")
    print(f"STATE={snap.state_name} {snap.state_digest}")
    print(f"SIG={snap.sig.hex()[:32]}...")

    if len(chain.snapshots)==1:
        print("\n>>> GENESIS SELLADO <<<")

def cmd_verify(args):
    priv, pub, keydata = load_or_create_keys()
    chain = load_chain(priv, pub)
    if not chain.snapshots:
        print("CHAIN vacia"); return
    ok = chain.verify_chain()
    print(f"CHAIN LEN={len(chain.snapshots)} VERIFY={ok}")
    for i,s in enumerate(chain.snapshots):
        status = "OK" if verify_root(pub, s.root, s.sig) else "FAIL"
        print(f" {i+1}. {s.root.hex()[:12]} -> {s.state_name} {status} LINK {s.link.hex()[:8]}")
    if ok:
        print("\nSISTEMA ONTOLÓGICO :: LISTO // REP==STATE")
    else:
        print("\n!!! CADENA ROTA !!!")

def cmd_genesis(args):
    if CHAIN_FILE.exists():
        print(f"Ya existe {CHAIN_FILE}, borrala si quieres re-génesis")
        return
    args.ref = "model.bin"
    args.digests = ["abc","abc","abc"]
    cmd_snapshot(args)

if __name__ == "__main__":
    p = argparse.ArgumentParser(prog="starkcore")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("snapshot", help="crea nuevo snapshot desde digests")
    s.add_argument("--ref", default="model.bin")
    s.add_argument("digests", nargs="*", default=["abc","abc","abc"])
    s.set_defaults(func=cmd_snapshot)

    v = sub.add_parser("verify-chain", help="verifica cadena completa")
    v.set_defaults(func=cmd_verify)

    g = sub.add_parser("genesis", help="sella genesis inicial")
    g.set_defaults(func=cmd_genesis)

    args = p.parse_args()
    args.func(args)
