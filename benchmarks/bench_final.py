import time, statistics
def vektor_kin(y,m,d):
    a=(14-m)//12
    y2=y+4800-a
    m2=m+12*a-3
    jdn=d+(153*m2+2)//5+365*y2+y2//4-y2//100+y2//400-32045
    return (jdn-2447005+294)%260+1

times=[]
for _ in range(100000):
    t0=time.perf_counter_ns()
    vektor_kin(1990,8,26)
    times.append(time.perf_counter_ns()-t0)
times.sort()
print(f"p50: {statistics.median(times)/1000:.2f} us")
print(f"p99: {times[int(len(times)*0.99)]/1000:.2f} us")
