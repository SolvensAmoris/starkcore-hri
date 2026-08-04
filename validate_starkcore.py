import sympy as sp
t = sp.symbols('t')

def verify(p, q, a, b, c, d): # all six in Z[t]
    p,q,a,b,c,d = [sp.Poly(e,t,domain='ZZ').as_expr() for e in (p,q,a,b,c,d)]
    assert q*b*d!= 0, "0) q,b,d!=0 FAIL"
    f = sp.cancel(p/q)
    assert f.has(t), "1) f no depende de t - p*n = q*m FAIL"
    x, y = sp.cancel(a/b), sp.cancel(c/d)
    assert sp.cancel(y**2 - x*(x+(2*f)**4)*(x+(f**2-1)**4)) == 0, "3) (x,y) no esta en la curva FAIL"
    T = [0,-4*f**5-8*f**4+8*f**2+4*f, 4*f**6-8*f**4+4*f**2,
         -4*f**7+8*f**6-8*f**4+4*f**3, 4*f**7+8*f**6-8*f**4-4*f**3, -16*f**4,
         -4*f**6+8*f**4-4*f**2, 4*f**5-8*f**4+8*f**2-4*f, -f**8+4*f**6-6*f**4+4*f**2-1]
    assert all(sp.cancel(x-e)!= 0 for e in T), "4) x pertenece a T FAIL"
    return "PASS: rank E(Q(t)) >= 1"

# TEST DEMO - esto debe fallar (no es solucion)
try:
    print(verify(t, 1, 0, 1, 0, 1))
except Exception as e:
    print(f"Esperado FAIL demo: {e}")

# AQUI PONES TU TUPLA (p,q,a,b,c,d) cuando la encuentres
# Ejemplo:
# p = t**2 + 1
# q = t + 1
# a =...
# print(verify(p,q,a,b,c,d))
