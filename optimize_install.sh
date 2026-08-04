#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# STARKCORE HAMMER — FINAL OPTIMIZATION & DEPLOYMENT SCRIPT
# Resuelve los problemas de visibilidad de módulos y empaquetado formal en UserLAnd.
# ---------------------------------------------------------------------------
set -e

echo "[⚙️] Iniciando optimización metalúrgica de StarkCore Hammer..."

# 1. Crear


# 2. Re-instalar de forma física (copia directa, no editable) saltando restricciones PEP 668
echo "[📦] Copiando módulos al entorno global de Python..."
pip install . --break-system-packages --force-reinstall

# 3. Blindar el acceso directo mediante un Alias robusto en el .bashrc
# Esto garantiza que funcione incluso si el directorio binario de Python local no está en el $PATH
if ! grep -q "alias starkcore-hammer=" ~/.bashrc; then
    echo "[🔗] Inyectando alias de alta resiliencia en ~/.bashrc..."
    echo "alias starkcore-hammer='PYTHONPATH=$(pwd) python3 -m starkcore.hammer'" >> ~/.bashrc
    echo "[🔄] Configuración del entorno actualizada."
else
    echo "[#] El alias de resiliencia ya se encuentra registrado."
fi

# 4. Probar el binario en caliente sobre el Adapter Forense Real
echo "[🧪] Ejecutando test de certificación forense en frío..."
PYTHONPATH=$(pwd) python3 -m starkcore.hammer --target target_test.npy --history history_test.npy --out evidence/real_audit.json

echo "================================================================================"
echo "🎯 OPTIMIZACIÓN COMPLETADA CON ÉXITO — EL PAQUETE ES UN ARMA AUTOMÁTICA"
echo "================================================================================"
echo "Para activar los cambios de la terminal de inmediato, ejecuta:"
echo "  source ~/.bashrc"
echo ""
echo "A partir de ese instante, podrás auditar desde cualquier ruta del sistema con:"
echo "  starkcore-hammer --target ruta/matriz.npy --history ruta/historia.npy"
echo "================================================================================"
