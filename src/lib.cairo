pub mod vektor_core;

#[cfg(test)]
mod tests {
    use super::vektor_core::VektorLogic;

    #[test]
    fn test_kin_120_guaymas() {
        let kin = VektorLogic::vektor_kin(1990, 8, 26);
        assert(kin == 120, 'kin!=120');
    }

    #[test]
    fn test_determinista() {
        let k1 = VektorLogic::vektor_kin(1990, 8, 26);
        let k2 = VektorLogic::vektor_kin(1990, 8, 26);
        assert(k1 == k2, 'no determ');
    }

    #[test]
    fn bench_100k() {
        let mut i = 0;
        let mut acc = 0;
        loop {
            if i >= 100000 { break; }
            acc += VektorLogic::vektor_kin(1990, 8, 26);
            i += 1;
        };
        assert(acc == 12000000, 'bench fail');
    }
}
