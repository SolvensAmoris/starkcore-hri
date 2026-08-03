from src.starkcore.validators.borromeo_validator import Hypothesis, BorromeoValidator

v = BorromeoValidator()

def test_rechaza_falso_C1_compresion_cobarde():
    h = Hypothesis("falso-c1", 120, 18, 10, 0,
                   ["p0","p1"], {"a"}, {"a"},
                   {k:True for k in ["n=0","n=1","n=inf","fijo","inversion","limite"]})
    r = v.validate(h)
    assert r["verdict"] == "REJECTED" and "C1" in r["reason"]
    print("✓ C1 rechazado")

def test_rechaza_falso_C2_terreno_propio():
    h = Hypothesis("falso-c2", 100, 20, 5, 10,
                   ["p0","p1"], {"a"}, {"a"},
                   {"n=1":True,"n=2":True})
    r = v.validate(h)
    assert r["verdict"] == "REJECTED" and "C2" in r["reason"]
    print("✓ C2 rechazado")

def test_rechaza_falso_C3_premisa_oculta():
    h = Hypothesis("falso-c3-CA002", 100, 20, 5, 10,
                   ["p0","p1","p2"], {"tag"}, {"tag","E!=H"},
                   {k:True for k in ["n=0","n=1","n=inf","fijo","inversion","limite"]})
    r = v.validate(h)
    assert r["verdict"] == "REJECTED" and "C3" in r["reason"]
    print("✓ C3 rechazado")

def test_reporte_explica_C3():
    h = Hypothesis("falso-c3", 100, 20, 5, 10,
                   ["p0","p1"], {"a"}, {"a","oculta"},
                   {k:True for k in ["n=0","n=1","n=inf","fijo","inversion","limite"]})
    r = v.validate(h)
    assert "oculta" in r["reason"] or "CA-002" in r["reason"]
    print("✓ Reporte explica")

def test_el_validador_se_rechaza_si_mismo():
    # Si no rechaza los 3 falsos, se invalida
    test_rechaza_falso_C1_compresion_cobarde()
    test_rechaza_falso_C2_terreno_propio()
    test_rechaza_falso_C3_premisa_oculta()
    print("✓ Auto-rechazo OK")

def test_acepta_starkcore_real():
    h = Hypothesis("301c88b", 200, 20, 0, 10,
                   ["def_F","def_G","I_C"], {"F","G","P","H"}, {"F","G","P","H"},
                   {k:True for k in ["n=0","n=1","n=inf","fijo","inversion","limite"]})
    r = v.validate(h)
    assert r["verdict"] == "BORROMEO_TIGHT"
    print("✓ 301c88b aceptado")
