import pandas as pd
import streamlit as st
import plotly.express as px

# Cargar los datos desde la hoja 'Data' con encabezado en la fila 13 (índice 12)
column_names = [
    "Activity Group", "Activity Group ID", "Activity", "Activity ID", "Advertiser",
    "Campaign", "Site (CM360)", "Placement", "Month",
    "Total Conversions", "Click-through Conversions", "View-through Conversions",
    "Total Revenue", "Click-through Revenue", "View-through Revenue"
]
df = pd.read_excel("3.3 Lab Reporting CM - Conversions.xlsx", sheet_name="Data", header=13, names=column_names, engine="openpyxl")

# Eliminar filas con valores nulos en columnas clave
df = df.dropna(subset=["Campaign", "Placement", "Month", "Total Conversions", "Click-through Conversions", "View-through Conversions"])

# Convertir columnas numéricas a tipo adecuado
numeric_cols = ["Total Conversions", "Click-through Conversions", "View-through Conversions", "Total Revenue"]
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

# Calcular campañas más populares
popular_campaigns = df.groupby("Campaign")["Total Conversions"].sum().sort_values(ascending=False).reset_index()

# Calcular campañas más rentables (revenue por conversión)
revenue_by_campaign = df.groupby("Campaign")[["Total Revenue", "Total Conversions"]].sum()
revenue_by_campaign["Revenue per Conversion"] = revenue_by_campaign["Total Revenue"] / revenue_by_campaign["Total Conversions"]
revenue_by_campaign = revenue_by_campaign.sort_values("Revenue per Conversion", ascending=False).reset_index()

# Comparación entre click-through y view-through
conversion_types = df[["Click-through Conversions", "View-through Conversions"]].sum().reset_index()
conversion_types.columns = ["Conversion Type", "Count"]

# Interfaz Streamlit
st.title("Dashboard de Conversiones de Campañas de Marketing")

# Gráfico de campañas más populares
st.subheader("Campañas más Populares por Número de Conversiones")
fig1 = px.bar(popular_campaigns.head(10), x="Total Conversions", y="Campaign", orientation="h", title="Top 10 Campañas Populares")
st.plotly_chart(fig1)

# Gráfico de campañas más rentables
st.subheader("Campañas más Rentables (Revenue por Conversión)")
fig2 = px.bar(revenue_by_campaign.head(10), x="Revenue per Conversion", y="Campaign", orientation="h", title="Top 10 Campañas Rentables")
st.plotly_chart(fig2)

# Gráfico de comparación de tipos de conversión
st.subheader("Comparación entre Click-through y View-through Conversions")
fig3 = px.pie(conversion_types, names="Conversion Type", values="Count", title="Distribución de Tipos de Conversión")
st.plotly_chart(fig3)

# Filtros interactivos para análisis por placement y fecha
st.subheader("Análisis Interactivo por Placement y Fecha")
selected_months = st.multiselect("Selecciona Meses:", options=df["Month"].unique(), default=df["Month"].unique())
selected_placements = st.multiselect("Selecciona Placements:", options=df["Placement"].unique(), default=df["Placement"].unique())

filtered_df = df[df["Month"].isin(selected_months) & df["Placement"].isin(selected_placements)]

# Gráfico de conversiones por placement
fig4 = px.bar(filtered_df.groupby("Placement")["Total Conversions"].sum().sort_values(ascending=False).reset_index(),
              x="Total Conversions", y="Placement", orientation="h", title="Conversiones por Placement")
st.plotly_chart(fig4)

# Gráfico de conversiones por mes
fig5 = px.bar(filtered_df.groupby("Month")["Total Conversions"].sum().reset_index(),
              x="Month", y="Total Conversions", title="Conversiones por Mes")
st.plotly_chart(fig5)


# streamlit run Dashboard.py