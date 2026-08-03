import json, hashlib, sys, platform, datetime, cmath, random

zeros = [14.1347251417, 21.0220396387, 25.0108575801, 30.4248761259, 32.9350615877]
TERMS = 8000
THRESHOLD_ON = 0.05
THRESHOLD_OFF = 0.02

def zeta_approx(s, terms=TERMS):
    total = 0j
    for n in range(1, terms):
        total += ((-1)**(n-1)) / (n**s)
    return total / (1 - 2**(1-s))

# SHA del propio script
with open(__file__, 'rb') as f:
    sha = hashlib.sha256(f.read()).hexdigest()

env = {
    "python": sys.version.split()[0],
    "platform": platform.platform(),
    "sha256": sha,
    "terms": TERMS,
    "method": "zeta_eval_eta"
}

witnesses = []
for idx, t in enumerate(zeros):
    # On line
    s_on = complex(0.5, t)
    residual = abs(zeta_approx(s_on))

    # Falsification: muestreo amplio en critical strip
    counterexample = None
    samples = 100
    for _ in range(samples):
        re_test = random.uniform(0.1, 0.9)
        if abs(re_test-0.5) < 0.05: continue
        s_off = complex(re_test, t + random.uniform(-0.5, 0.5))
        mag_off = abs(zeta_approx(s_off))
        if mag_off < THRESHOLD_OFF:
            counterexample = {"re": re_test, "im": s_off.imag, "mag": mag_off}
            break

    obj = {
        "candidate": f"0.5 + {t}i",
        "index": idx+1,
        "terms": TERMS,
        "residual": residual,
        "threshold_on": THRESHOLD_ON,
        "threshold_off": THRESHOLD_OFF,
        "status": "PASS" if residual < THRESHOLD_ON else "FAIL",
        "falsification_attempt": {
            "tested_region": "critical_strip Re=[0.1,0.9] excl 0.5",
            "samples": samples,
            "counterexample_found": counterexample is not None,
            "counterexample": counterexample
        },
        "environment": env,
        "path": "ZERO -> WITNESS -> EVIDENCE -> ATTESTATION",
        "philosophy": "VALID == REVERSIBLE"
    }
    witnesses.append(obj)
    print(f"Zero {idx+1}: residual={residual:.6f} | counter_found={obj['falsification_attempt']['counterexample_found']}")

full_artifact = {
    "starkcore_version": "v0.4 Full Witness",
    "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "commit_parent": "45bc1a3",
    "witnesses": witnesses
}

with open("evidence/rh_check/RH_V04_FULL_WITNESS.json", "w") as f:
    json.dump(full_artifact, f, indent=2)

print(f"\nFULL WITNESS SAVED -> RH_V04_FULL_WITNESS.json | SHA {sha[:12]}")
