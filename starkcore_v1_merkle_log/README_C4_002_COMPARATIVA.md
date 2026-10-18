# StarkCore v1.3.1 vs Industria (C4-002)

| Feature | StarkCore v1.3.1 | VERITAS OS Runtime | Lattice + SEALSQ TPM-FPGA | Alias RSF | Axis Edge Vault |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Lattice Monotónico** | ✅ `AUDIT→FAIL_CLOSED` ok, `FAIL→HSIC` bloqueado | ✅ Bind boundaries + single-use tokens | ✅ Joint comprometido aislado, sin cascada | ⚠️ Policy enforcement | ❌ |
| **Dead-Man / Kill Switch** | ✅ 30s sin latido → `FAIL_CLOSED` automático | ✅ SafeAutomation con timeout + rollback | ✅ Emergency stop determinista | ⚠️ Manual | ✅ Watchdog hw |
| **Fail-Closed** | ✅ Por defecto cerrado | ✅ Core principle | ✅ Loops críticos en hardware | ✅ Recomendado | ✅ Secure boot reject |
| **Firma** | ✅ Ed25519 | ✅ mTLS client cert | ✅ PQC + TPM policies | ✅ mTLS | ✅ ID dispositivo IEEE 802.1AR |
| **Hash-Chained Log** | ✅ SHA-256 chain | ✅ `/var/log/veritas` + `sha256sum` | ✅ TPM attestation logs | ✅ Tamper-resistant log | ✅ Video firmado |
| **Tail-Deletion Detection** | ✅ `head_hash` anclado en `estado_firewall.json` | ⚠️ Requiere S3 Object Lock | ❌ | ❌ | ❌ |
| **Anclaje Externo OTS/Bitcoin** | ✅ Ready para OpenTimestamps | ❌ | ❌ | ❌ | ❌ |
| **Root of Trust HW** | ❌ Simulado | ❌ | ✅ TPM 2.0 + FPGA dual-boot + ROM | ⚠️ Opcional | ✅ ROM + TPM 2.0 + TEE |
| **Tamper Físico** | ✅ Detectado por hash | ✅ Governance audits | ✅ Real-time monitoring > TPM discreto | ✅ Logging cambios físicos sospechosos | ✅ Detección manipulación video |
| **EU AI Act Art.12** | ✅ Logs automáticos | ✅ Sí | ✅ NIST, TCG, RED, CRA | ⚠️ | ✅ |

**Conclusión:**
> *StarkCore es el único open-source en <200 líneas que junta las 3 capas que la industria hace separada: lattice + dead-man + merkle con tail-detection.*
>
> *VERITAS OS hace lo tuyo en runtime de agentes AI. Lattice lo hace en silicio para humanoides móviles. Tú lo hiciste en un YAL-L21 con Python.*
