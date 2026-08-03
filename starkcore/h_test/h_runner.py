import json
import importlib
from pathlib import Path

REGISTRY = Path("starkcore_map.json")

def load_registry():
    return json.loads(REGISTRY.read_text())

def probe(module_name):
    try:
        m = importlib.import_module(module_name)

        report = {
            "module": module_name,
            "status": "ONLINE",
            "validators": []
        }

        # funciones típicas de validación
        for fn in (
            "validate",
            "verify",
            "check_state",
            "check_history",
            "check_constraints",
            "diacronic_validator",
            "run",
        ):
            if hasattr(m, fn):
                report["validators"].append(fn)

        # clases que tengan validate()
        for name in dir(m):
            obj = getattr(m, name)
            if isinstance(obj, type):
                if hasattr(obj, "validate"):
                    report["validators"].append(f"{name}.validate")

        return report

    except Exception as e:
        return {
            "module": module_name,
            "status": "FAIL",
            "error": str(e)
        }

def main():
    registry = load_registry()

    print("=" * 60)
    print("H-TEST DISCOVERY")
    print("=" * 60)

    for file in registry:

        path = file["file"]

        if not path.endswith(".py"):
            continue

        mod = (
            path[:-3]
            .replace("/", ".")
            .replace("\\", ".")
        )

        if mod.startswith("./"):
            mod = mod[2:]

        r = probe(mod)

        print(f"\n[{r['status']}] {mod}")

        if "validators" in r:
            for v in sorted(set(r["validators"])):
                print("  ->", v)

        if "error" in r:
            print("  !!", r["error"])

if __name__ == "__main__":
    main()
