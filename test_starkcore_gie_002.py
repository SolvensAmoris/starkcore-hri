from starkcore_gie_002 import enforce_with_evidence, enforce
def test_enforce_blocks_rejected_nodes():
    r=enforce({"crypto-lib":{"verdict":"REJECT","degraded":False},"application":{"verdict":"ACCEPT","degraded":False}})
    assert r["crypto-lib"]["decision"]=="REJECT" and r["application"]["decision"]=="ACCEPT"
def test_evidence_hash_deterministic():
    r1=enforce_with_evidence({"a":{"verdict":"REJECT","degraded":False}}); r2=enforce_with_evidence({"a":{"verdict":"REJECT","degraded":False}})
    assert r1["a"]["chain"]==r2["a"]["chain"] and r1["a"]["evidence_hash"]==r2["a"]["evidence_hash"] and len(r1["a"]["evidence_hash"])==64
def test_escalate_propagates():
    r=enforce_with_evidence({"dependency":{"verdict":"ESCALATE","degraded":False}}); assert r["dependency"]["decision"]=="ESCALATE"
def test_reject_hash_unique():
    r=enforce_with_evidence({"x":{"verdict":"REJECT","degraded":False},"y":{"verdict":"REJECT","degraded":False}}); assert r["x"]["evidence_hash"]!=r["y"]["evidence_hash"]
def test_three_level_with_evidence():
    nodes={"crypto-lib":{"verdict":"REJECT","degraded":False},"service-api":{"verdict":"REJECT","degraded":True},"application":{"verdict":"REJECT","degraded":True}}
    r=enforce_with_evidence(nodes); assert r["crypto-lib"]["decision"]=="REJECT" and r["service-api"]["degraded"]==True and "REP!=STATE" in r["crypto-lib"]["reason"]
def test_degraded_does_not_mean_reject():
    r=enforce_with_evidence({"a":{"verdict":"ACCEPT","degraded":True}}); assert r["a"]["decision"]=="ACCEPT" and r["a"]["degraded"]==True
