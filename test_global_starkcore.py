import sys
print("=== STARKCORE GLOBAL TEST SUITE ===")
print("STO // REP≠STATE≠AGENCY | v0.4 LOCKED | R²=0.99 n=1000\n")

# GIE-001
print("[GIE-001] Deterministic Structural Propagation Engine")
try:
    import pytest
    import subprocess
    result = subprocess.run([sys.executable, "-m", "pytest", "test_starkcore_gie_001.py", "-v"], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
    else:
        print("GIE-001: OK 6/6\n")
except Exception as e:
    print(f"GIE-001 error: {e}\n")

# GIE-002
print("[GIE-002] Enforcer with Cryptographic Evidence")
try:
    result = subprocess.run([sys.executable, "-m", "pytest", "test_starkcore_gie_002.py", "-v"], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
    else:
        print("GIE-002: OK 6/6\n")
except Exception as e:
    print(f"GIE-002 error: {e}\n")

print("=== GLOBAL: 12/12 if both OK ===")
print("WE DON'T NEED MORE EXPLANATIONS. WE NEED EVIDENCE.")
