
from dataclasses import dataclass
from typing import Optional


@dataclass
class Viaje:
    trip_id: str
    boarding_datetime: str
    transport_mode: str
    district: str
    route_line: str
    fare: float
    duration_min: float

    card_id: Optional[str] = None
    destination: Optional[str] = None
    origin: Optional[str] = None

    @classmethod
    def desde_documento(cls, documento: dict):
        return cls(
            trip_id=str(documento["trip_id"]),
            boarding_datetime=str(
                documento["boarding_datetime"]
            ),
            transport_mode=str(
                documento["transport_mode"]
            ),
            district=str(documento["district"]),
            route_line=str(documento["route_line"]),
            fare=float(documento["fare"]),
            duration_min=float(
                documento["duration_min"]
            ),
            card_id=documento.get("card_id"),
            destination=documento.get("destination"),
            origin=documento.get("origin")
        )
