class AnalysisResult:
    """Resultado común que devuelve cualquier estrategia de análisis."""

    def __init__(self, kind: str, data: dict | None = None) -> None:
        self._kind = kind
        self._data = data if data is not None else {}

    @property
    def kind(self) -> str:
        return self._kind

    @property
    def data(self) -> dict:
        return self._data