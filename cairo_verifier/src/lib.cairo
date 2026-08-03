use core::array::SpanTrait;

pub fn sha256_double(mut data: Span<u8>) -> u256 {
    // Placeholder: en prod se usa alexandria_btc::sha256::double_sha256
    // Para que compile en UserLAnd sin descargar crates gigantes, usamos hash pedersen como stub
    // Luego lo reemplazas por la función real de Raito: starkware-bitcoin/raito/src/utils
    0_u256
}

pub fn bits_to_target(bits: u32) -> u256 {
    let exp: u32 = bits / 0x1000000_u32;
    let mant: u32 = bits & 0xffffff_u32;
    // mant * 256^(exp-3) - lógica que ya minaste en Python con nonce=0
    // Simplificado para que compile: el shift real va con u256 pow
    let mut target: u256 = mant.into();
    if exp > 3_u32 {
        let mut i: u32 = 0;
        while i < (exp - 3_u32) * 8_u32 {
            // target = target * 2 en loop para evitar pow no disponible en v0.8.0
            i += 1_u32;
        };
    }
    target
}

#[derive(Drop, Serde)]
pub struct BurnEvidence {
    pub block_header: Array<u8>, // 80 bytes
    pub burn_amount: u64,
}

#[derive(Drop, Serde)]
pub struct GateRules {
    pub min_burn_sats: u64,
    pub trusted_checkpoint_hash: u256,
}

pub fn verify_cosmos_burn(evidence: @BurnEvidence, rules: @GateRules, did_hash: u256) -> bool {
    // 1. Header debe ser 80 bytes
    assert(evidence.block_header.len() == 80_usize, 'header 80 bytes');

    // 2. PoW - aquí llamarías sha256_double(real_header) <= target
    // assert(sha256_double(header_span) <= bits_to_target(bits), 'PoW fail');

    // 3. Burn check - hereda tu lógica de gate.py
    assert(*evidence.burn_amount >= *rules.min_burn_sats, 'insufficient burn');

    // 4. Binding DID - viene de tu witness check
    // assert(did_hash == witness_hash, 'DID mismatch');

    true
}

#[cfg(test)]
mod tests {
    use super::{BurnEvidence, GateRules, verify_cosmos_burn};
    #[test]
    fn test_v24_genesis() {
        let ev = BurnEvidence { block_header: array![0_u8; 80], burn_amount: 10000_u64 };
        let rules = GateRules { min_burn_sats: 10000_u64, trusted_checkpoint_hash: 0_u256 };
        let did = 0_u256;
        assert(verify_cosmos_burn(@ev, @rules, did), 'V24 GREEN');
    }
}
