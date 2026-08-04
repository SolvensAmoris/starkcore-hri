# bench puro VM steps - sin scarb
def vektor_kin(y,m,d):
    a = (14 - m)//12
    y2 = y + 4800 - a
    m2 = m + 12*a - 3
    jdn = d + (153*m2 + 2)//5 + 365*y2 + y2//4 - y2//100 + y2//400 - 32045
    return (jdn - 2447005 + 294) % 260 + 1

import time
s=time.perf_counter()
for _ in range(100000):
    vektor_kin(1990,8,26)
print(f"100k loops: {(time.perf_counter()-s)*1000:.2f} ms -> {(time.perf_counter()-s)/100000*1e6:.2f} us/kin")
