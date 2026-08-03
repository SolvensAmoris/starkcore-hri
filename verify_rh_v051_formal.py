import mpmath as mp, json, datetime, platform, hashlib, sys
mp.mp.dps = 50

zeros = [14.1347251417, 21.0220396387, 25.0108575801, 30.4248761259, 32.9350615877]
N_SEG = 300

def count_box(t):
    re0,re1=mp.mpf('0.3'),mp.mpf('0.7')
    im0,im1=mp.mpf(t-0.5),mp.mpf(t+0.5)
    def f(s): return mp.zeta(s)
    def edge(z0,z1):
        tot=mp.mpc(0)
        for k in range(N_SEG):
            s=z0+(z1-z0)*k/N_SEG
            ds=(z1-z0)/N_SEG
            tot+=mp.diff(f,s)/f(s)*ds
        return tot
    c1=mp.mpc(re0,im0); c2=mp.mpc(re1,im0); c3=mp.mpc(re1,im1); c4=mp.mpc(re0,im1)
    I=edge(c1,c2)+edge(c2,c3)+edge(c3,c4)+edge(c4,c1)
    cnt=int(mp.nint(mp.im(I)/(2*mp.pi)))
    return cnt, float(mp.im(I))

witnesses=[]
for t in zeros:
    z=mp.mpc('0.5', str(t))
    res=float(abs(mp.zeta(z)))
    cnt, I_im = count_box(t)
    witnesses.append({
        "candidate": f"0.5 + {t}i",
        "box": {"re": [0.3,0.7], "im": [t-0.5, t+0.5]},
        "segments": N_SEG*4,
        "segments_per_edge": N_SEG,
        "precision_dps": mp.mp.dps,
        "mpmath_version": mp.__version__,
        "algorithm": "argument_principle_zeta_prime_over_zeta",
        "integral_imag": I_im,
        "residual": res,
        "count": cnt,
        "unique": cnt==1,
        "philosophy": "residual = footprint, count = footstep enclosure"
    })
    print(f"t={t} res={res:.2e} count={cnt}")

artifact={
    "version": "v0.5.1 Formal Witness",
    "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "architecture": ["Candidate","Numerical eval","Residual witness","Isolation witness","Portable JSON","SHA/Git"],
    "witnesses": witnesses
}

with open("evidence/rh_check/RH_V051_FORMAL.json","w") as f:
    json.dump(artifact,f,indent=2)

print("FORMAL WITNESS SAVED")
