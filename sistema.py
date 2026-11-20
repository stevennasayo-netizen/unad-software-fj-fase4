"""
sistema.py
Gestor central que administra listas internas de clientes, servicios y reservas.
Captura todos los errores para que la aplicación nunca se detenga.
"""

from cliente import Cliente  # Clase Cliente
from reserva import Reserva  # Clase Reserva
from logger import log  # Logger global
from excepciones import SoftwareFJError, ClienteInvalidoError, LimiteReservasError  # Excepciones del sistema


class SistemaSoftwareFJ:  # Clase que coordina toda la operación
    """Administra clientes, servicios y reservas en memoria (sin base de datos)."""

    MAX_RESERVAS_ACTIVAS = 3  # Regla de negocio: máximo de reservas vigentes por cliente

    def __init__(self):  # Constructor del sistema
        self.__clientes = []  # Lista interna de clientes
        self.__servicios = []  # Lista interna de servicios
        self.__reservas = []  # Lista interna de reservas
        log.info("=== Sistema Software FJ iniciado ===")  # Evento de inicio

    # ---------- Clientes ----------

    def registrar_cliente(self, nombre, documento, correo, telefono):  # Registra un cliente nuevo
        """Crea y agrega un cliente. Devuelve el cliente o None si falla."""
        try:  # Bloque que puede fallar
            if any(c.documento == str(documento).strip() for c in self.__clientes):  # Documento repetido
                raise ClienteInvalidoError(f"Ya existe un cliente con documento {documento}")  # Error
            cliente = Cliente(nombre, documento, correo, telefono)  # Crea el cliente (valida en los setters)
        except SoftwareFJError as error:  # Si hubo un error del sistema
            log.error(f"Registro de cliente fallido: {error}")  # Se registra el error en el log
            return None  # Se devuelve None y el programa continúa
        else:  # Si no hubo error
            self.__clientes.append(cliente)  # Se agrega a la lista
            log.info(f"Cliente registrado: {cliente}")  # Se registra el evento
            return cliente  # Se devuelve el cliente creado

    # ---------- Servicios ----------

    def registrar_servicio(self, clase_servicio, *args, **kwargs):  # Registra cualquier tipo de servicio
        """Crea un servicio de la clase indicada. Devuelve el servicio o None si falla."""
        try:  # Bloque que puede fallar
            servicio = clase_servicio(*args, **kwargs)  # Se crea el servicio (polimorfismo de constructores)
        except SoftwareFJError as error:  # Error del sistema al crear
            log.error(f"Creación de servicio {clase_servicio.__name__} fallida: {error}")  # Se registra
            return None  # El programa continúa
        except TypeError as error:  # Parámetros faltantes o de más en el constructor
            log.error(f"Parámetros incorrectos para {clase_servicio.__name__}: {error}")  # Se registra
            return None  # El programa continúa
        else:  # Si no hubo error
            self.__servicios.append(servicio)  # Se agrega a la lista
            log.info(f"Servicio registrado: {servicio}")  # Se registra el evento
            return servicio  # Se devuelve el servicio

    # ---------- Reservas ----------

    def reservas_activas_de(self, cliente):  # Cuenta las reservas vigentes de un cliente
        """Devuelve cuántas reservas pendientes o confirmadas tiene el cliente."""
        return sum(1 for r in self.__reservas if r.cliente is cliente and r.activa)  # Conteo

    def crear_reserva(self, cliente, servicio, duracion, impuesto=None, descuento=0.0, fecha=None):  # Crea y confirma
        """Crea una reserva y la confirma. Devuelve la reserva o None si falla."""
        reserva = None  # Variable que guardará la reserva
        try:  # Bloque que puede fallar
            if cliente is not None and self.reservas_activas_de(cliente) >= self.MAX_RESERVAS_ACTIVAS:  # Límite
                raise LimiteReservasError(cliente.nombre, self.MAX_RESERVAS_ACTIVAS)  # Error de límite
            reserva = Reserva(cliente, servicio, duracion, fecha)  # Se crea la reserva con su fecha
            reserva.confirmar(impuesto, descuento)  # Se confirma (calcula el costo)
        except SoftwareFJError as error:  # Cualquier error del sistema
            causa = f" | Causa: {error.__cause__}" if error.__cause__ else ""  # Muestra la excepción encadenada
            log.error(f"Reserva fallida: {error}{causa}")  # Se registra el error con su causa
            if reserva is not None:  # Si la reserva alcanzó a crearse
                reserva.cancelar("Error en la confirmación")  # Se cancela automáticamente
                self.__reservas.append(reserva)  # Se guarda para trazabilidad
            return None  # El programa continúa
        else:  # Si no hubo error
            self.__reservas.append(reserva)  # Se agrega a la lista
            return reserva  # Se devuelve la reserva confirmada
        finally:  # Se ejecuta siempre
            log.debug(f"Intento de reserva terminado. Total reservas: {len(self.__reservas)}")  # Traza

    def ejecutar_operacion(self, descripcion, funcion, *args, **kwargs):  # Ejecuta cualquier acción segura
        """Ejecuta una operación protegida para que ningún error detenga el programa."""
        try:  # Bloque protegido
            resultado = funcion(*args, **kwargs)  # Se ejecuta la operación
        except SoftwareFJError as error:  # Error conocido del sistema
            causa = f" | Causa: {error.__cause__}" if error.__cause__ else ""  # Causa encadenada si existe
            log.error(f"{descripcion} -> {error}{causa}")  # Se registra
            return None  # Continúa
        except Exception as error:  # Cualquier error inesperado
            log.critical(f"{descripcion} -> error inesperado {type(error).__name__}: {error}")  # Se registra
            return None  # Continúa de todas formas
        else:  # Si salió bien
            log.info(f"{descripcion} -> OK")  # Se registra el éxito
            return resultado  # Devuelve el resultado

    # ---------- Consultas ----------

    @property  # Copia de la lista de clientes (no se expone la original)
    def clientes(self):  # Getter de clientes
        return list(self.__clientes)  # Devuelve una copia

    @property  # Copia de la lista de servicios
    def servicios(self):  # Getter de servicios
        return list(self.__servicios)  # Devuelve una copia

    @property  # Copia de la lista de reservas
    def reservas(self):  # Getter de reservas
        return list(self.__reservas)  # Devuelve una copia

    def buscar_cliente(self, documento):  # Busca un cliente por su documento
        """Devuelve el cliente con ese documento o None si no existe."""
        documento = str(documento).strip()  # Se limpia el texto recibido
        return next((c for c in self.__clientes if c.documento == documento), None)  # Primera coincidencia

    def buscar_reserva(self, id_reserva):  # Busca una reserva por su número
        """Devuelve la reserva con ese id o None si no existe."""
        return next((r for r in self.__reservas if r.id == id_reserva), None)  # Primera coincidencia

    def resumen(self):  # Devuelve un resumen del estado del sistema
        """Devuelve un texto con todo lo registrado en memoria."""
        lineas = ["\n========== RESUMEN DEL SISTEMA =========="]  # Encabezado
        lineas.append(f"Clientes ({len(self.__clientes)}):")  # Cantidad de clientes
        lineas += [f"  - {c}" for c in self.__clientes]  # Lista de clientes
        lineas.append(f"Servicios ({len(self.__servicios)}):")  # Cantidad de servicios
        lineas += [f"  - {s}" for s in self.__servicios]  # Lista de servicios
        lineas.append(f"Reservas ({len(self.__reservas)}):")  # Cantidad de reservas
        lineas += [f"  - {r}" for r in self.__reservas]  # Lista de reservas
        return "\n".join(lineas)  # Une todo en un solo texto
