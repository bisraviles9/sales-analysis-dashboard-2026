# Sales Analysis Dashboard 2026

Dashboard interactivo en Python y Streamlit, inspirado en la referencia visual enviada. Incluye filtros, indicadores y gráficos de ventas por región, categoría, segmento, subcategoría, estado y mes.

> La aplicación inicia con datos ficticios reproducibles del año 2026. No representan ventas reales. Puedes cargar tu propio CSV desde la barra lateral.

## Ejecutar localmente

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run app.py
```

## Formato del CSV

Columnas obligatorias: `Order Date`, `Region`, `Category`, `Segment`, `Sales`, `Quantity`, `Profit`, `Discount`.

Columnas opcionales: `State`, `Sub-Category`, `Order ID`. Las fechas pueden ser cualquier fecha; el selector de año muestra los años presentes en el archivo.

## Publicar en Streamlit Community Cloud

1. Sube este proyecto a un repositorio de GitHub.
2. En Streamlit Community Cloud, elige **Create app** y selecciona ese repositorio.
3. Indica `app.py` como archivo principal y publica.

## Archivos

- `app.py`: aplicación y datos de demostración.
- `requirements.txt`: dependencias.
