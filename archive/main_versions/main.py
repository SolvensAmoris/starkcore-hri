from starkcore.sanctuary.temple import Sanctuary
from starkcore.knights.zodiac import (
    AriesKnight, TaurusKnight, GeminiKnight, CancerKnight, LeoKnight,
    VirgoKnight, LibraKnight, ScorpioKnight, SagittariusKnight,
    CapricornKnight, AquariusKnight, PiscesKnight
)
from starkcore.executors.strategies import ValidationExecutor, KernelExecutor

def run_pipeline(has_anomaly: bool):
    santuario = Sanctuary()
    
    # Inyectar Executors específicos cumpliendo el desacoplamiento
    val_exec = ValidationExecutor()
    ker_exec = KernelExecutor()

    # Registrar las Casas del Santuario
    santuario.register(AriesKnight())
    santuario.register(TaurusKnight())
    santuario.register(GeminiKnight())
    santuario.register(CancerKnight())
    santuario.register(LeoKnight())
    santuario.register(VirgoKnight(executor=val_exec)) # Inyección de estrategia
    santuario.register(LibraKnight())
    santuario.register(ScorpioKnight())
    santuario.register(SagittariusKnight())
    santuario.register(CapricornKnight(executor=ker_exec)) # Inyección de estrategia
    santuario.register(AquariusKnight())
    santuario.register(PiscesKnight())

    ctx = {"anomaly": has_anomaly}
    final_ctx = santuario.invoke(ctx)
    
    print("\n📊 \033[1;36m[Contexto Final de la Red]\033[0m:", final_ctx)
    print("👁️  \033[1;35m[Logs del Observador Omega]\033[0m:")
    for log in santuario.observer.logs:
        print(f"   ↳ Casa {log['house']} | {log['knight'].ljust(10)} | Acción: {log['action'].ljust(18)} | Status: {log['status']}")

if __name__ == "__main__":
    print("\n🔥 === PRUEBA 1: CAMINO DEL GUERRERO (FLUJO NORMAL) ===")
    run_pipeline(has_anomaly=False)
    
    print("\n🔥 === PRUEBA 2: EL DESPERTAR DE OFIUCO (FLUJO CON EXCEPCIÓN) ===")
    run_pipeline(has_anomaly=True)
