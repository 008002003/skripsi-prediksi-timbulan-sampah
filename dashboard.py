import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Dashboard Prediksi Timbulan Sampah",
    page_icon="📊",
    layout="wide"
)

# ======================
# LOAD DATA
# ======================

df = pd.read_csv("dashboard_data.csv")
evaluasi = pd.read_csv("evaluasi_dashboard.csv")

# ======================
# SIDEBAR
# ======================

st.sidebar.title("📍 Filter Kecamatan")

kecamatan_pilih = st.sidebar.selectbox(
    "Pilih Kecamatan",
    sorted(df["kecamatan"].unique())
)

df_filter = df[
    df["kecamatan"] == kecamatan_pilih
].copy()

evaluasi_filter = evaluasi[
    evaluasi["kecamatan"] == kecamatan_pilih
].copy()

# Memisahkan data berdasarkan jenis
df_ground_truth = df_filter[
    df_filter["jenis"] == "Ground Truth"
].copy()

df_prediksi = df_filter[
    df_filter["jenis"] == "Prediksi"
].copy()

df_forecast = df_filter[
    df_filter["jenis"] == "Forecast"
].copy()
# ======================
# HEADER
# ======================

st.title(
    "📊 Dashboard Prediksi Timbulan Sampah Kabupaten Jember"
)

st.markdown("""
Dashboard hasil prediksi timbulan sampah menggunakan
metode Random Forest Regressor.
""")

# ======================
# KPI
# ======================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Timbulan Aktual",
        f"{df_ground_truth['Timbulan_Sampah_Ton'].sum():,.2f} Ton"
    )

with col2:
    st.metric(
        "Rata-rata Bulanan Aktual",
        f"{df_ground_truth['Timbulan_Sampah_Ton'].mean():,.2f} Ton"
    )

with col3:

    prediksi_2026 = df_forecast[
        "Timbulan_Sampah_Ton"
    ].sum()

    st.metric(
        "Forecast 2026",
        f"{prediksi_2026:,.2f} Ton"
    )

st.divider()

# ======================
# GRAFIK
# ======================

df_filter["periode"] = (
    df_filter["tahun"].astype(str)
    + "-"
    + df_filter["bulan"].astype(str).str.zfill(2)
)

fig = px.line(
    df_filter,
    x="periode",
    y="Timbulan_Sampah_Ton",
    color="jenis",
    markers=True,
    title=f"Perbandingan Ground Truth, Prediksi, dan Forecast Timbulan Sampah Kecamatan {kecamatan_pilih}"
)


st.plotly_chart(
    fig,
    use_container_width=True
)

st.caption("""
**Keterangan Grafik**

🔵 **Ground Truth** : Data aktual timbulan sampah Kabupaten Jember tahun 2020–2025.

🟦 **Prediksi** : Hasil prediksi model Random Forest terhadap data historis tahun 2020–2025.

🔴 **Forecast** : Hasil prediksi timbulan sampah tahun 2026 menggunakan model Random Forest.
""")

st.divider()

# ======================
# INFORMASI MODEL
# ======================
mae = evaluasi_filter[
    "Absolute_Error"
].mean()

st.subheader("🤖 Informasi Model")

info1, info2, info3, info4 = st.columns(4)

with info1:
    st.metric(
        "Metode",
        "Random Forest"
    )

with info2:
    st.metric(
        "RMSE",
        "53.34"
    )

with info3:
    st.metric(
        "MAPE",
        "14.52%"
    )

with info4:
    st.metric(
        "MAE",
        f"{mae:.2f} Ton"
    )
st.divider()

# ======================
# DATA DETAIL
# ======================

st.subheader("📋 Data Detail")

st.dataframe(
    df_filter[
        [
            "tahun",
            "bulan",
            "kecamatan",
            "Timbulan_Sampah_Ton",
            "jenis"
        ]
    ],
    use_container_width=True
)