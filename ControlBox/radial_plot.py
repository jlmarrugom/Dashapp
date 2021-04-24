
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from module_selection import *


def radial_plot(df):
    data = module_selection(df,1).copy(deep=True) #Info básica
    data.loc[:,'HA ESTADO ENFERMO A HA TENIDO SÍNTOMAS LOS ÚLTIMOS TRES MESES':'DIARREA'] = data.loc[:,'HA ESTADO ENFERMO A HA TENIDO SÍNTOMAS LOS ÚLTIMOS TRES MESES':'DIARREA'].replace({2:0,3:np.nan}) #Cambio según la convención 0: No, 1 Sí
    #Seleccionamos sólo personas con síntomas:
    data = data.loc[data['HA ESTADO ENFERMO A HA TENIDO SÍNTOMAS LOS ÚLTIMOS TRES MESES']!=0].dropna() #los nan bajan el promedio
    data = data.groupby('MUNICIPIO').mean() #Agrupamos el promedio de cada síntoma por municipio

    #Radial plot
    data = data.loc[:,'TOS':'DIARREA']

    categories = ['TOS','DIFICULTAD PARA RESPIRAR','FATIGA','DOLORES MUSCULARES Y CORPORALES',
                'DOLOR DE CABEZA','PERDIDAD DEL OLFATO O DEL GUSTO','DOLOR DE GARGANTA',
                'CONGESTION DE LA NARIZ','NÁUSEAS O VÓMITOS','DIARREA']

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=data.iloc[0],
        theta=categories,
        name='Lorica'
    ))
    fig.add_trace(go.Scatterpolar(
        r=data.iloc[1],
        theta=categories,

        name='Planeta Rica'
    ))
    fig.add_trace(go.Scatterpolar(
        r=data.iloc[2],
        theta=categories,
        name='Montelibano'
        ))
    fig.add_trace(go.Scatterpolar(
        r=data.iloc[3],
        theta=categories,
        name='Tierralta'
        ))
    fig.add_trace(go.Scatterpolar(
        r=data.iloc[4],
        theta=categories,
        name='Monteria'
        ))
    fig.add_trace(go.Scatterpolar(
        r=data.iloc[5],
        theta=categories,
        name='Sahagún'
        ))

    fig.update_layout(
    polar=dict(
        radialaxis=dict(
        visible=True,
        range=[0, 1]
        )),
    showlegend=True
    )

    fig.update_layout(
        title={
            'text': "Sintomas por Municipio",
            'y':0.95,
            'x':0.45,
            'xanchor': 'center',
            'yanchor': 'top'}
        # legend=dict(
        # yanchor="top",
        # y=0.99,
        # xanchor="left",
        # x=0.10)
    )

    #fig.show()
    return fig