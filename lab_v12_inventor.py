import math, random, ast

def eval_safe(e,n):
    try: return bool(eval(e, {"n":n,"math":math,"__builtins__":{}}))
    except: return False
def fails_of(f,d): return set(x for x in d if not eval_safe(f,x))

# GRAMÁTICA DE OPERADORES - el lenguaje, no la lista
GRAMMAR = {
    "TRANSFORM": ["div_pos", "log_both", "weaken", "strengthen", "square", "sqrt"],
}
def invent_operator():
    # inventa, no elige: "divide ambos lados por log(n+2)" etc
    name = random.choice(GRAMMAR["TRANSFORM"])
    if name=="div_pos":
        f = f"n+{random.randint(1,3)}"
        return (f"DIV({f})", lambda s: s.replace(" < ", f"/({f}) < ").replace(" <= ", f"/({f}) <= ") if s else None)
    if name=="log_both":
        return ("LOG()", lambda s: f"math.log({s.split('<')[0]}+1) < math.log({s.split('<')[1]}+1)" if "<" in s else None)
    if name=="weaken":
        return ("WEAKEN", lambda s: s.replace("<","<=",1) if "<" in s and "<=" not in s else None)
    if name=="square":
        return ("SQUARE_L", lambda s: s.replace("n**2",f"(n**2)**2") if "n**2" in s else None)
    return ("WEAKEN", lambda s: s.replace("<","<=",1) if "<" in s else None)

domain=list(range(1,30))
conjectures=["n**2 < 2**n","n**3 < 3**n","2*n < n**2","3**n < 2**n"]

print("🧬 v12 INVENTOR - Φ ya no se elige, se genera")
for _ in range(8):
    name, op = invent_operator()
    total_delta=0
    for c in conjectures:
        old=len(fails_of(c,domain))
        cand=op(c)
        if not cand: continue
        new=len(fails_of(cand,domain))
        delta=old-new - len(cand)*0.02 # tu Δ con penalización longitud
        total_delta+=delta
        if delta>0:
            print(f" ✨ {name}: {c} -> {cand[:30]} Δ={delta:+.1f}")
    if total_delta>2:
        print(f" >> Φ {name} CONSERVADO score {total_delta:.1f}")
