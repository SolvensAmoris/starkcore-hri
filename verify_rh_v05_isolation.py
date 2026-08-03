import mpmath as mp, json, datetime
mp.mp.dps = 50
zeros = [14.1347251417, 21.0220396387, 25.0108575801, 30.4248761259, 32.9350615877]

def count_zeros_in_box(t_center, n=300):
    re0, re1 = mp.mpf('0.3'), mp.mpf('0.7')
    im0, im1 = mp.mpf(t_center-0.5), mp.mpf(t_center+0.5)
    def f(s): return mp.zeta(s)
    def edge(z0,z1):
        tot=mp.mpc(0)
        for k in range(n):
            s=z0+(z1-z0)*k/n
            ds=(z1-z0)/n
            tot+=mp.diff(f,s)/f(s)*ds
        return tot
    c1=mp.mpc(re0,im0); c2=mp.mpc(re1,im0); c3=mp.mpc(re1,im1); c4=mp.mpc(re0,im1)
    I=edge(c1,c2)+edge(c2,c3)+edge(c3,c4)+edge(c4,c1)
    cnt=int(mp.nint(mp.im(I)/(2*mp.pi)))
    return cnt

for i,t in enumerate(zeros):
    z=mp.mpc('0.5', str(t))
    res=float(abs(mp.zeta(z)))
    cnt=count_zeros_in_box(t)
    print(f"Zero {i+1} t={t} |zeta| {res:.2e} | count {cnt} | unique {cnt==1}")

print("V0.5 DONE")
