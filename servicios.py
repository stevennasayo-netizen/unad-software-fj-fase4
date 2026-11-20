"""
servicios.py
Clase abstracta Servicio y tres servicios especializados:
ReservaSala, AlquilerEquipo y Asesoria.
"""

from abc import abstractmethod  # Decorador para métodos abstractos
from functools import singledispatchmethod  # Permite "sobrecargar" métodos según el tipo de argumento
from entidad import Entidad  # Clase abstracta base
from excepciones import (  # Excepciones usadas en este módulo
    ServicioInvalidoError,  # Error al crear un servicio
    ValidacionError,  # Error de datos inválidos
    CalculoInconsistenteError,  # Error de cálculo
)  # Fin de importaciones


class Servicio(Entidad):  # Clase abstracta Servicio, hereda de Entidad
    """Servicio genérico que ofrece Software FJ."""

    IVA = 0.19  # Impuesto por defecto (19 % en Colombia)

    def __init__(self, nombre, tarifa_base, disponible=True):  # Constructor común a todos los servicios
        super().__init__()  # Asigna id y fecha desde Entidad
        if not nombre or not str(nombre).strip():  # El nombre es obligatorio
            raise ServicioInvalidoError("El servicio debe tener un nombre")  # Error si falta
        if not isinstance(tarifa_base, (int, float)) or tarifa_base <= 0:  # La tarifa debe ser número positivo
            raise ServicioInvalidoError(f"Tarifa base inválida: {tarifa_base}")  # Error si es incorrecta
        self._nombre = str(nombre).strip()  # Atributo protegido: nombre
        self._tarifa_base = float(tarifa_base)  # Atributo protegido: tarifa por hora/unidad
        self._disponible = bool(disponible)  # Atributo protegido: disponibilidad

    @property  # Getter del nombre
    def nombre(self):  # Devuelve el nombre
        return self._nombre  # Atributo protegido

    @property  # Getter de la tarifa base
    def tarifa_base(self):  # Devuelve la tarifa
        return self._tarifa_base  # Atributo protegido

    @property  # Getter de disponibilidad
    def disponible(self):  # Indica si el servicio está disponible
        return self._disponible  # Atributo protegido

    def cambiar_disponibilidad(self, estado):  # Permite activar o desactivar el servicio
        self._disponible = bool(estado)  # Se actualiza el estado

    # ---------- Métodos abstractos (polimorfismo) ----------

    @abstractmethod  # Cada servicio calcula su costo base a su manera
    def costo_base(self, duracion):  # Costo antes de impuestos y descuentos
        """Calcula el costo base según la duración."""

    @abstractmethod  # Cada servicio valida sus propios parámetros
    def validar_parametros(self, duracion):  # Valida la duración solicitada
        """Valida que la duración sea correcta para este servicio."""

    # ---------- Método "sobrecargado" con parámetros opcionales ----------

    def calcular_costo(self, duracion, impuesto=None, descuento=0.0):  # Variantes según parámetros
        """
        Calcula el costo total. Variantes de uso:
          calcular_costo(duracion)                     -> con IVA por defecto
          calcular_costo(duracion, impuesto)           -> con impuesto personalizado
          calcular_costo(duracion, impuesto, descuento) -> con impuesto y descuento
        """
        self.validar_parametros(duracion)  # Primero se valida la duración (puede lanzar excepción)
        impuesto = self.IVA if impuesto is None else impuesto  # Si no se da impuesto, se usa el IVA
        if not 0 <= impuesto <= 1:  # El impuesto debe estar entre 0 y 100 %
            raise CalculoInconsistenteError(f"Impuesto fuera de rango: {impuesto}")  # Error de cálculo
        if not 0 <= descuento < 1:  # El descuento debe estar entre 0 y menos de 100 %
            raise CalculoInconsistenteError(f"Descuento fuera de rango: {descuento}")  # Error de cálculo
        base = self.costo_base(duracion)  # Se obtiene el costo base (polimórfico)
        total = base * (1 - descuento) * (1 + impuesto)  # Se aplica descuento y luego impuesto
        if total <= 0:  # Un total cero o negativo es inconsistente
            raise CalculoInconsistenteError(f"Costo total inconsistente: {total}")  # Error de cálculo
        return round(total, 2)  # Se devuelve redondeado a dos decimales

    # ---------- Sobrecarga por tipo con singledispatchmethod ----------

    @singledispatchmethod  # Método base: se elige la versión según el tipo del argumento
    def cotizar(self, datos):  # Versión por defecto (tipo no soportado)
        raise ValidacionError(f"Tipo de dato no soportado para cotizar: {type(datos).__name__}")  # Error

    @cotizar.register(int)  # Versión para enteros
    @cotizar.register(float)  # Versión para decimales
    def _(self, datos):  # Recibe solo la duración
        return self.calcular_costo(datos)  # Cotiza con IVA por defecto

    @cotizar.register(dict)  # Versión para diccionarios
    def _(self, datos):  # Recibe {'duracion': .., 'impuesto': .., 'descuento': ..}
        if "duracion" not in datos:  # La duración es obligatoria
            raise ValidacionError("El diccionario de cotización requiere 'duracion'")  # Error
        return self.calcular_costo(  # Llama al cálculo con los valores del diccionario
            datos["duracion"],  # Duración
            datos.get("impuesto"),  # Impuesto opcional
            datos.get("descuento", 0.0),  # Descuento opcional
        )  # Fin de la llamada

    def validar(self):  # Implementación del método abstracto de Entidad
        if self._tarifa_base <= 0:  # La tarifa no puede ser negativa ni cero
            raise ServicioInvalidoError("Tarifa base inválida")  # Error
        return True  # Servicio válido


