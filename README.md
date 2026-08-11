# STARKCORE | C4-002
WE DON'T NEED MORE EXPLANATIONS. WE NEED EVIDENCE.

L1 REFERENCE estable
L2 FACT insert-only 16/16 FSM
L3 CANONICAL quorum LIVE/STALE/INVALID/CONFLICT
L4 MERKLE ROOT=H(FACTS)
L5 FACTS->(ROOT,STATE) pero STATE -/-> FACTS
L6 SIGN(ROOT) = integridad
L7 LINK=H(prev||curr||meta) = continuidad

## Verificacion
pip install cryptography -q
python3 starkcore_cli.py verify-chain

Esperado: CHAIN LEN=3 VERIFY=True
ROOT1=18de4a5325905e783aa360b934b46c05
