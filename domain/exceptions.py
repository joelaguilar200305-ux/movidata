"""Jerarquía de excepciones del proyecto MoviData Panamá.

Todas las excepciones propias heredan de AppError, de modo que el código
que las captura puede atrapar cualquier error del proyecto con una sola
cláusula `except AppError`.
"""


class AppError(Exception):
    """Excepción base de la aplicación."""


class DataLoadError(AppError):
    """Error al leer o cargar los datos (archivo CSV ausente, formato inválido)."""


class RepositoryError(AppError):
    """Error de acceso a la base de datos (conexión, consulta, agregación)."""


class AnalysisError(AppError):
    """Error durante el análisis o procesamiento de los datos."""