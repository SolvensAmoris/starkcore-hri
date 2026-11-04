"""
STO // REP≠STATE≠AGENCY | v0.4 LOCKED
GIE-002: Enforcer with Cryptographic Evidence
"""
import json
import datetime

def _rotr(x,n): return ((x>>n)|(x<<(32-n)))&0xFFFFFFFF
def _sha256_pure(data: bytes)->str:
    K=[0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2]
    H=[0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19]
    ml=len(data)*8; data=data+b'\x80'
    while (len(data)*8)%512!=448: data+=b'\x00'
    data+=ml.to_bytes(8,'big')
    for i in range(0,len(data),64):
        chunk=data[i:i+64]; w=[0]*64
        for j in range(16): w[j]=int.from_bytes(chunk[j*4:(j+1)*4],'big')
        for j in range(16,64):
            s0=_rotr(w[j-15],7)^_rotr(w[j-15],18)^(w[j-15]>>3)
            s1=_rotr(w[j-2],17)^_rotr(w[j-2],19)^(w[j-2]>>10)
            w[j]=(w[j-16]+s0+w[j-7]+s1)&0xFFFFFFFF
        a,b,c,d,e,f,g,h=H
        for j in range(64):
            S1=_rotr(e,6)^_rotr(e,11)^_rotr(e,25); ch=(e&f)^((~e)&g)
            temp1=(h+S1+ch+K[j]+w[j])&0xFFFFFFFF
            S0=_rotr(a,2)^_rotr(a,13)^_rotr(a,22); maj=(a&b)^(a&c)^(b&c)
            temp2=(S0+maj)&0xFFFFFFFF
            h=g;g=f;f=e;e=(d+temp1)&0xFFFFFFFF;d=c;c=b;b=a;a=(temp1+temp2)&0xFFFFFFFF
        H=[(x+y)&0xFFFFFFFF for x,y in zip(H,[a,b,c,d,e,f,g,h])]
    return ''.join(f'{x:08x}' for x in H)

def canonical_json(o): return json.dumps(o,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def evidence_hash(b): return _sha256_pure(canonical_json(b).encode('utf-8'))

def enforce_with_evidence(propagated_nodes):
    result={}; ts=datetime.datetime.now(datetime.timezone.utc).isoformat()
    for node,attrs in propagated_nodes.items():
        raw_v=attrs.get("verdict"); v=getattr(raw_v,'value',str(raw_v)).upper()
        if "REJECT" in v: v="REJECT"
        elif "ESCALATE" in v: v="ESCALATE"
        else: v="ACCEPT"
        deg=attrs.get("degraded",False)
        d=deg if isinstance(deg,bool) else (deg.name=="DEGRADED" if hasattr(deg,'name') else str(deg).lower()=="true")
        if v=="REJECT": decision="REJECT"; reason=f"STRUCTURAL_REJECT_PROPAGATION: upstream REJECT contaminates {node} | REP!=STATE"
        elif v=="ESCALATE": decision="ESCALATE"; reason=f"STRUCTURAL_ESCALATE: {node} requires human review | STATE!=AGENCY"
        else: decision="ACCEPT"; reason=f"STRUCTURAL_ACCEPT: no REJECT in closure | DEGRADED={d}"
        chain={"node":node,"verdict":v,"degraded":d,"decision":decision,"reason":reason}
        result[node]={"decision":decision,"verdict":v,"degraded":d,"reason":reason,"evidence_hash":evidence_hash(chain),"chain":chain,"timestamp":ts}
    return result

def enforce(nodes_dict):
    norm={}
    for k,v in nodes_dict.items(): norm[k]={"verdict":v.get("verdict"),"degraded":v.get("degraded",False)}
    return enforce_with_evidence(norm)
