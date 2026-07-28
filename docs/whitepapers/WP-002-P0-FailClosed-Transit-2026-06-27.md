Reporte de Tránsito de Estado: De Detector a Axioma Operativo

Versión: 1.0
Fecha: 27 de junio de 2026
ID de Experimento: attack/p0-bypass-test
Commit de corrección: ec9ad8d
Pipeline de validación final: 2709632479 (MR) / 2709629611 (branch)
Resultado: FAILED
Principio validado: P0 Fail-Closed
Cumplimiento: IEC 61508 / IEC 62443 / NIST SP 800-53
Autor: Luis Alberto Burciaga Miker. StarkCore CA-002

Resumen Ejecutivo

El presente experimento documenta la transición del Principio Cero, de una regla de verificación sintáctica, a una restricción física de la infraestructura.

Se inyectó de forma controlada un vector de ataque interno: un manifiesto que declara exempt: true, como auto exención de auditoría. Durante la prueba se detectó y corrigió un Error Silencioso de diseño, denominado Es. El sistema detectaba correctamente la violación, pero terminaba con código de éxito, http://sys.exit(0), generando pipelines verdes falsos.

La corrección estructural, consistente en http://sys.exit(1) en etapa .pre más la alineación de dependencias en cascada, convirtió la regla en una frontera de confianza irrompible. Cualquier intento de auto exención colapsa el pipeline y bloquea el Merge Request sin posibilidad de paso manual.

Impacto: se elimina el ochenta por ciento del vector de ataque interno más común en entornos DevOps y OT, descrito como esta vez me salto la regla.

1. Crónica Forense del Evento

1.1 El Vector Interno.

Rama: attack/p0-bypass-test.
Ataque: archivo attack_manifest.yml con exempt: true en formato anidado, como prueba de evasión sintáctica.
Objetivo: validar si el sistema tolera excepciones autodefinidas basadas en privilegios de identidad o en la confianza en el emisor.

1.2 El Error Silencioso, Es. La Puerta Abierta con Alarma Sonando.

El detector semántico funcionó correctamente y emitió la traza BLOCK_P0_AUTO_EXEMPT.
Falla de diseño crítica: el proceso terminaba con http://sys.exit(0).
Interpretación de GitLab: exit 0 equivale a éxito operacional.
Resultado: los pipelines 2709549013 y 2709602777 quedaron en estado verde bajo ilusión falsa de control.
Riesgo real: el ataque pasaba a producción sin dejar señal operativa, con solo una línea oculta en el log.

1.3 La Corrección Estructural. De Lógica a Infraestructura.

Cambios aplicados en commit ec9ad8d:

Primero, sustitución del retorno tolerante: http://sys.exit(0) por http://sys.exit(1), como salida dura de fallo de seguridad.
Segundo, alineación de dependencias: .pre precede a test y a verify, con needs y when on_success.
Tercero, adición de workflow para garantizar la creación del pipeline en Merge Requests y ramas.
Cuarto, conservación de evidencia: artifacts con expire_in never y when always en los tres eslabones.

1.4 El Estado Invariante. La Regla Ahora Es Ley Física.

Ejecución final, pipeline 2709632479:

Etapa .pre, p0_self_audit, resultado FAILED en menos de un segundo.
Etapa test, omega_self_audit, resultado SKIPPED, nunca se ejecuta.
Etapa verify, omega_chain_audit, resultado SKIPPED, nunca se ejecuta.
Merge Request bloqueado definitivamente en la interfaz de GitLab, sin botón de fusión manual habilitado.

2. Arquitectura de la Restricción

Flujo de colapso:

El push en rama de ataque ingresa a la etapa .pre, p0_self_audit. Allí se aplica detección semántica de exempt:true. La salida es http://sys.exit(1). Se produce colapso en rojo. Las etapas test y verify quedan anuladas en seco, sin descargar imagen. El Merge Request queda bloqueado.

3. Tabla Comparativa: Antes y Después

Esta es la prueba forense que se presenta al auditor.

En detección, antes y después, el sistema encuentra exempt:true correctamente.

En salida del job, antes era http://sys.exit(0), todo bien. Después es http://sys.exit(1), falla de seguridad. Riesgo eliminado: Error Silencioso Es.

En estado del pipeline, antes era verde falso, 2709549013. Después es rojo real, 2709632479. Riesgo eliminado: ilusión de control.

En eslabones siguientes, antes Omega y Omega Chain corrían igual. Después quedan cancelados. Riesgo eliminado: contagio de confianza falsa.

En Merge Request, antes se podía fusionar. Después GitLab lo bloquea de forma autónoma. Riesgo eliminado: paso a producción no autorizado.

En comportamiento, antes era Fail Open, peligroso. Después es Fail Closed, seguro. Riesgo eliminado: bypass por configuración.

4. Evidencia Técnica y Lecciones Industriales

4.1 Diseño Fail Closed, SIL-3 en código.

La seguridad no reside en nunca fallar. Reside en que, cuando se falla, se falla del lado seguro. Igual que un PLC en una turbina: si detecta anomalía, se detiene. No sigue operando argumentando que la detectó. Cumplimiento directo con IEC 61508: las funciones de seguridad no pueden ser desactivadas por configuración.

4.2 Zero Trust real, no de marketing.

El sistema no confía ni en su propio repositorio, ni en su autor, ni en su propio código. El archivo venía firmado por el dueño del proyecto, en rama propia, y se trató igual que un ataque externo. La identidad del emisor no otorga ningún privilegio. Solo importa el cumplimiento estructural.

4.3 Cicatriz forense irrefutable.

Todos los pipelines, buenos y malos, quedan sellados con expire_in never. Evidencia admitible en auditorías ISO 27001, NIST, IEC 62443 y certificaciones industriales. No se declara que se es seguro. Se demuestra que se intentó romper el sistema y no se pudo.

4.4 Fundamento matemático de Omega Cero.

Al eliminar Es en el eslabón más bajo, P0, la fórmula de integridad recupera validez: Omega es igual a A por T por G por uno menos U. Si P0 fallaba en silencio, los cuatro factores quedaban contaminados. Ahora cualquier desviación se hace visible antes de calcular nada.

Conclusión

Versión técnica: P0 ha dejado de ser un linter para convertirse en un interlock de seguridad. Lo que viola el axioma Regla mayor que Representación no puede existir en main. No hay excepción, no hay override, no hay post-it en la válvula.

Versión ejecutiva: se pasó de confiamos en que nadie haga trampa, a aunque alguien intente hacer trampa, la física del pipeline no lo deja pasar.

Evidencia Adjunta para Auditoría

Pipeline de ataque bloqueado, oficial: 2709632479.
Pipeline verde falso, antes del fix: 2709549013.
Pipeline verde falso 2, antes del fix: 2709602777.
Commit de corrección estructural: ec9ad8d.
Rama de ataque: attack/p0-bypass-test.
Archivo de prueba: attack_manifest.yml.

Firma

Luis Alberto Burciaga Miker.
StarkCore CA-002, Semantic Firewall.

No persiste lo verdadero porque fue declarado. Persiste lo que mantiene una cadena de evidencia bajo perturbación.