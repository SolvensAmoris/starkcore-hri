StarkCore CA-003 - Mitigacion CVE-2025-30066
Ataque real afecto a 23,000 orgs (tj-actions/changed-files).
StarkCore detecta mutacion en tags ligeros y bloquea ejecucion maliciosa.
Evidencia reproducible:
- v1.0-ligero -> BLOCKED (vulnerable)
- v1.0-bueno -> PASSED (seguro)
- v2.0.0-firewall -> PASSED (protegido)
- v3.0.0-ca003 -> PASSED (mitigacion)
Firewall v2.0.0 + Magika = Proteccion total
Hash: 4fd6112a4c84cf5af7699c6366add24975f800118cf5227ca81e62695e4a4b23
#StarkCore #CVE202530066
