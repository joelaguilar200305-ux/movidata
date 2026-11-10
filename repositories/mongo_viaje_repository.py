
from typing import Any, Optional

from config.conexion_mongo import MongoConnection
from domain.viaje import Viaje
from repositories.i_viaje_repository import IViajeRepository


class MongoViajeRepository(IViajeRepository):

    # 1. CONEXION CENTRALIZADA A MONGODB ATLAS
    def __init__(self):
        self.conexion = MongoConnection.get_instance()
        self.coleccion = self.conexion.coleccion

    # 2. BUSCAR VIAJE POR ID
    def buscar_por_id(
        self,
        trip_id: str
    ) -> Optional[Viaje]:

        documento = self.coleccion.find_one(
            {"trip_id": trip_id},
            {"_id": 0},
            max_time_ms=15000
        )

        if documento is None:
            return None

        return Viaje.desde_documento(documento)

    # 3. BUSCAR VIAJES UTILIZANDO FILTROS
    def buscar_por_filtro(
        self,
        filtros: dict[str, Any],
        limite: int = 100
    ) -> list[Viaje]:

        if not 1 <= limite <= 1000:
            raise ValueError(
                "El limite debe estar entre 1 y 1000"
            )

        documentos = self.coleccion.find(
            filtros,
            {"_id": 0}
        ).limit(limite).max_time_ms(15000)

        return [
            Viaje.desde_documento(documento)
            for documento in documentos
        ]

    # 4. CONTAR DOCUMENTOS
    def contar_documentos(
        self,
        filtros: Optional[dict[str, Any]] = None
    ) -> int:

        return self.coleccion.count_documents(
            filtros if filtros is not None else {},
            maxTimeMS=15000
        )

    # 5. EJECUTAR AGREGACIONES
    def agregar(
        self,
        pipeline: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:

        if not pipeline:
            raise ValueError(
                "El pipeline no puede estar vacio"
            )

        etapas_prohibidas = {"$out", "$merge"}

        for etapa in pipeline:
            if any(
                operador in etapa
                for operador in etapas_prohibidas
            ):
                raise ValueError(
                    "No se permiten operaciones de escritura"
                )

        cursor = self.coleccion.aggregate(
            pipeline,
            allowDiskUse=False,
            maxTimeMS=15000
        )

        return list(cursor)

    # 6. BUSCAR VIAJES CON PROYECCION DE CAMPOS
    def buscar_con_proyeccion(
        self,
        filtros: dict[str, Any],
        campos: list[str],
        limite: int = 100
    ) -> list[dict[str, Any]]:

        if not 1 <= limite <= 1000:
            raise ValueError(
                "El limite debe estar entre 1 y 1000"
            )

        if not campos:
            raise ValueError(
                "Debes indicar al menos un campo"
            )

        if any(
            not isinstance(campo, str)
            or not campo
            or campo.startswith("$")
            for campo in campos
        ):
            raise ValueError(
                "Lista de campos invalida"
            )

        proyeccion = {
            campo: 1
            for campo in campos
        }

        proyeccion["_id"] = 0

        cursor = self.coleccion.find(
            filtros,
            proyeccion
        ).limit(limite).max_time_ms(15000)

        return list(cursor)

    # 7. CERRAR CONEXION MONGODB
    def cerrar(self):
        self.conexion.cerrar()
