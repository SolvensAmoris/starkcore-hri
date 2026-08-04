# Universo Clock - Arquitectura

## Principio

Universo Clock separa estrictamente tres capas:

1. Astronomía (hechos físicos)
2. Calendario (representación temporal)
3. Simbolismo (interpretaciones opcionales)

Ninguna capa superior modifica la inferior.

---

# Arquitectura

Fecha UTC
    │
    ▼
┌──────────────────────┐
│ Astronomy Engine      │
│                      │
│ • Equinoccios        │
│ • Solsticios         │
│ • Longitud solar     │
│ • Luna               │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Universe Calendar    │
│                      │
│ • Año                │
│ • Mes                │
│ • Día                │
│ • Semana             │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Symbolic Layer       │
│                      │
│ • Arquetipos Jung    │
│ • Astrología         │
│ • Tarot              │
│ • I Ching            │
│ • Otros sistemas     │
└──────────────────────┘

---

# Organización del proyecto

universo_clock/

    astronomy/
        equinox.py
        ecliptic.py
        moon.py

    calendar/
        universe_calendar.py

    symbolic/
        jung.py
        astrology13.py
        tarot.py
        iching.py

    core.py

---

# Principio de Diseño

La astronomía produce datos objetivos.

El calendario organiza esos datos.

La capa simbólica únicamente interpreta esos datos.

Nunca al revés.

---

# Ventajas

✔ Astronomía verificable.

✔ Calendario independiente.

✔ Sistemas simbólicos intercambiables.

✔ Compatible con StarkCore.

✔ Sin mezclar ciencia con interpretación.

---

# Filosofía

Los símbolos no alteran el universo.

El universo proporciona un marco estable sobre el cual diferentes lenguajes simbólicos pueden proyectar significado.

Cada interpretación es una vista del mismo dato, no una modificación del dato.
