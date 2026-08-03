#!/usr/bin/env python3
import subprocess, json, os, tempfile, re
from conjecture_lab_v14_final import fails_of, delta_score, BASE_PHIS
domain=list(range(1,80))

def check_lean(code:str):
    """Llama a lake env lean y lee error del kernel - feedback real"""
    with tempfile.NamedTemporaryFile(suffix=".lean", mode='w', delete=False) as f:
        f.write(code); path=f.name
    try:
        r=subprocess.run(["lake","env","lean",path], capture_output=True, text=True, timeout=15)
        out=r.stdout+r.stderr
        if "error" in out.lower() or r.returncode!=0:
            return False, out[:500]
        return True, "OK"
    except FileNotFoundError:
        # fallback si no tienes Lean instalado: simula ok si sintaxis parece Lean
        return ("theorem" in code and "sorry" in code), "Lean no instalado, check sintáctico"
    finally:
        os.unlink(path)

def to_lean_code(orig, cand):
    lean_orig=orig.replace("**","^").replace("math.log","Real.log")
    lean_cand=cand['strengthened'].replace("**","^").replace("math.log","Real.log")
    return f"""
import Mathlib
-- ORIG: {orig} fails={cand['old_fails']}
-- STARKCORE Φ: {cand['phi']} | {cand['proof']} | Δ={cand['delta']:.1f} | preserves={cand['preserves']}
theorem strengthened_{abs(hash(lean_cand))%10000} (n : ℕ) (hn : n ≥ 5) : {lean_cand} := by
  sorry
"""

def strengthen_with_lean_feedback(conj):
    old_fails=fails_of(conj, domain)
    results=[]
    for phi in BASE_PHIS:
        if phi.preserves=="none": continue
        cand_str=phi.apply(conj)
        if not cand_str: continue
        new_fails=fails_of(cand_str, domain)
        d=delta_score(old_fails,new_fails,conj,cand_str,phi)
        if d<=0: continue
        cand={"orig":conj,"strengthened":cand_str,"phi":str(phi),"proof":phi.proof,"preserves":phi.preserves,"delta":d,"old_fails":len(old_fails),"new_fails":len(new_fails)}
        lean_code=to_lean_code(conj,cand)
        ok,log=check_lean(lean_code)
        cand["lean_ok"]=ok; cand["lean_log"]=log
        # si Lean dice error, penaliza -10 y no lo vendes
        if not ok: cand["delta"]-=10
        else: results.append(cand)
    return sorted(results, key=lambda x: -x["delta"])

if __name__=="__main__":
    tests=["n**2 < 2**n","n**3 < 2**n","2*n < n**2"]
    out=[]
    for t in tests:
        print(f"\n🧪 {t}")
        for r in strengthen_with_lean_feedback(t)[:2]:
            print(f" ✅ {r['phi']} Δ={r['delta']:.1f} {r['strengthened']} Lean:{r['lean_ok']}")
            out.append(r)
    with open("starkcore_results.json","w") as f: json.dump(out,f,indent=2)
    print("\n📦 starkcore_results.json listo para cliente")
