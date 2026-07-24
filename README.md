# ca002-check RFC-0007

## Regla
- Ligero E==H -> BLOCKED
- Anotado E!=H -> PASSED

## Evidencia actual
- v2.0.0-firewall PASSED #2703450896
- bad-test FAILED #2703454803

## Test final
- git tag v0.9.0-bad -> debe FAIL
- git tag -a v1.0.0-good -m "release" -> debe PASS
