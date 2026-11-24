
import os
from pathlib import Path

from dotenv import load_dotenv
from pymongo import MongoClient


class MongoConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return

        base = Path(__file__).resolve().parent.parent
        load_dotenv(base / ".env")

        uri = os.getenv("MONGODB_URI")
        database_name = os.getenv("MONGODB_DATABASE")
        collection_name = os.getenv("MONGODB_COLLECTION")

        if not uri or not database_name or not collection_name:
            raise ValueError(
                "Faltan variables de MongoDB en .env"
            )

        cliente = MongoClient(
            uri,
            serverSelectionTimeoutMS=10000,
            socketTimeoutMS=30000,
            retryWrites=False
        )

        try:
            cliente.admin.command("ping")
        except Exception:
            cliente.close()
            raise

        self.cliente = cliente
        self.database = cliente[database_name]
        self.coleccion = self.database[collection_name]
        self._initialized = True

    @classmethod
    def get_instance(cls):
        return cls()

    def cerrar(self):
        if getattr(self, "_initialized", False):
            self.cliente.close()
            self._initialized = False
            type(self)._instance = None
