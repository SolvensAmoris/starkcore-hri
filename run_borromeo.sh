#!/bin/bash
set -e
echo "=== StarkCore Borromeo Character Test ==="
python3 -m pytest tests/test_borromeo_character.py -v
echo ""
echo "=== Validación directa ==="
python3 tests/test_borromeo_character.py
