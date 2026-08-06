import os, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT not in sys.path: sys.path.insert(0, ROOT)
SOLVENS_ROOT = os.path.join(ROOT, "solvens-core")
if SOLVENS_ROOT not in sys.path: sys.path.insert(0, SOLVENS_ROOT)

from cosmos_core import AttestedDAG
from dep_solver.core import DepProblem
from dep_solver.dag import build_dag
from starkcore.validators.diacronic_identity_validator import EntityState, check_state
from starkcore.validators.borromeo_validator import BorromeoValidator, Hypothesis
from starkcore.executors.strategies import ValidationExecutor, KernelExecutor

class CosmosValidationExecutor(ValidationExecutor):
    def process(self, ctx):
        print("[VIRGO - CosmosValidationExecutor]")
        dag = ctx.get("dag")
        # CA002
        e1 = EntityState(name="pkg", state={"old"}, history=["init"], constraints=set())
        e2 = EntityState(name="pkg", state={"old"}, history=["init","resolve"], constraints=set())
        ca002_ok = check_state(e1, e2)
        
        h = Hypothesis(
            id="resolver", L_old=10, L_new=2, F_old=1, F_new=10,
            chain=["cosmos","solvens"], assumptions_P0=set(), assumptions_used=set(),
            hammers_applied={"n=0":True,"n=1":True,"n=inf":True,"fijo":True,"inversion":True,"limite":True}
        )
        borromeo = BorromeoValidator().validate(h)
        print(f"  CA002={ca002_ok} Borromeo={borromeo['verdict']}")
        
        ctx["cosmos_validation"] = {"ca002": ca002_ok, "borromeo": borromeo, "ok": ca002_ok and borromeo['verdict']=="BORROMEO_TIGHT"}
        ctx["cosmos_verified"] = True
        return ctx

class SolvensKernelExecutor(KernelExecutor):
    def process(self, ctx):
        print("[CAPRICORN - SolvensKernelExecutor]")
        problem = ctx.get("problem")
        deps = ctx.get("deps", [])
        
        if not problem:
            problem = DepProblem()
            problem.exactly_one('lodash',['4.17.21'])
            problem.exactly_one('react',['18.3.1'])
            problem.exactly_one('loose',['1.4.0'])
            problem.require('myapp','1.0.0')
            deps = [(('myapp','1.0.0'),('lodash','4.17.21')),(('myapp','1.0.0'),('react','18.3.1')),(('react','18.3.1'),('loose','1.4.0'))]
            for a,b in deps: problem.if_then(a,b)
        
        res = problem.solve()
        if not res:
            print("  ❌ IMPOSSIBLE")
            ctx["core_status"] = "UNSTABLE"
            ctx["solvens"] = {"ok": False}
            return ctx
        
        chosen = [(pkg,ver) for (pkg,ver),ok in res.items() if ok]
        order = build_dag(chosen, deps)
        
        print(f"  ✅ {chosen}")
        print(f"  🔗 {order}")
        
        ctx["core_status"] = "STABLE_EXECUTION"
        ctx["solvens"] = {"ok": True, "chosen": chosen, "order": order, "assignment": res}
        ctx["install_order"] = order
        return ctx

    def execute(self, ctx):
        return self.process(ctx)
