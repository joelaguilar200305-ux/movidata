
import os
import re
from datetime import date, datetime
from typing import Any, Optional

from pymongo import UpdateOne
from pymongo.errors import PyMongoError

from config.conexion_mongo import MongoConnection
from domain.viaje import Viaje
from domain.exceptions import RepositoryError
from repositories.i_viaje_repository import IViajeRepository
from utils.logging_config import get_logger


logger = get_logger(__name__)


class MongoViajeRepository(IViajeRepository):

    # 1. CONEXION CENTRALIZADA A MONGODB ATLAS
    def __init__(self):
        try:
            self.conexion = MongoConnection.get_instance()
            self.coleccion = self.conexion.coleccion
            logger.info("Repository de viajes conectado correctamente")
        except PyMongoError as error:
            logger.exception("No fue posible conectar el Repository a MongoDB")
            raise RepositoryError("No se pudo conectar con MongoDB") from error

    # 2. BUSCAR VIAJE POR ID
    def buscar_por_id(self, trip_id: str) -> Optional[Viaje]:
        try:
            documento = self.coleccion.find_one(
                {"trip_id": trip_id},
                {"_id": 0},
                max_time_ms=15000
            )
            return None if documento is None else Viaje.desde_documento(documento)
        except PyMongoError as error:
            logger.exception("Error al buscar viaje por identificador")
            raise RepositoryError("No se pudo buscar el viaje") from error

    # 3. BUSCAR VIAJES UTILIZANDO FILTROS
    def buscar_por_filtro(
        self,
        filtros: dict[str, Any],
        limite: int = 100
    ) -> list[Viaje]:
        if isinstance(limite, bool) or not isinstance(limite, int) or not 1 <= limite <= 1000:
            raise ValueError("El limite debe estar entre 1 y 1000")

        try:
            documentos = self.coleccion.find(
                filtros,
                {"_id": 0}
            ).limit(limite).max_time_ms(15000)

            viajes = [Viaje.desde_documento(doc) for doc in documentos]
            logger.info("Filtro de viajes ejecutado; resultados: %s", len(viajes))
            return viajes
        except PyMongoError as error:
            logger.exception("Error al consultar viajes con filtros")
            raise RepositoryError("No se pudo consultar viajes con filtros") from error

    # 4. CONTAR DOCUMENTOS
    def contar_documentos(
        self,
        filtros: Optional[dict[str, Any]] = None
    ) -> int:
        try:
            total = self.coleccion.count_documents(
                filtros if filtros is not None else {},
                maxTimeMS=15000
            )
            logger.info("Conteo de viajes completado")
            return total
        except PyMongoError as error:
            logger.exception("Error al contar documentos")
            raise RepositoryError("No se pudieron contar los viajes") from error

    # 5. EJECUTAR AGREGACIONES
    def agregar(self, pipeline: list[dict[str, Any]]) -> list[dict[str, Any]]:
        if not pipeline:
            raise ValueError("El pipeline no puede estar vacio")

        etapas_prohibidas = {"$out", "$merge"}
        for etapa in pipeline:
            if any(operador in etapa for operador in etapas_prohibidas):
                raise ValueError("No se permiten operaciones de escritura")

        try:
            cursor = self.coleccion.aggregate(
                pipeline,
                allowDiskUse=False,
                maxTimeMS=15000
            )
            resultados = list(cursor)
            logger.info("Agregacion completada; resultados: %s", len(resultados))
            return resultados
        except PyMongoError as error:
            logger.exception("Error al ejecutar agregacion")
            raise RepositoryError("No se pudo ejecutar la agregacion") from error

    # 6. BUSCAR VIAJES CON PROYECCION DE CAMPOS
    def buscar_con_proyeccion(
        self,
        filtros: dict[str, Any],
        campos: list[str],
        limite: int = 100
    ) -> list[dict[str, Any]]:
        if isinstance(limite, bool) or not isinstance(limite, int) or not 1 <= limite <= 1000:
            raise ValueError("El limite debe estar entre 1 y 1000")
        if not campos:
            raise ValueError("Debes indicar al menos un campo")
        if any(
            not isinstance(campo, str) or not campo or campo.startswith("$")
            for campo in campos
        ):
            raise ValueError("Lista de campos invalida")

        proyeccion = {campo: 1 for campo in campos}
        proyeccion["_id"] = 0

        try:
            cursor = self.coleccion.find(
                filtros,
                proyeccion
            ).limit(limite).max_time_ms(15000)
            resultados = list(cursor)
            logger.info("Proyeccion completada; resultados: %s", len(resultados))
            return resultados
        except PyMongoError as error:
            logger.exception("Error al consultar con proyeccion")
            raise RepositoryError("No se pudo consultar con proyeccion") from error

    # AYUDANTE PARA CONVERTIR VIAJE A DOCUMENTO
    @staticmethod
    def _preparar_documento(registro: dict[str, Any] | Viaje) -> dict[str, Any]:
        if isinstance(registro, Viaje):
            fecha = registro.boarding_datetime
            documento = {
                "trip_id": registro.trip_id,
                "card_id": registro.card_id,
                "transport_mode": registro.transport_mode,
                "route_line": registro.route_line,
                "origin": registro.origin,
                "destination": registro.destination,
                "boarding_datetime": (
                    fecha.strftime("%Y-%m-%d %H:%M:%S")
                    if isinstance(fecha, datetime) else str(fecha)
                ),
                "day_of_week": registro.day_of_week,
                "hour": str(registro.hour),
                "distance_km": registro.distance_km,
                "duration_min": registro.duration_min,
                "fare": registro.fare,
                "payment_method": registro.payment_method,
                "weather": registro.weather
            }
        elif isinstance(registro, dict):
            documento = dict(registro)
        else:
            raise ValueError("El registro debe ser un Viaje o diccionario")

        documento.pop("_id", None)
        trip_id = documento.get("trip_id")
        if not isinstance(trip_id, str) or not trip_id.strip():
            raise ValueError("trip_id obligatorio")
        documento["trip_id"] = trip_id.strip()
        return documento

    # 7. HU-07: GUARDAR VIAJES POR LOTES
    def guardar_lote(
        self,
        registros: list[dict[str, Any] | Viaje]
    ) -> dict[str, int]:
        if not isinstance(registros, list) or not 1 <= len(registros) <= 1000:
            raise ValueError("El lote debe contener entre 1 y 1000 registros")

        # Por defecto no se permite modificar la coleccion de Atlas.
        if os.getenv("MOVIDATA_HABILITAR_ESCRITURA", "false").lower() != "true":
            logger.warning("Intento de escritura bloqueado por configuracion")
            raise PermissionError("La escritura esta deshabilitada por seguridad")

        operaciones = []
        identificadores = set()
        for registro in registros:
            documento = self._preparar_documento(registro)
            trip_id = documento["trip_id"]
            if trip_id in identificadores:
                continue
            identificadores.add(trip_id)
            operaciones.append(
                UpdateOne(
                    {"trip_id": trip_id},
                    {"$setOnInsert": documento},
                    upsert=True
                )
            )

        try:
            resultado = self.coleccion.bulk_write(operaciones, ordered=False)
            logger.info("Lote procesado; documentos nuevos: %s", resultado.upserted_count)
            return {
                "procesados": len(registros),
                "insertados": resultado.upserted_count,
                "existentes_o_repetidos": len(registros) - resultado.upserted_count
            }
        except PyMongoError as error:
            logger.exception("Error al guardar lote de viajes")
            raise RepositoryError("No se pudo guardar el lote de viajes") from error

    # 8. HU-07: CONSULTAR VIAJES POR PAGINAS
    def obtener_pagina(
        self,
        limite: int = 100,
        despues_de: Optional[str] = None
    ) -> list[Viaje]:
        if isinstance(limite, bool) or not isinstance(limite, int) or not 1 <= limite <= 1000:
            raise ValueError("El limite debe estar entre 1 y 1000")
        if despues_de is not None and (
            not isinstance(despues_de, str) or not despues_de.strip()
        ):
            raise ValueError("El cursor debe ser un trip_id valido")

        filtros = {}
        if despues_de is not None:
            filtros = {"trip_id": {"$gt": despues_de}}

        try:
            logger.info("Consultando pagina de viajes; limite: %s", limite)
            documentos = self.coleccion.find(
                filtros,
                {"_id": 0}
            ).sort("trip_id", 1).limit(limite).max_time_ms(15000)

            viajes = [Viaje.desde_documento(doc) for doc in documentos]
            logger.info("Pagina consultada; viajes obtenidos: %s", len(viajes))
            return viajes
        except PyMongoError as error:
            logger.exception("Error al consultar viajes por paginas")
            raise RepositoryError("No se pudo consultar la pagina de viajes") from error

    # 9. HU-08: FILTRAR VIAJES POR MODO, RUTA, DIA Y HORA
    def filtrar_viajes(
        self,
        modo: Optional[str] = None,
        ruta: Optional[str] = None,
        fecha: Optional[str] = None,
        hora: Optional[int] = None,
        limite: int = 100
    ) -> list[Viaje]:

        # VALIDAR QUE EXISTA AL MENOS UN FILTRO
        if all(valor is None for valor in (modo, ruta, fecha, hora)):
            raise ValueError("Debes indicar al menos un filtro")

        # CORRECCION HU-08: VALIDAR EL LIMITE
        if (
            isinstance(limite, bool)
            or not isinstance(limite, int)
            or not 1 <= limite <= 1000
        ):
            raise ValueError("El limite debe estar entre 1 y 1000")

        filtros = {}

        # FILTRO POR MODO
        if modo is not None:
            if not isinstance(modo, str) or not modo.strip():
                raise ValueError("Modo de transporte invalido")
            filtros["transport_mode"] = modo.strip()

        # FILTRO POR RUTA
        if ruta is not None:
            if not isinstance(ruta, str) or not ruta.strip():
                raise ValueError("Ruta invalida")
            filtros["route_line"] = ruta.strip()

        # FILTRO POR FECHA
        if fecha is not None:
            if not isinstance(fecha, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", fecha):
                raise ValueError("La fecha debe tener formato AAAA-MM-DD")
            try:
                date.fromisoformat(fecha)
            except ValueError as error:
                raise ValueError("La fecha indicada no existe") from error
            filtros["boarding_datetime"] = {"$regex": f"^{fecha} "}

        # FILTRO POR HORA
        if hora is not None:
            if isinstance(hora, bool) or not isinstance(hora, int) or not 0 <= hora <= 23:
                raise ValueError("La hora debe estar entre 0 y 23")
            filtros["hour"] = str(hora)

        return self.buscar_por_filtro(filtros, limite=limite)

    # 10. CERRAR CONEXION MONGODB
    def cerrar(self):
        self.conexion.cerrar()
