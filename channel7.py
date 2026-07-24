import hashlib,pathlib
ORIGEN="00000"
A=b"api"+b".x.com"
B=b"bear"+b"er_token"
def guardian(d): return A in d and B in d
def canal(p):
 data=pathlib.Path(p).read_bytes()
 sha=hashlib.sha256(data).hexdigest()
 if p!=__file__ and guardian(data):
  print(f"BLOCKED 403 {p}")
  return
 print(f"ACEPTAR {p} sha={sha[:8]} E==H")
import sys
for f in sys.argv[1:]: canal(f)
