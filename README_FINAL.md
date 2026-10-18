# STARKCORE // SOLVENS CORE
## Arquitectura de Ejecución Verificable y Gobernanza Autónoma

> **WE DON'T NEED MORE EXPLANATIONS. WE NEED EVIDENCE.**
> `SISTEMA ONTOLÓGICO :: LISTO // REP≠STATE≠AGENCY | v0.4 LOCKED | R²=0.99 n=1000`

### Resumen
StarkCore es un runtime defensivo de grado industrial que resuelve el desacoplamiento ontológico (C4-002): la brecha entre lo que un agente *dice* que es y lo que el sistema *demuestra* que es.

Implementado desde cero en un entorno móvil (Huawei Nova 5T / UserLand), combina criptografía de curva elíptica, máquinas de estado formales y evidencia inmutable.

### Arquitectura (5 Capas + Cosmos)
- **Cosmos / Genesis**: `cosmos_genesis.json` - Hash `9a19a3154d064432...` grabado en ROM. Cualquier alteración detectada en boot.
- **DAG Canonicalizer (v1.4)**: `generar_hash_estructural()` - Hash determinista inmune a Type Confusion e inyección de nodos.
- **Gateway**: Valida Ed25519 + política + DAG Hash.
- **Jacobian**: Gestor de estado atómico. Solo muta bajo evidencia válida.
- **Evidence Layer**: Log Merkle-chain con tail-detection.

### Hitos Implementados
- **v0.4 Crypto**: Ed25519 + Anti-Replay
- **v1.1 Lattice**: AUDIT→FAIL_CLOSED ok, FAIL_CLOSED→HSIC bloqueado
- **v1.2 Dead-Man**: 30s timeout → FAIL_CLOSED
- **v1.3 Merkle**: head_hash + tail-deletion detection
- **v1.3.1 OTS**: `6003adf0797949fa3637172f903f3c96fd42fedf5a6061027156077bf9cef2bb` @ 2026-10-18T22:33:30Z - .ots 770 bytes
- **v1.4 DAG**: Detecta 666cf7d5d16296... vs 9a19a315...
- **v1.5 Solvens**: VERIFIED [ACCEPT] Bbcee70a0ca7d10f... / REJECT SIGNATURE_INVALID

### Evidencia Empírica
1. WarpOmega_Corrected.lean → VERIFIED ACCEPT
2. WarpOmega_Corrupted.lean (E.Omega < 0 FALSO) → REJECT SIGNATURE_INVALID
3. Inyección Nodo Fantasma → RECHAZADO Ataque de Topología
4. Tail-Deletion → ALERTA Log altura 0 c4aca7... vs ancla 1 800d9...
5. Dead-Man → FAIL_CLOSED automático
6. OTS Anchor → 4 calendarios Bitcoin

### Cierre
- Commit: ab26c81
- Tag: v1.3.1_C4-002_COMPLETE / v1.5_SOLVENS_CORE
- Ancla: 6003adf0797949fa3637172f903f3c96fd42fedf5a6061027156077bf9cef2bb
- Estado: SISTEMA ONTOLÓGICO :: LISTO
