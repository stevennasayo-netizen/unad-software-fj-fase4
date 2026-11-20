"""
logger.py
Configura el registro de eventos y errores en el archivo logs/sistema.log.
"""

import logging  # Módulo estándar de Python para registrar eventos
import os  # Módulo para manejar rutas y carpetas del sistema operativo

CARPETA_LOGS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")  # Ruta de la carpeta de logs
ARCHIVO_LOG = os.path.join(CARPETA_LOGS, "sistema.log")  # Ruta completa del archivo de log


def obtener_logger(nombre="SoftwareFJ"):  # Función que entrega un logger configurado
    """Devuelve un logger que escribe en archivo y en consola."""
    os.makedirs(CARPETA_LOGS, exist_ok=True)  # Crea la carpeta de logs si no existe
    logger = logging.getLogger(nombre)  # Obtiene (o crea) el logger con ese nombre
    if logger.handlers:  # Si ya tiene manejadores configurados
        return logger  # Se devuelve tal cual para no duplicar mensajes
    logger.setLevel(logging.DEBUG)  # Se registran todos los niveles desde DEBUG
    formato = logging.Formatter(  # Se define el formato de cada línea del log
        "%(asctime)s | %(levelname)-8s | %(message)s",  # Fecha, nivel y mensaje
        datefmt="%Y-%m-%d %H:%M:%S",  # Formato de la fecha
    )  # Fin de la definición del formato
    manejador_archivo = logging.FileHandler(ARCHIVO_LOG, encoding="utf-8")  # Escribe en el archivo de log
    manejador_archivo.setFormatter(formato)  # Aplica el formato al archivo
    manejador_consola = logging.StreamHandler()  # Muestra los mensajes en consola
    manejador_consola.setLevel(logging.WARNING)  # En consola solo advertencias y errores
    manejador_consola.setFormatter(formato)  # Aplica el formato a la consola
    logger.addHandler(manejador_archivo)  # Agrega el manejador de archivo
    logger.addHandler(manejador_consola)  # Agrega el manejador de consola
    return logger  # Devuelve el logger listo para usar


log = obtener_logger()  # Instancia global del logger que usan los demás módulos
