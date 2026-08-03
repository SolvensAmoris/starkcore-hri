import hashlib, json

def execute_verified_paper(paper_path):
    with open(paper_path) as f:
        p = json.load(f)
    
    # Asumimos que ya pasó is_external_anchored()
    burn_header = p["evidence"]["block_header"]
    txid = p["evidence"]["txid"]
    did = p["cosmos_content"]["did"]
    
    seed_material = f"{burn_header}{txid}{did}".encode()
    seed = hashlib.sha256(seed_material).hexdigest()
    
    # Simulación de DSL -> logs encadenados
    logs = []
    prev = burn_header
    for i, op in enumerate(p["cosmos_content"].get("ops", ["init"])):
        h = hashlib.sha256(f"{prev}{op}{seed}".encode()).hexdigest()
        logs.append({"index": i, "op": op, "prev": prev[:16], "hash": h})
        prev = h
    
    final_root = prev
    print(f"EXECUTOR V24: seed={seed[:16]}.. root={final_root[:16]}.. logs={len(logs)}")
    print(f"Parent burn: {txid} -> inherited")
    return {"seed": seed, "final_root": final_root, "logs": logs}

if __name__ == "__main__":
    execute_verified_paper("examples/paper_btc_burn_v1.json")
