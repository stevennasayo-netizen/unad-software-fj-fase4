"""
menu.py
Menú interactivo en consola para operar el sistema Software FJ manualmente.
Cualquier dato mal digitado se controla con excepciones y el menú sigue funcionando.
"""

from servicios import ReservaSala, AlquilerEquipo, Asesoria  # Tipos de servicio disponibles
from logger import ARCHIVO_LOG, log  # Ruta del log y logger global
from excepciones import SoftwareFJError, ValidacionError  # Excepciones del sistema


def pedir(texto):  # Lee un texto del usuario
    """Pide un dato por teclado y lo devuelve sin espacios sobrantes."""
    return input(f"  {texto}: ").strip()  # Muestra la pregunta y limpia la respuesta


def pedir_numero(texto, tipo=float):  # Lee un número del usuario
    """Pide un número; si el usuario escribe algo no numérico lanza ValidacionError encadenado."""
    valor = pedir(texto)  # Se lee el texto
    try:  # Se intenta convertir al tipo pedido
        return tipo(valor.replace(",", "."))  # Acepta coma o punto decimal
    except ValueError as error:  # Si no es un número válido
        raise ValidacionError(f"'{valor}' no es un número válido") from error  # Error encadenado


def opcion_registrar_cliente(sistema):  # Opción 1 del menú
    print("\n[Registrar cliente]")  # Título de la opción
    cliente = sistema.registrar_cliente(  # Se intenta registrar con los datos digitados
        pedir("Nombre completo"),  # Nombre
        pedir("Documento"),  # Documento
        pedir("Correo"),  # Correo
        pedir("Teléfono (10 dígitos)"),  # Teléfono
    )  # Fin del registro
    print("  ✔ Cliente registrado" if cliente else "  ✘ No se pudo registrar (ver log)")  # Resultado


def opcion_registrar_servicio(sistema):  # Opción 2 del menú
    print("\n[Registrar servicio]  1) Sala  2) Alquiler de equipo  3) Asesoría")  # Tipos disponibles
    tipo = pedir("Tipo")  # Se elige el tipo
    nombre = pedir("Nombre del servicio")  # Nombre del servicio
    tarifa = pedir_numero("Tarifa base")  # Tarifa (puede lanzar ValidacionError)
    if tipo == "1":  # Sala
        servicio = sistema.registrar_servicio(ReservaSala, nombre, tarifa, pedir_numero("Capacidad", int))  # Crea sala
    elif tipo == "2":  # Alquiler de equipo
        servicio = sistema.registrar_servicio(  # Crea alquiler
            AlquilerEquipo, nombre, tarifa, pedir("Tipo de equipo"), pedir_numero("Cantidad", int))  # Datos
    elif tipo == "3":  # Asesoría
        servicio = sistema.registrar_servicio(  # Crea asesoría
            Asesoria, nombre, tarifa, pedir("Especialidad"), pedir("Nivel (basico/intermedio/experto)").lower())  # Datos
    else:  # Opción no válida
        raise ValidacionError(f"Tipo de servicio '{tipo}' no existe")  # Error
    print("  ✔ Servicio registrado" if servicio else "  ✘ No se pudo registrar (ver log)")  # Resultado


def opcion_crear_reserva(sistema):  # Opción 3 del menú
    print("\n[Crear reserva]")  # Título
    cliente = sistema.buscar_cliente(pedir("Documento del cliente"))  # Se busca el cliente
    if cliente is None:  # Si no existe
        raise ValidacionError("No existe un cliente con ese documento")  # Error
    for i, s in enumerate(sistema.servicios, start=1):  # Se listan los servicios numerados
        print(f"   {i}) {s.describir()}")  # Número y descripción
    indice = pedir_numero("Número de servicio", int) - 1  # Posición elegida
    if not 0 <= indice < len(sistema.servicios):  # Si el número no está en la lista
        raise ValidacionError("Número de servicio fuera de la lista")  # Error
    duracion = pedir_numero("Duración (horas o días según el servicio)")  # Duración
    if duracion.is_integer():  # Si la duración es entera (ej. 3.0)
        duracion = int(duracion)  # Se convierte a entero (los equipos se alquilan por días enteros)
    fecha = pedir("Fecha AAAA-MM-DD (Enter = hoy)") or None  # Fecha opcional
    reserva = sistema.crear_reserva(cliente, sistema.servicios[indice], duracion, fecha=fecha)  # Se crea
    print(f"  ✔ {reserva}" if reserva else "  ✘ No se pudo crear la reserva (ver log)")  # Resultado


