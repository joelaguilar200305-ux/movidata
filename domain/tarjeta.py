class Tarjeta:
    """Entidad que representa la tarjeta (usuario) del transporte público.

    Solo guarda datos: no contiene lógica de base de datos.
    """

    def __init__(self, card_id: str, user_type: str, district: str) -> None:
        self._card_id = card_id        # Identificador de la tarjeta (TRJ0000001)
        self._user_type = user_type    # Regular, Estudiante, Jubilado o Turista
        self._district = district      # Distrito de residencia del usuario

    @property
    def card_id(self) -> str:
        return self._card_id

    @property
    def user_type(self) -> str:
        return self._user_type

    @property
    def district(self) -> str:
        return self._district