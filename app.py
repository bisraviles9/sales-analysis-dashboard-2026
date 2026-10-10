import calendar
from datetime import date

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Sales Analysis Dashboard 2026", page_icon="📊", layout="wide")

BLUE = "#49a9e8"
DARK_BLUE = "#1261a0"
TEAL = "#28c4c7"
PALETTE = [BLUE, DARK_BLUE, TEAL, "#80c8f3", "#245da8", "#87dedb"]


def sample_data():
    """Reproducible demo dataset for 2026 (fictional—not real sales)."""
    import numpy as np

    rng = np.random.default_rng(2026)
    n = 10_000
    regions = ["West", "East", "Central", "South"]
    states_by_region = {
        "West": ["California", "Washington", "Oregon", "Nevada", "Arizona"],
        "East": ["New York", "Pennsylvania", "Massachusetts", "Virginia", "Georgia"],
        "Central": ["Illinois", "Ohio", "Michigan", "Missouri", "Colorado"],
        "South": ["Texas", "Florida", "Tennessee", "North Carolina", "Alabama"],
    }
    region = rng.choice(regions, n, p=[.31, .28, .22, .19])
    states = [rng.choice(states_by_region[r]) for r in region]
    categories = rng.choice(["Technology", "Furniture", "Office Supplies"], n, p=[.36, .32, .32])
    subcategories = []
    for cat in categories:
        options = {
            "Technology": ["Phones", "Accessories", "Copiers", "Machines"],
            "Furniture": ["Chairs", "Tables", "Bookcases", "Furnishings"],
            "Office Supplies": ["Binders", "Paper", "Storage", "Labels", "Art", "Envelopes"],
        }[cat]
        subcategories.append(rng.choice(options))
    # Use Python ordinals so generated dates always stay within calendar year 2026.
    dates = pd.to_datetime([date.fromordinal(int(x)) for x in rng.integers(date(2026, 1, 1).toordinal(), date(2027, 1, 1).toordinal(), n)])
    quantity = rng.integers(1, 9, n)
    unit_price = rng.uniform(18, 520, n)
    sales = unit_price * quantity
    discount = rng.choice([0, .05, .10, .15, .20], n, p=[.25, .25, .25, .15, .10])
    profit = sales * rng.uniform(.08, .34, n) - sales * discount * .25
    segment = rng.choice(["Consumer", "Corporate", "Home Office"], n, p=[.51, .31, .18])
    return pd.DataFrame({
        "Order Date": dates,
        "Region": region,
        "State": states,
        "Category": categories,
        "Sub-Category": subcategories,
        "Segment": segment,
        "Sales": sales.round(2),
        "Quantity": quantity,
        "Profit": profit.round(2),
        "Discount": discount,
    })


px.defaults.template = "plotly_dark"

