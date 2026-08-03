#!/bin/bash
set -e
# limpia venv roto si existe
rm -rf .venv

python3 -m venv .venv
source .venv/bin/activate

touch src/__init__.py
touch src/starkcore/__init__.py
touch src/starkcore/validators/__init__.py
touch tests/__init__.py

pip install pytest --quiet

echo "=== Validación directa ==="
PYTHONPATH=src python tests/test_borromeo_character.py

echo ""
echo "=== Con pytest ==="
PYTHONPATH=src python -m pytest tests/test_borromeo_character.py -v
