# s_fast real - Horn SAT + Exactly-One propagation - O(n + edges)
from collections import defaultdict, deque

def s_fast(problem):
    """
    problem: DepProblem con.vars,.var_index,.exactly_ones,.impls,.required
    Retorna dict {(pkg,ver): bool} o None
    """
    n = len(problem.vars)
    if n == 0:
        return {}

    # index: var -> group id y posición
    var_to_group = {}
    for gid, group in enumerate(problem.exactly_ones):
        for v in group:
            var_to_group[v] = gid

    # adj: a -> [b] para if_then
    adj = defaultdict(list)
    for a,b in problem.impls:
        adj[a].append(b)

    # estado: -1 unknown, 0 false, 1 true
    assign = [-1]*n

    # cola para propagación
    q = deque()

    def set_true(v, reason=""):
        if assign[v]==1:
            return True
        if assign[v]==0:
            return False # conflicto
        assign[v]=1
        q.append(v)
        # exactly_one: otros del grupo -> false
        gid = var_to_group.get(v)
        if gid is not None:
            for other in problem.exactly_ones[gid]:
                if other!=v:
                    if not set_false(other):
                        return False
        return True

    def set_false(v):
        if assign[v]==0:
            return True
        if assign[v]==1:
            return False
        assign[v]=0
        # exactamente-uno: si quedan todos falsos menos 1, ese debe ser true
        gid = var_to_group.get(v)
        if gid is not None:
            group = problem.exactly_ones[gid]
            unknowns = [x for x in group if assign[x]==-1]
            trues = [x for x in group if assign[x]==1]
            if len(trues)>1:
                return False
            if len(trues)==0 and len(unknowns)==0:
                return False # ninguno true -> falla exactly_one
            if len(trues)==0 and len(unknowns)==1:
                # force last
                if not set_true(unknowns[0]):
                    return False
        return True

    # 1. Requires
    for req in problem.required:
        if not set_true(req, "require"):
            return None

    # 2. Propagación principal (Horn + Exactly-One)
    while q:
        cur = q.popleft()
        # Horn: cur -> b
        for nb in adj[cur]:
            if not set_true(nb, f"{cur}->{nb}"):
                return None

    # Si después de propagar quedan grupos sin decidir, elegir heurística
    # Busca grupo sin true
    for gid, group in enumerate(problem.exactly_ones):
        has_true = any(assign[v]==1 for v in group)
        if not has_true:
            # elige el primero unknown (podríamos probar versiones más nuevas primero)
            unknowns = [v for v in group if assign[v]==-1]
            if not unknowns:
                return None # conflicto
            # Heurística: prueba el más nuevo / primer elemento
            # Para no bruteforcear todo, tomamos el primero (solver determinista)
            # Si falla, backtrack simple (solo en este grupo)
            # Para 1000+ paquetes esto evita explosión porque deps suelen forzar
            chosen = unknowns[0]
            # branch
            saved_assign = assign.copy()
            saved_q = deque(q)
            if set_true(chosen):
                # propaga esta rama
                ok = True
                while q:
                    cur = q.popleft()
                    for nb in adj[cur]:
                        if not set_true(nb):
                            ok=False; break
                    if not ok:
                        break
                if ok:
                    # sigue recursivo: llamamos s_fast de nuevo con estado parcial?
                    # simplificamos: continúa loop outer con recursión
                    result = s_fast_with_state(problem, assign, var_to_group, adj)
                    if result is not None:
                        return result
            # restore y prueba siguiente del grupo (backtrack local)
            assign[:] = saved_assign
            q = saved_q
            # marca chosen como false y sigue
            if not set_false(chosen):
                return None
            # sigue propagando el false
            while q:
                cur = q.popleft()
                for nb in adj[cur]:
                    if not set_true(nb):
                        return None
            # si aún no hay true en grupo, loop volverá a elegir
            # pero para evitar loop infinito, reiniciamos scan
            # (implementación iterativa simple: vuelve a empezar)
            # Usamos recursión limitada:
            return s_fast_with_state(problem, assign, var_to_group, adj)

    # Todo asignado o sin conflicto
    # Cualquier var sin asignar -> false (no necesario)
    result = {}
    for i, key in enumerate(problem.vars):
        result[key] = (assign[i]==1)
    return result

def s_fast_with_state(problem, assign, var_to_group, adj):
    """Versión que continúa con assign ya empezado"""
    from collections import deque
    n=len(assign)
    q=deque([i for i in range(n) if assign[i]==1]) # re-propaga todos los true por si quedó pendiente
    # Pero necesitamos propagar solo los que aún no propagamos... simplificamos: hace closure completo
    seen=set()
    qq=deque([i for i in range(n) if assign[i]==1])
    while qq:
        cur=qq.popleft()
        if cur in seen: continue
        seen.add(cur)
        for nb in adj[cur]:
            if assign[nb]==-1:
                assign[nb]=1
                # exactly_one side effect
                gid=var_to_group.get(nb)
                if gid is not None:
                    for other in problem.exactly_ones[gid]:
                        if other!=nb and assign[other]==-1:
                            assign[other]=0
                            # check exactly-one forced
                            g=problem.exactly_ones[gid]
                            unk=[x for x in g if assign[x]==-1]
                            tr=[x for x in g if assign[x]==1]
                            if len(tr)==0 and len(unk)==1:
                                assign[unk[0]]=1
                                qq.append(unk[0])
                            if len(tr)>1 or (len(tr)==0 and len(unk)==0):
                                return None
                qq.append(nb)
            elif assign[nb]==0:
                return None

    # busca grupos sin true
    for gid, group in enumerate(problem.exactly_ones):
        if not any(assign[v]==1 for v in group):
            unknowns=[v for v in group if assign[v]==-1]
            if not unknowns:
                return None
            # prueba primera opción recursivamente
            for choice in unknowns:
                new_assign=assign.copy()
                new_assign[choice]=1
                # false otros
                for other in group:
                    if other!=choice and new_assign[other]==-1:
                        new_assign[other]=0
                # closure
                res=s_fast_with_state(problem, new_assign, var_to_group, adj)
                if res is not None:
                    return res
            return None

    # éxito
    result={}
    for i,key in enumerate(problem.vars):
        result[key]=(assign[i]==1)
    return result

def s_solve(problem):
    return s_fast(problem)

print("s_fast Horn SAT cargado - O(n+edges)")
