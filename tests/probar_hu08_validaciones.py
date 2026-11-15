
from unittest.mock import patch

from repositories.mongo_viaje_repository import MongoViajeRepository


def main():

    print("=== VALIDACIONES HU-08 MOVIDATA ===")

    # Repository simulado sin conexion a Atlas
    repositorio = object.__new__(MongoViajeRepository)

    casos_invalidos = [
        {},
        {"hora": -1},
        {"hora": 24},
        {"hora": True},
        {"fecha": "2026-02-30"},
        {"fecha": "fecha-invalida"},
        {"modo": ""},
        {"ruta": "   "},
        {"modo": "Metro", "limite": 1001}
    ]

    for parametros in casos_invalidos:

        with patch.object(
            repositorio, "buscar_por_filtro"
        ) as buscar:

            try:
                repositorio.filtrar_viajes(**parametros)

            except ValueError:
                print("RECHAZADO CORRECTAMENTE:", parametros)

            else:
                raise AssertionError(
                    "Se acepto un filtro invalido"
                )

            buscar.assert_not_called()

    print("\n=== FILTROS COMBINADOS ===")

    with patch.object(
        repositorio,
        "buscar_por_filtro",
        return_value=[]
    ) as buscar:

        repositorio.filtrar_viajes(
            modo="Metrobus",
            ruta="Ruta de prueba",
            fecha="2026-11-15",
            hora=13,
            limite=5
        )

        buscar.assert_called_once_with(
            {
                "transport_mode": "Metrobus",
                "route_line": "Ruta de prueba",
                "boarding_datetime": {
                    "$regex": "^2026-11-15 "
                },
                "hour": "13"
            },
            limite=5
        )

    print("COMBINACION DE FILTROS CORRECTA")
    print("\nHU-08: VALIDACIONES FINALIZADAS")


if __name__ == "__main__":
    main()
