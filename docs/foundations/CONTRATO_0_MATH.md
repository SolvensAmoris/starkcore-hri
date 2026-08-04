# CONTRATO 0 - PRINCIPIO 0*

P0*: S(C0) = f8581c6f7d5e1557086c72fceb827f1df87cf212f5ee393c320d0126e9c6a5e9

## Anclajes
A11 = S(C0) = genesis
A33 = merkle_root = 3b1a7de5...
A66 = sign(A33, A-Stark)
A99 = OTS(A66) = TX 8447a3e2...

## Ley Libra
delta_max(n+1) - delta_max(n) <= 1

## Ley Virgo
verify = SHA256_canonical + policy_hash 3197f997... constante
