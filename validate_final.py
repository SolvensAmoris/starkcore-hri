import sympy as sp
t = sp.symbols('t')
def verify(p,q,a,b,c,d):
    p,q,a,b,c,d = [sp.Poly(e,t,domain='ZZ').as_expr() for e in (p,q,a,b,c,d)]
    assert q*b*d != 0
    f = sp.cancel(p/q)
    assert f.has(t), "f constante"
    x,y = sp.cancel(a/b), sp.cancel(c/d)
    assert sp.cancel(y**2 - x*(x+(2*f)**4)*(x+(f**2-1)**4)) == 0
    T=[0,-4*f**5-8*f**4+8*f**2+4*f,4*f**6-8*f**4+4*f**2,-4*f**7+8*f**6-8*f**4+4*f**3,4*f**7+8*f**6-8*f**4-4*f**3,-16*f**4,-4*f**6+8*f**4-4*f**2,4*f**5-8*f**4+8*f**2-4*f,-f**8+4*f**6-6*f**4+4*f**2-1]
    assert all(sp.cancel(x-e)!=0 for e in T)
    return f"PASS rank >=1 con f={f} x={x} y={y}"

# cuando tengas tu tupla, descomenta:
# print(verify(t**2+1, t+1, t, 1, t**2, 1))
