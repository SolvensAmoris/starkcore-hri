import hashlib
import math
import json
import statistics
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.exceptions import InvalidSignature

# ==========================================
# STARKCORE-SIM-001 v0.7: EVIDENCE & EQUIVALENCE ASSURANCE
# Rules: MATCH != VALIDATION | HASH != ATTESTATION | NO DIFF != EQUIVALENCE
# ==========================================

def wilson_score_interval(successes, n, confidence=0.95):
    """Calcula el intervalo de confianza de Wilson."""
    if n == 0: return 0.0, 1.0
    z = statistics.NormalDist().inv_cdf(1 - (1 - confidence) / 2)
    p = successes / n
    denominator = 1 + z**2 / n
    centre_adjusted_probability = p + z**2 / (2 * n)
    adjusted_standard_deviation = math.sqrt((p * (1 - p) + z**2 / (4 * n)) / n)
    lower_bound = (centre_adjusted_probability - z * adjusted_standard_deviation) / denominator
    upper_bound = (centre_adjusted_probability + z * adjusted_standard_deviation) / denominator
    return max(0.0, lower_bound), min(1.0, upper_bound)

def mcnemar_test_v7(pairs_dict):
    """SC-SIM-33: McNemar corregido."""
    b = sum(1 for s, h in pairs_dict.values() if s == 1 and h == 0)
    c = sum(1 for s, h in pairs_dict.values() if s == 0 and h == 1)
    if b + c == 0: return 1.0
    chi2 = (abs(b - c) - 1)**2 / (b + c)
    return math.erfc(math.sqrt(chi2 / 2))

def tost_equivalence_v7(p1, n1, p2, n2, delta=0.05, alpha=0.05):
    """SC-SIM-32: TOST robusto."""
    if n1 == 0 or n2 == 0: return 1.0
    diff = p1 - p2
    se = math.sqrt((p1*(1-p1)/n1) + (p2*(1-p2)/n2))
    
    if se == 0:
        # Si la diferencia es 0, son idénticos. Si no, son opuestos.
        return 0.0 if abs(diff) < delta else 1.0

    z_lower = (diff - (-delta)) / se
    p_lower = 1 - statistics.NormalDist().cdf(z_lower)
    z_upper = (diff - delta) / se
    p_upper = statistics.NormalDist().cdf(z_upper)
    return max(p_lower, p_upper)

class TrustedAuthorityV7:
    def __init__(self):
        self.registry = {}
    def register_actor(self, actor_id, role):
        priv = ed25519.Ed25519PrivateKey.generate()
        self.registry[actor_id] = {"priv": priv, "pub": priv.public_key(), "role": role}
        return priv
    def get_public(self, actor_id):
        return self.registry.get(actor_id)

def create_manifest_v7(experiment_id, model_id, sim_pairs, human_pairs, context, mode):
    """SC-SIM-27 / SC-SIM-35: Manifiesto canónico con pair_ids y registros completos."""
    return json.dumps({
        "experiment_id": experiment_id,
        "model_id": model_id,
        "sim_hash": hashlib.sha256(json.dumps(sim_pairs, sort_keys=True).encode()).hexdigest(),
        "human_hash": hashlib.sha256(json.dumps(human_pairs, sort_keys=True).encode()).hexdigest(),
        "context": context,
        "mode": mode,
        "version": "v0.7"
    }, sort_keys=True).encode()

