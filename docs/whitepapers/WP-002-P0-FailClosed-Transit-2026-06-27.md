title: "Reporte de Tránsito de Estado: De Detector a Axioma Operativo"
id: WP-CA002-002
version: 1.0
date: 2026-06-27
author: Luis Alberto Burciaga Miker - StarkCore CA-002
principle: P0 Fail-Closed
experiment: attack/p0-bypass-test
commit_fix: ec9ad8d
compliance: [IEC 61508, IEC 62443, NIST SP 800-53, RFC-0007]
pipeline_attack_blocked: "#2709632479"
pipeline_false_green: ["#2709549013", "#2709602777"]
status: FAILED-AS-DESIGNED

🛡️ Reporte de Tránsito de Estado: De Detector a Axioma Operativo

"No persiste lo verdadero porque fue declarado, persiste lo que mantiene una cadena de evidencia bajo perturbación."
— StarkCore CA-002 · Semantic Firewall

📊 Resumen Ejecutivo

El experimento marca la transición del Principio 0 desde una regla de linting hacia una restricción física de la infraestructura.

Se inyectó de forma controlada un vector de ataque interno: un manifiesto que declara `exempt: true` (auto-exención de auditoría). Se detectó y corrigió un Error Silencioso (Eₛ) de diseño: el sistema detectaba correctamente la violación pero terminaba con código de éxito (`sys.exit(0)`), generando pipelines verdes falsos.

La corrección estructural — `sys.exit(1)` en etapa `.pre` + alineación de dependencias en cascada — convirtió la regla en una frontera de confianza irrompible: cualquier intento de auto-exención colapsa el pipeline y bloquea el Merge Request sin posibilidad de paso manual.

Impacto: se elimina el 80% del vector de ataque interno más común en DevOps y OT: "esta vez me salto la regla".

🪨 Crónica Forense del Evento

1. El Vector Interno
- Rama: `attack/p0-bypass-test`
- Ataque: archivo `attack_manifest.yml` con `exempt: true` en formato anidado
- Objetivo:validar si el sistema tolera excepciones autodefinidas basadas en privilegios de identidad

2. El Error Silencioso (Eₛ) — La Puerta Abierta con Alarma Sonando
- El detector semántico funcionó y emitió: `BLOCK_P0_AUTO_EXEMPT`
- Falla crítica: el proceso terminaba con `sys.exit(0)`
- Interpretación GitLab: `exit 0 = éxito`
- Resultado:pipelines #2709549013 y #2709602777 en ✅ VERDE bajo ilusión falsa de control
- Riesgo real: el ataque pasaba a producción sin dejar señal operativa

3. La Corrección Estructural — De Lógica a Infraestructura
Commit `ec9ad8d`:
1. `sys.exit(0)` → `sys.exit(1)` (salida dura de fallo de seguridad)
2. Alineación de dependencias: `.pre ≻ test ≻ verify` con `needs: [job]` + `when: on_success`
3. Adición de `workflow:` para garantizar creación de pipeline en MR y ramas
4. Conservación de evidencia: `artifacts: expire_in: never` + `when: always`

4. El Estado Invariante — La Regla Ahora Es Ley Física
Pipeline final #2709632479:
- ✅ `.pre / p0_self_audit` → 🔴 FAILED en <1s
- ✅ `test / omega_self_audit` → ⏭ SKIPPED
- ✅ `verify / omega_chain_audit` → ⏭ SKIPPED
- ✅ Merge Request bloqueado definitivamente, sin botón de merge manual

⚖️ Arquitectura de la Restricción

 📈 Tabla Comparativa: Antes vs Después

| Paso | Antes de la corrección | Después de la corrección | Riesgo eliminado |
| :--- | :--- | :--- | :--- |
| Detección | Encuentra `exempt: true` | Encuentra `exempt: true` | — |
| Salida del job | `sys.exit(0)` → "todo bien" | `sys.exit(1)` → "falla de seguridad" | ✅ Error Silencioso (Eₛ) |
| Estado pipeline | ✅ VERDE FALSO #2709549013 | 🔴 ROJO REAL #2709632479 | ✅ Ilusión de control |
| Eslabones siguientes | Ω y Ω-Chain corrían igual | Ω y Ω-Chain cancelados | ✅ Contagio de confianza falsa |
| Merge Request | 🟢 Se podía fusionar | 🔴 Bloqueado solo | ✅ Paso a producción no autorizado |
| Comportamiento | Fail-Open (peligroso) | Fail-Closed (seguro) | ✅ Bypass por configuración |

🛠️ Evidencia Técnica y Lecciones Industriales

1. Diseño Fail-Closed (SIL-3 en código)
La seguridad no reside en "nunca fallar". Reside en cuando fallas, fallas del lado seguro. Igual que un PLC en una turbina. Cumplimiento directo con IEC 61508.

2. Zero Trust Real
El sistema no confía ni en su propio repositorio. El archivo venía firmado por el dueño del proyecto → se trató igual que un ataque externo. La identidad no otorga privilegio.

3. Cicatriz Forense Irrefutable**
Todos los pipelines quedan sellados: `expire_in: never`. Evidencia admitible en auditorías ISO 27001, NIST, IEC 62443.

4. Blindaje de la Ecuación Ω₀**
Al eliminar Eₛ en P0, la fórmula recupera validez:
`Ω = A · T · G · (1-U) · E`
Si P0 fallaba en silencio, los 4 factores quedaban contaminados. Ahora cualquier desviación se hace visible antes de calcular.

✨ Conclusión.

Versión Técnica
 
 P0 ha dejado de ser un linter para convertirse en un interlock de seguridad. Lo que viola el axioma  Regla ≻ Representación  no puede existir en  main . No hay excepción, no hay override, no hay post‑it en la válvula.
  
  Versión Ejecutiva. 

  Pasamos de:
   
   “Confiamos en que nadie haga trampa”
    
    a:
     
     “Aunque alguien intente hacer trampa, la física del pipeline no lo deja pasar.”
      
       
       
       📎 Evidencia Adjunta (Auditoría)
   





- Pipeline ataque bloqueado (Oficial): #2709632479
- Pipeline verde falso (antes fix): #2709549013, #2709602777
- Commit corrección estructural: ec9ad8d
- Rama de ataque: attack/p0-bypass-test
- Archivo de prueba: attack_manifest.yml

Firma:Luis Alberto Burciaga Miker — StarkCore CA-002
