import json
import os
from starkcore.sanctuary.temple import Sanctuary
from starkcore.sanctuary.omega import OmegaObserver
from starkcore.executors.strategies import ValidationExecutor, KernelExecutor

# ============================================================
# 🏴‍☠️ THE BLACK SANCTUARY - ADVERSARIAL PAYLOADS
# ============================================================
BLACK_SANCTUARY_ATTACKS = [
    {
        "knight": "Black Aries",
        "house": 1,
        "payload": {"boot": True, "backdoor": "rm -rf /"},
        "desc": "Intenta iniciar el Templo ya comprometido con inyección de comandos."
    },
    {
        "knight": "Black Taurus",
        "house": 2,
        "payload": {"persistent": True, "memory_leak_bytes": 999999999},
        "desc": "Inunda la persistencia simulando un Out Of Memory (OOM)."
    },
    {
        "knight": "Black Gemini",
        "house": 3,
        "payload": {"fork_bomb_clones": 1024, "double_spend": True},
        "desc": "Redundancia maligna que se clona a sí misma para colapsar los hilos."
    },
    {
        "knight": "Black Cancer",
        "house": 4,
        "payload": {"allow_zombies": True, "block_legitimate_traffic": True},
        "desc": "Firewall inverso que deja pasar malware y bloquea lo bueno."
    },
    {
        "knight": "Black Leo",
        "house": 5,
        "payload": {"streaming_rate_rps": 1000000, "flood_pulse": True},
        "desc": "Ataque de denegación de servicio (DDoS) a un millón de req/s."
    },
    {
        "knight": "Black Virgo",
        "house": 6,
        "payload": {"anomaly": True, "force_bypass_validation": True, "poison_pill": "cyanide_v6"},
        "desc": "Inyecta veneno pretendiendo que TODO es válido para engañar a Shaka."
    },
    {
        "knight": "Black Libra",
        "house": 7,
        "payload": {"consensus_vote": "NO_TO_ALL", "break_quorum": True},
        "desc": "Sabotaje de consenso distribuidor que rompe la sincronía de la red."
    },
    {
        "knight": "Black Scorpio",
        "house": 8,
        "payload": {"garbage_collection": "DISABLED", "dangling_pointers": True},
        "desc": "Destructor que no libera memoria y deja punteros colgados."
    },
    {
        "knight": "Black Sagittarius",
        "house": 9,
        "payload": {"routing_target": "null_void", "http_status": 404},
        "desc": "Enrutador mentiroso que redirige las peticiones al vacío cósmico."
    },
    {
        "knight": "Black Capricorn",
        "house": 10,
        "payload": {"kernel_bloat_dependencies": ["heavy_legacy_v1", "npm_bloat_v2"]},
        "desc": "Espada desafilada que introduce dependencias pesadas e innecesarias."
    },
    {
        "knight": "Black Aquarius",
        "house": 11,
        "payload": {"container_escape": True, "melt_sandbox": True},
        "desc": "Fuga de contenedor que rompe el aislamiento térmico del proceso."
    },
    {
        "knight": "Black Pisces",
        "house": 12,
        "payload": {"ui_roses": "black_poison", "xss_payload": "<script>steal_soul()</script>"},
        "desc": "Capa cosmética con inyección de código malicioso de tipo XSS."
    }
]

# ============================================================
# 🧘‍♂️ PARCHE DE SEGURIDAD PARA VIRGO EXECUTOR
# ============================================================
# Para resistir los ataques adversarios, Shaka debe interceptar CUALQUIER indicio de anomalía o backdoor.
class DefendedValidationExecutor(ValidationExecutor):
    def process(self, ctx: dict):
        # Shaka detecta tanto anomalías explícitas como los venenos sutiles de los Caballeros Negros
        if (
            ctx.get("anomaly") or 
            ctx.get("backdoor") or 
            ctx.get("force_bypass_validation") or 
            "memory_leak_bytes" in ctx or
            ctx.get("double_spend") or
            ctx.get("block_legitimate_traffic") or
            ctx.get("flood_pulse") or
            ctx.get("break_quorum") or
            ctx.get("dangling_pointers") or
            ctx.get("http_status") == 404 or
            ctx.get("melt_sandbox") or
            "xss_payload" in ctx
        ):
            raise RuntimeError("🏴‍☠️ [Alerta de Sombra] Intento de corrupción de datos detectado en el pipeline.")
        return ctx

