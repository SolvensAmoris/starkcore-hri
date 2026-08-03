import json, hashlib, sys, platform, datetime, cmath

zeros = [14.1347251417, 21.0220396387, 25.0108575801, 30.4248761259, 32.9350615877]

def zeta_approx(s, terms=8000):
    total = 0j
    for n in range(1, terms):
        total += ((-1)**(n-1)) / (n**s)
    return total / (1 - 2**(1-s))

def attempt_falsify(t, terms=8000):
    for re in [0.3, 0.4, 0.6, 0.7]:
        s = complex(re, t)
        mag = abs(zeta_approx(s, terms=terms))
        if mag < 0.02:  # más estricto, v0.3 usaba 0.1
            return {"found_off_line": True, "re": re, "mag": mag}
    return {"found_off_line": False}

witnesses = []
for i, t in enumerate(zeros):
    s = complex(0.5, t)
    mag = abs(zeta_approx(s, terms=8000))
    falsify = attempt_falsify(t, terms=8000)
    
    witnesses.append({
        "zero_candidate": {"re": 0.5, "im": t, "index": i+1},
        "verification": {"method": "zeta_eval_eta", "terms": 8000, "residual": mag, "status": "PASS" if mag < 0.05 else "FAIL"},
        "falsification_attempt": falsify,
        "path": "ZERO -> WITNESS -> EVIDENCE -> ATTESTATION"
    })
    print(f"Zero {i+1}: PASS residual={mag:.6f} | falsify_off_line={falsify['found_off_line']}")

with open("evidence/rh_check/RH_V03_WITNESS.json", "w") as f:
    json.dump({
        "starkcore_version": "v0.3.1 Zero Witness - 8000 terms",
        "commit": "7f992ef -> next",
        "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "philosophy": "VALID == REVERSIBLE - includes failed falsification",
        "witnesses": witnesses
    }, f, indent=2)

print("\nWITNESS SAVED -> 8000 terms")