st.markdown("""
<style>
:root { color-scheme: dark; }
.stApp, [data-testid="stAppViewContainer"] {background:#07111f; color:#e8f0fa;}
[data-testid="stMain"] {background:radial-gradient(ellipse at 50% -15%, #16375a 0%, #0b192a 42%, #07111f 78%);}
[data-testid="stHeader"] {background:rgba(7,17,31,.82);}
[data-testid="stSidebar"] {background:linear-gradient(180deg,#0d1c30 0%,#091523 100%); border-right:1px solid #20334b;}
.block-container {padding-top:1.4rem; padding-bottom:2.2rem; max-width:1500px;}
.hero {text-align:center; color:#f4f9ff; font-size:2.25rem; font-weight:800; letter-spacing:.02em; margin:.15rem 0 .7rem; padding:1.2rem; border:1px solid #2b5372; border-radius:18px; background:linear-gradient(105deg,#102842 0%,#143958 48%,#123246 100%); box-shadow:0 14px 38px #02081088;}
[data-testid="stCaptionContainer"] {color:#9eb1c9;}
[data-testid="stMetric"] {background:linear-gradient(145deg,#172a41 0%,#102238 100%); border:1px solid #29415c; border-top:2px solid #2bbec5; padding:15px 15px 13px; border-radius:15px; box-shadow:0 10px 24px #02081055; min-height:106px;}
[data-testid="stMetricLabel"] {justify-content:center; color:#a9bdd3;}
[data-testid="stMetricValue"] {justify-content:center; color:#f4f8ff; font-weight:750;}
[data-testid="stMetricValue"] > div {font-size:clamp(1rem,1.4vw,1.45rem); white-space:nowrap;}
[data-testid="stMetricDelta"] {justify-content:center;}
[data-testid="stFileUploaderDropzone"] {background:#102238 !important; border:1px dashed #3b718c !important; border-radius:12px !important;}
[data-testid="stFileUploaderDropzone"] * {color:#dce9f7 !important;}
[data-testid="stFileUploaderDropzone"] button {background:#193954 !important; border:1px solid #35788c !important;}
[data-baseweb="select"] > div {background:#102238 !important; border-color:#35516e !important; color:#e8f0fa !important;}
[data-baseweb="select"] input {color:#e8f0fa !important;}
[data-baseweb="tag"] {background:#126a78 !important; border:1px solid #28b7bb !important; color:#f3ffff !important;}
[data-baseweb="tag"] span, [data-baseweb="tag"] svg {color:#f3ffff !important; fill:#f3ffff !important;}
[data-baseweb="popover"] ul, [data-baseweb="popover"] li {background:#102238 !important; color:#e8f0fa !important;}
[data-baseweb="popover"] li:hover {background:#1b3954 !important;}
[data-testid="stPlotlyChart"] {background:#0e1b2b; border:1px solid #20344c; border-radius:15px; padding:8px; box-shadow:0 8px 22px #02081044;}
[data-testid="stMarkdownContainer"] h2, [data-testid="stMarkdownContainer"] h3 {color:#d9e9fb; font-weight:700;}
[data-testid="stExpander"] {background:#0e1b2b; border:1px solid #243a53; border-radius:12px;}
[data-testid="stDataFrame"] {border:1px solid #243a53; border-radius:10px;}
.stButton button, .stDownloadButton button {background:linear-gradient(100deg,#147d91,#1a9da6); color:white; border:1px solid #33c4c8; border-radius:9px;}
.stButton button:hover, .stDownloadButton button:hover {background:#23aeb5; color:white; border-color:#65e4de;}
hr {border-color:#243a53;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero">📊 Sales Analysis Dashboard · 2026</div>', unsafe_allow_html=True)
st.caption("Panel interactivo de ventas · Datos demostrativos ficticios para 2026")

with st.sidebar:
    st.header("Filtros")
    uploaded = st.file_uploader("Cargar tus datos (CSV)", type=["csv"], help="Columnas mínimas: Order Date, Region, Category, Segment, Sales, Quantity, Profit y Discount. State y Sub-Category son opcionales.")

    if uploaded:
        try:
            data = pd.read_csv(uploaded)
            required = {"Order Date", "Region", "Category", "Segment", "Sales", "Quantity", "Profit", "Discount"}
            missing = required - set(data.columns)
            if missing:
                st.error("Faltan columnas: " + ", ".join(sorted(missing)))
                data = sample_data()
            else:
                data["Order Date"] = pd.to_datetime(data["Order Date"], errors="coerce")
                for col in ["Sales", "Quantity", "Profit", "Discount"]:
                    data[col] = pd.to_numeric(data[col], errors="coerce")
                data = data.dropna(subset=["Order Date", "Sales", "Quantity", "Profit", "Discount"])
                if "State" not in data:
                    data["State"] = "Not specified"
                if "Sub-Category" not in data:
                    data["Sub-Category"] = "Not specified"
        except Exception as exc:
            st.error(f"No se pudo leer el CSV: {exc}")
            data = sample_data()
    else:
        data = sample_data()

    data["Year"] = data["Order Date"].dt.year
    years = sorted(data["Year"].dropna().unique().tolist())
    selected_year = st.selectbox("Año", years, index=years.index(2026) if 2026 in years else len(years)-1)
    data = data[data["Year"] == selected_year]
    region_options = sorted(data["Region"].dropna().unique().tolist())
    selected_regions = st.multiselect("Región", region_options, default=region_options)
    category_options = sorted(data["Category"].dropna().unique().tolist())
    selected_categories = st.multiselect("Categoría", category_options, default=category_options)
    segment_options = sorted(data["Segment"].dropna().unique().tolist())
    selected_segments = st.multiselect("Segmento", segment_options, default=segment_options)
    month_names = {i: calendar.month_abbr[i] for i in range(1, 13)}
    data["Month"] = data["Order Date"].dt.month
    month_options = sorted(data["Month"].dropna().unique().astype(int).tolist())
    selected_months = st.multiselect("Mes", month_options, default=month_options, format_func=lambda m: month_names[m])

filtered = data[
    data["Region"].isin(selected_regions)
    & data["Category"].isin(selected_categories)
    & data["Segment"].isin(selected_segments)
    & data["Month"].isin(selected_months)
].copy()

if filtered.empty:
    st.warning("No hay datos para los filtros elegidos. Ajusta los filtros de la izquierda.")
    st.stop()

# KPI cards
kpis = st.columns(5)
orders = filtered["Order ID"].nunique() if "Order ID" in filtered else len(filtered)
values = [
    ("Ventas totales", f"${filtered['Sales'].sum():,.0f}"),
    ("Unidades", f"{filtered['Quantity'].sum():,.0f}"),
    ("Ganancia", f"${filtered['Profit'].sum():,.0f}"),
    ("Descuento promedio", f"{filtered['Discount'].mean():.1%}"),
    ("Pedidos", f"{orders:,.0f}"),
]
for col, (label, value) in zip(kpis, values):
    with col:
        st.metric(label, value)

left, mid, right = st.columns([1, 1, 1.45])
with left:
    st.subheader("Ventas por región")
    by_region = filtered.groupby("Region", as_index=False)["Sales"].sum()
    fig = px.pie(by_region, names="Region", values="Sales", hole=.05, color_discrete_sequence=PALETTE)
    fig.update_traces(textposition="outside", textinfo="label+percent")
    fig.update_layout(margin=dict(t=8, b=5, l=5, r=5), showlegend=False, height=300)
    st.plotly_chart(fig, use_container_width=True)
with mid:
    st.subheader("Ventas por categoría")
    by_category = filtered.groupby("Category", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False)
    fig = px.bar(by_category, x="Category", y="Sales", color_discrete_sequence=[BLUE], text_auto=".2s")
    fig.update_layout(margin=dict(t=8, b=5, l=5, r=5), height=300, showlegend=False, xaxis_title="", yaxis_title="Ventas")
    st.plotly_chart(fig, use_container_width=True)
with right:
    st.subheader("Ventas por segmento")
    by_segment = filtered.groupby("Segment", as_index=False)["Sales"].sum()
    fig = px.pie(by_segment, names="Segment", values="Sales", hole=.62, color_discrete_sequence=[DARK_BLUE, BLUE, TEAL])
    fig.update_traces(textposition="outside", textinfo="label+percent")
    fig.update_layout(margin=dict(t=8, b=5, l=5, r=5), showlegend=False, height=300)
    st.plotly_chart(fig, use_container_width=True)

left, right = st.columns([1, 1.55])
with left:
    st.subheader("Ventas por subcategoría")
    by_sub = filtered.groupby("Sub-Category", as_index=False)["Sales"].sum().sort_values("Sales")
    fig = px.bar(by_sub, x="Sales", y="Sub-Category", orientation="h", color_discrete_sequence=[BLUE], text_auto=".2s")
    fig.update_layout(margin=dict(t=8, b=5, l=5, r=5), height=390, xaxis_title="Ventas", yaxis_title="")
    st.plotly_chart(fig, use_container_width=True)
with right:
    st.subheader("Tendencia mensual por región")
    monthly = filtered.groupby(["Month", "Region"], as_index=False)["Sales"].sum()
    monthly["Mes"] = monthly["Month"].map(month_names)
    fig = px.area(monthly, x="Mes", y="Sales", color="Region", category_orders={"Mes": [month_names[m] for m in range(1,13)]}, color_discrete_sequence=PALETTE)
    fig.update_layout(margin=dict(t=8, b=5, l=5, r=5), height=390, xaxis_title="Mes de 2026", yaxis_title="Ventas", legend_title="Región")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Ventas por estado")
if "State" in filtered and (filtered["State"] != "Not specified").any():
    by_state = filtered.groupby("State", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False)
    fig = px.bar(by_state, x="State", y="Sales", color="Sales", color_continuous_scale=["#b9e7f5", DARK_BLUE], text_auto=".2s")
    fig.update_layout(margin=dict(t=5, b=5, l=5, r=5), height=330, xaxis_title="Estado", yaxis_title="Ventas", coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("El CSV no incluye nombres de estado para mostrar este gráfico.")

with st.expander("Ver datos filtrados"):
    st.dataframe(filtered.drop(columns=["Year", "Month"], errors="ignore"), use_container_width=True, hide_index=True)
    st.download_button("Descargar datos filtrados (CSV)", filtered.to_csv(index=False).encode("utf-8"), file_name=f"ventas_{selected_year}_filtradas.csv", mime="text/csv")

st.caption("© Dashboard demostrativo · Puedes reemplazar la muestra cargando tu archivo CSV.")
