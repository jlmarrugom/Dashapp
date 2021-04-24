import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

def mun_to_coord(full_ser):
    """
    Recibe un Dataframe con municipios,
     añade sus coordenadas
    y regresa un Dataframe.
    """
    full_ser['MUNICIPIO'] = full_ser['MUNICIPIO'].astype(object).replace({1:'Lorica',
                                                                    2:'Planeta Rica',
                                                                    3:'Tierralta',
                                                                    4:'Sahagun',
                                                                    5:'Montelibano',
                                                                    6:'Montería'})

    full_ser['lat']=0
    full_ser['lon']=0

    full_ser['lat'].loc[full_ser['MUNICIPIO']=='Monteria'] = 8.7558921
    full_ser['lon'].loc[full_ser['MUNICIPIO']=='Monteria'] = -75.887029

    full_ser['lat'].loc[full_ser['MUNICIPIO']=='Lorica'] = 9.2394583
    full_ser['lon'].loc[full_ser['MUNICIPIO']=='Lorica'] = -75.8139786

    full_ser['lat'].loc[full_ser['MUNICIPIO']=='Planeta Rica'] = 8.4076739 
    full_ser['lon'].loc[full_ser['MUNICIPIO']=='Planeta Rica'] = -75.5840456 

    full_ser['lat'].loc[full_ser['MUNICIPIO']=='Tierralta'] = 8.1717342
    full_ser['lon'].loc[full_ser['MUNICIPIO']=='Tierralta'] = -76.059376

    full_ser['lat'].loc[full_ser['MUNICIPIO']=='Sahagun'] = 8.9472964
    full_ser['lon'].loc[full_ser['MUNICIPIO']=='Sahagun'] = -75.4434972

    full_ser['lat'].loc[full_ser['MUNICIPIO']=='Montelibano'] = 7.9800534
    full_ser['lon'].loc[full_ser['MUNICIPIO']=='Montelibano'] = -75.4167198

    return full_ser

def mapping_df(full_ser):
    """
    Recibe un Dataframe con Coordenadas y lo grafica
    en un mapa. retorna una figura.
    """
    df = full_ser.copy(deep=True)
    df = df[['lat','lon','MUNICIPIO']].groupby('MUNICIPIO').max()

    df = df.merge(full_ser[['RESULTADO SEROLOGIA','MUNICIPIO']].loc[full_ser['RESULTADO SEROLOGIA']==1].groupby(['MUNICIPIO']).count() ,how='outer',on='MUNICIPIO')
    df = df.merge(full_ser[['RESULTADO SEROLOGIA','MUNICIPIO']].groupby(['MUNICIPIO']).count() ,how='inner',on='MUNICIPIO')

    #df = df.merge(full_ser[['RESULTADO PCR','MUNICIPIO']].loc[full_ser['RESULTADO PCR']=='POSITIVO'].groupby(['MUNICIPIO']).agg(lambda x:x.value_counts().index[0])
    df['VULNERABILIDAD (%)'] = round(100*(1-(df['RESULTADO SEROLOGIA_x']/df['RESULTADO SEROLOGIA_y'])))
    df = df.rename(columns={'RESULTADO SEROLOGIA_x':'POSITIVOS SEROLOGIA',
                            'RESULTADO SEROLOGIA_y':'No DE PRUEBAS SEROLOGIA'})
    df = df.reset_index()
    #Mapa:
    import folium

    folium_hmap = folium.Figure(width=500, height=500)
    m = folium.Map(location=[8.3344713,-75.6666238],
                            width='100%',
                            height='100%',
                            zoom_start=8,#Por defecto es 10
                            tiles="OpenStreetMap" #OpenSteetMap ,Stamen Toner(Terrain, Watercolor)
                            ).add_to(folium_hmap)

    data = df
    for i in range(0,len(data)):
        html = f"""
                <head>
                    <link rel="stylesheet" href="https://codepen.io/chriddyp/pen/dZVMbK.css">
                <head>
                <h4> {data.iloc[i]['MUNICIPIO']}</h3>
                <p> Serología: </p>
                <p>Positivas: {data.iloc[i]['POSITIVOS SEROLOGIA']}</p>
                <p> Total: {data.iloc[i]['No DE PRUEBAS SEROLOGIA']}</p>
                """
        iframe = folium.IFrame(html=html,width=160, height=160)
        popup = folium.Popup(iframe, max_width=2650)
        folium.Circle(
            location=[data.iloc[i]['lat'], data.iloc[i]['lon']],
            popup=popup,
            radius=float(data.iloc[i]['No DE PRUEBAS SEROLOGIA'])*100,
            color='lightgray',
            fill=True,
            fill_color='gray'
        ).add_to(m)

    for i in range(0,len(data)):
        html = f"""
                <head>
                    <link rel="stylesheet" href="https://codepen.io/chriddyp/pen/dZVMbK.css">
                <head>
                <h4> {data.iloc[i]['MUNICIPIO']}</h3>
                <p> Serología: </p>
                <p>Positivas: {data.iloc[i]['POSITIVOS SEROLOGIA']}</p>
                <p> Total: {data.iloc[i]['No DE PRUEBAS SEROLOGIA']}</p>
                """
        iframe = folium.IFrame(html=html,width=160, height=160)
        popup = folium.Popup(iframe, max_width=2650)
        folium.Circle(
            location=[data.iloc[i]['lat'], data.iloc[i]['lon']],
            popup=popup,
            radius=float(data.iloc[i]['POSITIVOS SEROLOGIA'])*100,
            color='cadetblue',
            fill=True,
            fill_color='blue'
        ).add_to(m)

    folium_hmap.save('serologia_por_municipios.html')

    return folium_hmap

# mapping_df(mun_to_coord(df))