import hashlib
import json
import time
from pathlib import Path

def sha256_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def rebuild():
    print("=== INICIANDO PROTOCOLO DE REDENCIÓN (T_redemption) ===")
    
    # 1. Buscar archivos válidos (excluyendo .git y el propio script)
    files_to_hash = []
    for p in sorted(Path(".").rglob("*")):
        if p.is_file() and ".git" not in p.parts and "rebuild_ledger.py" not in p.name and "ledger.bundle" not in p.name:
            files_to_hash.append({
                "path": str(p),
                "sha256": sha256_file(p)
            })
            
    # 2. Crear el bloque de génesis (documentando la pérdida)
    genesis_block = {
        "event": "T_REDEMPTION",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "reason": "Original ledger.bundle lost during repository flattening (commit cfb9c7c not found).",
        "policy": "FAIL_CLOSED_REBUILD",
        "reconstructed_artifacts": files_to_hash
    }
    
    # 3. Calcular el hash del bloque
    block_str = json.dumps(genesis_block, sort_keys=True)
    genesis_hash = hashlib.sha256(block_str.encode()).hexdigest()
    
    # 4. Empaquetar el Ledger
    ledger = {
        "version": "StarkCore HRI v1.0 (Redemption)",
        "trajectory": [
            {
                "block_index": 0,
                "data": genesis_block,
                "hash": genesis_hash,
                "prev_hash": "0"*64
            }
        ]
    }
    
    # 5. Guardar físicamente
    Path("ledger.bundle").write_text(json.dumps(ledger, indent=2))
    print(f"[+] Ledger reconstruido y sellado en: ledger.bundle")
    print(f"[+] Nuevo Hash del Bloque Génesis: {genesis_hash}")

if __name__ == "__main__":
    rebuild()
