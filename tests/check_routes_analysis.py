from datetime import datetime

from analysis.strategy_factory import StrategyFactory
from domain.exceptions import AnalysisError
from domain.viaje import Viaje


def make_trip(trip_id: str, mode: str, route: str, origin: str) -> Viaje:
    return Viaje(
        trip_id=trip_id,
        card_id="TRJ0001",
        transport_mode=mode,
        route_line=route,
        origin=origin,
        destination="Destino",
        boarding_datetime=datetime(2024, 6, 1, 8, 0),
        day_of_week="Sabado",
        hour=8,
        distance_km=5.0,
        duration_min=20.0,
        fare=0.3,
        payment_method="Tarjeta_Metro",
        weather="Soleado",
    )


def main() -> None:
    trips = [
        make_trip("VJE1", "Metro", "Linea 1", "A"),
        make_trip("VJE2", "Metro", "Linea 1", "A"),
        make_trip("VJE3", "Metro", "Linea 2", "B"),
        make_trip("VJE4", "Metrobus", "Ruta 5", "C"),
    ]

    strategy = StrategyFactory.create("routes")
    result = strategy.analyze(trips)

    assert result.kind == "routes"
    assert result.data["total_trips"] == 4
    assert result.data["top_routes"][0]["route_line"] == "Linea 1"
    assert result.data["top_routes"][0]["trips"] == 2
    assert result.data["top_routes"][0]["share_percent"] == 50.0
    assert result.data["top_origins"][0]["origin"] == "A"
    print("Routes analysis: OK")

    try:
        strategy.analyze([])
    except AnalysisError:
        print("Empty list rejected: OK")
    else:
        raise AssertionError("An empty list must raise AnalysisError")


if __name__ == "__main__":
    main()