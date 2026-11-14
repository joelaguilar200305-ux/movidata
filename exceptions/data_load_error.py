class DataLoadError(Exception):
    """Error personalizado para problemas durante la carga de datos."""

    def _init_(self, message: str) -> None:
        super()._init_(message)