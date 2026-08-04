import mpmath as mp
mp.mp.dps=50
# tus 5 ceros verificados
gammas=[mp.mpf('14.134725141734693'), mp.mpf('21.02203963877155'), mp.mpf('25.010857580145688'), mp.mpf('30.424876125859513'), mp.mpf('32.93506158773919')]

def pi_real(x):
    # pi(x) conteo primos simple
    n=int(x)
    sieve=[True]*(n+1)
    sieve[0]=sieve[1]=False
    for i in range(2,int(n**0.5)+1):
        if sieve[i]:
            step=i; start=i*i
            sieve[start:n+1:step]=[False]*(((n-start)//step)+1)
    return sum(sieve)

def Li(x):
    return mp.li(x)

def explicit_correction(x):
    # suma x^rho / rho aproximada: x^{0.5+i g} / rho
    s=mp.mpc(0)
    for g in gammas:
        rho=mp.mpc(0.5,g)
        s+= mp.power(x,rho)/rho
        s+= mp.power(x, mp.conj(rho))/mp.conj(rho) # par conjugado
    return s

for X in [100, 1000, 10000]:
    pix=pi_real(X)
    lix=Li(X)
    corr=explicit_correction(X)
    # psi ~ pero para pi(x) aprox Li - Re(corr)/log x simplificado
    approx = lix - (mp.re(corr)/mp.log(X))
    print(f"x={X} pi_real={pix} Li={float(lix):.2f} Li-corr={float(approx):.2f} error_Li={float(pix-lix):.2f} error_corr={float(pix-approx):.2f}")

print("V0.6 DONE - ondas visibles")
