# 🏉 Club Tilcara — Simulador de Licencias

> **Trabajo Práctico Integrador — Organización Empresarial**  
> Tecnicatura Universitaria en Programación a Distancia · UTN · 2026  
> **Integrantes:** NUÑEZ, Lucía · ALTAVISTA, Lucio  
> **Docente:** Prof. Gabriela Martínez

---

## Descripción del proyecto

El **Club Tilcara** es una organización deportiva de rugby amateur ubicada en Paraná, Entre Ríos, con tres divisiones activas (Primera, M20 y M18) y un plantel de aproximadamente 120 jugadores.

Este proyecto automatiza el proceso de **solicitud de licencia de jugador** mediante un chatbot de consola en Python. El proceso anterior era completamente manual: el jugador se comunicaba en persona o por teléfono, el administrativo consultaba un cuaderno físico y el Director Técnico respondía verbalmente días después.

### Ineficiencias del proceso as-is

- Sin trazabilidad: no existía registro formal de cada solicitud
- Demoras de días o semanas entre la solicitud y la respuesta
- Registros manuales en cuadernos, propensos a errores y pérdidas
- Sin notificaciones automáticas al jugador sobre el estado de su solicitud

---

## Estructura del repositorio

```
club-tilcara-bot/
├── simulador_bot.py              # Código fuente del chatbot simulado
├── jugadores.csv                 # Base de datos de jugadores
├── historial_licencias.csv       # Registro histórico de solicitudes
├── bpmn_asis_club_tilcara.svg    # Diagrama BPMN as-is (proceso manual)
├── bpmn_licencia_club_tilcara.svg # Diagrama BPMN to-be (proceso automatizado)
├── TPI_OE_ClubTilcara_Final.pdf  # Informe completo del TPI
└── README.md
```

---

## Diagramas BPMN 2.0

### As-Is — Proceso manual actual

Tres carriles: **Jugador · Administrativo · Director Técnico**

El jugador solicita la licencia en persona o por teléfono. El administrativo busca la planilla física, verifica días disponibles y envía una nota escrita al DT. El DT decide y avisa verbalmente, con demoras de días o semanas.

### To-Be — Proceso automatizado con chatbot

Tres carriles: **Jugador · Sistema / Bot · Director Técnico**

El bot reemplaza al administrativo. Valida al jugador, consulta días disponibles en el CSV y eleva la solicitud al DT. El resultado se notifica de inmediato y los archivos se actualizan automáticamente.

Compuertas exclusivas del flujo to-be:
1. ¿El jugador tiene días disponibles?
2. ¿El DT aprueba la solicitud?

---

## Instalación y uso

### Requisitos

- Python 3.x (sin dependencias externas)
- Los archivos `jugadores.csv` e `historial_licencias.csv` en la misma carpeta que el script

### Ejecutar el simulador


python simulador_bot.py

### Pasos del proceso

| Paso | Acción |
|------|--------|
| 1 | El bot da la bienvenida y solicita el ID del jugador |
| 2 | El jugador ingresa su número de ID (ej: `3`) |
| 3 | El bot confirma nombre, categoría y días disponibles |
| 4 | El jugador ingresa el motivo de la licencia (ej: `Viaje familiar`) |
| 5 | El jugador ingresa cuántos días necesita |
| 6 | El bot informa que la solicitud fue enviada al Director Técnico |
| 7 | El DT ingresa su decisión; el bot notifica y actualiza el CSV |

### Comandos especiales (disponibles en cualquier paso)

| Comando | Acción |
|---------|--------|
| `ayuda` | Muestra las instrucciones del paso actual |
| `salir` | Cancela el proceso |
| `reiniciar` | Vuelve al inicio del flujo |

---

## Máquina de estados del bot

| Estado | Descripción | Siguiente estado posible |
|--------|-------------|--------------------------|
| `INICIO` | Saluda y solicita el ID | `VALIDAR_JUGADOR` |
| `VALIDAR_JUGADOR` | Verifica si el ID existe en el CSV | `CONSULTAR_DIAS` / `ERROR` |
| `CONSULTAR_DIAS` | Verifica días disponibles | `PEDIR_MOTIVO` / `RECHAZAR_SIN_DIAS` |
| `PEDIR_MOTIVO` | Solicita el motivo de la licencia | `PEDIR_CANTIDAD_DIAS` |
| `PEDIR_CANTIDAD_DIAS` | Solicita cuántos días necesita | `ESPERAR_DT` |
| `ESPERAR_DT` | Envía solicitud al DT y aguarda resolución | `APROBAR` / `RECHAZAR_DT` |
| `APROBAR` | Registra la licencia y notifica al jugador | `FIN` |
| `RECHAZAR_SIN_DIAS` | Notifica que no hay días disponibles | `FIN` |
| `RECHAZAR_DT` | Notifica el rechazo del Director Técnico | `FIN` |
| `ERROR` | Entrada inválida, solicita reintento | Estado anterior |

