
from repositories.mongo_viaje_repository import MongoViajeRepository


def main():

    repositorio = MongoViajeRepository()

    try:
        print("=== FASE 3: CONSULTAS HU-10 ===")

        # 1. RUTAS CON MAYOR CANTIDAD DE VIAJES
        pipeline_rutas = [
            {
                "$group": {
                    "_id": {
                        "modo": "$transport_mode",
                        "ruta": "$route_line"
                    },
                    "total_viajes": {"$sum": 1}
                }
            },
            {"$sort": {"total_viajes": -1}},
            {"$limit": 10}
        ]

        print("\nTOP 10 RUTAS MAS TRANSITADAS")

        rutas = repositorio.agregar(pipeline_rutas)

        for ruta in rutas:
            print(ruta)

        # 2. ORIGENES CON MAYOR CANTIDAD DE VIAJES
        pipeline_origenes = [
            {
                "$group": {
                    "_id": {
                        "modo": "$transport_mode",
                        "origen": "$origin"
                    },
                    "total_viajes": {"$sum": 1}
                }
            },
            {"$sort": {"total_viajes": -1}},
            {"$limit": 10}
        ]

        print("\nTOP 10 ORIGENES MAS UTILIZADOS")

        origenes = repositorio.agregar(pipeline_origenes)

        for origen in origenes:
            print(origen)

        assert len(rutas) > 0
        assert len(origenes) > 0

        print("\nHU-10: CONSULTAS VALIDADAS")

    finally:
        repositorio.cerrar()


if __name__ == "__main__":
    main()
