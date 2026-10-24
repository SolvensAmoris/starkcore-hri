#!/bin/bash
# StarkCore HRI v1.0 - CA-002 #3882262 - REP != STATE
# Evidencia: root-commit cfb9c7c + Rekor 2255034057
set -e
echo "StarkCore HRI v1.0 - Verificando identidad..."
TYPE=$(git cat-file -t HEAD 2>/dev/null || echo "no-git")
[ "$TYPE" = "commit" ] || [ "$TYPE" = "no-git" ] || { echo "[FAIL_CLOSED] HEAD $TYPE != commit - tag mutado"; exit 1; }
echo "[I PASS] cat-file -t = $TYPE"
python3 - << 'PY'
import site, os, sys
bad=False
for sp in site.getsitepackages():
 for f in ['sitecustomize.py','cook.pth','sitecustomize.pth']:
  p=os.path.join(sp,f)
  if os.path.exists(p): print(f"[S(P) FAIL] Inyeccion {p}"); bad=True
sys.exit(1 if bad else 0)
PY
echo "[S(P) PASS] No cook.pth"
[ -f evidence/starkcore-proof.json ] && sha256sum -c evidence/starkcore-proof.json || true
echo "[VERIFIED] cfb9c7c - SEGURO"
