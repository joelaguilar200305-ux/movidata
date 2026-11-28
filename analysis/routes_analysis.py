from collections import Counter

from analysis.analysis_result import AnalysisResult
from analysis.i_analysis_strategy import IAnalysisStrategy
from domain.exceptions import AnalysisError
from domain.viaje import Viaje
from utils.logging_config import get_logger

logger = get_logger(__name__)


class RoutesAnalysisStrategy(IAnalysisStrategy):
    """Estrategia HU-10: rutas y orígenes con más viajes."""

    def __init__(self, top_n: int = 10) -> None:
        self._top_n = top_n

    def analyze(self, data: list[Viaje]) -> AnalysisResult:
        if not data:
            raise AnalysisError("Cannot analyze routes: no trips provided")

        total_trips = len(data)
        routes = Counter((trip.transport_mode, trip.route_line) for trip in data)
        origins = Counter((trip.transport_mode, trip.origin) for trip in data)

        top_routes = [
            {
                "transport_mode": mode,
                "route_line": route,
                "trips": count,
                "share_percent": round(count / total_trips * 100, 2),
            }
            for (mode, route), count in routes.most_common(self._top_n)
        ]
        top_origins = [
            {"transport_mode": mode, "origin": origin, "trips": count}
            for (mode, origin), count in origins.most_common(self._top_n)
        ]

        logger.info(
            "Routes analysis finished: %d trips, %d distinct routes",
            total_trips,
            len(routes),
        )
        return AnalysisResult(
            "routes",
            {
                "total_trips": total_trips,
                "top_routes": top_routes,
                "top_origins": top_origins,
            },
        )