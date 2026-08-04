import os

print("🔱 Desplegando Causal Immune Layer (StarkCore V4)...")

paths = [
    "starkcore/immunity",
    "starkcore/knights",
    "starkcore/sanctuary",
    "starkcore/evidence",
]

for path in paths:
    os.makedirs(path, exist_ok=True)

with open("starkcore/immunity/__init__.py", "w") as f:
    f.write("# Causal Immune Layer\n")


print("✅ Estructura inmunológica creada")
print("👉 Ahora añade los módulos:")
print("   - immunity/sensor.py")
print("   - knights/zodiac.py")
print("   - sanctuary/temple.py")
print("   - black_sanctuary_test.py")