class ReservaSala(Servicio):  # Servicio especializado 1: reserva de salas
    """Reserva de salas de reuniones por horas."""

    def __init__(self, nombre, tarifa_base, capacidad, disponible=True):  # Constructor de la sala
        super().__init__(nombre, tarifa_base, disponible)  # Inicializa la parte común
        if not isinstance(capacidad, int) or capacidad <= 0:  # La capacidad debe ser entero positivo
            raise ServicioInvalidoError(f"Capacidad de sala inválida: {capacidad}")  # Error
        self._capacidad = capacidad  # Se guarda la capacidad de personas

    def validar_parametros(self, duracion):  # Sobrescribe la validación (polimorfismo)
        if not isinstance(duracion, (int, float)) or not 1 <= duracion <= 12:  # Entre 1 y 12 horas
            raise ValidacionError(f"Una sala se reserva entre 1 y 12 horas (recibido: {duracion})")  # Error
        return True  # Duración válida

    def costo_base(self, duracion):  # Sobrescribe el cálculo del costo base
        recargo = 1.2 if self._capacidad > 20 else 1.0  # Salas grandes tienen recargo del 20 %
        return self._tarifa_base * duracion * recargo  # Tarifa x horas x recargo

    def describir(self):  # Sobrescribe la descripción
        return f"Sala '{self._nombre}' para {self._capacidad} personas - ${self._tarifa_base:,.0f}/hora"  # Texto


class AlquilerEquipo(Servicio):  # Servicio especializado 2: alquiler de equipos
    """Alquiler de equipos tecnológicos por días."""

    def __init__(self, nombre, tarifa_base, tipo_equipo, cantidad, disponible=True):  # Constructor
        super().__init__(nombre, tarifa_base, disponible)  # Inicializa la parte común
        if not tipo_equipo:  # El tipo de equipo es obligatorio
            raise ServicioInvalidoError("Debe indicar el tipo de equipo")  # Error
        if not isinstance(cantidad, int) or cantidad <= 0:  # La cantidad debe ser entero positivo
            raise ServicioInvalidoError(f"Cantidad de equipos inválida: {cantidad}")  # Error
        self._tipo_equipo = tipo_equipo  # Se guarda el tipo de equipo
        self._cantidad = cantidad  # Se guarda la cantidad de unidades

    def validar_parametros(self, duracion):  # Sobrescribe la validación
        if not isinstance(duracion, int) or not 1 <= duracion <= 30:  # Días enteros entre 1 y 30
            raise ValidacionError(f"Los equipos se alquilan de 1 a 30 días enteros (recibido: {duracion})")  # Error
        return True  # Duración válida

    def costo_base(self, duracion):  # Sobrescribe el cálculo del costo base
        return self._tarifa_base * duracion * self._cantidad  # Tarifa x días x unidades

    def describir(self):  # Sobrescribe la descripción
        return f"{self._cantidad} x {self._tipo_equipo} ('{self._nombre}') - ${self._tarifa_base:,.0f}/día c/u"  # Texto


class Asesoria(Servicio):  # Servicio especializado 3: asesorías
    """Asesoría especializada por horas, con nivel de experticia."""

    NIVELES = {"basico": 1.0, "intermedio": 1.5, "experto": 2.0}  # Multiplicador según nivel

    def __init__(self, nombre, tarifa_base, especialidad, nivel="basico", disponible=True):  # Constructor
        super().__init__(nombre, tarifa_base, disponible)  # Inicializa la parte común
        if not especialidad:  # La especialidad es obligatoria
            raise ServicioInvalidoError("La asesoría debe tener una especialidad")  # Error
        if nivel not in self.NIVELES:  # El nivel debe existir en el diccionario
            raise ServicioInvalidoError(f"Nivel '{nivel}' no válido. Use: {list(self.NIVELES)}")  # Error
        self._especialidad = especialidad  # Se guarda la especialidad
        self._nivel = nivel  # Se guarda el nivel

    def validar_parametros(self, duracion):  # Sobrescribe la validación
        if not isinstance(duracion, (int, float)) or not 0.5 <= duracion <= 8:  # Entre media hora y 8 horas
            raise ValidacionError(f"Una asesoría dura entre 0.5 y 8 horas (recibido: {duracion})")  # Error
        return True  # Duración válida

    def costo_base(self, duracion):  # Sobrescribe el cálculo del costo base
        return self._tarifa_base * duracion * self.NIVELES[self._nivel]  # Tarifa x horas x nivel

    def describir(self):  # Sobrescribe la descripción
        return f"Asesoría en {self._especialidad} (nivel {self._nivel}) - ${self._tarifa_base:,.0f}/hora"  # Texto
