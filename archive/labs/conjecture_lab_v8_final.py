#!/usr/bin/env python3
import math, random, itertools
from collections import defaultdict
import numpy as np

def eval_safe(e,n):
    try: return bool(eval(e, {"n":n,"math":math,"__builtins__":{}}))
    except: return False

def fails_of(f,domain): return set(n for n in domain if not eval_safe(f,n))

def kmin_of(f,domain):
    for k in range(0,50):
        if not any(n>k and not eval_safe(f,n) for n in domain): return k
    return 50

def niche_of(f):
    if "2**n" in f or "3**n" in f: return "🚀 EXP vs POLY"
    if "2*n" in f or f.startswith("n <"): return "📈 LINEAL vs POLY"
    return "🌱 POLY vs POLY"

def interest(f,fails,k):
    s=len(fails)
    score=0.5
    if s>0 and s<5: score+=0.4
    if k<5: score+=0.3
    if "2**n" in f: score+=0.3
    if "+1" in f or "+2" in f: score-=0.3
    if fails==set(): score-=0.2
    return max(0,score)

def landscape_bar(fails,domain_max=20):
    bar=""
    for n in range(1,domain_max+1):
        bar+="█" if n in fails else "░"
    return bar

# MUTACIONES BASE - el sistema aprenderá cuáles sirven
MUTATORS=[
    ("< → <=", lambda f: f.replace("<","<=") if "<" in f and "<=" not in f else None),
    ("2**n → 3**n", lambda f: f.replace("2**n","3**n") if "2**n" in f else None),
    ("n**2 → 2n²", lambda f: f.replace("n**2","2*n**2",1) if "n**2" in f else None),
    ("+1", lambda f: f.replace("n**2",f"n**2+1") if "n**2" in f else None),
    ("+n", lambda f: f.replace("n**2",f"n**2+n") if "n**2" in f else None),
    ("n²→n³", lambda f: f.replace("n**2","n**3",1) if "n**2" in f else None),
]

def run():
    domain=list(range(1,60))
    print("╔════════════════════════════════════════════════════════════╗")
    print("🧪 STARKCORE CONJECTURE EVOLUTION LAB v8 🧪")
    print("╚════════════════════════════════════════════════════════════╝")

    # SEMILLAS
    seeds=["n < n**2","2*n < n**2","n**2 < 2**n","n**3 < 3**n"]
    pop=[]
    stats={"semillas":len(seeds),"mutaciones":0,"exitosas":0,"extintas":0}
    mut_success=defaultdict(int)

    for s in seeds:
        fails=fails_of(s,domain); k=kmin_of(s,domain)
        print(f"\n🌱 SEMILLA\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"📜 Fórmula : {s}\n🧬 Nicho : {niche_of(s)}\n📍 k_min : {k}\n💥 Fails : {sorted(fails)[:6]}\n🗺️ Paisaje : {landscape_bar(fails)}\n⭐ Interés : {interest(s,fails,k):.2f}\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        pop.append((s,fails,k))

    # EVOLUCIÓN ABIERTA
    print(f"\n🧬 MUTACIÓN ABIERTA")
    open_pop=pop[:]
    for gen in range(2):
        new=[]
        for f,fails,k in open_pop:
            for name,mut in MUTATORS:
                stats["mutaciones"]+=1
                nf=mut(f)
                if not nf or nf==f: continue
                nfails=fails_of(nf,domain)
                nk=kmin_of(nf,domain)
                if len(nfails) < len(fails) or nk < k:
                    stats["exitosas"]+=1
                    mut_success[name]+=len(fails)-len(nfails)
                    print(f"\n🧬 MUTACIÓN ({name})\n{f}\n │\n ▼\n{nf}\n🗺️ {landscape_bar(fails)} → {landscape_bar(nfails)}")
                    new.append((nf,nfails,nk))
        open_pop.extend(new)
        open_pop=list({x[0]:x for x in open_pop}.values())[:12] # dedup

    # CIRUGÍA
    print(f"\n🏥 CIRUGÍA EVOLUTIVA\n══════════════════════════")
    target=next((x for x in open_pop if x[0]=="n**2 < 2**n"), open_pop[0])
    f,fails,k=target
    print(f"🦠 Paciente\n{f}\n💥 Lesiones\n{sorted(fails)}\n🗺️ {landscape_bar(fails)}")
    cur_f,cur_fails=f,fails
    for i in range(3):
        if not cur_fails: break
        t=max(cur_fails) if cur_fails else None
        print(f"\n🔪 Operación {i+1} - eliminar {t}")
        # cirugía: probar debilitamiento que salve t
        cand=f"{cur_f.replace('n**2',f'n**2+{t}')}" if "n**2" in cur_f else cur_f.replace("<","<=")
        nfails=fails_of(cand,domain)
        print(f"{cur_f}\n │\n ▼\n{cand}\n❤️ Resultado\n{sorted(nfails)}\n🗺️ {landscape_bar(nfails)}")
        reduction=(len(cur_fails)-len(nfails))/max(1,len(cur_fails))*100
        print(f"🌄 El paisaje de error se redujo un {reduction:.0f}%")
        cur_f,cur_fails=cand,nfails
    if not cur_fails: print("🎉 Curación completa\n⭐ Nueva especie universal")

    # DEPREDADOR POR NICHO
    print(f"\n☠️──────────── EXTINCIÓN ────────────☠️")
    survivors=[]
    for f,fails,k in sorted(open_pop,key=lambda x: (len(x[1]), x[2])):
        dominated=False
        for sf,sfails,sk in survivors:
            if niche_of(sf)!=niche_of(f): continue
            if sfails.issubset(fails) and sfails!=fails and sk<=k:
                if sfails==set(): continue
                print(f"\n💀 {f}\n fue devorada por\n🦅 {sf}\nMotivo:\n✅ mismo nicho {niche_of(f)}\n✅ menos contraejemplos {sorted(sfails)} ⊆ {sorted(fails)}\n✅ más simple")
                stats["extintas"]+=1
                dominated=True; break
        if not dominated: survivors.append((f,fails,k))

    print(f"\n🏆 SUPERVIVIENTES\n══════════════════════════════")
    for i,(f,fails,k) in enumerate(sorted(survivors,key=lambda x: -interest(x[0],x[1],x[2]))[:5],1):
        medal=["🥇","🥈","🥉","🏅","🏅"][i-1]
        print(f"{medal} ⭐ {f} (n>{k}) 🗺️ {landscape_bar(fails)}")

    print(f"\n📊 ESTADÍSTICAS\n🌱 Semillas.............{stats['semillas']}\n🧬 Mutaciones..........{stats['mutaciones']}\n❤️ Exitosas............{stats['exitosas']}\n☠️ Extintas............{stats['extintas']}\n⭐ Supervivientes........{len(survivors)}")

    print(f"\n🧠 APRENDIZAJE DE MUTACIONES")
    for name,score in sorted(mut_success.items(), key=lambda x: -x[1])[:4]:
        print(f"🏆 {name} mejora = +{score} casos")

    print(f"\n🌿 Biodiversidad preservada.")
    print(f"\n> 🌄 Las conjeturas viven sobre un paisaje de errores. El laboratorio ya no estudia fórmulas; estudia cómo cambia ese paisaje con la evolución.")

if __name__=="__main__": run()
