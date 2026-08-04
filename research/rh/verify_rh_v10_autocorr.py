import math, random, statistics
gammas=[14.1347251417,21.0220396387,25.0108575801,30.4248761259,32.9350615877,37.5861781588,40.9187190121,43.3270732809,48.0051508811,49.7738324776,52.9703214777,56.4462476971,59.3476040029,60.8317785246,65.1125440480,67.0798105294,69.5464017723,72.0671576744,75.7046906990,77.1448400689,79.3373750202,82.9103808540,84.7354929805,87.4252746131,88.8091112076,92.4918992705,94.6513440405,95.8706342282,98.8311942181,101.3178510057,103.7255380404,105.4466230523,107.1686111843,111.0295355432,114.3202209151,116.2266803208,118.3297729815,121.4126923629,122.9468292937,124.2568185543,127.5166838796,129.5787041999,131.0876885301,133.4977372020,134.7565097536,138.1160420555,139.7362089521,141.1237074040,143.1118458076,146.0009824860]

# normalizados
sn=[]
for i in range(len(gammas)-1):
    d=gammas[i+1]-gammas[i]
    sn.append(d*math.log(gammas[i]/(2*math.pi))/(2*math.pi))

mean_s=statistics.mean(sn)

def autocorr(s,k):
    n=len(s)
    if k>=n: return 0
    m=mean_s
    num=sum((s[i]-m)*(s[i+k]-m) for i in range(n-k))
    den=sum((x-m)**2 for x in s)
    return num/den if den!=0 else 0

print(f"N=50 mean_s={mean_s:.3f}\nAutocorrelacion C(k):")
for k in range(1,6):
    print(f" C({k})={autocorr(sn,k):+.3f}")

# vs Poisson fake con misma media
random.seed(0)
poisson=[random.expovariate(1.0) for _ in sn] # mean 1
print(f"\nPoisson fake C(1)={autocorr(poisson,1):+.3f} (debe ~0)")

print("\nInterpretacion:")
print("C(1) negativo ~ -0.2/-0.3 => anticorrelacion = firma caotica")
print("C(1) ~ 0 => gaps independientes = Poisson")
print("\nV0.10 DONE - memoria del espectro")
