import sympy as sp
import itertools, random
t = sp.symbols('t')

def verify(p,q,a,b,c,d, verbose=False):
    try:
        p,q,a,b,c,d = [sp.Poly(e,t,domain='ZZ').as_expr() for e in (p,q,a,b,c,d)]
        if q*b*d == 0: return False
        f = sp.cancel(p/q)
        if not f.has(t): return False
        x, y = sp.cancel(a/b), sp.cancel(c/d)
        if sp.cancel(y**2 - x*(x+(2*f)**4)*(x+(f**2-1)**4))!= 0:
            return False
        T = [0,-4*f**5-8*f**4+8*f**2+4*f, 4*f**6-8*f**4+4*f**2,
             -4*f**7+8*f**6-8*f**4+4*f**3, 4*f**7+8*f**6-8*f**4-4*f**3, -16*f**4,
             -4*f**6+8*f**4-4*f**2, 4*f**5-8*f**4+8*f**2-4*f, -f**8+4*f**6-6*f**4+4*f**2-1]
        if not all(sp.cancel(x-e)!= 0 for e in T):
            return False
        return True
    except:
        return False

# generador de polinomios Z[t] chicos
def gen_polys(max_deg=2, coeff_range=(-2,2)):
    coeffs = range(coeff_range[0], coeff_range[1]+1)
    for deg in range(max_deg+1):
        for cs in itertools.product(coeffs, repeat=deg+1):
            if cs[-1]==0 and deg>0: continue # leading 0
            if all(c==0 for c in cs): continue
            poly = sum(c*t**i for i,c in enumerate(cs))
            yield poly

# StarkCore search loop
print("StarkCore search: p,q,a,b,c,d en Z[t] deg<=2 coeff -2..2")
print("Target: PASS: rank E(Q(t)) >=1")
count=0
for p in gen_polys(1, (-2,2)):
 for q in gen_polys(1, (-1,1)):
  f = sp.cancel(p/q)
  if not f.has(t): continue
  for a in gen_polys(1, (-2,2)):
   for b in [sp.Integer(1), t, t+1, t-1]: # b chicos para no explotar
    for c in gen_polys(1, (-2,2)):
     for d in [sp.Integer(1), t, t+1, t-1]:
      count+=1
      if count % 5000 == 0:
          print(f" {count} probados... p={p} q={q} f={f}")
      if verify(p,q,a,b,c,d):
          print(f"\n!!! ENCONTRADO!!!")
          print(f"p={p}\nq={q}\na={a}\nb={b}\nc={c}\nd={d}")
          print(f"f={f}")
          exit(0)
print("No encontrado en espacio chico - expande max_deg/coeff_range")
