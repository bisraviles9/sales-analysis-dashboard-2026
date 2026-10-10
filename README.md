# Panel de análisis de ventas · 2026

Tablero interactivo creado en Python con Streamlit, inspirado en el dashboard de referencia. Toda la interfaz, los datos de demostración, los gráficos y la descarga están en español.

> La app comienza con 10.000 registros ficticios y reproducibles para 2026; no son ventas reales. Puedes cargar un archivo CSV propio desde los filtros.

## Ejecutar la app

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run app.py
```

## Columnas para cargar un CSV

Obligatorias: `Fecha del pedido`, `Región`, `Categoría`, `Segmento`, `Ventas`, `Unidades`, `Ganancia` y `Descuento`.

Opcionales: `Estado`, `Subcategoría` e `ID del pedido`. La aplicación también reconoce los encabezados equivalentes en inglés (`Order Date`, `Region`, `Category`, `Segment`, `Sales`, `Quantity`, `Profit`, `Discount`, `State`, `Sub-Category`, `Order ID`).

La descarga de los registros filtrados usa encabezados en español y codificación compatible con Excel.

## Publicar en Streamlit Community Cloud

1. Sube este proyecto a GitHub.
2. En Streamlit Community Cloud, crea una app desde el repositorio.
3. Elige `app.py` como archivo principal y publícala.

## Archivos

- `app.py`: aplicación, visualizaciones y datos ficticios.
- `requirements.txt`: dependencias.
