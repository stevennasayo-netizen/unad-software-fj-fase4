"""
main.py
Punto de entrada del sistema Software FJ.
Simula operaciones válidas e inválidas para demostrar que el sistema
sigue funcionando aunque ocurran errores.

Autor: Alvaro Steven Carreño Nasayo
Curso: Programación 213023 - UNAD - Fase 4
"""

from sistema import SistemaSoftwareFJ  # Gestor principal
from servicios import Servicio, ReservaSala, AlquilerEquipo, Asesoria  # Clases de servicios
from logger import ARCHIVO_LOG  # Ruta del archivo de log para mostrarla al final


def titulo(numero, texto):  # Función auxiliar para imprimir el encabezado de cada operación
    print(f"\n--- Operación {numero}: {texto} ---")  # Imprime número y descripción


def main():  # Función principal
    sistema = SistemaSoftwareFJ()  # Se crea el sistema (listas vacías en memoria)

    # ===================== CLIENTES =====================
    titulo(1, "Registrar cliente válido")  # Encabezado
    ana = sistema.registrar_cliente("Ana María Rojas", "1023456789", "ana.rojas@correo.com", "3104567890")  # Válido
    print("Resultado:", ana)  # Muestra el cliente creado

    titulo(2, "Registrar cliente válido")  # Encabezado
    luis = sistema.registrar_cliente("Luis Pérez", "80123456", "luis.perez@empresa.co", "3209876543")  # Válido
    print("Resultado:", luis)  # Muestra el cliente creado

    titulo(3, "Registrar cliente con correo inválido")  # Encabezado
    print("Resultado:", sistema.registrar_cliente("Carlos Díaz", "1012345678", "carlos-correo", "3001234567"))  # Falla

    titulo(4, "Registrar cliente sin nombre (parámetro faltante)")  # Encabezado
    print("Resultado:", sistema.registrar_cliente("", "1098765432", "x@correo.com", "3001112233"))  # Falla

    titulo(5, "Registrar cliente con documento duplicado")  # Encabezado
    print("Resultado:", sistema.registrar_cliente("Ana Duplicada", "1023456789", "otra@correo.com", "3101112233"))  # Falla

    # ===================== SERVICIOS =====================
    titulo(6, "Crear servicio de sala válido")  # Encabezado
    sala = sistema.registrar_servicio(ReservaSala, "Sala Innovación", 50000, capacidad=30)  # Válido
    print("Resultado:", sala)  # Muestra el servicio

    titulo(7, "Crear servicio de alquiler de equipo válido")  # Encabezado
    equipo = sistema.registrar_servicio(AlquilerEquipo, "Portátiles Pro", 80000, "Portátil", 3)  # Válido
    print("Resultado:", equipo)  # Muestra el servicio

    titulo(8, "Crear asesoría válida")  # Encabezado
    asesoria = sistema.registrar_servicio(Asesoria, "Asesoría Cloud", 120000, "Computación en la nube", "experto")  # Válido
    print("Resultado:", asesoria)  # Muestra el servicio

    titulo(9, "Crear servicio con tarifa negativa")  # Encabezado
    print("Resultado:", sistema.registrar_servicio(ReservaSala, "Sala Rota", -100, capacidad=10))  # Falla

    titulo(10, "Crear asesoría con nivel inexistente")  # Encabezado
    print("Resultado:", sistema.registrar_servicio(Asesoria, "Asesoría X", 90000, "Redes", "maestro"))  # Falla

    titulo(11, "Crear alquiler sin parámetros obligatorios")  # Encabezado
    print("Resultado:", sistema.registrar_servicio(AlquilerEquipo, "Proyectores", 40000))  # Falla (TypeError)

    titulo(12, "Intentar instanciar la clase abstracta Servicio")  # Encabezado
    print("Resultado:", sistema.ejecutar_operacion(  # Operación protegida
        "Instanciar Servicio abstracto", Servicio, "Genérico", 1000))  # Falla: no se puede instanciar

    # ===================== RESERVAS =====================
    titulo(13, "Reserva exitosa de sala (IVA por defecto)")  # Encabezado
    r1 = sistema.crear_reserva(ana, sala, 3)  # 3 horas de sala
    print("Resultado:", r1)  # Muestra la reserva

    titulo(14, "Reserva exitosa de equipos con descuento del 10 %")  # Encabezado
    r2 = sistema.crear_reserva(luis, equipo, 5, impuesto=0.19, descuento=0.10)  # 5 días con descuento
    print("Resultado:", r2)  # Muestra la reserva

    titulo(15, "Reserva de asesoría con duración inválida (20 horas)")  # Encabezado
    print("Resultado:", sistema.crear_reserva(ana, asesoria, 20))  # Falla y queda cancelada

    titulo(16, "Reserva con descuento inconsistente (150 %)")  # Encabezado
    print("Resultado:", sistema.crear_reserva(luis, asesoria, 2, descuento=1.5))  # Falla

    titulo(17, "Reserva sobre un servicio no disponible")  # Encabezado
    asesoria.cambiar_disponibilidad(False)  # Se desactiva la asesoría
    print("Resultado:", sistema.crear_reserva(ana, asesoria, 2))  # Falla por disponibilidad
    asesoria.cambiar_disponibilidad(True)  # Se reactiva

    titulo(18, "Reserva con cliente inexistente (None)")  # Encabezado
    print("Resultado:", sistema.crear_reserva(None, sala, 2))  # Falla: cliente inválido

    # ===================== PROCESAMIENTO Y CANCELACIÓN =====================
    titulo(19, "Procesar pago con monto suficiente")  # Encabezado
    cambio = sistema.ejecutar_operacion(f"Procesar reserva #{r1.id}", r1.procesar, 250000)  # Pago correcto
    print("Cambio entregado:", cambio)  # Muestra el cambio

    titulo(20, "Procesar pago con monto no numérico")  # Encabezado
    print("Resultado:", sistema.ejecutar_operacion(  # Operación protegida
        f"Procesar reserva #{r2.id}", r2.procesar, "mil pesos"))  # Falla con encadenamiento

    titulo(21, "Procesar pago insuficiente")  # Encabezado
    print("Resultado:", sistema.ejecutar_operacion(  # Operación protegida
        f"Procesar reserva #{r2.id}", r2.procesar, 1000))  # Falla: pago insuficiente

    titulo(22, "Cancelar reserva ya procesada (operación no permitida)")  # Encabezado
    print("Resultado:", sistema.ejecutar_operacion(  # Operación protegida
        f"Cancelar reserva #{r1.id}", r1.cancelar, "Cliente se arrepintió"))  # Falla

    titulo(23, "Cancelar reserva confirmada (válido)")  # Encabezado
    sistema.ejecutar_operacion(f"Cancelar reserva #{r2.id}", r2.cancelar, "Cambio de fecha")  # Válido
    print("Estado:", r2.estado)  # Muestra el nuevo estado

    # ===================== SOBRECARGA DE MÉTODOS =====================
    titulo(24, "Cotizaciones con métodos sobrecargados")  # Encabezado
    print("Sala 2 h (solo duración):", sala.calcular_costo(2))  # Variante 1: solo duración
    print("Sala 2 h (sin impuesto):", sala.calcular_costo(2, 0))  # Variante 2: impuesto personalizado
    print("Sala 2 h (IVA + 20 % desc.):", sala.calcular_costo(2, 0.19, 0.20))  # Variante 3: con descuento
    print("Cotizar con número:", asesoria.cotizar(1.5))  # singledispatch con float
    print("Cotizar con diccionario:", asesoria.cotizar({"duracion": 2, "descuento": 0.05}))  # Con dict
    print("Cotizar con texto:", sistema.ejecutar_operacion(  # Tipo no soportado
        "Cotizar con texto", asesoria.cotizar, "dos horas"))  # Falla controlada

    # ===================== CIERRE =====================
    print(sistema.resumen())  # Muestra todo lo que quedó en memoria
    print(f"\nEl sistema terminó sin interrupciones. Revise el log en: {ARCHIVO_LOG}")  # Mensaje final


if __name__ == "__main__":  # Solo se ejecuta si el archivo se corre directamente
    main()  # Llama a la función principal
