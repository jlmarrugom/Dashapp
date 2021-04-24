import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from corr import *
from module_selection import *
from radial_plot import *
from mapa import *
sns.set()

url = 'https://raw.githubusercontent.com/jlmarrugom/covid/main/data/BDcomunitarioSeroprevalencia.csv'
df = pd.read_csv(url,error_bad_lines=False,index_col=0)
df['RESULTADO SEROLOGIA'] = df['RESULTADO SEROLOGIA'].replace({'2':0,
                                                                'POSITIVO':1,
                                                                'NEGATIVO':0,
                                                                'Pendiente':np.nan}).astype(float)


#print(df.head(3)) 
#for the correlation:
# data = module_selection(df,1).loc[:,'HA ESTADO ENFERMO A HA TENIDO SÍNTOMAS LOS ÚLTIMOS TRES MESES':'DIARREA'].copy(deep=True)#iloc con numeros, loc con nombres
# data = data.replace({2:0,3:np.nan})
# corr = data.corr()

# plt.figure(figsize=(10, 10))
# corrplot(corr)
# plt.show()

fig1 = radial_plot(df)
mapping_df(mun_to_coord(df))#generar el mapa html en folium

import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets =['https://codepen.io/chriddyp/pen/dZVMbK.css']# ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(children=[
    html.Div([
        html.Div([
            html.H1(children='Hello Dash'),
            html.Div(children='''
                Dash: A web application framework for Python.
            '''),
            dcc.Graph(
                id='graph1',
                figure=fig1)
                ],className='six columns'),
        html.Div([
            html.H1(children='Mapa Serología'),
            html.Div(children='''
                Dash: A web application framework for Python.
            '''),
            html.Iframe(id='map',#graficamos el mapa como un Iframe
            srcDoc=open('serologia_por_municipios.html','r').read(),width='100%',height='400')
                ],className = 'six columns'),
        ], className = 'row'),
        html.Div([
            html.H1(children='Hello Dash 3'),

            html.Div(children='''
                Dash: A web application framework for Python.
            '''),

            dcc.Graph(
                id='graph3',
                figure=fig1
            ),  
        ], className='row'),
])
if __name__ == '__main__':
    app.run_server(debug=False, use_reloader=False)