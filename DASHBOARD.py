# Equipo:
# Víctor Emiliano Chávez Ortega | A01710270
# Mayahuetl Medina Chanes | A01276295
# Montserrat Ramírez Olguín | A01276161
# Yibriham Ali Iñiguez Arteaga | A01540614
# Rodrigo Esparza Salas | A01705841


from dash import Dash, dcc, html, Output, Input
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

#cargar datos 
df = pd.read_csv("spotify.csv")

spotify_palette = ["#1DB954", "#1ED760", "#191414", "#E9E3E3", "#D7DAE5"]

df_long = df.melt(id_vars="Date", var_name="Song", value_name="Streams")
df_long["Date"] = pd.to_datetime(df_long["Date"])

#graficas
def build_figures():
    figs = {}

    #Gráfica 1: Top 10 Canciones
    song_streams = df.drop(columns="Date").sum().reset_index()
    song_streams.columns = ["song_name", "total_streams"]
    top10 = song_streams.sort_values("total_streams", ascending=False).head(10)

    figs["Top 10 Canciones"] = px.bar(
        top10,
        x="song_name", y="total_streams",
        color="song_name",
        color_discrete_sequence=spotify_palette,
        title="Top 10 Canciones Más Populares"
    )

    #Gráfica 2: Relación Shape of You vs Despacito
    figs["Shape of You vs Despacito"] = px.scatter(
        df,
        x="Shape of You", y="Despacito",
        color="Shape of You",
        color_continuous_scale=spotify_palette,
        title="Relación entre Streams: Shape of You vs Despacito"
    )

    #Gráfica 3: Series de tiempo (Todas las canciones) 
    figs["Serie de Tiempo (Todas)"] = px.line(
        df_long,
        x="Date", y="Streams",
        color="Song",
        color_discrete_sequence=spotify_palette,
        title="Evolución de Streams por Canción"
    )

    #Gráfica 4:  Área por cancion
    figs["Área Apilada"] = px.area(
        df_long,
        x="Date", y="Streams",
        color="Song",
        color_discrete_sequence=spotify_palette,
        title="Contribución de Cada Canción al Total Diario"
    )

    #Gráfica 5: Shape of you
    shape_df = df_long[df_long["Song"] == "Shape of You"]
    figs["Shape of You (Serie)"] = px.line(
        shape_df,
        x="Date", y="Streams",
        markers=True,
        title="Streams Diarios de 'Shape of You'"
    )

    #Gráfica 6: despacito
    desp_df = df_long[df_long["Song"] == "Despacito"]
    figs["Despacito (Serie)"] = px.line(
        desp_df,
        x="Date", y="Streams",
        markers=True,
        title="Streams Diarios de 'Despacito'"
    )

    #Grafica 7: top 3 canciones
    top3 = ["Shape of You", "Despacito", "Something Just Like This"]
    df_top3 = df_long[df_long["Song"].isin(top3)]
    figs["Top 3 Canciones"] = px.line(
        df_top3,
        x="Date", y="Streams",
        color="Song",
        color_discrete_sequence=spotify_palette[:3],
        markers=True,
        title="Comparación de Streams de las Top 3 Canciones"
    )

    #grafica 8 heat map
    corr = df.drop(columns="Date").corr()
    figs["Mapa de Correlación"] = go.Figure(
        data=go.Heatmap(
            z=corr.values,
            x=corr.columns, y=corr.columns,
            colorscale="Greens"
        )
    )
    figs["Mapa de Correlación"].update_layout(title="Mapa de Correlación entre Canciones")

    #Grafica 9: histograma shape of you
    figs["Histograma Shape of You"] = px.histogram(
        shape_df,
        x="Streams",
        nbins=40,
        color_discrete_sequence=[spotify_palette[0]],
        title="Distribución de Streams - Shape of You"
    )

    #grafica 10: boxplot
    top5 = song_streams.sort_values("total_streams", ascending=False).head(5)["song_name"]
    df_top5 = df_long[df_long["Song"].isin(top5)]
    figs["Boxplot Top 5"] = px.box(
        df_top5,
        x="Song", y="Streams",
        color="Song",
        color_discrete_sequence=spotify_palette,
        title="Distribución de Streams de las 5 Canciones Más Populares"
    )

    return figs


