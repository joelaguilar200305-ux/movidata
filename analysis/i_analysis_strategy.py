from abc import ABC, abstractmethod

from analysis.analysis_result import AnalysisResult
from domain.viaje import Viaje


class IAnalysisStrategy(ABC):
    """Interfaz común de todas las estrategias de análisis."""

    @abstractmethod
    def analyze(self, data: list[Viaje]) -> AnalysisResult:
        """Analiza una lista de viajes y devuelve un AnalysisResult."""
        ...