def opcion_procesar_pago(sistema):  # Opción 4 del menú
    print("\n[Procesar pago]")  # Título
    reserva = sistema.buscar_reserva(pedir_numero("Número de reserva", int))  # Se busca la reserva
    if reserva is None:  # Si no existe
        raise ValidacionError("No existe una reserva con ese número")  # Error
    cambio = reserva.procesar(pedir("Monto pagado"))  # Se procesa (procesar valida el monto)
    print(f"  ✔ Pago procesado. Cambio: ${cambio:,.2f}")  # Resultado


def opcion_cancelar(sistema):  # Opción 5 del menú
    print("\n[Cancelar reserva]")  # Título
    reserva = sistema.buscar_reserva(pedir_numero("Número de reserva", int))  # Se busca la reserva
    if reserva is None:  # Si no existe
        raise ValidacionError("No existe una reserva con ese número")  # Error
    reserva.cancelar(pedir("Motivo") or "Sin motivo")  # Se cancela (puede lanzar OperacionNoPermitidaError)
    print("  ✔ Reserva cancelada")  # Resultado


def opcion_ver_log(_sistema):  # Opción 7 del menú
    print(f"\n[Últimas 10 líneas de {ARCHIVO_LOG}]")  # Título
    with open(ARCHIVO_LOG, encoding="utf-8") as archivo:  # Se abre el log en modo lectura
        for linea in archivo.readlines()[-10:]:  # Solo las últimas 10 líneas
            print("  " + linea.rstrip())  # Se imprimen sin salto de línea doble


OPCIONES = {  # Diccionario que relaciona cada número con su función
    "1": ("Registrar cliente", opcion_registrar_cliente),  # Opción 1
    "2": ("Registrar servicio", opcion_registrar_servicio),  # Opción 2
    "3": ("Crear reserva", opcion_crear_reserva),  # Opción 3
    "4": ("Procesar pago", opcion_procesar_pago),  # Opción 4
    "5": ("Cancelar reserva", opcion_cancelar),  # Opción 5
    "6": ("Ver resumen", lambda sistema: print(sistema.resumen())),  # Opción 6
    "7": ("Ver últimas líneas del log", opcion_ver_log),  # Opción 7
}  # Fin del diccionario


def ejecutar_menu(sistema):  # Ciclo principal del menú
    """Muestra el menú hasta que el usuario elija salir. Ningún error lo detiene."""
    while True:  # Se repite indefinidamente
        print("\n========= MENÚ SOFTWARE FJ =========")  # Encabezado
        for clave, (texto, _) in OPCIONES.items():  # Se recorren las opciones
            print(f"  {clave}) {texto}")  # Se muestra cada opción
        print("  0) Salir")  # Opción para terminar
        try:  # Bloque protegido
            eleccion = pedir("Opción")  # Se lee la opción
            if eleccion == "0":  # Si elige salir
                break  # Se termina el ciclo
            if eleccion not in OPCIONES:  # Si la opción no existe
                raise ValidacionError(f"Opción '{eleccion}' no válida")  # Error
            OPCIONES[eleccion][1](sistema)  # Se ejecuta la función de la opción elegida
        except SoftwareFJError as error:  # Errores conocidos del sistema
            causa = f" | Causa: {error.__cause__}" if error.__cause__ else ""  # Causa encadenada
            log.error(f"Menú: {error}{causa}")  # Se registra en el log
            print(f"  ✘ {error}")  # Se informa al usuario
        except (EOFError, KeyboardInterrupt):  # El usuario cerró la entrada o presionó Ctrl+C
            print("\n  Saliendo del menú...")  # Aviso
            break  # Se termina el ciclo
        except Exception as error:  # Cualquier error inesperado
            log.critical(f"Menú: error inesperado {type(error).__name__}: {error}")  # Se registra
            print(f"  ✘ Error inesperado: {error}")  # Se informa y el menú continúa
    log.info("Menú interactivo cerrado")  # Evento de cierre
