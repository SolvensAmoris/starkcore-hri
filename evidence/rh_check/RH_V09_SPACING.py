import math, statistics
gammas=[14.1347251417,21.0220396387,25.0108575801,30.4248761259,32.9350615877,37.5861781588,40.9187190121,43.3270732809,48.0051508811,49.7738324776,52.9703214777,56.4462476971,59.3476040029,60.8317785246,65.1125440480,67.0798105294,69.5464017723,72.0671576744,75.7046906990,77.1448400689,79.3373750202,82.9103808540,84.7354929805,87.4252746131,88.8091112076,92.4918992705,94.6513440405,95.8706342282,98.8311942181,101.3178510057,103.7255380404,105.4466230523,107.1686111843,111.0295355432,114.3202209151,116.2266803208,118.3297729815,121.4126923629,122.9468292937,124.2568185543,127.5166838796,129.5787041999,131.0876885301,133.4977372020,134.7565097536,138.1160420555,139.7362089521,141.1237074040,143.1118458076,146.0009824860]

deltas=[gammas[i+1]-gammas[i] for i in range(len(gammas)-1)]

# normalizacion Montgomery-Odlyzko: s_n = delta_n * log(gamma_n/2pi)/(2pi)
sn=[]
for i, d in enumerate(deltas):
    g=gammas[i]
    mean_density = math.log(g/(2*math.pi))/(2*math.pi)
    sn.append(d*mean_density)

print(f"N={len(gammas)} spacings={len(sn)}")
print(f"mean raw delta={statistics.mean(deltas):.3f} var={statistics.variance(deltas):.3f}")
print(f"mean normalized s={statistics.mean(sn):.3f} (debe ~1.0 si normalizado)")
print(f"min s={min(sn):.3f} max s={max(sn):.3f}")

# repulsión: cuenta cuantos s < 0.2 (cerca de 0)
close = sum(1 for s in sn if s < 0.2)
print(f"\ns < 0.2 (niveles casi pegados): {close}/{len(sn)} = {close/len(sn):.1%}")
print("Si fueran Poisson aleatorio, esperarías ~18% aqui.")
print("Si es GUE/GOE caotico, esperas ~2-3% (repulsion)")

# histograma ASCII 0-3 en 10 bins
bins=[0]*10
for s in sn:
    if s<3.0: bins[int(s/0.3)]+=1
print("\nHistograma s_n (0-3.0):")
for i,c in enumerate(bins):
    print(f"{i*0.3:.1f}-{(i+1)*0.3:.1f} | {'#'*c} ({c})")

print("\nV0.9 DONE - spacing signature")
