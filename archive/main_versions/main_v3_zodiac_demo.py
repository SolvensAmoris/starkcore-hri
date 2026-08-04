from starkcore.sanctuary.temple import Sanctuary
from starkcore.sanctuary.omega import OmegaObserver
import os

if __name__ == "__main__":

    # Observador fresco: la persistencia depende del disco
    omega_fresco = OmegaObserver()

    # Verificar memoria persistente
    db_path = "starkcore/evidence/immunological_memory.json"

    if os.path.exists(db_path):
        print(
            f"\n💾 [Detección de Sistema] "
            f"Se encontró un bloque de memoria previa en disco con "
            f"{os.path.getsize(db_path)} bytes."
        )
    else:
        print(
            "\n🆕 [Detección de Sistema] "
            "Iniciando el Santuario sin memoria previa en disco."
        )

    print("\n🛡️ === INICIANDO UNA SOLA INVOCACIÓN DE ENTORNO EN PRODUCCIÓN ===")

    santuario = Sanctuary(observer=omega_fresco)

    santuario.load_constellation("gold_sanctuary")

    # Lanzar petición con anomalía
    status, ctx_final = santuario.invoke({"anomaly": True})

    print(f"\n📋 \033[1;36mEstatus de Salida:\033[0m {status}")
    print("📦 Contexto de Datos resultante:", ctx_final)
