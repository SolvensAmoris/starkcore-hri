import mpmath as mp
mp.mp.dps=50
gammas=[14.1347251417,21.0220396387,25.0108575801,30.4248761259,32.9350615877,37.5861781588,40.9187190121,43.3270732809,48.0051508811,49.7738324776,52.9703214777,56.4462476971,59.3476040029,60.8317785246,65.1125440480,67.0798105294,69.5464017723,72.0671576744,75.7046906990,77.1448400689,79.3373750202,82.9103808540,84.7354929805,87.4252746131,88.8091112076,92.4918992705,94.6513440405,95.8706342282,98.8311942181,101.3178510057]
gammas_m=[mp.mpf(str(g)) for g in gammas]

def pi_real(n):
    n=int(n); s=bytearray(b'\x01')*(n+1); s[0:2]=b'\x00\x00'
    import math
    for i in range(2,int(math.isqrt(n))+1):
        if s[i]: s[i*i:n+1:i]=b'\x00'*(((n-i*i)//i)+1)
    return sum(s)

for X in [100,1000,10000]:
    pix=pi_real(X)
    # Li(x) real
    lix=mp.li(X)
    # suma Li(x^rho) real con 30 ceros
    corr=mp.mpc(0)
    for g in gammas_m:
        rho=mp.mpc(0.5,g)
        z=mp.power(X,rho)
        # Li(z) complejo - mpmath lo hace
        corr+= mp.li(z)
        corr+= mp.li(mp.conj(z))
    approx = lix - mp.re(corr)
    # Riemann R es mejor que Li, pero probemos Li-corr directo
    print(f"x={X} pi={pix} Li={float(lix):.2f} Li - ΣLi(x^rho) = {float(approx):.2f}")
print("V0.6.2 DONE")
