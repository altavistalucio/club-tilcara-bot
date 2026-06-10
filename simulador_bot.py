#  SIMULADOR DE CHATBOT — Club Tilcara
#  Proceso: Solicitud de Licencia de Jugador
#  TPI — Organización Empresarial — UTN TUPaD 2026
#  Integrantes: NUÑEZ, Lucía; ALTAVISTA, Lucio

ARCHIVO_JUGADORES  = "jugadores.csv"
ARCHIVO_HISTORIAL  = "historial_licencias.csv"

# ── SEPARADOR VISUAL ─────────────────────────────────────
def linea():
    print("-" * 50)

# ── MENSAJES DEL BOT ─────────────────────────────────────
def bot(mensaje):
    print(f"\n  BOT: {mensaje}")

def usuario_input(prompt):
    return input(f"\n  VOS: {prompt} > ").strip()

# ── AYUDA CONTEXTUAL ─────────────────────────────────────
AYUDA = {
    "id":     "Ingresá tu número de ID de jugador (ej: 3). Lo encontrás en la planilla del club.",
    "motivo": "Describí brevemente el motivo de tu licencia (ej: Viaje familiar, Lesion).",
    "dias":   "Ingresá la cantidad de días que necesitás como número entero (ej: 5).",
    "dt":     "El Director Técnico debe escribir 'aprobar' o 'rechazar' para resolver la solicitud.",
}

def mostrar_ayuda(contexto):
    bot(f" AYUDA: {AYUDA.get(contexto, 'Seguí las instrucciones del bot en pantalla.')}")

# ── CARGAR JUGADORES DESDE CSV ───────────────────────────
def cargar_jugadores():
    """Lee jugadores.csv y devuelve un diccionario con ID como clave."""
    jugadores = {}
    try:
        archivo = open(ARCHIVO_JUGADORES, "r", encoding="utf-8")
        lineas = archivo.readlines()
        archivo.close()
    except:
        print(f"\nERROR: No se encontró el archivo '{ARCHIVO_JUGADORES}'.")
        print("Asegurate de tenerlo en la misma carpeta que este script.")
        exit()

    # La primera línea es el encabezado, se omite
    for linea_csv in lineas[1:]:
        linea_csv = linea_csv.strip()
        if linea_csv == "":
            continue
        datos = linea_csv.split(",")
        id_jug = int(datos[0])
        jugadores[id_jug] = {
            "id":          id_jug,
            "nombre":      datos[1],
            "dni":         datos[2],
            "posicion":    datos[3],
            "categoria":   datos[4],
            "disponibles": int(datos[5]),
            "usados":      int(datos[6]),
            "estado":      datos[7],
        }
    return jugadores

# ── GUARDAR JUGADORES EN CSV ─────────────────────────────
def guardar_jugadores(jugadores):
    """Reescribe jugadores.csv con los datos actualizados."""
    archivo = open(ARCHIVO_JUGADORES, "w", encoding="utf-8")
    archivo.write("ID,Apellido y Nombre,DNI,Posicion,Categoria,Dias Disponibles,Dias Usados,Estado\n")
    for jug in jugadores.values():
        linea_csv = f"{jug['id']},{jug['nombre']},{jug['dni']},{jug['posicion']},{jug['categoria']},{jug['disponibles']},{jug['usados']},{jug['estado']}\n"
        archivo.write(linea_csv)
    archivo.close()

# ── REGISTRAR LICENCIA EN HISTORIAL ─────────────────────
def registrar_licencia(jugador, dias_solicitados, motivo, fecha_hoy):
    """Agrega una nueva fila al historial y actualiza el jugador."""

    # Calcular el próximo ID de solicitud
    try:
        archivo = open(ARCHIVO_HISTORIAL, "r", encoding="utf-8")
        lineas = archivo.readlines()
        archivo.close()
    except:
        lineas = ["ID Solicitud,ID Jugador,Jugador,Fecha Solicitud,Dias Solicitados,Motivo,Estado DT,Fecha Resolucion\n"]

    ultimo_id = 0
    for linea_csv in lineas[1:]:
        linea_csv = linea_csv.strip()
        if linea_csv != "":
            ultimo_id = int(linea_csv.split(",")[0])
    nuevo_id = ultimo_id + 1

    # Agregar la nueva fila al historial
    nueva_fila = f"{nuevo_id},{jugador['id']},{jugador['nombre']},{fecha_hoy},{dias_solicitados},{motivo},Aprobado,{fecha_hoy}\n"
    archivo = open(ARCHIVO_HISTORIAL, "a", encoding="utf-8")
    archivo.write(nueva_fila)
    archivo.close()

