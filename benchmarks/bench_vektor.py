import time, statistics, hashlib
from vektor_core import vektor_generate

def bench_eof(file="seed.txt", iters=100000):
    data = open(file, 'rb').read()
    print(f"input tail: {data[-20:]} len={len(data)}B EOF raw")
    times = []
    h = None
    s = data.decode().strip()
    for _ in range(iters):
        t0 = time.perf_counter_ns()
        out = vektor_generate(s)
        t1 = time.perf_counter_ns()
        times.append(t1-t0)
        cur_h = hashlib.sha256(out.encode()).hexdigest()
        if h is None:
            h = cur_h
        else:
            assert cur_h == h
    times.sort()
    print(f"p50: {statistics.median(times)/1000:.2f} us")
    print(f"p99: {times[int(len(times)*0.99)]/1000:.2f} us")
    print(f"hash: {h} DETERMINISTA PASS")
    print(f"sample: {out}")

bench_eof()
