
import os
from unittest.mock import Mock, patch

from pymongo.errors import PyMongoError

from domain.exceptions import RepositoryError
from repositories.mongo_viaje_repository import MongoViajeRepository


def comprobar_error(nombre, operacion):

    try:
        operacion()

    except RepositoryError as error:
        assert isinstance(error.__cause__, PyMongoError)
        print(nombre, ": CORRECTO")

    else:
        raise AssertionError(
            "No se genero RepositoryError"
        )


def main():

    print("=== PRUEBAS DE EXCEPCIONES HU-07 ===")

    # Repository simulado, sin conexion a Atlas
    repositorio = object.__new__(MongoViajeRepository)

    # 1. SIMULAR ERROR DE BUSQUEDA
    repositorio.coleccion = Mock()
    repositorio.coleccion.find_one.side_effect = PyMongoError(
        "Error simulado de consulta"
    )

    comprobar_error(
        "Busqueda por ID",
        lambda: repositorio.buscar_por_id("PRUEBA001")
    )

    # 2. SIMULAR ERROR DE PAGINACION
    repositorio.coleccion = Mock()
    repositorio.coleccion.find.side_effect = PyMongoError(
        "Error simulado de paginacion"
    )

    comprobar_error(
        "Paginacion",
        lambda: repositorio.obtener_pagina(limite=5)
    )

    # 3. VERIFICAR BLOQUEO DE ESCRITURA
    repositorio.coleccion = Mock()

    with patch.dict(
        os.environ,
        {"MOVIDATA_HABILITAR_ESCRITURA": "false"}
    ):
        try:
            repositorio.guardar_lote([
                {"trip_id": "PRUEBA001"}
            ])

        except PermissionError:
            print("Proteccion de escritura: CORRECTA")

        else:
            raise AssertionError(
                "La escritura no fue bloqueada"
            )

    repositorio.coleccion.bulk_write.assert_not_called()

    # 4. SIMULAR ERROR DE INSERCION
    repositorio.coleccion = Mock()
    repositorio.coleccion.bulk_write.side_effect = PyMongoError(
        "Error simulado de insercion"
    )

    with patch.dict(
        os.environ,
        {"MOVIDATA_HABILITAR_ESCRITURA": "true"}
    ):
        comprobar_error(
            "Insercion por lotes",
            lambda: repositorio.guardar_lote([
                {"trip_id": "PRUEBA001"}
            ])
        )

    print("\nHU-07: EXCEPCIONES VALIDADAS")


if __name__ == "__main__":
    main()
