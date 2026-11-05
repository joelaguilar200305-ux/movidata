
import os
from pathlib import Path
from typing import Any, Optional

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError

from domain.viaje import Viaje
from repositories.i_readable_repository import IReadableRepository


class MongoViajesRepository(IReadableRepository):

    def __init__(self):
        base = Path(__file__).resolve().parent.parent
        load_dotenv(base / ".env")

        uri = os.getenv("MONGODB_URI")

        if not uri:
            raise ValueError("Falta MONGODB_URI en .env")

        self.cliente = MongoClient(
            uri,
            serverSelectionTimeoutMS=10000,
            socketTimeoutMS=30000,
            retryWrites=False
        )

        try:
            self.cliente.admin.command("ping")
        except PyMongoError:
            self.cliente.close()
            raise

        self.coleccion = self.cliente["movidata"]["viajes"]

    def buscar_por_id(self, trip_id: str) -> Optional[Viaje]:
        documento = self.coleccion.find_one(
            {"trip_id": trip_id},
            {"_id": 0}
        )

        if documento is None:
            return None

        return Viaje.desde_documento(documento)

    def buscar_por_filtro(
        self,
        filtros: dict[str, Any],
        limite: int = 100
    ) -> list[Viaje]:

        if not 1 <= limite <= 1000:
            raise ValueError("El limite debe estar entre 1 y 1000")

        documentos = self.coleccion.find(
            filtros,
            {"_id": 0}
        ).limit(limite).max_time_ms(15000)

        return [
            Viaje.desde_documento(documento)
            for documento in documentos
        ]

    def contar_documentos(
        self,
        filtros: Optional[dict[str, Any]] = None
    ) -> int:

        return self.coleccion.count_documents(
            filtros if filtros is not None else {},
            maxTimeMS=15000
        )

    def agregar(
        self,
        pipeline: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:

        if not pipeline:
            raise ValueError("El pipeline no puede estar vacio")

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

    def cerrar(self):
        self.cliente.close()
