"""
entidad.py
Clase abstracta que representa cualquier entidad general del sistema.
"""

from abc import ABC, abstractmethod  # Herramientas para crear clases abstractas
from datetime import datetime  # Para registrar la fecha de creación


class Entidad(ABC):  # Clase abstracta base: no se puede instanciar directamente
    """Entidad general del sistema con identificador único y fecha de creación."""

    _contador = 0  # Atributo de clase que lleva la cuenta de entidades creadas

    def __init__(self):  # Constructor común a todas las entidades
        Entidad._contador += 1  # Se incrementa el contador global
        self._id = Entidad._contador  # Se asigna un identificador único (atributo protegido)
        self._fecha_creacion = datetime.now()  # Se guarda el momento de creación

    @property  # Permite leer el id como atributo sin poder modificarlo
    def id(self):  # Getter del identificador
        return self._id  # Devuelve el identificador

    @property  # Propiedad de solo lectura
    def fecha_creacion(self):  # Getter de la fecha de creación
        return self._fecha_creacion  # Devuelve la fecha de creación

    @abstractmethod  # Obliga a las clases hijas a implementarlo
    def describir(self):  # Método que describe la entidad
        """Devuelve una descripción en texto de la entidad."""

    @abstractmethod  # Obliga a las clases hijas a implementarlo
    def validar(self):  # Método que valida el estado de la entidad
        """Valida los datos de la entidad y lanza una excepción si son inválidos."""

    def __str__(self):  # Representación en texto común para todas las entidades
        return f"{self.__class__.__name__}#{self._id}: {self.describir()}"  # Clase, id y descripción