figures = build_figures()

#descripciones con markdown 
descriptions = {
    "Top 10 Canciones": 
        "### Descripción\nEste gráfico presenta una comparación directa del total de streams acumulados por las diez canciones más reproducidas dentro del dataset.",
    "Shape of You vs Despacito": 
        "### Descripción\nEl gráfico de dispersión compara los streams de Shape of You y Despacito para cada día disponible en el dataset. Esta visualización revela si existe una relación entre ambas canciones en términos de popularidad diaria.",
    "Serie de Tiempo (Todas)": 
        "### Descripción\nEsta visualización de series de tiempo nos permite analizar el comportamiento que tiene cada canción a lo largo del periodo estudiado. Así podemos identificar claramente las fechas de lanzamiento, los picos máximos de popularidad y también como decae el interés de la audiencia para cada canción.",
    "Área Apilada": 
        "### Descripción\nEste gráfico de áreas apiladas lo que nos demuestra es una perspectiva macro del consumo musical. La altura total del gráfico representa la suma de reproducciones de todas las canciones combinadas día tras día, permitiendo ver si el consumo general aumentó o disminuyó en ciertas temporadas. Los colores dividen este total para mostrar la aportación o su comportamiento propio de cada canción, dejandonos ver así qué tema dominaba la plataforma en cada momento y cómo se distribuyó la atención de los usuarios entre los diferentes éxitos.",
    "Shape of You (Serie)": 
        "### Descripción\nEsta visualización se enfoca exclusivamente en la trayectoria temporal de streams para Shape of You. La inclusión de puntos en cada observación permite identificar cambios día por día con mayor precisión.",
    "Despacito (Serie)": 
        "### Descripción\nEsta gráfica analiza el comportamiento diario de los streams para Despacito, su visualización temporal facilita la identificación de patrones de consumo, permitiendo compararla con otras canciones para evaluar su estabilidad o volatilidad.",
    "Top 3 Canciones": 
        "### Descripción\nLa gráfica compara simultáneamente los streams diarios de Shape of You, Despacito y Something Just Like This. Al superponer las tres líneas, se vuelve sencillo evaluar cuál de ellas posee un mejor desempeño en un momento dado y cómo cambian.",
    "Mapa de Correlación": 
        "### Descripción\nEl heatmap muestra las correlaciones estadísticas entre las canciones del dataset. Un valor alto indica que las canciones tienden a aumentar y disminuir juntas en sus streams diarios; una correlación baja o negativa implica comportamientos independientes.",
    "Histograma Shape of You": 
        "### Descripción\nEste histograma representa la distribución completa de streams de Shape of You. Permite identificar si la mayoría de sus reproducciones se concentran en niveles bajos, medios o altos.",
    "Boxplot Top 5": 
        "### Descripción\nEste boxplot compara la variación de streams entre las cinco canciones más escuchadas del dataset. Permite identificar la mediana, la dispersión, los cuartiles y los valores atípicos para cada canción."
}

#dash layout
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Dashboard Spotify", style={"color": "#1DB954"}),

    dcc.Markdown("""
### **Equipo: **
- Víctor Emiliano Chávez Ortega | A01710270  
- Mayahuetl Medina Chanes | A01276295  
- Montserrat Ramírez Olguín | A01276161  
- Yibriham Ali Iñiguez Arteaga | A01540614  
- Rodrigo Esparza Salas | A01705841  

---
"""),

    dcc.Dropdown(
        id="selector",
        options=list(figures.keys()),
        value="Top 10 Canciones",
        clearable=False,
        style={"width": "60%"}
    ),

    html.H2(id="titulo_grafica", style={"marginTop": "20px"}),

    dcc.Graph(id="grafica"),

    dcc.Markdown(id="descripcion", style={"marginTop": "20px", "fontSize": 18})
])

#CALLBACKS paraActualizar título, gráfica y descripción

@app.callback(
    Output("titulo_grafica", "children"),
    Output("grafica", "figure"),
    Output("descripcion", "children"),
    Input("selector", "value")
)
def update_dashboard(selected):
    return selected, figures[selected], descriptions[selected]

#ejecutar
if __name__ == "__main__":
    app.run(debug=True)
