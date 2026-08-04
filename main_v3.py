from starkcore.sanctuary.temple import Sanctuary
from starkcore.sanctuary.omega import OmegaObserver
from starkcore.executors.strategies import ValidationExecutor, KernelExecutor
import os

if __name__ == "__main__":
    # Importante: Instanciamos un observador fresco. 
    # Al simular ejecuciones separadas, la única forma de recordar es leyendo el DISCO DURO.
    omega_fresco = OmegaObserver()
    
    executors_map = {
        "VirgoKnight": ValidationExecutor(),
        "CapricornKnight": KernelExecutor()
    }

    # Verificar si ya había memoria en el disco para mostrar persistencia real
    db_path = "starkcore/evidence/immunological_memory.json"
    if os.path.exists(db_path):
        print(f"\n💾 [Detección de Sistema] Se encontró un bloque de memoria previa en disco con {os.path.getsize(db_path)} bytes.")
    else:
        print("\n🆕 [Detección de Sistema] Iniciando el Santuario sin memoria previa en disco.")

    print("\n🛡️ === INICIANDO UNA SOLA INVOCACIÓN DE ENTORNO EN PRODUCCIÓN ===")
    santuario = Sanctuary(observer=omega_fresco)
    santuario.load_constellation("gold_sanctuary", executors=executors_map)
    
    # Lanzar petición con anomalía
    status, ctx_final = santuario.invoke({"anomaly": True})
    
    print(f"\n📋 \033[1;36mEstatus de Salida:\033[0m {status}")
    print(f"📦 Contexto de Datos resultante:", ctx_final)
