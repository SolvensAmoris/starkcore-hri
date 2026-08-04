import mpmath as mp
mp.mp.dps=50
# 30 primeros gammas (Odlyzko)
gammas=[14.1347251417,21.0220396387,25.0108575801,30.4248761259,32.9350615877,37.5861781588,40.9187190121,43.3270732809,48.0051508811,49.7738324776,52.9703214777,56.4462476971,59.3476040029,60.8317785246,65.1125440480,67.0798105294,69.5464017723,72.0671576744,75.7046906990,77.1448400689,79.3373750202,82.9103808540,84.7354929805,87.4252746131,88.8091112076,92.4918992705,94.6513440405,95.8706342282,98.8311942181,101.3178510057]

def pi_real(n):
    n=int(n); sieve=bytearray(b'\x01')*(n+1); sieve[0:2]=b'\x00\x00'
    import math
    for i in range(2,int(math.isqrt(n))+1):
        if sieve[i]:
            sieve[i*i:n+1:i]=b'\x00'*(((n - i*i)//i)+1)
    return sum(sieve)

def Li(x): return mp.li(x)

gammas_m=[mp.mpf(str(g)) for g in gammas]

for X in [100,1000,10000,100000]:
    pix=pi_real(X)
    lix=Li(X)
    s=mp.mpc(0)
    for g in gammas_m:
        rho=mp.mpc(0.5,g)
        # Riemann's R correction: Li(x^rho) term
        # approx como x^rho/(rho log x) para demo rapida
        # usamos formula simplificada sum x^rho/(rho log x)
        s+= mp.power(X,rho)/(rho*mp.log(X))
        s+= mp.power(X, mp.conj(rho))/(mp.conj(rho)*mp.log(X))
    approx=lix - mp.re(s)
    print(f"x={X:<6} pi={pix:<6} Li={float(lix):8.1f} Li-corr30={float(approx):8.1f} err_Li={float(pix-lix):6.1f} err_30={float(pix-approx):6.1f}")

print("V0.6.1 DONE - 30 ondas")
