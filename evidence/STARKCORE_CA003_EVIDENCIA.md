# STARKCORE CA-003 - CVE-2025-30066 Mitigation

## Ataque real que afecto 23,000 orgs - tj-actions/changed-files
- Tag v1 ligero mutado por attacker
- Workflow ejecutó código malicioso

## Defensa StarkCore
- Detecta TYPE=commit vs TYPE=tag
- BLOCKED E==H en tags ligeros (mutables)
- PASSED E1==H en tags anotados (SHA inmutable)

## Evidencia OpenLand
v1.0-ligero -> BLOCKED (vulnerable)
v1.0-bueno -> PASSED (seguro)
v2.0.0-firewall -> PASSED

Firewall v2.0.0 + Magika = Protección total
