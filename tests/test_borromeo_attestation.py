import sys
sys.path.insert(0,'src')
from starkcore.validators.borromeo_validator import Hypothesis, BorromeoValidator
v=BorromeoValidator()
H={k:True for k in ["n=0","n=1","n=inf","fijo","inversion","limite"]}

def test_attestation_valida():
    h=Hypothesis("c1c7951",500,25,0,8,["6327f3e","301c88b"],{"S10"},{"S10"},H)
    assert v.validate(h)["verdict"]=="BORROMEO_TIGHT"

def test_attestation_detecta_estado_invalido():
    h=Hypothesis("fake-invalid",10,20,0,0,["a"],{"P0"},{"P0"},{"x":True})
    r=v.validate(h)
    assert r["verdict"]=="REJECTED" and "C1" in r["reason"]

def test_attestation_detecta_commit_vacio():
    h=Hypothesis("fake-empty",10,5,1,2,[],{"a"},{"a"},H)
    r=v.validate(h)
    assert r["verdict"]=="REJECTED" and "C3" in r["reason"]
