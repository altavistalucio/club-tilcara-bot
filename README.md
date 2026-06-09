# Club Tilcara — Simulador de Licencias

Trabajo Práctico Integrador — Organización Empresarial

Integrantes:NUÑEZ, Lucia ; ALTAVISTA, Lucio 
Cátedra: Organización Empresarial  
Docente titular: Prof. Gabriela Martínez

## Descripción del proyecto

Este proyecto automatiza el proceso de **solicitud de licencia de jugadores** del Club Tilcara, un club de rugby ficticio ubicado en Paraná, Entre Ríos.

El proceso fue modelado con la metodología **BPMN 2.0** (diagramas as-is y to-be) y luego implementado como un **simulador de chatbot por consola** en Python, que interactúa con una base de datos simulada en formato Excel.

## Estructura del repositorio

club-tilcara-bot/
│
├── simulador_bot.py                     # Código fuente del simulador
├── ClubTilcara_Planilla_Licencias.xlsx  # Base de datos simulada
├── README.md                            # Este archivo
│
└── diagramas/
    ├── bpmn_asis_club_tilcara.svg       # Diagrama BPMN as-is (proceso actual)
    └── bpmn_licencia_club_tilcara.svg   # Diagrama BPMN to-be (con chatbot)

## Cómo ejecutar el simulador

## Requisitos previos

- Python 3.8 o superior
- 
Biblioteca `openpyxl`

## Instalación

bash
# Instalar la dependencia necesaria
pip install openpyxl

## Ejecución

bash
# Asegurate de estar en la carpeta del proyecto
python simulador_bot.py

> El archivo `ClubTilcara_Planilla_Licencias.xlsx` debe estar en la **misma carpeta** que el script.


## Cómo usar el simulador

Al ejecutar el script, el bot guía al jugador paso a paso:

| Paso | Qué hace el bot | Qué hace el jugador |
|------|----------------|---------------------|
| 1 | Da la bienvenida y pide el ID | Ingresa su número de ID |
| 2 | Verifica el jugador en la planilla | — |
| 3 | Informa los días disponibles | — |
| 4 | Pide el motivo de la licencia | Escribe el motivo |
| 5 | Pide la cantidad de días | Ingresa un número |
| 6 | Envía la solicitud al DT | — |
| 7 | El DT aprueba o rechaza | DT escribe `aprobar` o `rechazar` |
| 8 | Notifica el resultado y actualiza la planilla | — |

## Comandos especiales

| Comando | Efecto |
|---------|--------|
| `salir` | Cancela el proceso en cualquier momento |

## Base de datos simulada

La planilla Excel contiene tres hojas:

- Jugadores — 10 jugadores de ejemplo con ID, nombre, posición, categoría, días disponibles y estado.
- Historial Licencias — registro de todas las solicitudes procesadas.
- Diccionario de Datos — descripción de cada campo utilizado.

Cuando una licencia es aprobada, el bot **actualiza automáticamente** la planilla: descuenta los días usados y agrega una fila en el historial.

## Diagrama BPMN

El proceso fue modelado en dos versiones:

- As-Is — cómo se realizaba el proceso manualmente (verbal, sin trazabilidad).
- To-Be — cómo lo automatiza el chatbot (con validaciones, estados y registro).

Ambos diagramas se encuentran en la carpeta `/diagramas`.

Los carriles del diagrama to-be son:
1. Jugador — inicia la solicitud y recibe la respuesta.
2. Sistema / Bot — valida, consulta la planilla y coordina el flujo.
3. Director Técnico — recibe y aprueba o rechaza la solicitud.

Las dos compuertas (gateways) del flujo son:
- ¿El jugador tiene días disponibles?
- ¿El Director Técnico aprueba la solicitud?

## Manejo de errores (camino infeliz)

El simulador contempla los siguientes casos de error:

| Situación | Respuesta del bot |
|-----------|-------------------|
| ID con letras o símbolos | Pide que ingrese solo números |
| ID que no existe en la planilla | Avisa y permite reintentar |
| Jugador con estado Suspendido | Informa y termina el proceso |
| Jugador sin días disponibles | Informa y ofrece reiniciar |
| Motivo vacío o muy corto | Pide que describa el motivo |
| Días ingresados no numéricos | Pide que ingrese un número |
| Días que superan los disponibles | Informa el máximo permitido |


## Herramientas de IA utilizadas

Durante el desarrollo se utilizaron las siguientes herramientas:

- Claude (Anthropic) — diseño del proceso BPMN, generación de diagramas, desarrollo del simulador y documentación.
- ChatGPT (OpenAI) — consultas sobre notación BPMN 2.0 y máquinas de estado.
- Gemini (Google) — verificación de conceptos y revisión de redacción.

## Licencia

Proyecto académico — UTN TUPaD 2026. Sin fines comerciales.
