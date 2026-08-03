import hashlib, json, time

def notarize(execution_result, paper_path):
    with open(paper_path) as f:
        paper = json.load(f)
    
    did = paper["cosmos_content"]["did"]
    txid = paper["evidence"]["txid"]
    burn_header = paper["evidence"]["block_header"]
    
    # El objeto notarizable: todo lo que un catálogo externo necesita para re-verificar sin ti
    notary_doc = {
        "version": "cosmos-notary-v1",
        "did": did,
        "parent_burn_txid": txid,
        "parent_burn_header": burn_header,
        "execution_seed": execution_result["seed"],
        "final_state_root": execution_result["final_root"],
        "logs_root": hashlib.sha256(json.dumps(execution_result["logs"]).encode()).hexdigest(),
        "timestamp": int(time.time()),
        "proof_type": "btc-burn-v24"
    }
    
    # Hash final que se publica en el registry (75e47009... que mencionaste)
    notary_hash = hashlib.sha256(json.dumps(notary_doc, sort_keys=True).encode()).hexdigest()
    notary_doc["notary_hash"] = notary_hash
    
    with open("examples/notary_v1.json","w") as out:
        json.dump(notary_doc, out, indent=2)
    
    print(f"NOTARY V1: notary_hash={notary_hash}")
    print(f"Final root: {execution_result['final_root']}")
    print(f"Exportable a: examples/notary_v1.json")
    print(f"Listo para registry público")
    return notary_doc

if __name__ == "__main__":
    from starkcore.executor import execute_verified_paper
    exec_res = execute_verified_paper("examples/paper_btc_burn_v1.json")
    notarize(exec_res, "examples/paper_btc_burn_v1.json")
