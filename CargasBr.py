from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)

server = app.server

file='CargasBrasil.xlsx'
df_expo=pd.read_excel(file,'Exportações')
fig = px.scatter_geo(
    df_expo,
    lat = df_expo['Latitude'],
    lon = df_expo['Longitude'],
    color = df_expo['Classe'],
    size = df_expo['Quantidade'],
    animation_frame = df_expo['Data (Mês)'],
    projection="equirectangular")
opcoes = list(df_expo['Classe'].unique())
opcoes.append("Todas as Classes")
app.layout = html.Div(children=[
    html.H1(children='Mapa de cargas do Brasil'),
    html.H2(children='Descrever'),
    dcc.Dropdown(opcoes,value='Todas as Classes',id='lista_classes'),
    dcc.Graph(
        id='grafico_mapa',
        figure=fig
    )
])

@app.callback(
    Output ('grafico_mapa','figure'),
    Input ('lista_classes','value'), prevent_initial_call=True
)
def update_output(value):
    if value == ("Todas as Classes"):
        fig= px.scatter_geo(
        df_expo,
        lat = df_expo['Latitude'],
        lon = df_expo['Longitude'],
        color = df_expo['Classe'],
        size = df_expo['Quantidade'],
        animation_frame = df_expo['Data (Mês)'],
        projection="equirectangular")
    else:
        df_expo_filtrada = df_expo.loc[df_expo['Classe']==value]
        #df_expo_filtrada.show()
        fig= px.scatter_geo(
        df_expo_filtrada,
        lat = df_expo_filtrada['Latitude'],
        lon = df_expo_filtrada['Longitude'],
        color = df_expo_filtrada['Classe'],
        size = df_expo_filtrada['Quantidade'],
        animation_frame = df_expo_filtrada['Data (Mês)'],
        projection="equirectangular")
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)