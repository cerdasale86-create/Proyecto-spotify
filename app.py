import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# CONFIGURACIÓN GENERAL
st.set_page_config(page_title="Spotify Music Analytics", layout="wide")

st.markdown("""
<style>

/* ===== SIDEBAR FONDO ===== */
section[data-testid="stSidebar"] {
    background-color: #181818;
}

/* ===== TITULOS Y LABELS ===== */
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #1AA34A !important;
    font-weight: 600;
}

/* ===== SELECTBOX Y MULTISELECT ===== */
div[data-baseweb="select"] > div {
    background-color: #222222 !important;
    color: white !important;
    border-radius: 6px;
    border: 1px solid #2e2e2e;
}

/* Texto dentro del select */
div[data-baseweb="select"] span {
    color: #e0e0e0 !important;
}

/* Dropdown */
ul[role="listbox"] {
    background-color: #222222 !important;
}

/* Opciones */
ul[role="listbox"] li {
    color: #e0e0e0 !important;
}

/* Hover más suave */
ul[role="listbox"] li:hover {
    background-color: #1AA34A !important;
    color: white !important;
}

/* Tags seleccionados (más sobrios) */
span[data-baseweb="tag"] {
    background-color: #2c2c2c !important;
    color: #1AA34A !important;
    border: 1px solid #1AA34A;
}

/* ===== SLIDER ESTILO MINIMALISTA ===== */
div[data-testid="stSlider"] div[data-baseweb="slider"] > div {
    background-color: #2e2e2e !important;
}

/* Parte activa del slider */
div[data-testid="stSlider"] div[data-baseweb="slider"] > div > div {
    background-color: #1AA34A !important;
}

/* Botón del slider */
div[data-testid="stSlider"] div[role="slider"] {
    background-color: #1AA34A !important;
    border: none !important;
}

            
            
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

/* ===== FONDO GENERAL ===== */
.stApp {
    background-color: #111111;
    color: #EAEAEA;
}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {
    background-color: #181818;
}

/* ===== TITULOS PRINCIPALES ===== */
h1, h2, h3, h4 {
    color: #1AA34A !important;
}

/* ===== TEXTO NORMAL ===== */
p, span, div {
    color: #EAEAEA;
}

/* ===== TABS ===== */
button[data-baseweb="tab"] {
    background-color: #1C1C1C !important;
    color: #A0A0A0 !important;
    border-radius: 6px 6px 0px 0px;
}

button[data-baseweb="tab"][aria-selected="true"] {
    background-color: #1AA34A !important;
    color: white !important;
}

/* ===== METRICS (KPIs) ===== */
div[data-testid="metric-container"] {
    background-color: #1C1C1C;
    border-radius: 12px;
    padding: 15px;
    box-shadow: 0px 0px 10px rgba(0,0,0,0.4);
}

/* ===== TABLA ===== */
div[data-testid="stDataFrame"] {
    background-color: #1C1C1C;
    border-radius: 10px;
}

/* ===== BOTONES ===== */
button[kind="primary"] {
    background-color: #1AA34A !important;
    border: none !important;
    border-radius: 8px;
}

button[kind="secondary"] {
    background-color: #2A2A2A !important;
    border-radius: 8px;
}

/* ===== SCROLLBAR ===== */
::-webkit-scrollbar {
    width: 8px;
}
::-webkit-scrollbar-thumb {
    background: #1AA34A;
    border-radius: 10px;
}

/* ===== GRÁFICAS MATPLOTLIB ===== */
figure {
    background-color: #1C1C1C !important;
    border-radius: 10px;
    padding: 10px;
}

</style>
""", unsafe_allow_html=True)

plt.style.use("dark_background")

SPOTIFY_GREEN = "#2FCA65"

st.title("🎧 Spotify Music Analytics") 
st.caption("Explora tendencias, artistas y popularidad")

# CARGAR DATA
@st.cache_data
def load_data():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(BASE_DIR, "data", "spotify.csv")

    df = pd.read_csv(
        file_path,
        sep=";",
        parse_dates=["album_release_date"],
        dayfirst=True
    )
    return df

df = load_data()

# LIMPIAR COLUMNAS
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

df["release_year"] = df["album_release_date"].dt.year
df["year_month"] = df["album_release_date"].dt.to_period("M").dt.to_timestamp()

