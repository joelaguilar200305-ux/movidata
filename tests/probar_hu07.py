
import os
from types import SimpleNamespace
from unittest.mock import Mock, patch

from repositories.mongo_viaje_repository import MongoViajeRepository


def probar_guardado_simulado():

    print("\n=== PRUEBA DE INSERCION SIMULADA ===")

    # Crear Repository sin conexion real
    repositorio = object.__new__(MongoViajeRepository)
    repositorio.coleccion = Mock()

    registros = [
        {"trip_id": "PRUEBA001"},
        {"trip_id": "PRUEBA002"},
        {"trip_id": "PRUEBA001"}
    ]

    # Comprobar que las escrituras estan bloqueadas
    with patch.dict(
        os.environ,
        {"MOVIDATA_HABILITAR_ESCRITURA": "false"}
    ):
        try:
            repositorio.guardar_lote(registros)
            raise AssertionError(
                "La escritura no fue bloqueada"
            )
        except PermissionError:
            print("Proteccion de escritura: CORRECTA")

    repositorio.coleccion.bulk_write.assert_not_called()

    # Simular el resultado de MongoDB sin conectar
    repositorio.coleccion.bulk_write.return_value = (
        SimpleNamespace(upserted_count=2)
    )

    with patch.dict(
        os.environ,
        {"MOVIDATA_HABILITAR_ESCRITURA": "true"}
    ):
        resultado = repositorio.guardar_lote(registros)

    operaciones = (
        repositorio.coleccion.bulk_write.call_args.args[0]
    )

    assert len(operaciones) == 2
    assert resultado["procesados"] == 3
    assert resultado["insertados"] == 2
    assert resultado["existentes_o_repetidos"] == 1

    print("Registros recibidos:", resultado["procesados"])
    print("Inserciones simuladas:", resultado["insertados"])
    print("Duplicados simulados: 1")
    print("INSERCION SIMULADA CORRECTA")


def probar_paginacion():

    print("\n=== PRUEBA DE PAGINACION REAL ===")

    repositorio = MongoViajeRepository()

    try:
        pagina1 = repositorio.obtener_pagina(limite=5)

        assert len(pagina1) == 5

        ultimo_id = pagina1[-1].trip_id

        pagina2 = repositorio.obtener_pagina(
            limite=5,
            despues_de=ultimo_id
        )

        assert len(pagina2) == 5

        ids1 = {viaje.trip_id for viaje in pagina1}
        ids2 = {viaje.trip_id for viaje in pagina2}

        assert ids1.isdisjoint(ids2)

        print("Primera pagina:")
        for viaje in pagina1:
            print(viaje.trip_id)

        print("\nSegunda pagina:")
        for viaje in pagina2:
            print(viaje.trip_id)

        print("\nPAGINACION VALIDADA CORRECTAMENTE")

        total = repositorio.contar_documentos()

        print("\nDocumentos en MongoDB:", total)

        assert total == 1000000, (
            "El total no coincide con el esperado"
        )

        print("MILLON DE DOCUMENTOS VERIFICADO")

    finally:
        repositorio.cerrar()


def main():

    print("=== VALIDACION HU-07 MOVIDATA ===")

    probar_guardado_simulado()
    probar_paginacion()

    print("\nHU-07: PRUEBAS FINALIZADAS")


if __name__ == "__main__":
    main()
