import numpy as np
import pandas as pd
import plotly.graph_objects as go

def donut_plot(bats,bw):
    """
    bw: string con nombre de la columna.
    Recibe un Dataframe y la columna bw,
    agrupa los datos respecto a bw, hace el conteo
    y grafica una donut.
    """
    bats = bats[['Conteo',bw]].groupby(bw).sum().sort_values(by='Conteo',ascending=False)

    labels = bats.index
    values = bats['Conteo']

    fig = go.Figure(
        data=[go.Pie(
            labels=labels,
            values=values,
            hole=.5
        )]
    )
    return fig

# url2 = 'https://raw.githubusercontent.com/jlmarrugom/covid/main/data/BasedeDatosMurcielagosC%C3%B3rdoba_Dic2020.csv'
# df_mur = pd.read_csv(url2,error_bad_lines=False,index_col=0)

# donut_plot(df_mur,'Lugar').show()