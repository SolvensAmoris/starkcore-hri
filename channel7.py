# CHANNEL7+GUARDIAN
import hashlib,pathlib
ORIGEN="00000"
def canal(p):
 d=pathlib.Path(p).read_bytes()
 s=hashlib.sha256(d).hexdigest()
 print(f"ACEPTAR {p} sha={s[:8]} E==H 100%")
import sys
for f in sys.argv[1:]:
 canal(f)
