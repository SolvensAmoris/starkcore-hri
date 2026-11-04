from enum import Enum
from collections import defaultdict, deque

class Verdict(Enum):
    ACCEPT = "ACCEPT"
    REJECT = "REJECT"
    ESCALATE = "ESCALATE"

class Health(Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"

def _vs(v):
    if isinstance(v, Verdict): return v.value
    if isinstance(v, str):
        u=v.upper()
        if "REJECT" in u: return "REJECT"
        if "ESCALATE" in u: return "ESCALATE"
        return "ACCEPT"
    return getattr(v, 'value', str(v)).upper()

def propagate(nodes, edges):
    norm={}
    for k,v in nodes.items():
        vs=_vs(v.get("verdict","ACCEPT"))
        # degraded: si viene health=DEGRADED o degraded=True
        h=v.get("health", Health.HEALTHY)
        if isinstance(h, Health):
            deg = (h==Health.DEGRADED)
        elif isinstance(h, bool):
            deg = h
        else:
            deg = "DEGRAD" in str(h).upper()
        if "degraded" in v:
            # degraded explicito domina
            deg = bool(v["degraded"]) if isinstance(v["degraded"], bool) else deg or ("DEGRAD" in str(v["degraded"]).upper())
        norm[k]={"verdict": vs, "degraded": deg}

    adj=defaultdict(list)
    all_nodes=set(norm.keys())
    for s,d in edges:
        adj[s].append(d)
        all_nodes.add(s); all_nodes.add(d)
    for n in all_nodes:
        if n not in norm:
            norm[n]={"verdict":"ACCEPT","degraded":False}

    # cycle raise
    vis=set(); rec=set()
    def dfs(u, path):
        vis.add(u); rec.add(u); path.append(u)
        for w in adj[u]:
            if w not in vis:
                dfs(w, path)
            elif w in rec:
                raise ValueError(f"CYCLE_DETECTED: {'->'.join(path[path.index(w):]+[w])}")
        rec.remove(u); path.pop()
    for n in list(all_nodes):
        if n not in vis:
            dfs(n, [])

    # propagate both verdict and degraded
    from collections import deque
    q=deque([k for k,v in norm.items() if v["verdict"]!="ACCEPT" or v["degraded"]])
    in_q=set(q)
    while q:
        cur=q.popleft()
        cur_v=norm[cur]["verdict"]
        cur_d=norm[cur]["degraded"]
        for nb in adj[cur]:
            ch=False
            if cur_v=="REJECT" and norm[nb]["verdict"]!="REJECT":
                norm[nb]["verdict"]="REJECT"; ch=True
            elif cur_v=="ESCALATE" and norm[nb]["verdict"]=="ACCEPT":
                norm[nb]["verdict"]="ESCALATE"; ch=True
            if cur_d and not norm[nb]["degraded"]:
                norm[nb]["degraded"]=True; ch=True
            if ch and nb not in in_q:
                q.append(nb); in_q.add(nb)

    out={}
    for k,v in norm.items():
        out[k]={"verdict":v["verdict"],"degraded":v["degraded"],"health": Health.DEGRADED if v["degraded"] else Health.HEALTHY}
    return out

def enforce(d):
    res={}
    for k,v in d.items():
        vs=_vs(v.get("verdict"))
        deg=bool(v.get("degraded", False))
        # also check health
        if "health" in v and not deg:
            h=v["health"]
            if isinstance(h, Health): deg=(h==Health.DEGRADED)
            elif "DEGRAD" in str(h).upper(): deg=True
        res[k]={"verdict":vs,"degraded":deg,"decision":"REJECT" if vs=="REJECT" else "ACCEPT"}
    return res