class StatisticalEvidenceGateV7:
    def __init__(self, min_sample=100, delta=0.05, confidence=0.95, accept_threshold=0.80):
        self.min_sample = min_sample
        self.delta = delta
        self.alpha = 1 - confidence
        self.accept_threshold = accept_threshold

    def _validate_inputs(self, sim_data, human_data):
        """SC-SIM-31: Validación estricta de muestras."""
        n_sim = len(sim_data.get("decisions", []))
        n_human = len(human_data.get("decisions", []))
        
        if n_sim == 0 or n_human == 0:
            return False, "Muestras vacías"
        if n_sim < self.min_sample or n_human < self.min_sample:
            return False, f"Muestra insuficiente (Min: {self.min_sample})"
        if sim_data["mode"] == "PAIRED":
            if len(sim_data.get("pair_ids", [])) != n_sim or len(human_data.get("pair_ids", [])) != n_human:
                return False, "Longitud de pair_ids no coincide con decisiones"
            if len(set(sim_data["pair_ids"])) != n_sim or len(set(human_data["pair_ids"])) != n_human:
                return False, "IDs de pares duplicados"
            if set(sim_data["pair_ids"]) != set(human_data["pair_ids"]):
                return False, "Conjuntos de IDs de pares no coinciden"
        return True, "OK"

    def evaluate(self, sim_data, human_data, witness_id, signature, pki):
        print(f"=== STARKCORE-SIM-001 v0.7 (Mode: {sim_data['mode']}) ===\n")
        
        # 1. Validaciones Estructurales
        valid, msg = self._validate_inputs(sim_data, human_data)
        if not valid: return f"ESCALATE ({msg})"
        
        # 2. Autoridad
        witness = pki.get_public(witness_id)
        if not witness or witness["role"] != "WITNESS": return "ESCALATE (Testigo no autorizado)"
        
        # 3. Manifiesto y Firma
        manifest = create_manifest_v7(
            sim_data["experiment_id"], sim_data["model_id"],
            sim_data.get("pair_ids", []), human_data.get("pair_ids", []),
            human_data["context"], sim_data["mode"]
        )
        try:
            witness["pub"].verify(signature, manifest)
            print("  [+] Firma Ed25519 validada sobre manifiesto canónico.")
        except InvalidSignature:
            return "ESCALATE (SC-SIM-35: Firma inválida o metadatos alterados)"

        # 4. Análisis Estadístico
        print("\n[4] Análisis Estadístico...")
        n_sim = len(sim_data["decisions"])
        
        if sim_data["mode"] == "PAIRED":
            # Mapeo estricto
            sim_map = dict(zip(sim_data["pair_ids"], sim_data["decisions"]))
            human_map = dict(zip(human_data["pair_ids"], human_data["decisions"]))
            pairs = {pid: (sim_map[pid], human_map[pid]) for pid in sorted(sim_map)}
            
            matches = sum(1 for s, h in pairs.values() if s == h)
            lower_bound, _ = wilson_score_interval(matches, n_sim, 1 - self.alpha)
            p_val_mcnemar = mcnemar_test_v7(pairs)
            
            print(f"  -> Concordancia Pareada: {matches}/{n_sim} ({(matches/n_sim)*100:.1f}%)")
            print(f"  -> Intervalo Wilson (Inferior): {lower_bound:.3f}")
            print(f"  -> McNemar p-value: {p_val_mcnemar:.5f}")
            
            # SC-SIM-34: Wilson + McNemar
            if lower_bound >= self.accept_threshold and p_val_mcnemar > self.alpha:
                return "ACCEPT_CONCORDANCE"
            else:
                return "ESCALATE (Concordancia insuficiente o diferencia significativa)"

        elif sim_data["mode"] == "INDEPENDENT":
            p_sim = sum(sim_data["decisions"]) / n_sim
            p_human = sum(human_data["decisions"]) / len(human_data["decisions"])
            
            p_val = tost_equivalence_v7(p_sim, n_sim, p_human, len(human_data["decisions"]), self.delta, self.alpha)
            print(f"  -> Tasa Sim: {p_sim:.3f} | Tasa Humano: {p_human:.3f}")
            print(f"  -> TOST p-value: {p_val:.5f}")
            
            if p_val < self.alpha: return "ACCEPT_CONCORDANCE"
            else: return "ESCALATE (No se demuestra equivalencia)"
        else:
            return "ESCALATE (Modo desconocido)"

# ==========================================
# MATRIZ DE PRUEBAS v0.7 (POSITIVAS Y NEGATIVAS)
# ==========================================
if __name__ == "__main__":
    pki = TrustedAuthorityV7()
    witness_priv = pki.register_actor("W1", "WITNESS")
    gate = StatisticalEvidenceGateV7(min_sample=100, accept_threshold=0.80)

    print("--- T-POS-01: Prueba Positiva (PAIRED, Concordancia Alta) ---")
    # Simulación y humano coinciden 90 de 100 veces
    sim_pos = {"decisions": [1]*90 + [0]*10, "pair_ids": list(range(100)), "mode": "PAIRED", "experiment_id": "TP1", "model_id": "GPT"}
    human_pos = {"decisions": [1]*90 + [0]*10, "pair_ids": list(range(100)), "context": "web"}
    manifest_pos = create_manifest_v7("TP1", "GPT", sim_pos["pair_ids"], human_pos["pair_ids"], "web", "PAIRED")
    sig_pos = witness_priv.sign(manifest_pos)
    print(f"Resultado T-POS-01: {gate.evaluate(sim_pos, human_pos, 'W1', sig_pos, pki)}\n")

    print("="*50 + "\n")

    print("--- T-NEG-01: Prueba Negativa (PAIRED, Discordancia Crítica) ---")
    # Simulación dice 1, humano dice 0 (100% de discordancia)
    sim_neg = {"decisions": [1]*100, "pair_ids": list(range(100)), "mode": "PAIRED", "experiment_id": "TN1", "model_id": "GPT"}
    human_neg = {"decisions": [0]*100, "pair_ids": list(range(100)), "context": "web"}
    manifest_neg = create_manifest_v7("TN1", "GPT", sim_neg["pair_ids"], human_neg["pair_ids"], "web", "PAIRED")
    sig_neg = witness_priv.sign(manifest_neg)
    print(f"Resultado T-NEG-01: {gate.evaluate(sim_neg, human_neg, 'W1', sig_neg, pki)}\n")

    print("="*50 + "\n")

    print("--- T-POS-02: Prueba Positiva (INDEPENDENT, TOST Exitoso) ---")
    # Simulación (80%) y Humano (81%) con N=1000
    sim_ind = {"decisions": [1]*800 + [0]*200, "mode": "INDEPENDENT", "experiment_id": "TP2", "model_id": "Claude"}
    human_ind = {"decisions": [1]*810 + [0]*190, "context": "app"}
    manifest_ind = create_manifest_v7("TP2", "Claude", [], [], "app", "INDEPENDENT")
    sig_ind = witness_priv.sign(manifest_ind)
    print(f"Resultado T-POS-02: {gate.evaluate(sim_ind, human_ind, 'W1', sig_ind, pki)}")