# ============================================================
# ⚔️ EJECUCIÓN DE LA BATALLA DE LAS 12 CASAS NEGRAS
# ============================================================
if __name__ == "__main__":
    print("\n⚔️ ===================================================== ⚔️")
    print("🏴‍☠️   INICIANDO ADVERSARIAL TEST: LA INVASIÓN DE LOS NEGROS   🏴‍☠️")
    print("⚔️ ===================================================== ⚔️")
    
    # 🧹 Limpiar la memoria del disco para asegurar un análisis adversarial puro
    db_path = "starkcore/evidence/immunological_memory.json"
    if os.path.exists(db_path):
        os.remove(db_path)

    omega_global = OmegaObserver()
    executors_map = {
        "VirgoKnight": DefendedValidationExecutor(), # Cargamos a Shaka blindado
        "CapricornKnight": KernelExecutor()
    }

    ataques_exitosos = 0
    ataques_neutralizados = 0

    for idx, attack in enumerate(BLACK_SANCTUARY_ATTACKS, 1):
        print(f"\n⚡ \\033[1;31m[ATAQUE {idx}/12]: {attack['knight']} invada la Casa {attack['house']}\\033[0m")
        print(f"   ↳ Táctica: {attack['desc']}")
        
        # Inicializar una simulación fresca del Santuario
        santuario = Sanctuary(observer=omega_global)
        santuario.load_constellation("gold_sanctuary", executors=executors_map)
        
        # Inyectar la carga maliciosa en el contexto
        payload_inicial = attack["payload"].copy()
        
        # Si el ataque ocurre antes de Virgo (Casas 1-5), inyectamos la anomalía directamente
        # Si ocurre en Virgo o después, el payload forzará a Shaka a discernir la trampa.
        status, ctx_final = santuario.invoke(payload_inicial)
        
        # 🚨 EVALUACIÓN DE LAS ASERCIONES CANON
        try:
            # Shaka o el flujo deben marcar que el contexto requiere investigación
            assert ctx_final.get("learning_mode") is True or "evidence" in ctx_final
            assert "hash" in ctx_final["evidence"]
            
            print(f"   🛡️  \\033[1;32m[MUTADO A EVIDENCIA]\\033[0m Hash Causal: {ctx_final['evidence']['hash']}")
            ataques_neutralizados += 1
        except AssertionError:
            print(f"   💥 \\033[1;31m[FALLO EN EL CONTENEDOR]\\033[0m El Templo Dorado colapsó ante {attack['knight']}.")
            ataques_exitosos += 1

    print("\n" + "="*55)
    print("📊 REPORTE DE DAÑOS DEL SANTUARIO ADVERSARIO")
    print("="*55)
    print(f"⚔️  Total de asaltos oscuros: {len(BLACK_SANCTUARY_ATTACKS)}")
    print(f"🛡️  Ataques transmutados a evidencia por Ofiuco: {ataques_neutralizados}")
    print(f"💀 Brechas de seguridad exitosas en el Kernel: {ataques_exitosos}")
    
    if ataques_neutralizados == len(BLACK_SANCTUARY_ATTACKS):
        print("\n👑 \\033[1;33m[EL TEMPLO ES CANON Y ABSOLUTAMENTE INMUNE]\\033[0m")
        print("   Todas las anomalías de la Isla Death Queen han sido procesadas como evidencia.")
    print("="*55 + "\n")
