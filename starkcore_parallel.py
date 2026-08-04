import sympy as sp, multiprocessing, random, os
t=sp.symbols('t')

def verify_tuple(args):
    p,q,a,b,c,d = args
    try:
        if q*b*d==0: return None
        f=sp.cancel(p/q)
        if not f.has(t): return None
        x,y=sp.cancel(a/b), sp.cancel(c/d)
        if sp.cancel(y**2 - x*(x+(2*f)**4)*(x+(f**2-1)**4))!=0: return None
        T=[0,-4*f**5-8*f**4+8*f**2+4*f,4*f**6-8*f**4+4*f**2,-4*f**7+8*f**6-8*f**4+4*f**3,4*f**7+8*f**6-8*f**4-4*f**3,-16*f**4,-4*f**6+8*f**4-4*f**2,4*f**5-8*f**4+8*f**2-4*f,-f**8+4*f**6-6*f**4+4*f**2-1]
        if not all(sp.cancel(x-e)!=0 for e in T): return None
        return (p,q,a,b,c,d,f,x,y)
    except: return None

def rand_poly(max_deg=2, C=2):
    deg=random.randint(0,max_deg)
    poly=0
    for i in range(deg+1):
        poly+=random.randint(-C,C)*t**i
    if poly==0: return t
    return poly

def worker(n):
    for _ in range(5000):
        p=rand_poly(2,2)
        q=rand_poly(1,1)
        if q==0: continue
        a=rand_poly(2,2)
        b=sp.Integer(1)
        c=rand_poly(2,3)
        d=sp.Integer(1)
        res=verify_tuple((p,q,a,b,c,d))
        if res:
            print(f"\nFOUND! p={res[0]} q={res[1]} a={res[2]} b={res[3]} c={res[4]} d={res[5]} f={res[6]}", flush=True)
            with open("FOUND.txt","w") as out: out.write(str(res))
            os._exit(0)
    return n*5000

if __name__=="__main__":
    print(f"StarkCore parallel {multiprocessing.cpu_count()} cores - cazando rank>=1...")
    with multiprocessing.Pool() as pool:
        total=0
        for done in pool.imap_unordered(worker, range(1000000)):
            total+=done
            if total%50000==0:
                print(f"{total} intentos... f vivo")
