import hashlib, platform, sys, datetime, math

#... tu código de zeta_approx y zeros igual...

# Al final:
script_path = __file__
with open(script_path, 'rb') as f:
    sha = hashlib.sha256(f.read()).hexdigest()

print(f"\n--- AUDIT TRAIL ---")
print(f"SHA-256: {sha}")
print(f"Python: {sys.version.split()[0]}")
print(f"Platform: {platform.platform()}")
print(f"Precision: terms=1500 | threshold=0.1")
print(f"UTC: {datetime.datetime.utcnow().isoformat()}Z")
print(f"Commit: ff1389e -> next")
