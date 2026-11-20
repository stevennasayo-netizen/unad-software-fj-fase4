"""
main.py
Punto de entrada del sistema Software FJ.
1. Ejecuta una simulación automática de 29 operaciones válidas e inválidas.
2. Al final ofrece abrir el menú interactivo para operar el sistema manualmente.

Autor: Alvaro Steven Carreño Nasayo
Curso: Programación 213023 - UNAD - Fase 4
"""

from datetime import date, timedelta  # Para calcular fechas de prueba
from sistema import SistemaSoftwareFJ  # Gestor principal
from servicios import Servicio, ReservaSala, AlquilerEquipo, Asesoria  # Clases de servicios
from menu import ejecutar_menu  # Menú interactivo
from logger import ARCHIVO_LOG  # Ruta del archivo de log para mostrarla al final


def titulo(numero, texto):  # Función auxiliar para imprimir el encabezado de cada operación
    print(f"\n--- Operación {numero}: {texto} ---")  # Imprime número y descripción


def proximo_sabado():  # Calcula la fecha del próximo sábado
    dias = (5 - date.today().weekday()) % 7 or 7  # Días que faltan (si hoy es sábado, el siguiente)
    return date.today() + timedelta(days=dias)  # Fecha resultante


def simulacion(sistema):  # Simulación automática de operaciones
    # ===================== CLIENTES =====================
    titulo(1, "Registrar cliente válido")  # Encabezado
    valentina = sistema.registrar_cliente("Valentina Gómez", "1019876543", "valentina.gomez@correo.com", "3157654321")
    print("Resultado:", valentina)  # Muestra el cliente creado

    titulo(2, "Registrar cliente válido")  # Encabezado
    andres = sistema.registrar_cliente("Andrés Castillo", "79654321", "andres.castillo@redes.co", "3012345678")
    print("Resultado:", andres)  # Muestra el cliente creado

    titulo(3, "Registrar cliente con correo incompleto")  # Encabezado
    print("Resultado:", sistema.registrar_cliente("Jorge Ruiz", "1030123456", "jorge.ruiz@", "3001234567"))  # Falla

    titulo(4, "Registrar cliente con teléfono de 7 dígitos")  # Encabezado
    print("Resultado:", sistema.registrar_cliente("Laura Méndez", "52123456", "laura@correo.com", "6012345"))  # Falla

    titulo(5, "Registrar cliente con documento duplicado")  # Encabezado
    print("Resultado:", sistema.registrar_cliente("Otra Persona", "79654321", "otra@correo.com", "3101112233"))  # Falla

    # ===================== SERVICIOS =====================
    titulo(6, "Crear sala de reuniones válida")  # Encabezado
    sala = sistema.registrar_servicio(ReservaSala, "Sala Chapinero", 65000, capacidad=25)  # Válido
    print("Resultado:", sala)  # Muestra el servicio

    titulo(7, "Crear alquiler de equipos de red válido")  # Encabezado
    kit = sistema.registrar_servicio(AlquilerEquipo, "Kit de red Cisco", 95000, "Switch Catalyst 9200", 2)  # Válido
    print("Resultado:", kit)  # Muestra el servicio

    titulo(8, "Crear asesoría especializada válida")  # Encabezado
    asesoria = sistema.registrar_servicio(Asesoria, "Asesoría SD-Access", 150000,  # Válido
                                          "Catalyst Center y SD-Access", "experto")  # Especialidad y nivel
    print("Resultado:", asesoria)  # Muestra el servicio

    titulo(9, "Crear sala con capacidad cero")  # Encabezado
    print("Resultado:", sistema.registrar_servicio(ReservaSala, "Sala Usaquén", 40000, capacidad=0))  # Falla

    titulo(10, "Crear asesoría con nivel inexistente")  # Encabezado
    print("Resultado:", sistema.registrar_servicio(Asesoria, "Asesoría WiFi", 90000, "Redes inalámbricas", "senior"))

    titulo(11, "Crear alquiler sin parámetros obligatorios")  # Encabezado
    print("Resultado:", sistema.registrar_servicio(AlquilerEquipo, "Access Points", 30000))  # Falla (TypeError)

    titulo(12, "Intentar instanciar la clase abstracta Servicio")  # Encabezado
    print("Resultado:", sistema.ejecutar_operacion(  # Operación protegida
        "Instanciar Servicio abstracto", Servicio, "Genérico", 1000))  # Falla: no se puede instanciar

    # ===================== RESERVAS =====================
    titulo(13, "Reserva de sala para hoy (IVA por defecto)")  # Encabezado
    r1 = sistema.crear_reserva(valentina, sala, 4)  # 4 horas de sala
    print("Resultado:", r1)  # Muestra la reserva

    titulo(14, "Reserva de equipos con descuento del 10 %")  # Encabezado
    r2 = sistema.crear_reserva(andres, kit, 3, impuesto=0.19, descuento=0.10)  # 3 días con descuento
    print("Resultado:", r2)  # Muestra la reserva

    titulo(15, "Reserva de sala un sábado (recargo de fin de semana)")  # Encabezado
    r3 = sistema.crear_reserva(andres, sala, 2, fecha=proximo_sabado())  # Fecha de fin de semana
    print("Resultado:", r3)  # Muestra la reserva con recargo

    titulo(16, "Tercera reserva activa del mismo cliente")  # Encabezado
    r4 = sistema.crear_reserva(andres, asesoria, 2)  # Llega al máximo permitido
    print("Resultado:", r4)  # Muestra la reserva

    titulo(17, "Cuarta reserva activa (supera el límite por cliente)")  # Encabezado
    print("Resultado:", sistema.crear_reserva(andres, asesoria, 1))  # Falla: LimiteReservasError

    titulo(18, "Reserva de asesoría de 12 horas (duración inválida)")  # Encabezado
    print("Resultado:", sistema.crear_reserva(valentina, asesoria, 12))  # Falla y queda cancelada

    titulo(19, "Reserva con fecha pasada")  # Encabezado
    ayer = date.today() - timedelta(days=1)  # Fecha de ayer
    print("Resultado:", sistema.crear_reserva(valentina, sala, 2, fecha=ayer))  # Falla: FechaInvalidaError

    titulo(20, "Reserva con fecha en formato incorrecto")  # Encabezado
    print("Resultado:", sistema.crear_reserva(valentina, sala, 2, fecha="25/12/2026"))  # Falla encadenada

    titulo(21, "Reserva con descuento inconsistente (120 %)")  # Encabezado
    print("Resultado:", sistema.crear_reserva(valentina, kit, 2, descuento=1.2))  # Falla

    titulo(22, "Reserva sobre un servicio no disponible")  # Encabezado
    kit.cambiar_disponibilidad(False)  # Se desactiva el kit (en mantenimiento)
    print("Resultado:", sistema.crear_reserva(valentina, kit, 1))  # Falla por disponibilidad
    kit.cambiar_disponibilidad(True)  # Se reactiva

    titulo(23, "Reserva sin cliente (None)")  # Encabezado
    print("Resultado:", sistema.crear_reserva(None, sala, 2))  # Falla: cliente inválido

    # ===================== PROCESAMIENTO Y CANCELACIÓN =====================
    titulo(24, "Procesar pago con monto suficiente")  # Encabezado
    cambio = sistema.ejecutar_operacion(f"Procesar reserva #{r1.id}", r1.procesar, 400000)  # Pago correcto
    print("Cambio entregado:", cambio)  # Muestra el cambio

    titulo(25, "Procesar pago con monto en letras")  # Encabezado
    print("Resultado:", sistema.ejecutar_operacion(  # Operación protegida
        f"Procesar reserva #{r2.id}", r2.procesar, "quinientos mil"))  # Falla con encadenamiento

    titulo(26, "Procesar pago insuficiente")  # Encabezado
    print("Resultado:", sistema.ejecutar_operacion(  # Operación protegida
        f"Procesar reserva #{r2.id}", r2.procesar, 50000))  # Falla: pago insuficiente

    titulo(27, "Cancelar reserva ya procesada (operación no permitida)")  # Encabezado
    print("Resultado:", sistema.ejecutar_operacion(  # Operación protegida
        f"Cancelar reserva #{r1.id}", r1.cancelar, "Cambio de planes"))  # Falla

    titulo(28, "Cancelar reserva confirmada (válido)")  # Encabezado
    sistema.ejecutar_operacion(f"Cancelar reserva #{r2.id}", r2.cancelar, "Equipos ya no se necesitan")  # Válido
    print("Estado:", r2.estado, "| Reservas activas de Andrés:", sistema.reservas_activas_de(andres))  # Estado

    # ===================== SOBRECARGA DE MÉTODOS =====================
    titulo(29, "Cotizaciones con métodos sobrecargados")  # Encabezado
    print("Sala 2 h (solo duración):", sala.calcular_costo(2))  # Variante 1: solo duración
    print("Sala 2 h (sin impuesto):", sala.calcular_costo(2, 0))  # Variante 2: impuesto personalizado
    print("Sala 2 h (IVA + 20 % desc.):", sala.calcular_costo(2, 0.19, 0.20))  # Variante 3: con descuento
    print("Sala 2 h (IVA + recargo 15 %):", sala.calcular_costo(2, 0.19, 0, 0.15))  # Variante 4: con recargo
    print("Cotizar con número:", asesoria.cotizar(1.5))  # singledispatch con float
    print("Cotizar con diccionario:", asesoria.cotizar({"duracion": 2, "descuento": 0.05}))  # Con dict
    print("Cotizar con texto:", sistema.ejecutar_operacion(  # Tipo no soportado
        "Cotizar con texto", asesoria.cotizar, "dos horas"))  # Falla controlada


def main():  # Función principal
    sistema = SistemaSoftwareFJ()  # Se crea el sistema (listas vacías en memoria)
    simulacion(sistema)  # Se ejecuta la simulación automática
    print(sistema.resumen())  # Muestra todo lo que quedó en memoria
    print(f"\nLa simulación terminó sin interrupciones. Log: {ARCHIVO_LOG}")  # Mensaje de cierre
    try:  # Se pregunta si se quiere usar el menú
        respuesta = input("\n¿Desea abrir el menú interactivo? (s/n): ").strip().lower()  # Respuesta
    except EOFError:  # Si no hay teclado disponible (ejecución automática)
        respuesta = "n"  # Se asume que no
    if respuesta == "s":  # Si el usuario acepta
        ejecutar_menu(sistema)  # Se abre el menú con los datos de la simulación ya cargados
    print("Programa finalizado.")  # Mensaje final


if __name__ == "__main__":  # Solo se ejecuta si el archivo se corre directamente
    main()  # Llama a la función principal
