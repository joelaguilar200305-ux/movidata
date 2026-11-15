
from domain.viaje import Viaje
from repositories.mongo_viaje_repository import MongoViajeRepository


def main():

    print("=== PRUEBA DE CONVERSION HU-07 ===")

    documento = {
        "trip_id": "HU07_PRUEBA001",
        "card_id": "TARJETA001",
        "transport_mode": "Metro",
        "route_line": "Linea 1",
        "origin": "Albrook",
        "destination": "5 de Mayo",
        "boarding_datetime": "2026-11-15 13:00:00",
        "day_of_week": "Domingo",
        "hour": "13",
        "distance_km": 3.5,
        "duration_min": 12.0,
        "fare": 0.35,
        "payment_method": "Tarjeta",
        "weather": "Soleado"
    }

    # Convertir documento a objeto Viaje
    viaje = Viaje.desde_documento(documento)

    assert isinstance(viaje, Viaje)

    print("Documento convertido a Viaje: CORRECTO")

    # Convertir Viaje nuevamente a documento
    convertido = MongoViajeRepository._preparar_documento(
        viaje
    )

    assert convertido == documento

    print("Viaje convertido a documento: CORRECTO")

    # Comprobar que no se conserva el _id de MongoDB
    documento_con_id = dict(documento)
    documento_con_id["_id"] = "SIMULADO"

    preparado = MongoViajeRepository._preparar_documento(
        documento_con_id
    )

    assert "_id" not in preparado

    print("Eliminacion de _id: CORRECTA")

    print("\nHU-07: CONVERSION VALIDADA")
    print("No se modificaron registros en Atlas")


if __name__ == "__main__":
    main()
