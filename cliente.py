"""
cliente.py
Clase Cliente con encapsulación de datos personales y validaciones estrictas.
"""

import re  # Módulo de expresiones regulares para validar formatos
from entidad import Entidad  # Clase abstracta base
from excepciones import ValidacionError, ParametroFaltanteError  # Excepciones usadas


class Cliente(Entidad):  # Cliente hereda de Entidad
    """Representa un cliente de Software FJ."""

    PATRON_CORREO = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.-]+$")  # Patrón válido de correo electrónico

    def __init__(self, nombre, documento, correo, telefono):  # Constructor del cliente
        super().__init__()  # Llama al constructor de Entidad (asigna id y fecha)
        self.__nombre = None  # Atributo privado: nombre
        self.__documento = None  # Atributo privado: documento de identidad
        self.__correo = None  # Atributo privado: correo electrónico
        self.__telefono = None  # Atributo privado: teléfono
        self.nombre = nombre  # Se asigna usando el setter (valida automáticamente)
        self.documento = documento  # Se asigna usando el setter
        self.correo = correo  # Se asigna usando el setter
        self.telefono = telefono  # Se asigna usando el setter

    # ---------- Propiedades (encapsulación) ----------

    @property  # Getter del nombre
    def nombre(self):  # Devuelve el nombre
        return self.__nombre  # Acceso al atributo privado

    @nombre.setter  # Setter del nombre con validación
    def nombre(self, valor):  # Recibe el nuevo nombre
        if valor is None or str(valor).strip() == "":  # Si el nombre está vacío
            raise ParametroFaltanteError("nombre")  # Se lanza error de parámetro faltante
        valor = str(valor).strip()  # Se limpian espacios al inicio y final
        if not all(c.isalpha() or c.isspace() for c in valor):  # Solo letras y espacios
            raise ValidacionError(f"El nombre '{valor}' solo puede contener letras")  # Error de formato
        if len(valor) < 3:  # Longitud mínima de 3 caracteres
            raise ValidacionError("El nombre debe tener al menos 3 caracteres")  # Error de longitud
        self.__nombre = valor.title()  # Se guarda con mayúscula inicial en cada palabra

    @property  # Getter del documento
    def documento(self):  # Devuelve el documento
        return self.__documento  # Acceso al atributo privado

    @documento.setter  # Setter del documento con validación
    def documento(self, valor):  # Recibe el nuevo documento
        if valor is None or str(valor).strip() == "":  # Si el documento está vacío
            raise ParametroFaltanteError("documento")  # Error de parámetro faltante
        valor = str(valor).strip()  # Se convierte a texto sin espacios
        if not valor.isdigit() or not 6 <= len(valor) <= 10:  # Solo dígitos, entre 6 y 10
            raise ValidacionError(f"Documento '{valor}' inválido: debe tener 6 a 10 dígitos")  # Error
        self.__documento = valor  # Se guarda el documento válido

    @property  # Getter del correo
    def correo(self):  # Devuelve el correo
        return self.__correo  # Acceso al atributo privado

    @correo.setter  # Setter del correo con validación
    def correo(self, valor):  # Recibe el nuevo correo
        if not valor:  # Si el correo está vacío o es None
            raise ParametroFaltanteError("correo")  # Error de parámetro faltante
        if not self.PATRON_CORREO.match(valor):  # Si no cumple el patrón de correo
            raise ValidacionError(f"Correo '{valor}' con formato inválido")  # Error de formato
        self.__correo = valor.lower()  # Se guarda en minúsculas

    @property  # Getter del teléfono
    def telefono(self):  # Devuelve el teléfono
        return self.__telefono  # Acceso al atributo privado

    @telefono.setter  # Setter del teléfono con validación
    def telefono(self, valor):  # Recibe el nuevo teléfono
        valor = str(valor or "").strip()  # Se convierte a texto (vacío si es None)
        if not valor.isdigit() or len(valor) != 10:  # Debe tener exactamente 10 dígitos
            raise ValidacionError(f"Teléfono '{valor}' inválido: debe tener 10 dígitos")  # Error
        self.__telefono = valor  # Se guarda el teléfono válido

    # ---------- Métodos abstractos implementados ----------

    def validar(self):  # Implementación del método abstracto de Entidad
        """Verifica que todos los datos obligatorios estén presentes."""
        for campo in ("nombre", "documento", "correo", "telefono"):  # Recorre los campos
            if getattr(self, campo) is None:  # Si alguno quedó sin valor
                raise ParametroFaltanteError(campo)  # Se lanza el error correspondiente
        return True  # Si todo está bien, retorna True

    def describir(self):  # Implementación del método abstracto de Entidad
        """Devuelve una descripción del cliente ocultando parte del documento."""
        doc_oculto = "*" * (len(self.__documento) - 4) + self.__documento[-4:]  # Oculta dígitos iniciales
        return f"{self.__nombre} (Doc: {doc_oculto}, {self.__correo})"  # Texto descriptivo
