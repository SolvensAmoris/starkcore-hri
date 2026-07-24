Solvens Amoris - StarkCore Defense Software
 CA-002 Firewall - Evidencia Viva

> StarkCore CA-002 - Semantic Firewall
> No filtra paquetes. Filtra **significado**. Distingue tag ligero `E==H` mutable vs anotado `E!=H` inmutable con `git cat-file -t`.

**Evidencia Viva:** [PASSED #2703508639](https://gitlab.com/luis.albm77/ca002-gitlab-test/-/pipelines/2703508639) vs [BLOCKED #2703507877](https://gitlab.com/luis.albm77/ca002-gitlab-test/-/pipelines/2703507877) - Validado contra paper ACM REP '26 (10.2M mutaciones)

[![MIT License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Author](https://img.shields.io/badge/Author-Luis%20Alberto%20Burciaga%20Mtz-blue)](https://mx.linkedin.com/in/luis-burciaga-680905311)
[![StarkCore](https://img.shields.io/badge/StarkCore-CA--002-orange)](https://gitlab.com/luis.albm77/ca002-gitlab-test)

Objetivo
Firewall semántico contra CA-002 Trust Boundary Failure.
Distingue tag ligero (E==H mutable) vs tag anotado (E!=H inmutable) RFC-0007.

Implementación
```yaml
ca002-firewall:
  script:
      - TYPE=$(git cat-file -t $CI_COMMIT_TAG)
          - |
                if [ "$TYPE" = "commit" ]; then
                        echo "[STARKCORE] E==H DETECTED - BLOCKED"
                                exit 1
                                      else
                                              echo "[STARKCORE] E!=H VERIFIED - PASSED"
                                                    fi
                                                      rules:
                                                          - if: $CI_COMMIT_TAG