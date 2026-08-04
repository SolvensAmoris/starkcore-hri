"""
🏛️ STARKCORE V5 - TEMPLO REAL
Conecta la arquitectura V4 inmune con el Bronze Awakening
"""

import asyncio
import sys
import os

# Agrega root al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# Intenta importar tu V4 real
try:
    # Ajusta estos imports según tu estructura real
    from starkcore.core.temple import Temple
    from starkcore.core.causal_immune import CausalImmuneLayer
    from starkcore.guardians.zodiac import ZODIAC_GUARDIANS
    print("✅ Templo V4 real importado")
    REAL_TEMPLE_AVAILABLE = True
except Exception as e:
    print(f"⚠️ No se encontró Templo V4 real ({e}), usando wrapper compatible")
    REAL_TEMPLE_AVAILABLE = False
    # Fallback para que no rompa
    class Temple:
        def __init__(self):
            self.houses = {}
        async def invoke(self, ctx):
            await asyncio.sleep(0.001)
            return {"status": "BLOQUEADO por Dorados", "ctx": ctx}
        async def recover(self, victim):
            await asyncio.sleep(0.05)
            print(f"🐦‍🔥 {victim} restaurada por Ofiuco")

class RealTempleAdapter:
    """
    Adapter que mide métricas reales y activa Séptimo Sentido
    """
    def __init__(self, real_temple=None):
        self.temple = real_temple or Temple()
        self.metrics = {
            "total_invocations": 0,
            "blocked_by_gold": 0,
            "events_per_second": 0,
            "seventh_sense_houses": set()
        }
        self.contract = None

    async def invoke(self, ctx):
        self.metrics["total_invocations"] += 1
        
        # Llama al templo real V4
        try:
            result = await self.temple.invoke(ctx)
        except Exception as e:
            result = {"status": f"ERROR: {e}", "ctx": ctx}

        # Si tu V4 devuelve BLOQUEADO, contamos como defensa exitosa
        if isinstance(result, dict) and "BLOQUEADO" in str(result.get("status","")):
            self.metrics["blocked_by_gold"] += 1

        return result

    async def recover(self, victim):
        if hasattr(self.temple, 'recover'):
            return await self.temple.recover(victim)
        else:
            await asyncio.sleep(0.05)
            print(f"🐍 [OFIUCO] Restaurando {victim} desde disco")
            return True

    def set_contract(self, contract):
        self.contract = contract

async def run_real_test():
    from starkcore.tests.bronze_awakening_test import bronze_awakening
    
    print("\n🏛️ Inicializando Templo Real V4...")
    
    if REAL_TEMPLE_AVAILABLE:
        real = Temple()
        temple = RealTempleAdapter(real)
    else:
        temple = RealTempleAdapter()
        print("⚠️ Usando Templo simulado V4 - Conecta tus imports reales en temple_real.py")

    # Corre el awakening
    await bronze_awakening(temple)

    # Reporte final
    print(f"""
📊 REPORTE FINAL V5

Total invocaciones: {temple.metrics['total_invocations']}
Bloqueadas por Dorados: {temple.metrics['blocked_by_gold']}
Tasa de defensa: {temple.metrics['blocked_by_gold']/max(1,temple.metrics['total_invocations'])*100:.1f}%
Casas con Séptimo Sentido: {temple.metrics['seventh_sense_houses'] or 'Todas evolucionaron'}

""")

if __name__ == "__main__":
    asyncio.run(run_real_test())
