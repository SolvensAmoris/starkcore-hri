import datetime
import math

def calcular_equinoccio_marzo(ano: int) -> datetime.datetime:
    """
    Calcula el equinoccio de marzo (Punto 0 del Universo).
    Algoritmo de Meeus simplificado, error <10min para 1900-2100.
    """
    y = (ano - 2000) / 1000
    jd = 2451623.80984 + 365242.37404*y + 0.05169*y**2 - 0.00411*y**3 - 0.00057*y**4
    
    jd += 0.5
    z = int(jd)
    f = jd - z
    a = z
    if z >= 2299161:
        alpha = int((z - 1867216.25)/36524.25)
        a = z + 1 + alpha - alpha//4
    b = a + 1524
    c = int((b - 122.1)/365.25)
    d = int(365.25*c)
    e = int((b - d)/30.6001)
    day = b - d - int(30.6001*e) + f
    month = e - 1 if e < 14 else e - 13
    year = c - 4716 if month > 2 else c - 4715
    
    base = datetime.datetime(year, month, int(day), tzinfo=datetime.timezone.utc)
    return base + datetime.timedelta(days=day-int(day))

def calcular_longitud_ecliptica_sol(fecha_utc: datetime.datetime, equinoccio: datetime.datetime) -> float:
    """
    Posición del Sol en la eclíptica 0-360° con corrección elíptica.
    """
    d = (fecha_utc - equinoccio).total_seconds() / 86400.0
    L_mean = (d * 360.0 / 365.24219) % 360.0
    g = math.radians((357.529 + 0.98560028 * d) % 360)
    correccion = 1.915 * math.sin(g) + 0.020 * math.sin(2*g)
    return (L_mean + correccion) % 360.0

LIMITES_13 = [
    ("Piscis", 0, 29, "El Místico Infinito"),
    ("Aries", 29, 53, "El Iniciador de Fuego"),
    ("Tauro", 53, 90, "El Ancla de la Tierra"),
    ("Géminis", 90, 118, "Los Espejos de la Mente"),
    ("Cáncer", 118, 138, "El Protector del Origen"),
    ("Leo", 138, 174, "El Rey Sol Extrovertido"),
    ("Virgo", 174, 218, "El Alquimista del Orden"),
    ("Libra", 218, 241, "El Eje del Equilibrio"),
    ("Escorpio", 241, 248, "El Transformador Profundo"),
    ("Ofiuco", 248, 266, "El Sanador Alquimista (La Serpiente)"),
    ("Sagitario", 266, 300, "El Buscador del Horizonte"),
    ("Capricornio", 300, 328, "El Arquitecto del Tiempo"),
    ("Acuario", 328, 352, "El Visionario de la Red"),
    ("Piscis", 352, 360, "El Místico Infinito"),
]

def obtener_constelacion_13(longitud_ecliptica: float):
    for nombre, mn, mx, arq in LIMITES_13:
        if mn <= longitud_ecliptica < mx:
            return nombre, arq
    return "Piscis", "El Místico Infinito"

def transformar_a_calendario_universo(fecha_nacimiento_utc: datetime.datetime):
    """
    Transforma fecha gregoriana a calendario del universo:
    13 meses de 28 días = 364 + 1 Día Fuera del Tiempo (equinoccio).
    S(d) = Hash(Canonical(d))
    """
    ano = fecha_nacimiento_utc.year
    equinoccio = calcular_equinoccio_marzo(ano)

    if fecha_nacimiento_utc < equinoccio:
        equinoccio = calcular_equinoccio_marzo(ano-1)
        ano_universo = ano - 1
    else:
        ano_universo = ano

    delta = fecha_nacimiento_utc - equinoccio
    dias = delta.days

    if dias == 0:
        return {
            "ano_universo": ano_universo,
            "mes": 0,
            "dia": 0,
            "nombre": "Día Fuera del Tiempo - Año Nuevo Universal",
            "longitud_ecliptica": 0.0,
            "constelacion_real": "Piscis",
            "arquetipo": "El Místico Infinito",
            "hash_canonico": f"{ano_universo:04d}-00-00:RESET"
        }
    
    mes_universo = (dias - 1) // 28 + 1
    dia_universo = (dias - 1) % 28 + 1

    long_sol = calcular_longitud_ecliptica_sol(fecha_nacimiento_utc, equinoccio)
    signo, arquetipo = obtener_constelacion_13(long_sol)

    return {
        "ano_universo": ano_universo,
        "mes": mes_universo,
        "dia": dia_universo,
        "longitud_ecliptica": round(long_sol, 2),
        "constelacion_real": signo,
        "arquetipo": arquetipo,
        "hash_canonico": f"{ano_universo:04d}-{mes_universo:02d}-{dia_universo:02d}:{signo}"
    }

# --- TEST RAPIDO ---
if __name__ == "__main__":
    ahora = datetime.datetime.now(datetime.timezone.utc)
    print(transformar_a_calendario_universo(ahora))
