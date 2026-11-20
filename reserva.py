"""
reserva.py
Clase Reserva que integra cliente, servicio, duración y estado.
Implementa confirmación, cancelación y procesamiento con manejo de excepciones.
"""

from entidad import Entidad  # Clase abstracta base
from cliente import Cliente  # Clase Cliente para validar el tipo
from servicios import Servicio  # Clase Servicio para validar el tipo
from logger import log  # Logger global del sistema
from excepciones import (  # Excepciones usadas
    ReservaInvalidaError,  # Error al crear/procesar la reserva
    ServicioNoDisponibleError,  # Servicio no disponible
    OperacionNoPermitidaError,  # Transición de estado inválida
    SoftwareFJError,  # Excepción base del sistema
)  # Fin de importaciones


class Reserva(Entidad):  # Reserva hereda de Entidad
    """Reserva de un servicio por parte de un cliente."""

    PENDIENTE = "PENDIENTE"  # Estado inicial
    CONFIRMADA = "CONFIRMADA"  # Estado después de confirmar
    CANCELADA = "CANCELADA"  # Estado después de cancelar
    PROCESADA = "PROCESADA"  # Estado final después de procesar el pago

    def __init__(self, cliente, servicio, duracion):  # Constructor de la reserva
        super().__init__()  # Asigna id y fecha
        if not isinstance(cliente, Cliente):  # El cliente debe ser un objeto Cliente
            raise ReservaInvalidaError("La reserva requiere un cliente válido")  # Error
        if not isinstance(servicio, Servicio):  # El servicio debe ser un objeto Servicio
            raise ReservaInvalidaError("La reserva requiere un servicio válido")  # Error
        self.__cliente = cliente  # Atributo privado: cliente
        self.__servicio = servicio  # Atributo privado: servicio
        self.__duracion = duracion  # Atributo privado: duración solicitada
        self.__estado = Reserva.PENDIENTE  # Toda reserva inicia como pendiente
        self.__costo = None  # El costo se calcula al confirmar

    @property  # Getter del estado
    def estado(self):  # Devuelve el estado actual
        return self.__estado  # Atributo privado

    @property  # Getter del costo
    def costo(self):  # Devuelve el costo calculado
        return self.__costo  # Atributo privado

    @property  # Getter del cliente
    def cliente(self):  # Devuelve el cliente
        return self.__cliente  # Atributo privado

    @property  # Getter del servicio
    def servicio(self):  # Devuelve el servicio
        return self.__servicio  # Atributo privado

    def validar(self):  # Implementación del método abstracto de Entidad
        self.__cliente.validar()  # Valida el cliente
        self.__servicio.validar_parametros(self.__duracion)  # Valida la duración para ese servicio
        return True  # Reserva válida

    def describir(self):  # Implementación del método abstracto de Entidad
        costo = f"${self.__costo:,.2f}" if self.__costo else "sin calcular"  # Texto del costo
        return (f"{self.__cliente.nombre} -> {self.__servicio.nombre} "  # Cliente y servicio
                f"({self.__duracion}) [{self.__estado}] costo: {costo}")  # Duración, estado y costo

    def confirmar(self, impuesto=None, descuento=0.0):  # Confirma la reserva
        """Confirma la reserva usando try/except/else."""
        if self.__estado != Reserva.PENDIENTE:  # Solo se confirman reservas pendientes
            raise OperacionNoPermitidaError(  # Error si el estado no es el correcto
                f"No se puede confirmar la reserva #{self.id} en estado {self.__estado}")  # Mensaje
        if not self.__servicio.disponible:  # Si el servicio no está disponible
            raise ServicioNoDisponibleError(self.__servicio.nombre)  # Error de disponibilidad
        try:  # Bloque que puede fallar
            self.validar()  # Valida cliente y duración
            costo = self.__servicio.calcular_costo(self.__duracion, impuesto, descuento)  # Calcula el costo
        except SoftwareFJError as error:  # Si falla la validación o el cálculo
            raise ReservaInvalidaError(  # Se lanza un error de reserva...
                f"No se pudo confirmar la reserva #{self.id}") from error  # ...encadenado con la causa original
        else:  # Solo se ejecuta si NO hubo excepción
            self.__costo = costo  # Se guarda el costo calculado
            self.__estado = Reserva.CONFIRMADA  # Se cambia el estado
            log.info(f"Reserva #{self.id} confirmada por ${costo:,.2f}")  # Se registra el evento
        return self.__costo  # Devuelve el costo confirmado

    def cancelar(self, motivo="Sin motivo"):  # Cancela la reserva
        """Cancela la reserva si su estado lo permite."""
        if self.__estado in (Reserva.CANCELADA, Reserva.PROCESADA):  # No se cancela lo ya cancelado o procesado
            raise OperacionNoPermitidaError(  # Error de operación no permitida
                f"No se puede cancelar la reserva #{self.id} en estado {self.__estado}")  # Mensaje
        self.__estado = Reserva.CANCELADA  # Se cambia el estado
        log.info(f"Reserva #{self.id} cancelada. Motivo: {motivo}")  # Se registra el evento

    def procesar(self, monto_pagado):  # Procesa el pago de la reserva
        """Procesa el pago usando try/except/finally y encadenamiento."""
        log.info(f"Iniciando procesamiento de la reserva #{self.id}")  # Evento de inicio
        try:  # Bloque que puede fallar
            if self.__estado != Reserva.CONFIRMADA:  # Solo se procesan reservas confirmadas
                raise OperacionNoPermitidaError(  # Error de estado
                    f"La reserva #{self.id} debe estar CONFIRMADA (estado actual: {self.__estado})")  # Mensaje
            monto = float(monto_pagado)  # Convierte el monto a número (puede lanzar ValueError/TypeError)
            if monto < self.__costo:  # Si el pago no cubre el costo
                raise ReservaInvalidaError(  # Error de pago insuficiente
                    f"Pago insuficiente: ${monto:,.2f} de ${self.__costo:,.2f}")  # Mensaje
            self.__estado = Reserva.PROCESADA  # Se marca como procesada
            cambio = round(monto - self.__costo, 2)  # Se calcula el cambio
            log.info(f"Reserva #{self.id} procesada. Cambio: ${cambio:,.2f}")  # Evento exitoso
            return cambio  # Devuelve el cambio al cliente
        except (ValueError, TypeError) as error:  # Errores nativos de Python al convertir el monto
            raise ReservaInvalidaError(  # Se transforman en error del sistema...
                f"Monto de pago inválido: {monto_pagado!r}") from error  # ...encadenando la causa
        finally:  # Se ejecuta SIEMPRE, haya o no error
            log.info(f"Fin del procesamiento de la reserva #{self.id} (estado: {self.__estado})")  # Cierre
