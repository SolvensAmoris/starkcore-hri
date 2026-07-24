# Solvens Amoris – StarkCore Defense Software
**CA-002 Firewall – Evidencia Viva**

![MIT License](https://img.shields.io/badge/License-MIT-green)
![Author](https://img.shields.io/badge/Author-Luis%20Alberto%20Burciaga%20Miker-blue)
![StarkCore](https://img.shields.io/badge/StarkCore-CA--002-orange)

## Objetivo
Firewall semántico contra CA-002 Trust Boundary Failure.
Distingue tag ligero (E==H mutable) vs tag anotado (E!=H inmutable) RFC-0007.

## Implementación
```yaml
ca002_firewall:
  script:
    - git cat-file -t $CI_COMMIT_TAG | grep -q tag

