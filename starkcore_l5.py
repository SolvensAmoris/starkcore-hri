import hashlib
from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, List, Tuple

class State(Enum):
    UNKNOWN = auto(); LIVE = auto(); STALE = auto(); INVALID = auto()
class Event(Enum):
    CHECK_OK = auto(); POLL_VENCIDO = auto(); CHANGE_DETECTED = auto(); CHECK_ERROR = auto()
class CanonicalState(Enum):
    UNKNOWN = auto(); LIVE = auto(); STALE = auto(); INVALID = auto(); CONFLICT = auto()

TRANSITIONS = {
    State.UNKNOWN: {Event.CHECK_OK: State.LIVE, Event.POLL_VENCIDO: State.UNKNOWN, Event.CHANGE_DETECTED: State.UNKNOWN, Event.CHECK_ERROR: State.UNKNOWN},
    State.LIVE: {Event.CHECK_OK: State.LIVE, Event.POLL_VENCIDO: State.STALE, Event.CHANGE_DETECTED: State.INVALID, Event.CHECK_ERROR: State.LIVE},
    State.STALE: {Event.CHECK_OK: State.LIVE, Event.POLL_VENCIDO: State.STALE, Event.CHANGE_DETECTED: State.INVALID, Event.CHECK_ERROR: State.STALE},
    State.INVALID: {Event.CHECK_OK: State.LIVE, Event.POLL_VENCIDO: State.INVALID, Event.CHANGE_DETECTED: State.INVALID, Event.CHECK_ERROR: State.INVALID},
}
def is_noop(s,e):
    if s==State.LIVE and e==Event.CHECK_OK: return False
    return TRANSITIONS[s][e]==s

@dataclass(frozen=True)
class Fact:
    ref_id: str
    observer_id: str
    version: int
    digest: str
    ts: int
    trigger: Event

DOMAIN = b"STARKCORE_FACT_V1:"
def canonical_bytes(f: Fact) -> bytes:
    return DOMAIN + f"FACT:v1|{f.ref_id}|{f.observer_id}|{f.version}|{f.digest}|{f.ts}|{f.trigger.name}".encode()
def leaf_hash(f: Fact) -> bytes:
    return hashlib.sha256(canonical_bytes(f)).digest()
def merkle_root(facts: List[Fact]) -> bytes:
    if not facts:
        return hashlib.sha256(b"STARKCORE_EMPTY").digest()
    sorted_facts = sorted(facts, key=lambda x: (x.ref_id, x.observer_id, x.version))
    level = [leaf_hash(f) for f in sorted_facts]
    while len(level)>1:
        nxt=[]
        for i in range(0,len(level),2):
            l=level[i]
            r=level[i+1] if i+1 < len(level) else l
            nxt.append(hashlib.sha256(b"NODE:"+l+r).digest())
        level=nxt
    return level[0]

def projections(facts: List[Fact]) -> Dict[str, Tuple[State,str]]:
    logs: Dict[str, List[Fact]] = {}
    for f in facts:
        logs.setdefault(f.observer_id, []).append(f)
    out={}
    for oid, flist in logs.items():
        flist_sorted = sorted(flist, key=lambda x: x.version)
        st=State.UNKNOWN
        last_digest=""
        for fact in flist_sorted:
            # solo si no es no-op segun L2
            if not is_noop(st, fact.trigger):
                st = TRANSITIONS[st][fact.trigger]
                last_digest = fact.digest
            # si es CHECK_OK LIVE->LIVE refresca digest
            elif st==State.LIVE and fact.trigger==Event.CHECK_OK:
                st = State.LIVE
                last_digest = fact.digest
        out[oid]=(st,last_digest)
    return out

def canonical_state(facts: List[Fact]) -> Tuple[CanonicalState, str]:
    projs = projections(facts)
    if not projs:
        return CanonicalState.UNKNOWN, ""
    live_digests: Dict[str, List[str]]={}
    has_invalid=False; has_live=False; has_stale=False
    for oid,(st,dig) in projs.items():
        if st==State.INVALID: has_invalid=True
        if st==State.LIVE:
            has_live=True
            live_digests.setdefault(dig,[]).append(oid)
        if st==State.STALE: has_stale=True
    if len(live_digests)>1:
        return CanonicalState.CONFLICT, "|".join(sorted(live_digests))
    if has_invalid and has_live:
        return CanonicalState.CONFLICT, "LIVE vs INVALID"
    if has_invalid:
        return CanonicalState.INVALID, ""
    if live_digests:
        return CanonicalState.LIVE, list(live_digests.keys())[0]
    if has_stale:
        return CanonicalState.STALE, ""
    return CanonicalState.UNKNOWN, ""

