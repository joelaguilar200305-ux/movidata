from collections import Counter

from analysis.analysis_result import AnalysisResult
from analysis.i_analysis_strategy import IAnalysisStrategy
from domain.exceptions import AnalysisError
from domain.viaje import Viaje
from utils.logging_config import get_logger

logger = get_logger(__name__)


class DemandAnalysisStrategy(IAnalysisStrategy):
    """Analyzes trip demand by hour and by day of the week (HU-09)."""

    def analyze(self, data: list[Viaje]) -> AnalysisResult:
        if not data:
            raise AnalysisError("There are no trips to analyze")

        logger.info("Analyzing demand for %s trips", len(data))

        trips_by_hour = Counter(trip.hour for trip in data)
        trips_by_day = Counter(trip.day_of_week for trip in data)

        peak_hour = max(trips_by_hour, key=trips_by_hour.get)
        peak_day = max(trips_by_day, key=trips_by_day.get)

        logger.info("Peak hour: %s | Peak day: %s", peak_hour, peak_day)

        return AnalysisResult(
            kind="demand",
            data={
                "trips_by_hour": dict(sorted(trips_by_hour.items())),
                "trips_by_day": dict(trips_by_day),
                "peak_hour": peak_hour,
                "peak_day": peak_day,
            },
        )