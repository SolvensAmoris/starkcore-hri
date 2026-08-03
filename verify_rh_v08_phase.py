import mpmath as mp, math, random
mp.mp.dps=40
gammas_all=[14.1347251417,21.0220396387,25.0108575801,30.4248761259,32.9350615877,37.5861781588,40.9187190121,43.3270732809,48.0051508811,49.7738324776,52.9703214777,56.4462476971,59.3476040029,60.8317785246,65.1125440480,67.0798105294,69.5464017723,72.0671576744,75.7046906990,77.1448400689,79.3373750202,82.9103808540,84.7354929805,87.4252746131,88.8091112076,92.4918992705,94.6513440405,95.8706342282,98.8311942181,101.3178510057,103.7255380404,105.4466230523,107.1686111843,111.0295355432,114.3202209151,116.2266803208,118.3297729815,121.4126923629,122.9468292937,124.2568185543,127.5166838796,129.5787041999,131.0876885301,133.4977372020,134.7565097536,138.1160420555,139.7362089521,141.1237074040,143.1118458076,146.0009824860]

def psi_real(x):
    n=int(x); is_prime=bytearray(b'\x01')*(n+1); is_prime[0:2]=b'\x00\x00'
    for i in range(2,int(math.isqrt(n))+1):
        if is_prime[i]: is_prime[i*i:n+1:i]=b'\x00'*(((n-i*i)//i)+1)
    s=0.0
    for p in range(2,n+1):
        if is_prime[p]:
            pk=p; lp=math.log(p)
            while pk<=n: s+=lp; pk*=p
    return s

def psi_approx(x, gammas):
    corr=mp.mpc(0)
    for g in gammas:
        rho=mp.mpc(0.5, mp.mpf(str(g)))
        corr+= mp.power(x,rho)/rho + mp.power(x, mp.conj(rho))/mp.conj(rho)
    return float(mp.re(x - corr - mp.log(2*mp.pi)))

X=10000
pr=psi_real(X)
print(f"X={X} psi_real={pr:.2f}\n")

# 1) primeros 10 exactos
g10=gammas_all[:10]
print(f"EXACTOS 10 primeros: err={pr-psi_approx(X,g10):.2f}")

# 2) 10 aleatorios entre primeros 50
random.seed(42)
g_rand=random.sample(gammas_all[:50],10)
print(f"RANDOM 10 de 50: err={pr-psi_approx(X,g_rand):.2f}")

# 3) 10 altos (40-50)
g_high=gammas_all[40:50]
print(f"ALTOS 10 (40-50): err={pr-psi_approx(X,g_high):.2f}")

# 4) ruido: mismas magnitudes pero fase random +5
g_shifted=[g+5*random.uniform(-1,1) for g in g10]
print(f"RUIDO shift ±5: err={pr-psi_approx(X,g_shifted):.2f}")

print("\nV0.8 DONE - si la posicion importa, exactos debe ganar")
