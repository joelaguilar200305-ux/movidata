
from time import perf_counter

from domain.viaje import Viaje
from repositories.mongo_viaje_repository import MongoViajeRepository


def main():

    repositorio = MongoViajeRepository()

    try:
        print("=== PRUEBAS HU-08 MOVIDATA ===")

        # Obtener datos reales como referencia
        muestra = repositorio.coleccion.find_one(
            {},
            {
                "_id": 0,
                "transport_mode": 1,
                "route_line": 1,
                "boarding_datetime": 1,
                "hour": 1
            },
            max_time_ms=15000
        )

        if muestra is None:
            raise ValueError("No hay viajes para probar")

        modo = muestra["transport_mode"]
        ruta = muestra["route_line"]
        fecha = str(muestra["boarding_datetime"])[:10]
        hora = int(muestra["hour"])

        pruebas = [
            ("Modo", {"modo": modo}),
            ("Ruta", {"ruta": ruta}),
            ("Fecha", {"fecha": fecha}),
            ("Hora", {"hora": hora}),
            (
                "Combinados",
                {
                    "modo": modo,
                    "ruta": ruta,
                    "fecha": fecha,
                    "hora": hora
                }
            )
        ]

        for nombre, parametros in pruebas:

            inicio = perf_counter()

            viajes = repositorio.filtrar_viajes(
                **parametros,
                limite=5
            )

            tiempo = (perf_counter() - inicio) * 1000

            assert 1 <= len(viajes) <= 5

            for viaje in viajes:

                assert isinstance(viaje, Viaje)

                if "modo" in parametros:
                    assert viaje.transport_mode == modo

                if "ruta" in parametros:
                    assert viaje.route_line == ruta

                if "fecha" in parametros:
                    assert (
                        viaje.boarding_datetime.date().isoformat()
                        == fecha
                    )

                if "hora" in parametros:
                    assert viaje.hour == hora

            print("\nFiltro:", nombre)
            print("Viajes encontrados:", len(viajes))
            print("Tiempo (ms):", round(tiempo, 2))
            print("VALIDADO CORRECTAMENTE")

        print("\nHU-08: FILTROS VALIDADOS")

    finally:
        repositorio.cerrar()


if __name__ == "__main__":
    main()
