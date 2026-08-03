import json
import importlib
from pathlib import Path


REGISTRY = Path(__file__).parent / "NODE_REGISTRY.json"


def load_registry():
    return json.loads(REGISTRY.read_text())


def evaluate_node(node):
    try:
        importlib.import_module(node["module"])
        return {
            "id": node["id"],
            "status": "ONLINE"
        }

    except Exception as e:
        return {
            "id": node["id"],
            "status": "FAIL",
            "error": str(e)
        }


def run_h_test():
    registry = load_registry()

    results = []

    for node in registry["nodes"]:
        results.append(evaluate_node(node))

    return results


if __name__ == "__main__":
    for result in run_h_test():
        print(result)
