"""EDA del dataset MoviData Panamá.

Lee data/viajes_movidata.csv con pandas, calcula estadísticos y guarda:
- docs/eda_tablas.md (tablas en Markdown para usar en docs/eda.md)
- docs/eda_viajes_por_hora.png
- docs/eda_tarifa_por_tipo_usuario.png

Es una herramienta de exploración aparte; no forma parte del núcleo de la aplicación.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # genera las imágenes sin abrir ventanas
import matplotlib.pyplot as plt
import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
CSV = RAIZ / "data" / "viajes_movidata.csv"
DOCS = RAIZ / "docs"

COLUMNAS_NUMERICAS = ["hour", "distance_km", "duration_min", "fare"]
COLUMNAS_TEXTO = [
    "user_type", "district", "transport_mode", "route_line", "origin",
    "destination", "day_of_week", "payment_method", "weather",
]


def a_markdown(tabla: pd.DataFrame) -> str:
    """Convierte un DataFrame a tabla Markdown sin depender de otras librerías."""
    encabezado = "| " + " | ".join(str(c) for c in tabla.columns) + " |"
    separador = "| " + " | ".join("---" for _ in tabla.columns) + " |"
    filas = [
        "| " + " | ".join(str(v) for v in fila) + " |"
        for fila in tabla.itertuples(index=False)
    ]
    return "\n".join([encabezado, separador, *filas])


def conteo(datos: pd.DataFrame, columna: str) -> pd.DataFrame:
    """Cantidad y porcentaje de viajes por cada valor de una columna."""
    tabla = datos[columna].value_counts().rename_axis(columna).reset_index(name="viajes")
    tabla["porcentaje"] = (tabla["viajes"] / len(datos) * 100).round(2)
    return tabla


def guardar_grafico_horas(datos: pd.DataFrame) -> None:
    por_hora = datos.groupby("hour").size()
    plt.figure(figsize=(10, 5))
    plt.bar(por_hora.index, por_hora.values)
    plt.title("Viajes por hora del día")
    plt.xlabel("Hora")
    plt.ylabel("Cantidad de viajes")
    plt.xticks(range(0, 24))
    plt.tight_layout()
    plt.savefig(DOCS / "eda_viajes_por_hora.png", dpi=150)
    plt.close()


def guardar_grafico_tarifa(datos: pd.DataFrame) -> None:
    tarifa = datos.groupby("user_type", observed=True)["fare"].mean().sort_values()
    plt.figure(figsize=(8, 5))
    plt.bar(tarifa.index.astype(str), tarifa.values)
    plt.title("Tarifa promedio por tipo de usuario")
    plt.xlabel("Tipo de usuario")
    plt.ylabel("Tarifa promedio (PAB)")
    plt.tight_layout()
    plt.savefig(DOCS / "eda_tarifa_por_tipo_usuario.png", dpi=150)
    plt.close()


def main() -> None:
    DOCS.mkdir(exist_ok=True)
    tipos = {columna: "category" for columna in COLUMNAS_TEXTO}
    datos = pd.read_csv(CSV, dtype=tipos, parse_dates=["boarding_datetime"])

    resumen = pd.DataFrame({
        "dato": ["Registros", "Columnas", "Valores vacíos", "trip_id repetidos",
                 "Primer viaje", "Último viaje"],
        "valor": [
            f"{len(datos):,}", datos.shape[1], int(datos.isna().sum().sum()),
            int(datos["trip_id"].duplicated().sum()),
            datos["boarding_datetime"].min(), datos["boarding_datetime"].max(),
        ],
    })

    estadisticos = (
        datos[COLUMNAS_NUMERICAS].describe().round(2).T
        .rename_axis("variable").reset_index()
    )

    secciones = [
        "## Resumen general\n\n" + a_markdown(resumen),
        "## Estadísticos descriptivos\n\n" + a_markdown(estadisticos),
    ]
    for columna in ["transport_mode", "user_type", "payment_method", "weather"]:
        secciones.append(f"## Viajes por {columna}\n\n" + a_markdown(conteo(datos, columna)))
    secciones.append(
        "## Las 5 rutas con más viajes\n\n" + a_markdown(conteo(datos, "route_line").head(5))
    )

    por_hora = datos.groupby("hour").size()
    secciones.append(
        f"## Hora pico\n\nLa hora con más viajes es las {por_hora.idxmax()}:00 "
        f"con {por_hora.max():,} viajes."
    )

    (DOCS / "eda_tablas.md").write_text("\n\n".join(secciones), encoding="utf-8")
    guardar_grafico_horas(datos)
    guardar_grafico_tarifa(datos)


if __name__ == "__main__":
    main()
    