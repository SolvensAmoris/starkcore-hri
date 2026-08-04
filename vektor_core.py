import hashlib

BASE_JDN = 2447005
K0 = 223

def julian_day(y,m,d):
    a = (14 - m)//12
    y2 = y + 4800 - a
    m2 = m + 12*a - 3
    return d + (153*m2 + 2)//5 + 365*y2 + y2//4 - y2//100 + y2//400 - 32045

def vektor_kin(y,m,d):
    jdn = julian_day(y,m,d)
    diff = jdn - BASE_JDN
    kin = (diff + K0) % 260
    if kin < 0:
        kin += 260
    return kin + 1

def vektor_generate(inp: str) -> str:
    inp = inp.strip()
    date_part = inp.split(",")[0]
    y,m,d = map(int, date_part.split("-"))
    kin = vektor_kin(y,m,d)
    seal = (kin-1) % 20
    tone = (kin-1) % 13
    return f"KIN {kin} seal={seal} tone={tone} | {date_part} Guaymas | No viniste a brillar para todos. Portador de fuego."

if __name__ == "__main__":
    print(vektor_generate("1990-08-26,14:00,Guaymas"))
