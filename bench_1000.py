import sys
sys.path.insert(0, "solvens-core")
from dep_solver.core import DepProblem
import time, random

p=DepProblem()
# 1000 paquetes, 3 versiones cada uno = 3000 vars
PKGS=1000
for i in range(PKGS):
    p.exactly_one(f"pkg{i}", [f"{j}.0.0" for j in range(3)])

# cadena de deps: myapp -> pkg0 -> pkg1 ->... -> pkg999
p.require("myapp","1.0.0")
p.exactly_one("myapp",["1.0.0"])
deps=[]
prev=("myapp","1.0.0")
for i in range(PKGS):
    cur=(f"pkg{i}","0.0.0")
    p.if_then(prev, cur)
    deps.append((prev, cur))
    prev=cur

start=time.time()
res=p.solve()
elapsed=time.time()-start
print(f"PKGS={PKGS} vars={len(p.vars)} solved in {elapsed:.4f}s")
print(f"OK={res is not None} selected={sum(1 for v in res.values() if v)}")
# verifica orden DAG
from dep_solver.dag import build_dag
chosen=[(pkg,ver) for (pkg,ver),ok in res.items() if ok]
order=build_dag(chosen, deps)
print(f"ORDER len={len(order)} first={order[:3]} last={order[-3:]}")
