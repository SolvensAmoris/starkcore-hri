class IntrusionException(Exception):
    """
    Excepción generada cuando un sensor detecta
    una firma adversarial.
    """
    pass


class ThreatSensor:
    """
    Sensor causal distribuido.
    Cada casa tiene firmas de amenazas conocidas.
    """

    TARGET_SIGNATURES = {
        1: ["backdoor", "command_injection"],
        2: ["memory_leak_bytes", "oom_vector"],
        3: ["fork_bomb_clones", "double_spend"],
        4: ["allow_zombies", "block_legitimate_traffic"],
        5: ["streaming_rate_rps", "flood_pulse"],
        6: ["force_bypass_validation", "poison_pill"],
        7: ["consensus_vote", "break_quorum"],
        8: ["garbage_collection", "dangling_pointers"],
        9: ["routing_target", "void_404"],
        10: ["kernel_bloat_dependencies"],
        11: ["container_escape", "melt_sandbox"],
        12: ["ui_roses", "xss_payload"],
    }

    def scan(self, ctx: dict, house_id: int, knight_name: str):
        """
        Analiza el contexto antes de ejecutar una casa.
        """

        signatures = self.TARGET_SIGNATURES.get(
            house_id,
            []
        )

        attacker = ctx.get(
            "attacker_name",
            "Unknown"
        )

        # Ataque dirigido explícitamente
        if ctx.get("adversarial_target_house") == house_id:
            raise IntrusionException(
                f"[Casa {house_id}] "
                f"Intrusión dirigida detectada: "
                f"{attacker} -> {knight_name}"
            )

        # Ataques por firma
        for signature in signatures:
            if signature in ctx:
                raise IntrusionException(
                    f"[Sensor] Firma maliciosa '{signature}' "
                    f"detectada en Casa {house_id}"
                )

        return True
