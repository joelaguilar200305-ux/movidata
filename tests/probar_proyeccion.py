
from repositories.mongo_viaje_repository import 	MongoViajeRepository


def main():
    repositorio = None

    try:
        repositorio = 	MongoViajeRepository()

        print("=== PRUEBA DE PROYECCION MOVIDATA ===")

        viajes = repositorio.buscar_con_proyeccion(
            {"district": "San Miguelito"},
            ["trip_id", "district"],
            limite=5
        )

        print("\nViajes encontrados:", len(viajes))

        for viaje in viajes:
            print(viaje)

        assert len(viajes) == 5, (
            "Se esperaban 5 viajes"
        )

        for viaje in viajes:
            assert set(viaje.keys()) == {
                "trip_id", "district"
            }, "La proyeccion contiene campos incorrectos"

        print("\nPROYECCION VALIDADA CORRECTAMENTE")

    except Exception as error:
        print("ERROR:", str(error))
        raise

    finally:
        if repositorio is not None:
            repositorio.cerrar()


if __name__ == "__main__":
    main()
