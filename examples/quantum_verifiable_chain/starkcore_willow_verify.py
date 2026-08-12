#!/usr/bin/env python3
# STARKCORE-Q // VERIFIABLE CHAIN, NOT FULL COMPUTATION
# PRINCIPLE: No verificas el universo. Verificas la evidencia.

import json
import hashlib
import time

# Cadena oficial de Google Willow publicada en Nature Dec 2024
# Esta es tu "registry" como en tu verificacion de Chrome Store
WILLOW_REGISTRY = {
    "chip": "Willow",
    "qubits": 105,
    "connectivity_avg": 3.47,
    "gate_1q_error_max": 0.00035,  # 0.035%
    "gate_2q_error_max": 0.0033,   # 0.33% CZ
    "meas_error_max": 0.0077,      # 0.77%
    "T1_min_us": 68,
    "paper": "Nature 2024, Google Quantum AI",
    "paper_hash": "willow_nature_2024_sha"
}

def shasum(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()[:12]

def verify_claim_chain(job_manifest: dict):
    """
    StarkCore no simula 105 qubits. Imposible en userland.
    Verifica 3 links de la cadena:
    1. claim vs registry
    2. counts vs estructura esperada
    3. attestation vs tiempo
    """
    evidence = []
    is_chain_valid = True

    # LINK 1: Registry check (como live shasum vs registry)
    if job_manifest["chip"] != WILLOW_REGISTRY["chip"]:
        evidence.append("FAIL: chip claim != registry")
        is_chain_valid = False
    else:
        evidence.append(f"PASS: chip={WILLOW_REGISTRY['chip']} matches registry")

    # LINK 2: Error budget check - si te dicen que corrio bien, los errors deben estar dentro del budget
    # No necesitas recalcular todo, solo verificar que lo que reportan no viola su propio paper
    reported_1q = job_manifest.get("reported_1q_error", 0)
    if reported_1q > WILLOW_REGISTRY["gate_1q_error_max"]:
        evidence.append(f"FAIL: reported 1q error {reported_1q} > max {WILLOW_REGISTRY['gate_1q_error_max']}")
        is_chain_valid = False
    else:
        evidence.append(f"PASS: 1q error {reported_1q} within budget")

    # LINK 3: La distribucion observable - no todo el calculo, solo la invariante
    # Ej: si es Bell, P(00)+P(11) debe dominar. Si no, alguien te vendio humo
    counts = job_manifest.get("counts", {})
    shots = sum(counts.values()) or 1
    if counts:
        p00 = counts.get('00',0)/shots
        p11 = counts.get('11',0)/shots
        bell_mass = p00 + p11
        if bell_mass < 0.85:
            evidence.append(f"FAIL: bell_mass {bell_mass:.2f} < 0.85 - distribution broken")
            is_chain_valid = False
        else:
            evidence.append(f"PASS: bell_mass {bell_mass:.2f} structure holds")

    verdict = "VALID" if is_chain_valid else "FAIL-CLOSED"
    
    return {
        "starkcore_principle": "Structure over Representation - Verify chain, not computation",
        "registry_source": WILLOW_REGISTRY["paper"],
        "registry_shasum": shasum(json.dumps(WILLOW_REGISTRY)),
        "job_shasum": shasum(json.dumps(job_manifest)),
        "evidence_chain": evidence,
        "verdict": verdict,
        "collembolo_note": "400M years in prod. No cloud. No trust."
    }

# --- EJEMPLO DESDE USERLAND ---
# Esto es lo que te devuelve cualquier provider (IBM, Google, etc)
# Tu no recalculas 10^25 años de RCS. Solo verificas la cadena.

job_good = {
    "chip": "Willow",
    "reported_1q_error": 0.00033,
    "counts": {"00": 5100, "11": 4900}
}

job_bad = {
    "chip": "Willow",
    "reported_1q_error": 0.002, # 0.2% > 0.035% -> miente o esta degradado
    "counts": {"00": 3000, "01": 2500, "10": 2500, "11": 2000}
}

for label, job in [("GOOD CHAIN", job_good), ("BAD CHAIN", job_bad)]:
    print(f"\n--- {label} ---")
    print(json.dumps(verify_claim_chain(job), indent=2))
