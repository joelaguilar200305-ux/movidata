"""Configuración de logging del proyecto MoviData Panamá.

Envía los mensajes por niveles (DEBUG, INFO, WARNING, ERROR) a la consola
y al archivo logs/movidata.log.
"""

import logging
from pathlib import Path

CARPETA_LOGS = Path("logs")
ARCHIVO_LOG = CARPETA_LOGS / "movidata.log"
FORMATO = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"


def get_logger(nombre: str, nivel: int = logging.INFO) -> logging.Logger:
    """Devuelve un logger configurado con salida a consola y a archivo."""
    CARPETA_LOGS.mkdir(exist_ok=True)

    logger = logging.getLogger(nombre)
    logger.setLevel(nivel)

    # Evita duplicar mensajes si se llama varias veces con el mismo nombre
    if not logger.handlers:
        formato = logging.Formatter(FORMATO)

        consola = logging.StreamHandler()
        consola.setFormatter(formato)

        archivo = logging.FileHandler(ARCHIVO_LOG, encoding="utf-8")
        archivo.setFormatter(formato)

        logger.addHandler(consola)
        logger.addHandler(archivo)

    return logger