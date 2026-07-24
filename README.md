# ca002-check RFC-0007

## Regla
- Ligero E==H -> BLOCKED
- Anotado E!=H -> PASSED

## Evidencia
- v2.0.0-firewall PASSED #2703450896
- bad-test FAILED #2703454803

## Test
- git tag v0.9.0-bad && git push origin v0.9.0-bad -> FAILED
- git tag -a v1.0.0-good -m "release" && git push origin v1.0.0-good -> PASSED
