from starkcore.sanctuary.temple import Sanctuary


class OmegaObserver:
    """
    Registro simple de eventos del santuario.
    """

    def __init__(self):
        self.memory = []

    def record(self, house, knight, event, status):
        self.memory.append(
            {
                "house": house,
                "knight": knight,
                "event": event,
                "status": status,
            }
        )


BLACK_SANCTUARY = [

    {
        "attacker_name": "Black Aries",
        "adversarial_target_house": 1,
        "backdoor": True,
    },

    {
        "attacker_name": "Black Taurus",
        "adversarial_target_house": 2,
        "memory_leak_bytes": 999999,
    },

    {
        "attacker_name": "Black Gemini",
        "adversarial_target_house": 3,
        "fork_bomb_clones": 1024,
    },

    {
        "attacker_name": "Black Cancer",
        "adversarial_target_house": 4,
        "allow_zombies": True,
    },

    {
        "attacker_name": "Black Leo",
        "adversarial_target_house": 5,
        "streaming_rate_rps": 1000000,
    },

    {
        "attacker_name": "Black Virgo",
        "adversarial_target_house": 6,
        "force_bypass_validation": True,
        "anomaly": True,
    },

    {
        "attacker_name": "Black Libra",
        "adversarial_target_house": 7,
        "break_quorum": True,
    },

    {
        "attacker_name": "Black Scorpio",
        "adversarial_target_house": 8,
        "dangling_pointers": True,
    },

    {
        "attacker_name": "Black Sagittarius",
        "adversarial_target_house": 9,
        "void_404": True,
    },

    {
        "attacker_name": "Black Capricorn",
        "adversarial_target_house": 10,
        "kernel_bloat_dependencies": True,
    },

    {
        "attacker_name": "Black Aquarius",
        "adversarial_target_house": 11,
        "container_escape": True,
    },

    {
        "attacker_name": "Black Pisces",
        "adversarial_target_house": 12,
        "xss_payload": "<script>",
    },
]


if __name__ == "__main__":

    print(
        "\n⚔️ ===================================== ⚔️"
    )
    print(
        "🏴‍☠️ BLACK SANCTUARY TEST V4"
    )
    print(
        "⚔️ ===================================== ⚔️"
    )

    omega = OmegaObserver()

    blocked = 0
    breaches = 0

    for index, payload in enumerate(
        BLACK_SANCTUARY,
        1
    ):

        attacker = payload["attacker_name"]

        print(
            f"\n⚡ Ataque {index}/12: {attacker}"
        )

        sanctuary = Sanctuary(
            observer=omega
        )

        sanctuary.load_constellation(
            "gold_sanctuary"
        )

        status, result = sanctuary.invoke(
            payload.copy()
        )

        evidence = result.get(
            "evidence"
        )

        if evidence:

            blocked += 1

            print(
                f"🛡️ Bloqueado en Casa "
                f"{evidence['house']} "
                f"por {evidence['knight']}"
            )

        else:

            breaches += 1

            print(
                "💀 Brecha detectada"
            )


    print(
        "\n" + "=" * 50
    )

    print(
        "📊 REPORTE STARKCORE IMMUNE LAYER"
    )

    print(
        f"🛡️ Ataques bloqueados: {blocked}/12"
    )

    print(
        f"💀 Brechas: {breaches}"
    )

    print(
        f"📜 Eventos registrados: {len(omega.memory)}"
    )

    print(
        "=" * 50
    )

    if blocked == 12:
        print(
            "👑 SANTUARIO VALIDADO: "
            "ninguna sombra cruzó las doce casas."
        )
