"""
excepciones.py
Módulo que define las excepciones personalizadas del sistema Software FJ.
Todas heredan de una excepción base común para poder capturarlas en grupo.
"""


class SoftwareFJError(Exception):  # Excepción base de todo el sistema
    """Excepción raíz de la que heredan todos los errores propios del sistema."""

    def __init__(self, mensaje, codigo="ERR-GEN"):  # Constructor recibe mensaje y código de error
        super().__init__(mensaje)  # Se inicializa la clase Exception con el mensaje
        self.mensaje = mensaje  # Se guarda el mensaje para usarlo en los logs
        self.codigo = codigo  # Se guarda un código corto que identifica el tipo de error

    def __str__(self):  # Representación en texto de la excepción
        return f"[{self.codigo}] {self.mensaje}"  # Se muestra el código junto al mensaje


class ValidacionError(SoftwareFJError):  # Error genérico de datos inválidos
    """Se lanza cuando un dato no cumple las reglas de validación."""

    def __init__(self, mensaje):  # Constructor con el mensaje del error
        super().__init__(mensaje, "ERR-VAL")  # Se asigna el código de validación


class ParametroFaltanteError(ValidacionError):  # Error cuando falta un dato obligatorio
    """Se lanza cuando un parámetro obligatorio no fue suministrado."""

    def __init__(self, parametro):  # Recibe el nombre del parámetro que falta
        super().__init__(f"Falta el parámetro obligatorio: '{parametro}'")  # Mensaje descriptivo
        self.codigo = "ERR-PAR"  # Se sobrescribe el código para diferenciarlo


class ClienteInvalidoError(SoftwareFJError):  # Error al registrar un cliente
    """Se lanza cuando no es posible crear o registrar un cliente."""

    def __init__(self, mensaje):  # Constructor con el mensaje del error
        super().__init__(mensaje, "ERR-CLI")  # Código propio de clientes


class ServicioInvalidoError(SoftwareFJError):  # Error al crear un servicio
    """Se lanza cuando un servicio se crea con parámetros incorrectos."""

    def __init__(self, mensaje):  # Constructor con el mensaje del error
        super().__init__(mensaje, "ERR-SRV")  # Código propio de servicios


class ServicioNoDisponibleError(SoftwareFJError):  # Error cuando el servicio no se puede usar
    """Se lanza cuando se intenta reservar un servicio que no está disponible."""

    def __init__(self, nombre_servicio):  # Recibe el nombre del servicio
        super().__init__(f"El servicio '{nombre_servicio}' no está disponible", "ERR-DIS")  # Mensaje y código


class ReservaInvalidaError(SoftwareFJError):  # Error al crear o procesar una reserva
    """Se lanza cuando una reserva no puede crearse o procesarse."""

    def __init__(self, mensaje):  # Constructor con el mensaje del error
        super().__init__(mensaje, "ERR-RES")  # Código propio de reservas


class OperacionNoPermitidaError(SoftwareFJError):  # Error de transición de estado inválida
    """Se lanza cuando se intenta una acción no permitida en el estado actual."""

    def __init__(self, mensaje):  # Constructor con el mensaje del error
        super().__init__(mensaje, "ERR-OPE")  # Código de operación no permitida


class CalculoInconsistenteError(SoftwareFJError):  # Error en el cálculo de costos
    """Se lanza cuando un cálculo produce un resultado ilógico (ej. costo negativo)."""

    def __init__(self, mensaje):  # Constructor con el mensaje del error
        super().__init__(mensaje, "ERR-CAL")  # Código de cálculo inconsistente


class FechaInvalidaError(ValidacionError):  # Error cuando la fecha de la reserva no es válida
    """Se lanza cuando la fecha de una reserva es anterior a hoy o no tiene el formato correcto."""

    def __init__(self, mensaje):  # Constructor con el mensaje del error
        super().__init__(mensaje)  # Se inicializa como error de validación
        self.codigo = "ERR-FEC"  # Código propio para errores de fecha


class LimiteReservasError(SoftwareFJError):  # Error cuando un cliente supera el máximo de reservas
    """Se lanza cuando un cliente intenta tener más reservas activas de las permitidas."""

    def __init__(self, nombre_cliente, limite):  # Recibe el nombre del cliente y el límite vigente
        super().__init__(  # Se inicializa la excepción base
            f"{nombre_cliente} ya tiene {limite} reservas activas (máximo permitido: {limite})",  # Mensaje
            "ERR-LIM",  # Código propio del límite de reservas
        )  # Fin de la inicialización
