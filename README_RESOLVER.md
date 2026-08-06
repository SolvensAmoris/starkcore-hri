# StarkCore + Cosmos + Solvens - Resolver Integrado

## 4 Componentes
1. cosmos-core: AttestedDAG + SeedChannel + attest()
2. CosmosDAG: topological_order() verificable
3. solvens-core: DepProblem (exactly_one + if_then + require)
4. starkcore-resolver-demo: bridge con Santuario

## Performance
- PKGS=1000, vars=3001 -> 0.0226s
- Algoritmo: Horn SAT + Exactly-One propagation O(n+edges)
- Antes: O(2^n) bruteforce

## Integracion Santuario
santuario.load_constellation("gold", executors={
  "VirgoKnight": CosmosValidationExecutor(),
  "CapricornKnight": SolvensKernelExecutor()
})

## Test
- python3.14 bench_1000.py
- python3.14 test_santuario_cosmos.py
- python3.14 starkcore-resolver-demo-final.py

## Arquitectura
Sanctuary
 - VirgoKnight (Shaka) -> CosmosValidationExecutor (CA002 + Borromeo TIGHT)
 - CapricornKnight (Shura) -> SolvensKernelExecutor (s_fast + AttestedDAG + build_dag)

## Estado
CORAZON LATIENDO - 1001 nodos attestados en 22ms
