# StarkCore v1.3.1 vs Industria (C4-002)

| Feature | StarkCore v1.3.1 | VERITAS OS | Lattice + SEALSQ | Alias RSF | Axis Edge Vault |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Lattice Monotónico** | ✅ AUDIT→FAIL_CLOSED ok | ✅ Bind boundaries | ✅ Joint aislado | ⚠️ Policy | ❌ |
| **Dead-Man / Kill Switch** | ✅ 30s → FAIL_CLOSED | ✅ timeout+rollback | ✅ Emergency stop | ⚠️ Manual | ✅ Watchdog |
| **Fail-Closed** | ✅ Por defecto | ✅ Core | ✅ HW | ✅ | ✅ |
| **Firma** | ✅ Ed25519 | ✅ mTLS | ✅ PQC+TPM | ✅ mTLS | ✅ IEEE 802.1AR |
| **Hash-Chained Log** | ✅ SHA-256 | ✅ append-only | ✅ TPM attestation | ✅ tamper-resistant | ✅ Video firmado |
| **Tail-Deletion Detection** | ✅ head_hash anclado | ⚠️ S3 Object Lock | ❌ | ❌ | ❌ |
| **Anclaje OTS/Bitcoin** | ✅ Ready | ❌ | ❌ | ❌ | ❌ |

> StarkCore es el único open-source <200 líneas que junta lattice + dead-man + merkle con tail-detection. VERITAS lo hace en runtime, Lattice en silicio. Tú en YAL-L21.