# SIDEBAR
st.sidebar.header("🎛 Filtros")

artistas = st.sidebar.multiselect(
    "Artista",
    sorted(df["artist_name"].dropna().unique()),
    default=sorted(df["artist_name"].dropna().unique())
)

album_type = st.sidebar.multiselect(
    "Tipo de Álbum",
    sorted(df["album_type"].dropna().unique()),
    default=sorted(df["album_type"].dropna().unique())
)

pop_range = st.sidebar.slider("Rango de Popularidad", 0, 100, (0, 100))

anio_range = st.sidebar.slider(
    "Año",
    int(df["release_year"].min()),
    int(df["release_year"].max()),
    (int(df["release_year"].min()), int(df["release_year"].max()))
)

df_filtrado = df[
    (df["artist_name"].isin(artistas)) &
    (df["album_type"].isin(album_type)) &
    (df["track_popularity"].between(pop_range[0], pop_range[1])) &
    (df["release_year"].between(anio_range[0], anio_range[1]))
]

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["📊 KPIs", "📈 Gráficos", "🎧 Perfil Artista", "📋 Tabla", "🔍Curiosidades"]
)

# TAB 1 - KPIs
with tab1:
    st.subheader("📊 Métricas Principales")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("⭐ Popularidad Promedio", round(df_filtrado["track_popularity"].mean(), 2))
    col2.metric("🎤 Total Artistas", df_filtrado["artist_name"].nunique())
    col3.metric("⏱ Duración Promedio", f"{round(df_filtrado['track_duration_min'].mean(),2)} min")
    col4.metric("🎵 Total Canciones", len(df_filtrado))

# TAB 2 - GRÁFICOS
with tab2:

      if len(df_filtrado) > 0:

        st.subheader("🔥 Top 10 Artistas Más Populares")

        top_artistas = (
            df_filtrado.groupby("artist_name")["artist_popularity"]
            .mean()
            .sort_values(ascending=False)
            .head(10)
        )

        fig1, ax1 = plt.subplots(figsize=(10, 6))

        ax1.bar(
            top_artistas.index,
            top_artistas.values,
            color="#1AA34A"
        )

        ax1.set_title("Top 10 Artistas por Popularidad Promedio")
        ax1.set_xlabel("Artista")
        ax1.set_ylabel("Popularidad Promedio")
        plt.xticks(rotation=45)

        st.pyplot(fig1)

        # ---- Duración ----
        st.subheader("⏱ Popularidad Promedio por Rango de Duración")

        df_temp = df_filtrado.copy()

        df_temp["duracion_grupo"] = pd.cut(
            df_temp["track_duration_min"],
            bins=[0, 3, 4, 5, float("inf")],
            labels=["0-3 min", "3-4 min", "4-5 min", "5+ min"]
        )

        duracion_pop = (
            df_temp.groupby("duracion_grupo")["track_popularity"]
            .mean()
            .reset_index()
        )

        fig3, ax3 = plt.subplots(figsize=(8, 5))

        ax3.bar(
         duracion_pop["duracion_grupo"],
         duracion_pop["track_popularity"],
         color="#1AA34A"
        )
 
        ax3.set_title("Popularidad Promedio por Rango de Duración")
        ax3.set_xlabel("Rango de Duración")
        ax3.set_ylabel("Popularidad Promedio")

        plt.xticks(rotation=30)

        st.pyplot(fig3)

        # ---- Popularidad por Año y Tipo ----
        st.subheader("📊 Popularidad Promedio por Año y Tipo de Álbum")

        promedio_anual = (
            df_filtrado.groupby(["release_year", "album_type"])["track_popularity"]
            .mean()
            .reset_index()
            .sort_values("release_year")
        )

        fig2, ax2 = plt.subplots(figsize=(12, 6))

        tipos = promedio_anual["album_type"].unique()
        años = sorted(promedio_anual["release_year"].unique())

        ancho = 0.25
        posiciones = range(len(años))

        colores = ['#1DB954', "#6DBB88", "#1A5832"]

        for i, tipo in enumerate(tipos):
            datos_tipo = promedio_anual[
                promedio_anual["album_type"] == tipo
            ]

            valores = [
                datos_tipo[datos_tipo["release_year"] == año]["track_popularity"].values[0]
                if año in datos_tipo["release_year"].values else 0
                for año in años
            ]

            ax2.bar(
                [p + i * ancho for p in posiciones],
                valores,
                width=ancho,
                label=tipo,
                color=colores[i % len(colores)]
                
            )

        ax2.set_xticks([p + ancho for p in posiciones])
        ax2.set_xticklabels(años, rotation=45)
        ax2.set_xlabel("Año")
        ax2.set_ylabel("Popularidad Promedio")
        ax2.set_title("Comparación de Popularidad por Tipo de Álbum")
        ax2.legend(title="Tipo de Álbum")

        st.pyplot(fig2)

      else: 
        st.warning("No hay datos con los filtros seleccionados.")

