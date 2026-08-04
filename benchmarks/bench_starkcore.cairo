use vektor_core::VektorCore::vektor_kin;

fn main() -> u32 {
    let mut total = 0;
    let mut i = 0;
    loop {
        if i >= 100000 { break; }
        total += vektor_kin(1990, 8, 26);
        i += 1;
    };
    total
}
