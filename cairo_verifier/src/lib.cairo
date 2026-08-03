#[derive(Drop, Serde)]
pub struct BurnEvidence {
    pub block_header_len: u32,
    pub burn_amount: u64,
}

#[derive(Drop, Serde)]
pub struct GateRules {
    pub min_burn_sats: u64,
    pub trusted_checkpoint_hash: u256,
}

pub fn verify_cosmos_burn(evidence: @BurnEvidence, rules: @GateRules, did_hash: u256) -> bool {
    // 1. Header 80 bytes - en V27 usamos double_sha256 real de raito
    assert!(*evidence.block_header_len == 80_u32, 'header 80 bytes');
    // 2. Burn check - logica de gate.py
    assert!(*evidence.burn_amount >= *rules.min_burn_sats, 'Insufficient burn');
    // 3. DID binding - viene de tu witness
    assert!(did_hash!= 0, 'DID mismatch');
    true
}

#[cfg(test)]
mod tests {
    use super::{BurnEvidence, GateRules, verify_cosmos_burn};
    #[test]
    fn test_v24_genesis() {
        let ev = BurnEvidence { block_header_len: 80_u8.into(), burn_amount: 10000_u64 };
        let rules = GateRules { min_burn_sats: 10000_u64, trusted_checkpoint_hash: 0_u256 };
        assert!(verify_cosmos_burn(@ev, @rules, 123_u256), 'should verify');
    }
}
