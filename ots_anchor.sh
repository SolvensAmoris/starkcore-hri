#!/bin/bash
set -e
LOG_DIR="starkcore_v1_merkle_log"
HEAD=$(python3 -c "import json; print(json.load(open('$LOG_DIR/estado_firewall.json'))['head_hash'])")
ALTURA=$(python3 -c "import json; print(json.load(open('$LOG_DIR/estado_firewall.json'))['altura'])")
echo "🔐 StarkCore C4-002 - Head Anchor"
echo "Head: $HEAD"
echo "Altura: $ALTURA"
echo "$HEAD" > $LOG_DIR/head_anchor.txt
echo "Timestamp: $(date -u --iso-8601=seconds)" >> $LOG_DIR/head_anchor.txt
echo "Altura: $ALTURA" >> $LOG_DIR/head_anchor.txt
cat $LOG_DIR/head_anchor.txt

if command -v ots &> /dev/null; then
  echo "📡 Anclando en Bitcoin via OpenTimestamps..."
  ots stamp $LOG_DIR/head_anchor.txt
  echo "✅ Generado $LOG_DIR/head_anchor.txt.ots - Subelo a https://opentimestamps.org"
else
  echo "⚠️ ots no instalado. Instalalo: pip install opentimestamps-client"
  echo "Luego: ots stamp $LOG_DIR/head_anchor.txt"
  echo "O sube el hash manualmente a https://ots.btc.catallaxy.com/"
  # Creamos prueba local de todos modos
  sha256sum $LOG_DIR/head_anchor.txt > $LOG_DIR/head_anchor.txt.sha256
  echo "📄 SHA256 local: $(cat $LOG_DIR/head_anchor.txt.sha256)"
fi
