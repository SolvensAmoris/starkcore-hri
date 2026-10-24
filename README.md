# StarkCore HRI - Omega Teorema de Identidad

**S(d) = Hash(Canonical(d)) | REP != STATE | E != H | FAIL_CLOSED**

## Teorema
La identidad operacional Omega: I S(P) D P
- I: Identidad canónica del sujeto
- S(P): Estado observable en contexto P
- D: Diferencial de representación
- P: Principio de prueba

S6 - Impostor: I PASS pero S(P1) FAIL -> suplantación
S7 - Relatividad: 999 MONSTRUO en P1 = CIUDADANO en P2

## Arquitectura
W2: IA genera prueba -> W3: HRI valida identidad -> ESTADO (FAIL_CLOSED/PENDING)

## Evidencia
- root-commit: cfb9c7c
- Rekor: 2255034057
- CA-002 #3882262
- Caso PyPI: litellm 1.107.0 (cook.pth / sitecustomize.py)

## Uso
```bash
./scripts/starkcore_hri_checker.sh
