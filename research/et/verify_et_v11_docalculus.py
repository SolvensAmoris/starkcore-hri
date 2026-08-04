import random
random.seed(1)
N=60
STEPS=60

def run_world(blocked=None, seed=0):
    random.seed(seed)
    state=[random.random() for _ in range(N)]
    hist=[list(state)]
    for t in range(STEPS):
        active=[i for i,s in enumerate(state) if s>0.6 and i!=blocked]
        if active:
            a=random.choice(active)
            for _ in range(2):
                b=random.randrange(N)
                if b==blocked or a==b: continue
                delta=(state[a]-0.5)*0.25 + random.uniform(-0.03,0.03)
                state[b]=max(0,min(1,state[b]+delta))
        # decaimiento natural
        for i in range(N):
            if i!=blocked: state[i]*=0.995
        hist.append(list(state))
    return hist

# Mundo base
base=run_world(blocked=None, seed=123)

# Para cada posible causa A, mide impacto causal: do(A) vs do(not A)
# impacto = distancia de futuros
causal_power=[]
for A in range(N):
    real=run_world(blocked=None, seed=123) # do(A)
    fake=run_world(blocked=A, seed=123) # do(no A)
    # distancia L1 entre futuros despues de t=10
    dist=0
    for t in range(10,STEPS):
        dist+=sum(abs(real[t][i]-fake[t][i]) for i in range(N))/N
    causal_power.append((dist,A))

causal_power.sort(reverse=True)
print("ET v1.1 DO-CALCULUS - Poder causal por intervencion")
for dist,A in causal_power[:15]:
    print(f" Nodo {A:2d} poder={dist:.3f}")

# ¿Hay agentes reales vs ruido?
top_dist=causal_power[0][0]
mid_dist=causal_power[N//2][0]
ratio=top_dist/(mid_dist+1e-9)
print(f"\nRatio top/medio = {ratio:.2f}")
if ratio>2.5:
    print("-> AGENCIA EMERGIO: algunos eventos cambian el futuro mucho mas que otros")
else:
    print("-> todo es ruido, no hay agencia")

# Flecha + memoria
# Si bloqueo un hub causal, ¿colapsa mas?
blocked_top=causal_power[0][1]
h_top=run_world(blocked=blocked_top, seed=123)
h_rand=run_world(blocked=random.randrange(N), seed=123)
energy_top=sum(sum(row) for row in h_top)/len(h_top)
energy_rand=sum(sum(row) for row in h_rand)/len(h_rand)
print(f"\nEnergia media futuro sin top causal {blocked_top}: {energy_top:.2f}")
print(f"Energia media futuro sin random: {energy_rand:.2f}")
print(f"Delta = {energy_rand-energy_top:.2f} -> {'nodo critico' if abs(energy_rand-energy_top)>1 else 'no critico'}")

print("\nV1.1 DONE - causa = lo que cambia el universo cuando lo quitas")
