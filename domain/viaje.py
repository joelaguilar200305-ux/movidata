from datetime import datetime


class Viaje:
    """Entidad que representa un viaje en Metro o Metrobus.

    Solo guarda datos: no contiene lógica de base de datos.
    """

    def __init__(
        self,
        trip_id: str,
        card_id: str,
        transport_mode: str,
        route_line: str,
        origin: str,
        destination: str,
        boarding_datetime: datetime,
        day_of_week: str,
        hour: int,
        distance_km: float,
        duration_min: float,
        fare: float,
        payment_method: str,
        weather: str,
    ) -> None:
        self._trip_id = trip_id                      # Identificador único del viaje (VJE...)
        self._card_id = card_id                      # Tarjeta que realizó el viaje (TRJ...)
        self._transport_mode = transport_mode        # Metro o Metrobus
        self._route_line = route_line                # Línea del Metro o ruta del Metrobus
        self._origin = origin                        # Estación o parada de origen
        self._destination = destination              # Estación o parada de destino
        self._boarding_datetime = boarding_datetime  # Fecha y hora de abordaje
        self._day_of_week = day_of_week              # Día de la semana
        self._hour = hour                            # Hora de abordaje (0-23)
        self._distance_km = distance_km              # Distancia en kilómetros
        self._duration_min = duration_min            # Duración en minutos
        self._fare = fare                            # Tarifa pagada en balboas (PAB)
        self._payment_method = payment_method        # Medio de pago
        self._weather = weather                      # Clima estimado del viaje

    @property
    def trip_id(self) -> str:
        return self._trip_id

    @property
    def card_id(self) -> str:
        return self._card_id

    @property
    def transport_mode(self) -> str:
        return self._transport_mode

    @property
    def route_line(self) -> str:
        return self._route_line

    @property
    def origin(self) -> str:
        return self._origin

    @property
    def destination(self) -> str:
        return self._destination

    @property
    def boarding_datetime(self) -> datetime:
        return self._boarding_datetime

    @property
    def day_of_week(self) -> str:
        return self._day_of_week

    @property
    def hour(self) -> int:
        return self._hour

    @property
    def distance_km(self) -> float:
        return self._distance_km

    @property
    def duration_min(self) -> float:
        return self._duration_min

    @property
    def fare(self) -> float:
        return self._fare

    @property
    def payment_method(self) -> str:
        return self._payment_method

    @property
    def weather(self) -> str:
        return self._weather
    