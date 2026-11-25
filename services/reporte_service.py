import os
import pandas as pd


class ReportService:
    def __init__(self, folder="exports"):
        self.folder = folder

    def generate_summary(self, data):
        summary = {
            "total_trips": len(data),
            "total_revenue": round(data["fare"].sum(), 2),
            "average_duration": round(data["duration_min"].mean(), 1),
        }
        by_mode = data.groupby("transport_mode").agg(
            trips=("fare", "size"),
            revenue=("fare", "sum"),
        ).round(2)
        return summary, by_mode

    def export_csv(self, table, filename):
        os.makedirs(self.folder, exist_ok=True)
        path = os.path.join(self.folder, filename)
        table.to_csv(path)
        return path


if __name__ == "__main__":
    from utils.data_loader import DataLoader

    data = DataLoader().load_csv().head(1000000)
    service = ReportService()
    summary, by_mode = service.generate_summary(data)

    print(summary)
    print(by_mode)
    print("Exported to:", service.export_csv(by_mode, "report_by_mode.csv"))