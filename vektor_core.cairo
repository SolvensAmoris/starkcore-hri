#[starknet::contract]
mod VektorCore {
    const BASE_JDN: u32 = 2447005;
    const K0: u32 = 294; // para que 1990-08-26 = KIN 120

    fn julian_day(y: u32, m: u32, d: u32) -> u32 {
        let a = (14 - m) / 12;
        let y2 = y + 4800 - a;
        let m2 = m + 12 * a - 3;
        d + (153 * m2 + 2) / 5 + 365 * y2 + y2 / 4 - y2 / 100 + y2 / 400 - 32045
    }

    #[external(v0)]
    fn vektor_kin(self: @ContractState, y: u32, m: u32, d: u32) -> u32 {
        let jdn = Self::julian_day(y, m, d);
        let diff = jdn - Self::BASE_JDN;
        let kin = (diff + Self::K0) % 260 + 1
    }

    #[external(v0)]
    fn vektor_generate(self: @ContractState, y: u32, m: u32, d: u32) -> u32 {
        Self::vektor_kin(y,m,d) // determinista, no alloc
    }
}
