import mpmath as mp
mp.mp.dps=50
gammas=[14.1347251417,21.0220396387,25.0108575801,30.4248761259,32.9350615877,37.5861781588,40.9187190121,43.3270732809,48.0051508811,49.7738324776,52.9703214777,56.4462476971,59.3476040029,60.8317785246,65.1125440480,67.0798105294,69.5464017723,72.0671576744,75.7046906990,77.1448400689,79.3373750202,82.9103808540,84.7354929805,87.4252746131,88.8091112076,92.4918992705,94.6513440405,95.8706342282,98.8311942181,101.3178510057]
gammas_m=[mp.mpc(0.5, mp.mpf(str(g))) for g in gammas]

def psi_real(x):
    x=int(x)
    # criba primos y suma log p^k <= x
    import math
    n=x
    is_prime=bytearray(b'\x01')*(n+1); is_prime[0:2]=b'\x00\x00'
    for i in range(2,int(math.isqrt(n))+1):
        if is_prime[i]: is_prime[i*i:n+1:i]=b'\x00'*(((n-i*i)//i)+1)
    primes=[i for i, v in enumerate(is_prime) if v]
    s=0.0
    for p in primes:
        pk=p
        while pk <= x:
            s+= math.log(p)
            pk*=p
    return s

for X in [100,1000,10000]:
    psi_r=psi_real(X)
    corr=mp.mpc(0)
    for rho in gammas_m:
        corr+= mp.power(X,rho)/rho
        corr+= mp.power(X, mp.conj(rho))/mp.conj(rho)
    psi_approx = X - mp.re(corr) - mp.log(2*mp.pi)
    print(f"x={X} psi_real={psi_r:.2f} psi_aprox_30={float(psi_approx):.2f} error={float(psi_r-psi_approx):.2f}")

print("V0.6.3 DONE - aqui si se ve la musica de Riemann")
