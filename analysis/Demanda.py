import pandas as pd
from utils.data_loader import DataLoader

datos = DataLoader().load_csv()
datos = datos.head(1000000)
print ("Total analizado:",len(datos))
datos["boarding_datetime"] = pd.to_datetime(datos["boarding_datetime"])

dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

por_hora = datos.groupby("hour").size()
por_dia = datos.groupby(datos["boarding_datetime"].dt.dayofweek).size()
por_dia.index = [dias[i] for i in por_dia.index]

print("Viajes por hora:")
print(por_hora)
print("Viajes por día:")
print(por_dia)
print("Hora pico:", por_hora.idxmax())
print("Día con más demanda:", por_dia.idxmax())