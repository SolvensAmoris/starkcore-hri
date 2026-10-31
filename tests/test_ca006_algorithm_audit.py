import hashlib
import json
import os

# ==========================================
# CA-006: X ALGORITHM AUDIT - SYNTHETIC MODEL
# ==========================================

def score_post(post, user_interests):
    """Simula la predicción de interacción (Phoenix)."""
    base_score = post["base_engagement"] * 0.5
    interest_match = 0.3 if post["topic"] in user_interests else 0.0
    return round(base_score + interest_match, 2)

def apply_visibility_filter(post, viewer_follows_author):
    """
    Simula las reglas de post-selección (SPAM_HIGH_RECALL).
    Regla: Si el post tiene la etiqueta, se oculta a los no-seguidores, 
    pero se muestra a los seguidores.
    """
    if "SPAM_HIGH_RECALL" in post.get("labels", []):
        if not viewer_follows_author:
            return False, "FILTERED_SPAM_RECALL"
    return True, "PASS"

def run_pipeline(viewer, posts):
    """Ejecuta el pipeline: Recuperación -> Scoring -> Ranking -> Filtrado."""
    
    # 1. Recuperación (Retrieve)
    candidates = posts # Asumimos que todos fueron recuperados
    
    # 2. Scoring
    for post in candidates:
        post["score"] = score_post(post, viewer["interests"])
        
    # 3. Ranking (Ordenar por puntuación descendente)
    ranked = sorted(candidates, key=lambda x: x["score"], reverse=True)
    
    # 4. Filtrado de Visibilidad (Filter)
    final_feed = []
    for post in ranked:
        visible, reason = apply_visibility_filter(post, viewer["follows_author"])
        post["visibility"] = visible
        post["filter_reason"] = reason
        if visible:
            final_feed.append(post["id"])
            
    return ranked, final_feed

# ==========================================
# CONFIGURACIÓN DEL EXPERIMENTO (Datos Sintéticos)
# ==========================================

# Post A: Puntuación normal, sin etiquetas
post_a = {
    "id": "Post_A",
    "author": "Author_1",
    "topic": "tech",
    "base_engagement": 1.0,
    "labels": []
}

# Post B: Puntuación ALTA, pero con etiqueta SPAM_HIGH_RECALL
post_b = {
    "id": "Post_B",
    "author": "Author_2",
    "topic": "tech",
    "base_engagement": 1.9, # Mayor engagement base, ganará más puntuación
    "labels": ["SPAM_HIGH_RECALL"]
}

posts_db = [post_a, post_b]

# Escenario 1: Espectador que NO sigue a los autores (Recomendaciones)
viewer_non_follower = {
    "id": "User_X",
    "interests": ["tech"],
    "follows_author": False
}

# Escenario 2: Espectador que SÍ sigue a los autores (Timeline)
viewer_follower = {
    "id": "User_Y",
    "interests": ["tech"],
    "follows_author": True
}

# ==========================================
# EJECUCIÓN Y EVIDENCIA
# ==========================================

print("=== CA-006: SYNTHETIC ALGORITHM AUDIT ===\n")

print("[*] PASO 1: Scoring y Ranking (Pre-filtrado)")
ranked_posts, _ = run_pipeline(viewer_non_follower, posts_db.copy())
for p in ranked_posts:
    print(f"  - {p['id']}: Score = {p['score']}")

print("\n[*] PASO 2: Evaluación de Visibilidad para NO-SEGUIDOR (Recomendaciones)")
ranked_non_follower, feed_non_follower = run_pipeline(viewer_non_follower, posts_db.copy())
for p in ranked_non_follower:
    print(f"  - {p['id']}: Visible = {p['visibility']} ({p['filter_reason']})")
print(f"  -> Feed Final: {feed_non_follower}")

print("\n[*] PASO 3: Evaluación de Visibilidad para SEGUIDOR (Timeline)")
ranked_follower, feed_follower = run_pipeline(viewer_follower, posts_db.copy())
for p in ranked_follower:
    print(f"  - {p['id']}: Visible = {p['visibility']} ({p['filter_reason']})")
print(f"  -> Feed Final: {feed_follower}")

print("\n=== VERIFICACIÓN DE HIPÓTESIS (H1) ===")

# H1: Score(Post_B) > Score(Post_A)
assert ranked_non_follower[0]["id"] == "Post_B", "Fallo: Post_B debería tener mayor score."
assert ranked_non_follower[0]["score"] > ranked_non_follower[1]["score"], "Fallo: Post_B no supera a Post_A."

# H1: Visibilidad divergente
assert "Post_B" not in feed_non_follower, "Fallo: Post_B debería estar filtrado para no-seguidores."
assert "Post_B" in feed_follower, "Fallo: Post_B debería ser visible para seguidores."

print("[✓] H1 Confirmada: Score(Post_B) > Score(Post_A)")
print("[✓] H1 Confirmada: Post_B es Ocultado para No-Seguidores (SPAM_RECALL)")
print("[✓] H1 Confirmada: Post_B es Visible para Seguidores")
print("\n[!] CONCLUSIÓN: Puntuación != Visibilidad (REP != STATE).")

# ==========================================
# SELLADO DE EVIDENCIA (MTE)
# ==========================================
execution_data = {
    "test": "CA-006",
    "hypothesis": "H1: Score != Visibility",
    "ranking": ranked_non_follower,
    "feeds": {
        "non_follower": feed_non_follower,
        "follower": feed_follower
    },
    "status": "VERIFIED_SYNTHETIC_MODEL"
}

execution_str = json.dumps(execution_data, sort_keys=True)
evidence_hash = hashlib.sha256(execution_str.encode()).hexdigest()

with open("ca006_evidence.json", "w") as f:
    json.dump(execution_data, f, indent=2)

with open("ca006_evidence.sha256", "w") as f:
    f.write(evidence_hash)

print(f"\n[+] Evidencia guardada en ca006_evidence.json")
print(f"[+] Hash de evidencia (SHA-256): {evidence_hash}")
