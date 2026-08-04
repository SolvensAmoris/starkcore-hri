action, min_G, optimal_policy = agent.act()

print("=== RESULTADOS INFERENCIA ACTIVA (T=4) ===")
print(f"Estado de Creencia Inicial: {agent.belief}")
print(f"Política Óptima Planificada: {optimal_policy}")
print(f"Energía Libre Esperada (G): {min_G:.4f}")
print(f"Acción a Ejecutar (a_t): {action}")