def test_l5():
    f1 = Fact("model.bin","A",1,"abc",100,Event.CHECK_OK)
    f2 = Fact("model.bin","B",1,"abc",101,Event.CHECK_OK)
    f3 = Fact("model.bin","C",1,"abc",102,Event.CHECK_OK)

    # 1. mismos FACTS reordenados -> mismo ROOT y STATE
    root_a = merkle_root([f1,f2,f3])
    state_a = canonical_state([f1,f2,f3])
    root_b = merkle_root([f3,f1,f2])
    state_b = canonical_state([f3,f1,f2])
    assert root_a==root_b, "1 root"
    assert state_a==state_b, "1 state"
    print(f"1 OK: determinismo orden -> ROOT {root_a.hex()[:12]} STATE {state_a}")

    # 2. cambiar digest -> ROOT cambia
    f_mut = Fact("model.bin","A",1,"XXX",100,Event.CHECK_OK)
    root_mut = merkle_root([f_mut,f2,f3])
    state_mut = canonical_state([f_mut,f2,f3])
    assert root_mut!= root_a, "2 root debe cambiar"
    assert state_mut[0]==CanonicalState.CONFLICT, "2 debe ser CONFLICT por digest distinto"
    print("2 OK: digest mutado -> ROOT cambia, STATE CONFLICT")

    # 3. cambiar observer -> ROOT y STATE pueden cambiar
    f_obs = Fact("model.bin","Z",1,"abc",100,Event.CHECK_OK)
    assert merkle_root([f_obs,f2,f3])!= root_a
    print("3 OK: observer cambia -> ROOT cambia")

    # 4. conflicto -> INVALID/CONFLICT
    f_bad = Fact("model.bin","B",2,"DEF",103,Event.CHANGE_DETECTED)
    f_bad2 = Fact("model.bin","B",3,"DEF",104,Event.CHECK_OK)
    state_conf = canonical_state([f1,f_bad,f_bad2])
    assert state_conf[0]==CanonicalState.CONFLICT
    print("4 OK: LIVE vs INVALID -> CONFLICT")

    # 5. quorum consistente -> LIVE
    assert state_a[0]==CanonicalState.LIVE and state_a[1]=="abc"
    print("5 OK: quorum -> LIVE")

    # 6. todos STALE -> STALE
    s1 = Fact("model.bin","A",1,"abc",100,Event.CHECK_OK)
    s2 = Fact("model.bin","A",2,"abc",200,Event.POLL_VENCIDO)
    assert canonical_state([s1,s2])[0]==CanonicalState.STALE
    print("6 OK: STALE")

    # 7. ausencia -> UNKNOWN
    assert canonical_state([])[0]==CanonicalState.UNKNOWN
    print("7 OK: UNKNOWN vacio")

    # 8. mismo ROOT -> mismo STATE
    assert canonical_state([f1,f2,f3])==canonical_state([f2,f3,f1])
    print("8 OK: ROOT igual -> STATE igual")

    # 9. mismo REFERENCE no implica mismo STATE
    f_inv = Fact("model.bin","A",2,"abc",200,Event.CHANGE_DETECTED)
    assert canonical_state([f1])[0]==CanonicalState.LIVE
    assert canonical_state([f1,f_inv])[0]==CanonicalState.INVALID
    print("9 OK: REFERENCE!= STATE")

    # 10. ROOT no reconstruible desde STATE
    # STATE es (LIVE, abc) pero no puedes saber si fueron 2 o 3 FACTS
    root_2 = merkle_root([f1,f2])
    root_3 = merkle_root([f1,f2,f3])
    st_2 = canonical_state([f1,f2])
    st_3 = canonical_state([f1,f2,f3])
    assert st_2==st_3 and root_2!=root_3, "10 STATE pierde info, ROOT no"
    print("10 OK: STATE no -> FACTS, ROOT compromete FACTS")

    print("\nOK: Canonical State L5 - 10 pruebas")
    print(f"REFERENCE=model.bin FACTS=3 ROOT={root_a.hex()[:16]}... STATE={state_a[0].name} STATE DERIVED FROM FACTS ROOT COMMITS TO FACTS")

if __name__ == "__main__":
    test_l5()
