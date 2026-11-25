
from time import perf_counter

from repositories.mongo_viaje_repository import MongoViajeRepository


# EJECUTAR CONSULTAS Y MEDIR RENDIMIENTO
def ejecutar_consulta(repositorio, nombre, pipeline):

    print("\n" + nombre)

    inicio = perf_counter()

    resultados = repositorio.agregar(pipeline)

    tiempo = (perf_counter() - inicio) * 1000

    for resultado in resultados:
        print(resultado)

    print("Tiempo (ms):", round(tiempo, 2))

    assert len(resultados) > 0, (
        "ERROR: La consulta no devolvio resultados"
    )

    return resultados


def main():

    repositorio = MongoViajeRepository()

    try:
        print("=== FASE 3: CONSULTAS HU-11 ===")

        # CONVERTIR TARIFAS A NUMEROS PARA SUMAR
        # Se utiliza durante la consulta.
        # No modifica los documentos de MongoDB.
        tarifa_numerica = {
            "$convert": {
                "input": "$fare",
                "to": "double",
                "onError": None,
                "onNull": None
            }
        }

        # 1. RECAUDACION POR MODO DE TRANSPORTE
        pipeline_modo = [
            {
                "$group": {
                    "_id": "$transport_mode",
                    "total_viajes": {"$sum": 1},
                    "recaudacion": {
                        "$sum": tarifa_numerica
                    },
                    "tarifas_invalidas": {
                        "$sum": {
                            "$cond": [
                                {
                                    "$eq": [
                                        tarifa_numerica,
                                        None
                                    ]
                                },
                                1,
                                0
                            ]
                        }
                    }
                }
            },
            {
                "$sort": {
                    "recaudacion": -1
                }
            }
        ]

        resultados_modo = ejecutar_consulta(
            repositorio,
            "1. RECAUDACION POR MODO",
            pipeline_modo
        )

        # 2. RECAUDACION POR TIPO DE USUARIO
        pipeline_usuario = [
            {
                "$group": {
                    "_id": "$user_type",
                    "total_viajes": {"$sum": 1},
                    "recaudacion": {
                        "$sum": tarifa_numerica
                    }
                }
            },
            {
                "$sort": {
                    "recaudacion": -1
                }
            }
        ]

        resultados_usuario = ejecutar_consulta(
            repositorio,
            "2. RECAUDACION POR TIPO DE USUARIO",
            pipeline_usuario
        )

        # 3. TOP 10 RUTAS CON MAYOR RECAUDACION
        pipeline_rutas = [
            {
                "$group": {
                    "_id": {
                        "modo": "$transport_mode",
                        "ruta": "$route_line"
                    },
                    "total_viajes": {"$sum": 1},
                    "recaudacion": {
                        "$sum": tarifa_numerica
                    }
                }
            },
            {
                "$sort": {
                    "recaudacion": -1
                }
            },
            {
                "$limit": 10
            }
        ]

        resultados_rutas = ejecutar_consulta(
            repositorio,
            "3. TOP 10 RUTAS POR RECAUDACION",
            pipeline_rutas
        )

        # 4. RECAUDACION POR MODO, RUTA Y TIPO DE USUARIO
        pipeline_combinado = [
            {
                "$group": {
                    "_id": {
                        "modo": "$transport_mode",
                        "ruta": "$route_line",
                        "tipo_usuario": "$user_type"
                    },
                    "total_viajes": {"$sum": 1},
                    "recaudacion": {
                        "$sum": tarifa_numerica
                    }
                }
            },
            {
                "$sort": {
                    "recaudacion": -1
                }
            },
            {
                "$limit": 10
            }
        ]

        resultados_combinados = ejecutar_consulta(
            repositorio,
            "4. RECAUDACION COMBINADA",
            pipeline_combinado
        )

        # 5. VALIDACION DE RESULTADOS
        print("\n5. VALIDACION DE RESULTADOS")

        total_modo = sum(
            resultado["total_viajes"]
            for resultado in resultados_modo
        )

        total_usuario = sum(
            resultado["total_viajes"]
            for resultado in resultados_usuario
        )

        recaudacion_modo = sum(
            resultado["recaudacion"]
            for resultado in resultados_modo
        )

        recaudacion_usuario = sum(
            resultado["recaudacion"]
            for resultado in resultados_usuario
        )

        tarifas_invalidas = sum(
            resultado["tarifas_invalidas"]
            for resultado in resultados_modo
        )

        tipos_esperados = {
            "Estudiante",
            "Jubilado",
            "Regular",
            "Turista"
        }

        tipos_encontrados = {
            resultado["_id"]
            for resultado in resultados_usuario
        }

        print("Viajes agrupados por modo:", total_modo)
        print("Viajes agrupados por usuario:", total_usuario)

        print(
            "Recaudacion por modo (PAB):",
            round(recaudacion_modo, 2)
        )

        print(
            "Recaudacion por usuario (PAB):",
            round(recaudacion_usuario, 2)
        )

        print(
            "Tarifas invalidas o vacias:",
            tarifas_invalidas
        )

        print(
            "Tipos de usuario encontrados:",
            sorted(tipos_encontrados)
        )

        # VALIDAR EL MILLON DE DOCUMENTOS
        assert total_modo == 1000000, (
            "ERROR: El total por modo no coincide"
        )

        assert total_usuario == 1000000, (
            "ERROR: El total por usuario no coincide"
        )

        # VALIDAR QUE LAS TARIFAS SEAN NUMERICAS
        assert tarifas_invalidas == 0, (
            "ERROR: Existen tarifas invalidas o vacias"
        )

        # VALIDAR QUE EXISTA RECAUDACION
        assert recaudacion_modo > 0, (
            "ERROR: La recaudacion total no puede ser cero"
        )

        # VALIDAR QUE AMBOS CALCULOS COINCIDAN
        assert abs(
            recaudacion_modo - recaudacion_usuario
        ) < 0.01, (
            "ERROR: Las recaudaciones no coinciden"
        )

        # VALIDAR LOS TIPOS DE USUARIO
        assert tipos_encontrados == tipos_esperados, (
            "ERROR: Los tipos de usuario no coinciden"
        )

        # VALIDAR RESULTADOS DE RUTAS
        assert len(resultados_rutas) > 0
        assert len(resultados_combinados) > 0

        print("\nTOTALES VALIDADOS CORRECTAMENTE")
        print("HU-11: CONSULTAS VALIDADAS")

    finally:
        repositorio.cerrar()


if __name__ == "__main__":
    main()
