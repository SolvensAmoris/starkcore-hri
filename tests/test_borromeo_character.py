import sys
sys.path.insert(0,'src')
from starkcore.validators.borromeo_validator import Hypothesis, BorromeoValidator
v=BorromeoValidator()
H={k:True for k in ["n=0","n=1","n=inf","fijo","inversion","limite"]}

def test_rechaza_falso_C1_compresion_cobarde():
    h=Hypothesis("falso-c1",120,18,10,0,["p0","p1"],{"a"},{"a"},H)
    assert "C1" in v.validate(h)["reason"]

def test_rechaza_falso_C2_terreno_propio():
    h=Hypothesis("falso-c2",100,20,5,10,["p0","p1"],{"a"},{"a"},{"n=1":True})
    assert "C2" in v.validate(h)["reason"]

def test_rechaza_falso_C3_premisa_oculta():
    h=Hypothesis("falso-c3",100,20,5,10,["p0","p1"],{"tag"},{"tag","E!=H"},H)
    assert "C3" in v.validate(h)["reason"]

def test_reporte_explica_C3():
    h=Hypothesis("falso-c3b",100,20,5,10,["p0","p1"],{"a"},{"a","oculta"},H)
    r=v.validate(h)
    assert "oculta" in r["reason"]

def test_el_validador_se_rechaza_si_mismo():
    test_rechaza_falso_C1_compresion_cobarde()
    test_rechaza_falso_C2_terreno_propio()
    test_rechaza_falso_C3_premisa_oculta()
