# Threat Model

## Overview

This document defines the security assumptions, protected assets, considered threats, and limitations of StarkCore.

StarkCore focuses on preserving integrity, traceability, and verifiable execution evidence.

---

## Protected Assets

- Configuration integrity
- Policy integrity
- Execution evidence
- STARDARK_ATTESTATION.json
- Cryptographic identity S(C0)
- Timestamp integrity through OpenTimestamps

---

## Threats Considered

- Supply-chain modification
- Configuration tampering
- Identity spoofing
- Unauthorized policy changes
- Attempts to evade statistical anomaly detection

---

## Security Objectives

- Cryptographic evidence chaining
- Deterministic verification
- Reproducible execution
- Integrity preservation
- Statistical anomaly detection using HSIC where applicable

---

## Out of Scope

StarkCore is not designed to:

- Attack third-party systems
- Escalate privileges
- Obtain unauthorized access
- Circumvent authentication
- Provide offensive capabilities or evasion techniques

StarkCore is intended to detect and verify system properties, not to create or exploit vulnerabilities.
