import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from corr import *
from module_selection import *
from radial_plot import *
from mapa import *
from donut import *
sns.set()

url = 'https://raw.githubusercontent.com/jlmarrugom/covid/main/data/BDcomunitarioSeroprevalencia.csv'
df = pd.read_csv(url,error_bad_lines=False,index_col=0)
df['RESULTADO SEROLOGIA'] = df['RESULTADO SEROLOGIA'].replace({'2':0,
                                                                'POSITIVO':1,
                                                                'NEGATIVO':0,
                                                                'Pendiente':np.nan}).astype(float)
url2 = 'https://raw.githubusercontent.com/jlmarrugom/covid/main/data/pat_df2021GATEWAY.csv'
df_pcr = pd.read_csv(url2,error_bad_lines=False,index_col=0)

url3 = 'https://raw.githubusercontent.com/jlmarrugom/covid/main/data/BasedeDatosMurcielagosC%C3%B3rdoba_Dic2020.csv'
df_mur = pd.read_csv(url3,error_bad_lines=False,index_col=0)
df_mur['Coordenadas'] = df_mur['lat'].astype(str) + ', '+df_mur['lon'].astype(str)

#print(df.head(3)) 
#for the correlation:
# data = module_selection(df,1).loc[:,'HA ESTADO ENFERMO A HA TENIDO SÍNTOMAS LOS ÚLTIMOS TRES MESES':'DIARREA'].copy(deep=True)#iloc con numeros, loc con nombres
# data = data.replace({2:0,3:np.nan})
# corr = data.corr()

# plt.figure(figsize=(10, 10))
# corrplot(corr)
# plt.show()

fig1 = radial_plot(df)
#mapping_df(mun_to_coord(df))#generar el mapa html en folium
# fig3 = donut_plot(df_mur,'Lugar')

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

external_stylesheets =['https://codepen.io/chriddyp/pen/dZVMbK.css']# ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(children=[
    html.Div([
        html.Div([
            html.H1(children='ControlBox'),
            html.P('Sistema de información para la caracterización, identificación, información, y previsión de riesgo de contagio por covid-19.'),
            html.Div(children='''
                En este es el Dashboard puede encontrar
                toda la información relacionada al proyecto
                ControlBox
            '''),
           
        ], className='row'),

        html.Div([
            html.H3(children='Síntomas'),
            html.Div(children='''
                Dash: A web application framework for Python.
            '''),
            dcc.Graph(
                id='graph1',
                figure=fig1)
                ],className='six columns'),
        html.Div([
            html.H3(children='Mapa de Pruebas'),
            html.P('Prueba:'),
            dcc.Dropdown(
                id='prueba',
                value='Serologia',
                options=[{'value':x, 'label':x}
                        for x in ['PCR','Serologia']],
                clearable=False   
            ),
            html.Iframe(id='map',#graficamos el mapa como un Iframe
            srcDoc=open('Serologia_por_municipios.html','r').read(),width='90%',height='400')
                ],className = 'six columns'),
        ], className = 'row'),
        html.Div([
            html.H3(children='Murcielagos'),

            html.Div(children='''
                Murcielagos
            '''),
            html.P('Variable:'),
            dcc.Dropdown(
                id='variables',
                value='Lugar',
                options=[{'value':x, 'label':x}
                        for x in df_mur.columns[2:8]],
                clearable=False   
            ),
            dcc.Graph(
                id='donut_chart',
                #figure=fig3
            ),  
        ], className='row'),
])
@app.callback(
    Output('map','srcDoc'),
    [Input('prueba','value')]
)
def generate_map(prueba):
    if prueba=='Serologia':
        mapping_df(mun_to_coord(df),prueba)
    else:
        mapping_df(mun_to_coord(df_pcr),prueba)
    return open('prueba_por_municipios.html','r').read()

@app.callback(
    Output('donut_chart','figure'),
    [Input('variables','value')]
)
def generate_donut(variables):
    fig3 = donut_plot(df_mur,str(variables))
    return fig3


if __name__ == '__main__':
    app.run_server(debug=False, use_reloader=False)