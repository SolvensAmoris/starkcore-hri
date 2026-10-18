# STARKCORE // SOLVENS CORE

**Arquitectura de Ejecución Verificable y Gobernanza Autónoma**

## 📌 Resumen
StarkCore es un runtime defensivo de grado industrial que resuelve el **desacoplamiento ontológico (CA-002)**: la brecha entre lo que un agente *dice* que es y lo que el sistema *demuestra* que es. 

Implementado desde cero en un entorno móvil (Huawei Nova 5T / UserLAnd), combina criptografía de curva elíptica, máquinas de estado formales y evidencia inmutable.

## 🏗️ Arquitectura (Cosmos Terminal)
*   **Ingest / Parser:** Normalización de datos.
*   **Cosmos (DAG Canonicalizer):** Genera un hash estructural determinista e inmune a manipulaciones (Topology-Aware Secure Boot).
*   **Gateway (Runtime):** Valida firmas Ed25519, políticas (Π) y la topología del grafo (DAG).
*   **Jacobian (State):** Gestor de estado de escritura atómica. Solo muta bajo evidencia válida.
*   **Evidence Layer (Bus):** Log encadenado por hashes (Merkle-chain) con detección de truncamiento.

## 🛡️ Hitos de Seguridad Implementados
*   **v0.4 (Crypto):** Firmas Ed25519 y Anti-Replay (Nonces).
*   **v1.0 (Threshold):** Consenso 2-de-3 (Multi-firma distribuida).
*   **v1.1 (Lattice):** Política Π monótona (imposible escalar privilegios).
*   **v1.2 (Dead-Man):** Timeout de 30s fuerza `FAIL_CLOSED` automáticamente.
*   **v1.3.1 (Immutability):** Merkle Log con detección de borrado de cola (`head_hash`).
*   **v1.4 (DAG):** Canonicalización estructural. Inmune a *Type Confusion* e inyección de nodos.
*   **v1.5 (Solvens):** Orquestación completa. Rechazo en seco de artefactos manipulados.

## 🧠 Evidencia Empírica
Todas las pruebas de estrés (Tampering, Replay, PrivEsc, Dead-Man, DAG Injection) se ejecutaron localmente y los logs (`.log`, `.json`) se encuentran en este repositorio. La evidencia está anclada criptográficamente.

---
*"No necesitamos más explicaciones. Necesitamos evidencia."*
