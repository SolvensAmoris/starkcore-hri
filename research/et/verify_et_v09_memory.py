import random, math, collections
random.seed(11)
N=80

def make_G0(seed):
    random.seed(seed)
    edges=set()
    while len(edges)<N*2:
        a=random.randrange(N); b=random.randrange(N)
        if a!=b: edges.add((min(a,b),max(a,b)))
    return list(edges)

def evolve(edges, steps=80):
    edges=list(edges)
    for _ in range(steps):
        adj={i:set() for i in range(N)}
        for a,b in edges: adj[a].add(b); adj[b].add(a)
        new=set(edges)
        # breath v0.8 rules
        for i in range(N):
            neigh=list(adj[i])
            if len(neigh)>=2:
                for _ in range(2):
                    a,b=random.sample(neigh,2)
                    if (min(a,b),max(a,b)) in new: continue
                    if len(adj[a]&adj[b])==1 and random.random()<0.08:
                        new.add((min(a,b),max(a,b)))
        for a,b in list(new):
            if len(adj[a]&adj[b])>3 and random.random()<0.5:
                new.discard((a,b))
        adj2={i:set() for i in range(N)}
        for a,b in new: adj2[a].add(b); adj2[b].add(a)
        for i in range(N):
            while len(adj2[i])>8:
                worst=min(adj2[i], key=lambda nb: len(adj2[i]&adj2[nb]))
                new.discard((min(i,worst),max(i,worst)))
                adj2[i].discard(worst); adj2[worst].discard(i)
        if random.random()<0.3:
            a=random.randrange(N); b=random.randrange(N)
            if a!=b: new.add((min(a,b),max(a,b)))
        edges=list(new)
    return edges

def jaccard(a,b):
    sa=set(a); sb=set(b)
    inter=len(sa&sb); union=len(sa|sb)
    return inter/(union+1e-9)

def overlap_communities(edges):
    # vector de comunidad via label propagation 5 iter
    adj={i:set() for i in range(N)}
    for a,b in edges: adj[a].add(b); adj[b].add(a)
    label=list(range(N))
    for _ in range(5):
        for i in range(N):
            if not adj[i]: continue
            vals=[label[n] for n in adj[i]]
            label[i]=collections.Counter(vals).most_common(1)[0][0]
    return label

print("ET v0.9 - MEMORIA DE ORIGEN")
G0 = make_G0(100)
Gt = evolve(G0, 80)

# 1) memoria directa aristas
jac_direct = jaccard(G0, Gt)
print(f"G0 {len(G0)} edges -> Gt {len(Gt)} edges")
print(f"Jaccard aristas G0 vs Gt: {jac_direct:.3f}")

# control: Gt random con mismo M
random.seed(999)
Gr=set()
while len(Gr)<len(Gt):
    a=random.randrange(N); b=random.randrange(N)
    if a!=b: Gr.add((min(a,b),max(a,b)))
jac_rand = jaccard(G0, Gr)
print(f"Jaccard G0 vs Random: {jac_rand:.3f}")

# 2) memoria comunitaria: ¿barrios de G0 sobreviven?
lab0=overlap_communities(G0)
labt=overlap_communities(Gt)
# Adjusted Rand proxy simple: pares que quedan juntos
same0=0; sameT=0; both=0; tot=0
for i in range(N):
    for j in range(i+1,N):
        tot+=1
        s0=1 if lab0[i]==lab0[j] else 0
        st=1 if labt[i]==labt[j] else 0
        if s0: same0+=1
        if st: sameT+=1
        if s0 and st: both+=1
# precision de memoria comunitaria
prec = both/(sameT+1e-9)
rec = both/(same0+1e-9)
print(f"Memoria comunidades: precision {prec:.3f} recall {rec:.3f} (pares que siguen juntos)")

# 3) I(G0;Gt) proxy via reconstruccion: entrena predictor simple de arista
# usa common neighbors en Gt para predecir si arista estaba en G0
adjT={i:set() for i in range(N)}
for a,b in Gt: adjT[a].add(b); adjT[b].add(a)
setG0=set(G0)
correct=0; total=1000
random.seed(1)
for _ in range(total):
    # 50% arista real de G0, 50% no
    if random.random()<0.5:
        a,b=random.choice(G0); label=1
    else:
        while True:
            a=random.randrange(N); b=random.randrange(N)
            if a!=b and (min(a,b),max(a,b)) not in setG0:
                break
        label=0
    score=len(adjT[a]&adjT[b])
    pred=1 if score>=2 else 0
    if pred==label: correct+=1
acc=correct/total
print(f"Reconstruccion G0 desde Gt via CN: acc {acc:.3f} (0.5=azar)")

if jac_direct>jac_rand+0.05 and acc>0.6:
    print("\n-> MEMORIA EMERGENTE: Gt recuerda G0 mas que azar")
elif prec>0.3:
    print("\n-> MEMORIA DE BARRIOS: no recuerda aristas, pero si estructura")
else:
    print("\n-> OLVIDO: evolucion borro origen")

print("\nV0.9 DONE - esto ya es identidad, no solo geometria")
