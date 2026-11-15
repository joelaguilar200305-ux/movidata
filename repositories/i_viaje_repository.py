
from abc import ABC, abstractmethod
from typing import Any, Optional

from domain.viaje import Viaje


class IViajeRepository(ABC):

    # 1. BUSCAR VIAJE POR ID
    @abstractmethod
    def buscar_por_id(
        self,
        trip_id: str
    ) -> Optional[Viaje]:
        pass

    # 2. BUSCAR VIAJES POR FILTROS
    @abstractmethod
    def buscar_por_filtro(
        self,
        filtros: dict[str, Any],
        limite: int = 100
    ) -> list[Viaje]:
        pass

    # 3. CONTAR DOCUMENTOS
    @abstractmethod
    def contar_documentos(
        self,
        filtros: Optional[dict[str, Any]] = None
    ) -> int:
        pass

    # 4. EJECUTAR AGREGACIONES
    @abstractmethod
    def agregar(
        self,
        pipeline: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        pass

    # 5. BUSCAR CON PROYECCION
    @abstractmethod
    def buscar_con_proyeccion(
        self,
        filtros: dict[str, Any],
        campos: list[str],
        limite: int = 100
    ) -> list[dict[str, Any]]:
        pass

    # 6. HU-07: INSERTAR VIAJES POR LOTES
    @abstractmethod
    def guardar_lote(
        self,
        registros: list[dict[str, Any]]
    ) -> dict[str, int]:
        pass

    # 7. HU-07: CONSULTAR VIAJES POR PAGINAS
    @abstractmethod
    def obtener_pagina(
        self,
        limite: int = 100,
        despues_de: Optional[str] = None
    ) -> list[Viaje]:
        pass
