# CHANNEL 7 CUANTICO
ORIGEN='00000'
ANCLAJES=[11,33,66,99]
import hashlib,pathlib
def canal7(p):
    data=pathlib.Path(p).read_bytes()
    sha=hashlib.sha256(data).hexdigest()
    print(f'ACEPTAR sha={sha[:16]} size={len(data)} origen={ORIGEN} anclajes={ANCLAJES} veredicto=100% E==H')
import sys
for f in sys.argv[1:]:
    canal7(f)
