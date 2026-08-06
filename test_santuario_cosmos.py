import sys
sys.path.insert(0, ".")
sys.path.insert(0, "solvens-core")

from starkcore.sanctuary.temple import Sanctuary
from starkcore.executors.cosmos_solvers import CosmosValidationExecutor, SolvensKernelExecutor
from cosmos_core import CosmosDAG, CosmosNode
from dep_solver.core import DepProblem

# Usa el loader oficial
santuario = Sanctuary()
santuario.load_constellation("gold", executors={
    "VirgoKnight": CosmosValidationExecutor(),
    "CapricornKnight": SolvensKernelExecutor()
})

dag = CosmosDAG()
dag.add_node(CosmosNode(id="myapp", version="1.0.0"))
dag.add_node(CosmosNode(id="lodash", version="4.17.21"))
dag.add_edge("myapp","lodash")

p=DepProblem()
p.exactly_one('lodash',['4.17.21'])
p.exactly_one('react',['18.3.1'])
p.exactly_one('loose',['1.4.0'])
p.require('myapp','1.0.0')
deps=[(('myapp','1.0.0'),('lodash','4.17.21')),(('myapp','1.0.0'),('react','18.3.1')),(('react','18.3.1'),('loose','1.4.0'))]
for a,b in deps: p.if_then(a,b)

ctx = {"anomaly": False, "dag": dag, "problem": p, "deps": deps, "cosmos_verified": True}

print("\n=== INVOCANDO SANTUARIO CON COSMOS+SOLVENS ===")
status, final = santuario.invoke(ctx)
print(f"\nSTATUS: {status}")
print(f"SOLVENS: {final.get('solvens')}")
print(f"VALIDATION: {final.get('cosmos_validation')}")
print(f"CORE_STATUS: {final.get('core_status')}")
print(f"ORDER: {final.get('install_order')}")
print("\n💓 SANTUARIO + COSMOS + SOLVENS = INTEGRADO")