# ── OBTENER FECHA DE HOY (sin módulos externos) ──────────
def obtener_fecha():
    """Devuelve la fecha actual como string AAAA-MM-DD."""
    import time
    t = time.localtime()
    return f"{t.tm_year}-{t.tm_mon:02d}-{t.tm_mday:02d}"

#  MÁQUINA DE ESTADOS

def estado_inicio():
    """ESTADO: INICIO — saludo y solicitud de ID."""
    linea()
    bot("¡Bienvenido al sistema de licencias del Club Tilcara!")
    bot("Podés escribir 'salir' en cualquier momento para cancelar.")
    bot("Escribí 'ayuda' si necesitás orientación en cualquier paso.")
    bot("¿Cuál es tu número de ID de jugador?")

def estado_validar_jugador(jugadores):
    """ESTADO: VALIDAR_JUGADOR — verifica si el ID existe."""
    while True:
        entrada = usuario_input("Ingresá tu ID")

        if entrada.lower() == "salir":
            return None, "salir"
        if entrada.lower() == "reiniciar":
            return None, "reiniciar"
        if entrada.lower() == "ayuda":
            mostrar_ayuda("id")
            continue

        # Camino infeliz: no es número
        if not entrada.isdigit():
            bot(" Por favor ingresá solo números para el ID. Intentá de nuevo.")
            continue

        id_jug = int(entrada)

        # Camino infeliz: ID inexistente
        if id_jug not in jugadores:
            bot(f" No encontré ningún jugador con el ID {id_jug}.")
            bot("Verificá el número e intentá de nuevo.")
            continue

        jugador = jugadores[id_jug]

        # Camino infeliz: suspendido
        if jugador["estado"] == "Suspendido":
            bot(f" Hola, {jugador['nombre']}.")
            bot("Tu cuenta está suspendida. Contactá al club para más información.")
            return None, "suspendido"

        bot(f" Jugador encontrado: {jugador['nombre']} — {jugador['categoria']}")
        bot(f" Días disponibles: {jugador['disponibles']} | Días usados: {jugador['usados']}")
        return jugador, "ok"

def estado_consultar_dias(jugador):
    """ESTADO: CONSULTAR_DIAS — verifica si tiene días disponibles."""
    if jugador["disponibles"] <= 0:
        bot(f" Lo sentimos, {jugador['nombre']}.")
        bot("No tenés días de licencia disponibles.")
        bot("Contactá al Director Técnico si creés que es un error.")
        return False
    return True

def estado_pedir_motivo():
    """ESTADO: PEDIR_MOTIVO — solicita el motivo."""
    bot("¿Cuál es el motivo de tu solicitud de licencia?")
    while True:
        motivo = usuario_input("Motivo")

        if motivo.lower() == "salir":
            return None
        if motivo.lower() == "reiniciar":
            return "reiniciar"
        if motivo.lower() == "ayuda":
            mostrar_ayuda("motivo")
            continue

        # Camino infeliz: motivo vacío o muy corto
        if len(motivo) < 3:
            bot(" Por favor describí brevemente el motivo (mínimo 3 caracteres).")
            continue

        return motivo

def estado_pedir_dias(jugador):
    """ESTADO: PEDIR_CANTIDAD_DIAS — solicita cuántos días necesita."""
    bot(f"¿Cuántos días necesitás? (Tenés {jugador['disponibles']} disponibles)")
    while True:
        entrada = usuario_input("Cantidad de días")

        if entrada.lower() == "salir":
            return None
        if entrada.lower() == "reiniciar":
            return "reiniciar"
        if entrada.lower() == "ayuda":
            mostrar_ayuda("dias")
            continue

        # Camino infeliz: no es número
        if not entrada.isdigit():
            bot(" Por favor ingresá la cantidad como número (ej: 3).")
            continue

        dias = int(entrada)

        # Camino infeliz: cero o negativo
        if dias <= 0:
            bot(" La cantidad de días debe ser al menos 1.")
            continue

        # Camino infeliz: supera los disponibles
        if dias > jugador["disponibles"]:
            bot(f" Solo tenés {jugador['disponibles']} días disponibles.")
            bot(" Podés solicitar hasta ese máximo.")
            continue

        return dias

