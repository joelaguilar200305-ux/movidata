from analysis.i_analysis_strategy import IAnalysisStrategy
from analysis.routes_analysis import RoutesAnalysisStrategy
from domain.exceptions import AnalysisError


class StrategyFactory:
    """Crea estrategias de análisis según su nombre (Factory Method)."""

    # Registro: nombre del tipo -> clase de la estrategia (HU-09 se registra aquí también)
    _registry: dict[str, type[IAnalysisStrategy]] = {
        "routes": RoutesAnalysisStrategy,
    }

    @classmethod
    def create(cls, kind: str) -> IAnalysisStrategy:
        try:
            return cls._registry[kind]()
        except KeyError as error:
            raise AnalysisError(f"Unsupported analysis kind: {kind}") from error
        