---

## Robustez — Camino infeliz (unhappy path)

| Situación de error | Entrada de ejemplo | Respuesta del bot |
|---|---|---|
| ID no numérico | `juan` | "Por favor ingresá solo números para el ID." |
| ID inexistente | ID que no está en el CSV | "No encontré ese jugador. Verificá el ID e intentá de nuevo." |
| Jugador suspendido | Estado = Suspendido | "Tu cuenta está suspendida. Contactá al club." |
| Días no numéricos | `tres` | "Por favor ingresá la cantidad como número (ej: 3)." |
| Días superan los disponibles | Pide 10, tiene 3 | "Solo tenés 3 días disponibles." |
| Días = 0 o negativos | `0` o `-1` | "La cantidad de días debe ser al menos 1." |
| Motivo vacío o muy corto | Espacio en blanco | "Por favor describí brevemente el motivo (mínimo 3 caracteres)." |

---

## Base de datos simulada

### `jugadores.csv`

| Campo | Tipo | Descripción | Valores posibles |
|---|---|---|---|
| ID | Entero | Identificador único | 1 al 999 |
| Apellido y Nombre | Texto | Nombre completo | Texto libre |
| DNI | Texto | Documento de identidad | 8 dígitos |
| Posición | Texto | Puesto en el campo | Pilar, Hooker, etc. |
| Categoría | Texto | División | Primera, M20, M18 |
| Días Disponibles | Entero | Días de licencia restantes | 0 a 15 |
| Días Usados | Entero | Días ya utilizados | 0 a 15 |
| Estado | Texto | Situación actual | Activo / En licencia / Suspendido |

### `historial_licencias.csv`

| Campo | Tipo | Descripción | Valores posibles |
|---|---|---|---|
| ID Solicitud | Entero | Número único de solicitud | 1 al 9999 |
| ID Jugador | Entero | FK tabla Jugadores | — |
| Jugador | Texto | Nombre del jugador | Texto libre |
| Fecha Solicitud | Fecha | Fecha de ingreso | AAAA-MM-DD |
| Días Solicitados | Entero | Cantidad de días pedidos | 1 a 15 |
| Motivo | Texto | Razón de la licencia | Texto libre |
| Estado DT | Texto | Decisión del DT | Aprobado / Rechazado / Pendiente |
| Fecha Resolución | Fecha | Fecha de respuesta del DT | AAAA-MM-DD |

---

## Jugadores de prueba

| ID | Jugador | Categoría | Días disponibles | Estado |
|---|---|---|---|---|
| 1 | Ferreyra Marcos | Primera | 15 | Activo ✅ |
| 2 | Gomez Sebastian | Primera | 0 | En licencia |
| 3 | Rios Facundo | Primera | 6 | En licencia |
| 5 | Perez Tomas | M20 | 15 | Activo ✅ |
| 6 | Navarro Julian | Primera | 0 | Suspendido ⛔ |
| 8 | Benitez Cristian | Primera | 15 | Activo ✅ |

> El ID `6` (Navarro) permite probar el camino de suspensión. Los IDs `2` y `10` permiten probar el camino de días agotados.

---

## Stack tecnológico

| Componente | Tecnología | Justificación |
|---|---|---|
| Lenguaje | Python 3.x | Sintaxis clara; lenguaje principal de la carrera |
| Plataforma | Simulador de consola | Sin dependencias externas, fácil despliegue |
| Persistencia | CSV con `open()` built-in | Lectura/escritura sin librerías adicionales |

**Alternativas para una implementación real:** JavaScript + Node.js (Telegram Bot API), PHP + Twilio (WhatsApp Business), Python + Flask (interfaz web).

---

## Herramientas de IA utilizadas

| Herramienta | Uso principal |
|---|---|
| Claude (Anthropic) | Diseño del proceso BPMN, generación de diagramas as-is y to-be, desarrollo del simulador y documentación |
| ChatGPT (OpenAI) | Consultas sobre notación BPMN 2.0 y ejemplos de máquinas de estado |
| Gemini (Google) | Verificación de conceptos de organización empresarial y revisión de redacción |