# TAB 3 - PERFIL ARTISTA
with tab3:

    if len(df_filtrado) > 0:

        artista = st.selectbox(
            "Selecciona un artista",
            sorted(df_filtrado["artist_name"].unique())
        )

        df_artista = df_filtrado[df_filtrado["artist_name"] == artista]

        col1, col2, col3 = st.columns(3)

        col1.metric("⭐ Popularidad Promedio",
                    round(df_artista["artist_popularity"].mean(), 2))
        col2.metric("🎵 Número de Canciones",
                    df_artista["track_name"].nunique())
        col3.metric("💿 Álbum Más Frecuente",
                    df_artista["album_type"].mode()[0])

        top_song = df_artista.loc[df_artista["track_popularity"].idxmax()]

        st.success(
            f"🎶 Canción más popular: {top_song['track_name']} "
            f"(Popularidad: {top_song['track_popularity']})"
        )

# TAB 4 - TABLA
with tab4:

    st.subheader("📄 Lista de canciones")

    tabla = df_filtrado[[
        "album_release_date",
        "artist_name",
        "artist_popularity",
        "track_duration_min"
    ]].copy()

    tabla.columns = [
        "Fecha Lanzamiento",
        "Artista",
        "Popularidad",
        "Duración (min)"
    ]

    st.dataframe(tabla, use_container_width=True)

# TAB 5 - CURIOSIDADES
with tab5:


    st.markdown("## 🎵 ¿Sabías que...?")

    if len(df_filtrado) > 0:

        # 🎶 Canción más popular
        top_song = df_filtrado.loc[df_filtrado["track_popularity"].idxmax()]

        st.success(
            f"La canción más popular es: "
            f"{top_song['track_name']} - {top_song['artist_name']} "
            f"(Popularidad: {top_song['track_popularity']})"
        )

    if len(df_filtrado) > 0:

        col1, col2 = st.columns(2)

        # 🎤 Artista más constante
        artista_constante = df_filtrado["artist_name"].value_counts().idxmax()
        total_canciones = df_filtrado["artist_name"].value_counts().max()

        col1.success(
            f"🎤 **{artista_constante}** es el artista más constante "
            f"con **{total_canciones} canciones** en el dataset."
        )

        # 📅 Año más popular
        anio_top = (
            df_filtrado.groupby("release_year")["track_popularity"]
            .mean()
            .idxmax()
        )

        col2.info(
            f"📅 El año con mayor popularidad promedio fue **{anio_top}**."
        )

        st.divider()

        col3, col4 = st.columns(2)

        # 💿 Tipo de álbum más exitoso
        tipo_top = (
            df_filtrado.groupby("album_type")["track_popularity"]
            .mean()
            .idxmax()
        )

        col3.warning(
            f"💿 El tipo de álbum más exitoso es **{tipo_top}**."
        )

        # 👑 Artista con mayor popularidad promedio
        artista_top = (
            df_filtrado.groupby("artist_name")["artist_popularity"]
            .mean()
            .idxmax()
        )

        col4.success(
            f"👑 El artista con mayor popularidad promedio es **{artista_top}**."
        )

        st.divider()

        # 🔥 Canción más popular
        top_song = df_filtrado.loc[df_filtrado["track_popularity"].idxmax()]

        st.markdown(
            f"""
            ### 🔥 Hit del Dataset  
            🎶 **{top_song['track_name']}**  
            🎤 {top_song['artist_name']}  
            ⭐ Popularidad: **{top_song['track_popularity']}**
            """
        )

    else:
        st.warning("No hay datos con los filtros seleccionados.")