def estado_esperar_dt(jugador, dias, motivo):
    """ESTADO: ESPERAR_DT — simula la decisión del DT."""
    linea()
    bot(" Solicitud enviada al Director Técnico.")
    bot(f"   Jugador:  {jugador['nombre']}")
    bot(f"   Días:     {dias}")
    bot(f"   Motivo:   {motivo}")
    linea()

    bot("(Simulación) El Director Técnico debe ingresar su decisión:")
    while True:
        decision = usuario_input("DT — Escribí 'aprobar' o 'rechazar'").lower()

        if decision == "aprobar":
            return True
        elif decision == "rechazar":
            return False
        elif decision == "ayuda":
            mostrar_ayuda("dt")
        else:
            bot(" Opción no válida. Escribí 'aprobar' o 'rechazar'.")

def estado_aprobar(jugadores, jugador, dias, motivo):
    """ESTADO: APROBAR — actualiza datos y notifica."""
    fecha_hoy = obtener_fecha()

    # Actualizar el jugador en el diccionario
    jugadores[jugador["id"]]["disponibles"] -= dias
    jugadores[jugador["id"]]["usados"]      += dias
    jugadores[jugador["id"]]["estado"]       = "En licencia"

    # Guardar cambios en los archivos CSV
    guardar_jugadores(jugadores)
    registrar_licencia(jugador, dias, motivo, fecha_hoy)

    linea()
    bot(f" ¡Licencia APROBADA para {jugador['nombre']}!")
    bot(f"   Días otorgados: {dias}")
    bot(f"   Días restantes: {jugadores[jugador['id']]['disponibles']}")
    bot("   Los archivos fueron actualizados correctamente.")

def estado_rechazar_dt(jugador):
    """ESTADO: RECHAZAR_DT — notifica rechazo del DT."""
    linea()
    bot(f" Lo sentimos, {jugador['nombre']}.")
    bot("El Director Técnico rechazó tu solicitud.")
    bot("Podés comunicarte con él para más detalles.")

#  FLUJO PRINCIPAL

def ejecutar_bot():
    jugadores = cargar_jugadores()

    while True:
        # INICIO
        estado_inicio()

        # VALIDAR JUGADOR
        jugador, resultado = estado_validar_jugador(jugadores)
        if resultado == "salir":
            bot("Proceso cancelado. ¡Hasta luego!")
            linea()
            break
        if resultado in ("suspendido", "reiniciar"):
            if resultado == "reiniciar":
                bot(" Reiniciando el proceso...")
            linea()
            continue

        # CONSULTAR DÍAS
        tiene_dias = estado_consultar_dias(jugador)
        if not tiene_dias:
            linea()
            reintentar = usuario_input("¿Querés iniciar una nueva consulta? (si/no)")
            if reintentar.lower() == "si":
                continue
            else:
                bot("¡Hasta luego!")
                linea()
                break

        # PEDIR MOTIVO
        motivo = estado_pedir_motivo()
        if motivo is None:
            bot("Proceso cancelado. ¡Hasta luego!")
            linea()
            break
        if motivo == "reiniciar":
            bot(" Reiniciando el proceso...")
            linea()
            continue

        # PEDIR CANTIDAD DE DÍAS
        dias = estado_pedir_dias(jugador)
        if dias is None:
            bot("Proceso cancelado. ¡Hasta luego!")
            linea()
            break
        if dias == "reiniciar":
            bot(" Reiniciando el proceso...")
            linea()
            continue

        # ESPERAR DT
        aprobado = estado_esperar_dt(jugador, dias, motivo)

        # RESULTADO
        if aprobado:
            estado_aprobar(jugadores, jugador, dias, motivo)
        else:
            estado_rechazar_dt(jugador)

        linea()
        reintentar = usuario_input("¿Querés realizar otra consulta? (si/no)")
        if reintentar.lower() != "si":
            bot("¡Hasta luego!")
            linea()
            break

# ── PUNTO DE ENTRADA ─────────────────────────────────────
if __name__ == "__main__":
    ejecutar_bot()
