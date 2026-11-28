import os

from domain.exceptions import AnalysisError
from utils.logging_config import get_logger

logger = get_logger(__name__)


class ReportService:
    def __init__(self, folder="exports"):
        self.folder = folder

    def generate_summary(self, data):
        try:
            summary = {
                "total_trips": len(data),
                "total_revenue": round(data["fare"].sum(), 2),
                "average_duration": round(data["duration_min"].mean(), 1),
            }
            by_mode = data.groupby("transport_mode").agg(
                trips=("fare", "size"),
                revenue=("fare", "sum"),
            ).round(2)
        except (KeyError, ValueError) as error:
            logger.error("Could not generate summary: %s", error)
            raise AnalysisError("Could not generate summary") from error
        logger.info("Summary generated for %s trips", summary["total_trips"])
        return summary, by_mode

    def export_csv(self, table, filename):
        try:
            os.makedirs(self.folder, exist_ok=True)
            path = os.path.join(self.folder, filename)
            table.to_csv(path)
        except OSError as error:
            logger.error("Could not export CSV: %s", error)
            raise AnalysisError("Could not export CSV") from error
        logger.info("Report exported to %s", path)
        return path