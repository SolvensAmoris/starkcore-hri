pub mod VektorLogic {
    pub const BASE_JDN: u32 = 2447005;
    pub const K0: u32 = 294;

    pub fn julian_day(y: u32, m: u32, d: u32) -> u32 {
        let a = (14 - m) / 12;
        let y2 = y + 4800 - a;
        let m2 = m + 12 * a - 3;
        d + (153 * m2 + 2) / 5 + 365 * y2 + y2 / 4 - y2 / 100 + y2 / 400 - 32045
    }
    pub fn vektor_kin(y: u32, m: u32, d: u32) -> u32 {
        (julian_day(y,m,d) - BASE_JDN + K0) % 260 + 1
    }
    pub fn vektor_seal(kin: u32) -> u32 { (kin - 1) % 20 }
    pub fn vektor_tone(kin: u32) -> u32 { (kin - 1) % 13 }
}
