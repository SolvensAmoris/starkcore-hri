# ca002-check - StarkCore RFC-0007 Firewall

Prevención de CA-002: Tags mutables en releases.

## El Problema (CA-002)
En Git, un tag ligero es solo un puntero: `E == H` (evidencia es igual al hash del commit). Es mutable, se puede mover y borrar sin dejar rastro. No cumple RFC-0007.

Un tag anotado es un objeto inmutable: `E != H` (la evidencia apunta a un objeto `tag` que a su vez apunta al commit). Tiene firma, mensaje y autor.

## La Solución: Firewall Semántico en GitLab CI

Este repo implementa un firewall que **bloquea** releases con tags ligeros y solo permite anotados.

### .gitlab-ci.yml (versión final funcional)

```yaml
stages:
    - audit
    - deploy

ca002_firewall:
  stage: audit
  image:
    name: alpine/git
    entrypoint: [""] # Fix: alpine/git tiene entrypoint git, rompe sh
  script:
        - git fetch --tags
        - git cat-file -t $CI_COMMIT_TAG
        - git cat-file -t $CI_COMMIT_TAG | grep -q tag # Falla si es ligero
        - echo OK_tag_anotado
        - git cat-file -p $CI_COMMIT_TAG
  rules
