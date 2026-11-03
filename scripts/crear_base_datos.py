
import os
from pathlib import Path
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError

# PASO 1: Localizar el archivo .env
ruta_env = Path(__file__).resolve().parent.parent / ".env"

# PASO 2: Cargar las variables del archivo .env
load_dotenv(dotenv_path=ruta_env)

# PASO 3: Obtener la cadena de conexion
uri = os.getenv("MONGODB_URI")

if not uri:
    print("ERROR: Falta configurar MONGODB_URI en .env")

else:
    cliente = None

    try:
        # PASO 4: Conectar con MongoDB Atlas
        cliente = MongoClient(
            uri,
            serverSelectionTimeoutMS=5000
        )

        # PASO 5: Verificar la conexion
        cliente.admin.command("ping")
        print("Conexion exitosa con MongoDB Atlas")

        # PASO 6: Seleccionar la base de datos
        db = cliente["movidata"]

        # PASO 7: Crear la coleccion si no existe
        if "viajes" not in db.list_collection_names():
            db.create_collection("viajes")
            print("Coleccion viajes creada correctamente")
        else:
            print("La coleccion viajes ya existe")

        print("Base de datos: movidata")
        print("Coleccion: viajes")
        print("Proceso finalizado correctamente")

    except PyMongoError as error:
        print("Error de conexion:", type(error).__name__)
        print("Detalle:", error)

    finally:
        if cliente is not None:
            cliente.close()
