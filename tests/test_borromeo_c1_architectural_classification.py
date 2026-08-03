"""
C1 Architectural Classification Test
Distingue MODO_COMPRESION vs MODO_EXPANSION.

Definiciones operativas (unidades deben ser IGUALES entre A y B):
  L = costo: watts * horas, numero de parametros, lineas de especificacion o $
  F = poder: superficie de falsacion, predicciones verificables o cobertura de casos

Reglas:
  COMPRESION     : reduce costo SIN perder poder (C1 real)
  EXPANSION      : aumenta mucho costo para ganancia marginal (C1 fallido)
  EXPANSION_EXTREMA : caso LLM frontier: >10x costo para <5% de ganancia real
  INDEFINIDO     : no hay suficiente diferencia para clasificar
"""
import os

def classify(L_old, L_new, F_old, F_new):
    if F_old == 0:
        dF = float('inf')
    else:
        dF = F_new / F_old
    dL = L_new / L_old

    if dL < 1.0 and dF >= 1.0:
        return "MODO_COMPRESION"
    if dL > 10.0 and dF < 1.05:
        return "MODO_EXPANSION_EXTREMA"
    if dL > 2.0 and dF < 1.5:
        return "MODO_EXPANSION"
    return "INDEFINIDO"

# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
def test_starkcore_h_test_es_compresion():
    # Datos extraidos de evidence/H_TEST_REPORT_v2.md
    L_old = 1e9   # Proxy: 1 GW = referencia paradigma contrario
    L_new = 5     # Medido: H-Test Android UserLAnd ~5W
    F_old = 1     # Antes: 1 forma de ejecutar (datacenter)
    F_new = 12    # Ahora: 12 componentes + 5 experimentos offline
    assert classify(L_old, L_new, F_old, F_new) == "MODO_COMPRESION"

def test_llm_scaling_es_expansion_extrema():
    # GPT-3 -> GPT-4 ~ 10x costo para ~2% mejora real
    L_old = 1.0
    L_new = 12.0
    F_old = 1.0
    F_new = 1.02
    assert classify(L_old, L_new, F_old, F_new) == "MODO_EXPANSION_EXTREMA"

def test_llm_es_expansion_normal():
    assert classify(1, 2.5, 1, 1.25) == "MODO_EXPANSION"

def test_caso_limite_indefinido():
    assert classify(1, 0.9, 1, 0.95) == "INDEFINIDO"
    assert classify(1, 1.8, 1, 1.6) == "INDEFINIDO"

def test_h_test_evidence_existe():
    assert os.path.exists("evidence/H_TEST_REPORT_v2.md")

def test_el_clasificador_se_autoclasifica_como_compresion():
    # Auto-martillo: este test es C1 real
    lineas = open(__file__).read().count("\n")
    # L_old = paper 15 paginas ~6000 lineas, L_new = este archivo
    assert classify(6000, lineas, 1, 6) == "MODO_COMPRESION"
