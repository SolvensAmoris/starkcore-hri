import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

nodes = []

for py in ROOT.rglob("*.py"):
    if "venv" in py.parts or ".venv" in py.parts or "__pycache__" in py.parts:
        continue

    try:
        source = py.read_text(encoding="utf-8")
        tree = ast.parse(source)
    except Exception as e:
        nodes.append({
            "file": str(py.relative_to(ROOT)),
            "status": "PARSE_ERROR",
            "error": str(e)
        })
        continue

    classes = []
    functions = []
    imports = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            classes.append(node.name)

        elif isinstance(node, ast.FunctionDef):
            functions.append(node.name)

        elif isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)

        elif isinstance(node, ast.ImportFrom):
            imports.append(node.module or "")

    nodes.append({
        "file": str(py.relative_to(ROOT)),
        "status": "ONLINE",
        "classes": classes,
        "functions": functions,
        "imports": imports
    })

print("=" * 70)
print("STARKCORE H-TEST CARTOGRAPHER")
print("=" * 70)

for n in nodes:
    print(f"\n📄 {n['file']}")
    print(f"Status: {n['status']}")

    if n["status"] != "ONLINE":
        print(f"Error: {n['error']}")
        continue

    if n["classes"]:
        print("Classes:")
        for c in n["classes"]:
            print(f"  • {c}")

    if n["functions"]:
        print("Functions:")
        for f in n["functions"]:
            print(f"  • {f}")

    if n["imports"]:
        print("Imports:")
        for i in sorted(set(n["imports"])):
            print(f"  • {i}")

with open(ROOT / "starkcore_map.json", "w", encoding="utf-8") as f:
    json.dump(nodes, f, indent=2)

print("\n✅ Mapa guardado en starkcore_map.json")
