import random, math
random.seed(42)
N=100 # eventos
STEPS=120

# Estado: cada evento tiene energia 0-1
state=[random.random() for _ in range(N)]
# Log real de quien influyo a quien (verdad oculta)
causal_log=[] # (cause, effect, time)

for t in range(STEPS):
    # elige un evento activo si energia > 0.5
    active=[i for i,s in enumerate(state) if s>0.6]
    if not active:
        state[random.randrange(N)]=random.random()
        continue
    a=random.choice(active)
    # a intenta modificar a vecinos aleatorios
    for _ in range(3):
        b=random.randrange(N)
        if a==b: continue
        before=state[b]
        # regla: a transfiere energia
        delta = (state[a]-0.5)*0.2 + random.uniform(-0.05,0.05)
        state[b]=max(0,min(1,state[b]+delta))
        # si cambio significativo, registra causa
        if abs(state[b]-before)>0.08:
            causal_log.append((a,b,t,state[b]-before))

print(f"ET v1.0 CAUSALIDAD - {len(causal_log)} influencias reales")
# Ahora BORRAMOS reglas y log. Solo queda serie temporal de estados
# Reconstruccion: C(A,B)=P(B sube | A activo antes) - P(B sube)

# reconstruimos serie temporal (guardamos historia)
# para demo simple, re-ejecutamos con historial
random.seed(42)
state=[random.random() for _ in range(N)]
history=[list(state)]
for t in range(STEPS):
    active=[i for i,s in enumerate(state) if s>0.6]
    if not active:
        state[random.randrange(N)]=random.random()
    else:
        a=random.choice(active)
        for _ in range(3):
            b=random.randrange(N)
            if a==b: continue
            delta=(state[a]-0.5)*0.2 + random.uniform(-0.05,0.05)
            state[b]=max(0,min(1,state[b]+delta))
    history.append(list(state))

# Calcula C(A,B)
C=[[0]*N for _ in range(N)]
for A in range(N):
    for B in range(N):
        if A==B: continue
        # P(B sube)
        ups=0; total=0
        ups_given_A=0; total_given_A=0
        for t in range(STEPS-1):
            total+=1
            if history[t+1][B] - history[t][B] > 0.05:
                ups+=1
            if history[t][A] > 0.6: # A activo
                total_given_A+=1
                if history[t+1][B] - history[t][B] > 0.05:
                    ups_given_A+=1
        pB = ups/(total+1e-9)
        pB_given_A = ups_given_A/(total_given_A+1e-9) if total_given_A>0 else pB
        C[A][B]=pB_given_A - pB

# Top causas detectadas vs reales
real_pairs=set((a,b) for a,b,_,_ in causal_log)
detected=sorted([(C[a][b],a,b) for a in range(N) for b in range(N) if a!=b], reverse=True)[:100]
hits=sum(1 for _,a,b in detected if (a,b) in real_pairs)
print(f"Top 100 aristas causales detectadas por C(A,B): {hits} aciertos reales ({hits}%)")
print(f"Azar esperaria: {len(real_pairs)/(N*N)*100:.1f}%")

# Flecha del tiempo: ¿C es asimetrica?
asym=sum(1 for a in range(N) for b in range(N) if a!=b and C[a][b]>0.1 and C[b][a]<0.02)
sym=sum(1 for a in range(N) for b in range(N) if a!=b and C[a][b]>0.1 and C[b][a]>0.1)
print(f"Asimetria causal: {asym} pares A->B sin B->A, {sym} simetricos")
if asym>sym*2:
    print("-> FLECHA EMERGIO: causalidad es dirigida, no correlacion")
else:
    print("-> no hay flecha clara")

# Entropia temporal
diffs=[]
for t in range(STEPS):
    diffs.append(sum(abs(history[t][i]-history[t-1][i]) if t>0 else 0 for i in range(N))/N)
trend = sum(1 for i in range(1,len(diffs)) if diffs[i]<diffs[i-1])
print(f"Dinamica: tendencia a estabilizar? {trend}/{len(diffs)} pasos decreciendo energia")

print("\nV1.0 DONE - historia, no geometria")
