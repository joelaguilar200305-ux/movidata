
from abc import ABC, abstractmethod
from typing import Any, Optional

from domain.viaje import Viaje


class IViajeRepository(ABC):

    @abstractmethod
    def buscar_por_id(
        self,
        trip_id: str
    ) -> Optional[Viaje]:
        pass

    @abstractmethod
    def buscar_por_filtro(
        self,
        filtros: dict[str, Any],
        limite: int = 100
    ) -> list[Viaje]:
        pass

    @abstractmethod
    def contar_documentos(
        self,
        filtros: Optional[dict[str, Any]] = None
    ) -> int:
        pass

    @abstractmethod
    def agregar(
        self,
        pipeline: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        pass

    @abstractmethod
    def buscar_con_proyeccion(
        self,
        filtros: dict[str, Any],
        campos: list[str],
        limite: int = 100
    ) -> list[dict[str, Any]]:
        pass

from abc import ABC, abstractmethod
from typing import Any, Optional

from domain.viaje import Viaje


class IViajeRepository(ABC):

    @abstractmethod
    def buscar_por_id(self, trip_id: str) -> Optional[Viaje]:
        pass

    @abstractmethod
    def buscar_por_filtro(
        self,
        filtros: dict[str, Any],
        limite: int = 100
    ) -> list[Viaje]:
        pass

    @abstractmethod
    def contar_documentos(
        self,
        filtros: Optional[dict[str, Any]] = None
    ) -> int:
        pass

    @abstractmethod
    def agregar(
        self,
        pipeline: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        pass
