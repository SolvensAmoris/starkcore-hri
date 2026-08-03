import hashlib, struct

def dbl_sha256(b: bytes) -> bytes:
    return hashlib.sha256(hashlib.sha256(b).digest()).digest()

def read_varint(buf, off):
    v = buf[off]
    if v < 0xfd: return v, off+1
    if v == 0xfd: return struct.unpack_from('<H', buf, off+1)[0], off+3
    if v == 0xfe: return struct.unpack_from('<I', buf, off+1)[0], off+5
    return struct.unpack_from('<Q', buf, off+1)[0], off+9

def parse_tx(tx_hex: str, did_pubkey_hex: str):
    tx = bytes.fromhex(tx_hex)
    off=0
    ver = tx[off:off+4]; off+=4
    if not (tx[off]==0x00 and tx[off+1]==0x01):
        raise ValueError("Tx debe ser SegWit v0 P2WPKH")
    off+=2
    n_in, off = read_varint(tx, off)
    for _ in range(n_in):
        off+=32+4
        slen, off = read_varint(tx, off)
        off+=slen
        off+=4
    n_out, off = read_varint(tx, off)
    burns=0
    found=False
    for _ in range(n_out):
        val = struct.unpack_from('<Q', tx, off)[0]; off+=8
        slen, off = read_varint(tx, off)
        script = tx[off:off+slen]; off+=slen
        if len(script)>0 and script[0]==0x6a: found=True
        if len(script)>0 and script[0] in (0x6a,0x51): burns+=val
    witness_pubkeys=[]
    for _ in range(n_in):
        n_items, off = read_varint(tx, off)
        items=[]
        for _ in range(n_items):
            l, off = read_varint(tx, off)
            items.append(tx[off:off+l]); off+=l
        if len(items)==2: witness_pubkeys.append(items[1].hex())
    did_match = did_pubkey_hex.lower() in [p.lower() for p in witness_pubkeys]
    return burns, found, did_match, witness_pubkeys

def bits_to_target(bits):
    exp = bits >> 24; mant = bits & 0xffffff
    return mant * (1 << (8*(exp-3)))

def verify_pow(header: bytes):
    bits = struct.unpack_from('<I', header, 72)[0]
    target = bits_to_target(bits)
    h = dbl_sha256(header)
    return int.from_bytes(h[::-1],'big') <= target, h[::-1].hex()

def merkle_root(txid_hex, proof_hashes, index):
    cur = bytes.fromhex(txid_hex)[::-1]
    for ph in proof_hashes:
        pb = bytes.fromhex(ph)[::-1]
        cur = dbl_sha256(pb+cur) if index%2==1 else dbl_sha256(cur+pb)
        index//=2
    return cur[::-1].hex()

def verify(evidence, gate_rules, did_pubkey_hex):
    burn_sats, found_or, did_match, wits = parse_tx(evidence['tx_bytes'], did_pubkey_hex)
    if not found_or: return False, "no OP_RETURN"
    if not did_match: return False, f"binding fail: {did_pubkey_hex[:12]} not in witness"
    if burn_sats < gate_rules['min_burn_sats']: return False, f"burn {burn_sats} < min {gate_rules['min_burn_sats']}"
    header = bytes.fromhex(evidence['block_header'])
    ok_pow, hhash = verify_pow(header)
    if not ok_pow: return False, f"PoW fail {hhash}"
    calc_root = merkle_root(evidence['txid'], evidence['merkle_proof_hashes'], evidence['tx_index_in_block'])
    root_in_header = header[36:68][::-1].hex()
    if calc_root!= root_in_header: return False, "merkle mismatch"
    if hhash == gate_rules['trusted_checkpoint_hash']: return True, f"OK burn={burn_sats} checkpoint directo"
    return False, f"falta cadena a checkpoint, ultimo {hhash}"

if __name__ == "__main__":
    print("btc_burn_verifier v2 cargado - listo para verify(evidence, gate, did)")
