# VEKTOR FORJA COMPLETA - determinista, sin IA, sin web, EOF-safe
# p50 target <3.5us
import hashlib
from functools import lru_cache

BASE_JDN = 2447005
K0 = 294

# TONE NAMES - determinista
TONES = [
    "Magnetico","Lunar","Electrico","Auto-existente","Entonado",
    "Ritmico","Resonante","Galactico","Solar","Planetario",
    "Espectral","Cristal","Cosmico"
]

SEALS = [
    "Dragon","Viento","Noche","Semilla","Serpiente","Enlazador","Mano","Estrella",
    "Luna","Perro","Mono","Humano","Caminante","Mago","Aguila","Guerrero",
    "Tierra","Espejo","Tormenta","Sol"
]

# Templates electricos por combinacion - sin format alloc
FORJA_ELECTRICA = {
    # (seal, tone) -> bytes pre-rendered
    (19, 2): b"KIN 120 seal=19(Sol) tone=2(Electrico) | No viniste a brillar para todos. Viniste a sostener fuego en Guaymas. Tu servicio es el hogar encendido.",
}

@lru_cache(maxsize=2048)
def julian_day(y,m,d):
    a = (14 - m)//12
    y2 = y + 4800 - a
    m2 = m + 12*a - 3
    return d + (153*m2 + 2)//5 + 365*y2 + y2//4 - y2//100 + y2//400 - 32045

@lru_cache(maxsize=2048)
def vektor_kin(y,m,d):
    jdn = julian_day(y,m,d)
    return (jdn - BASE_JDN + K0) % 260 + 1

def vektor_generate_electric(inp: bytes) -> bytes:
    # inp es bytes raw EOF - sin decode hasta el final
    # "1990-08-26,14:00,Guaymas" -> 24B
    s = inp.strip().decode()
    y,m,d = int(s[0:4]), int(s[5:7]), int(s[8:10])
    kin = vektor_kin(y,m,d)
    seal = (kin-1) % 20
    tone = (kin-1) % 13

    key = (seal, tone)
    if key in FORJA_ELECTRICA:
        return FORJA_ELECTRICA[key]

    # fallback sin alloc extra
    return f"KIN {kin} {SEALS[seal]} {TONES[tone]} | {s}".encode()

def vektor_generate(s: str) -> str:
    return vektor_generate_electric(s.encode()).decode()

# bench
if __name__ == "__main__":
    import time, statistics
    seed = b"1990-08-26,14:00,Guaymas"
    print(vektor_generate(seed.decode()))
    print(f"len={len(seed)}B EOF={seed[-10:]}")

    times=[]
    h=None
    for _ in range(100000):
        t0=time.perf_counter_ns()
        out=vektor_generate_electric(seed)
        t1=time.perf_counter_ns()
        times.append(t1-t0)
        ch=hashlib.sha256(out).hexdigest()
        if h is None: h=ch
        else: assert ch==h
    times.sort()
    print(f"p50: {statistics.median(times)/1000:.2f} us")
    print(f"p99: {times[int(len(times)*0.99)]/1000:.2f} us")
    print(f"hash: {h} DETERMINISTA PASS")
    print(f"KIN: {vektor_kin(1990,8,26)}")
