import pandas as pd
def module_selection(data,number):
  """
  Selector de modulo de los datos. Entrega DataFrame.
  1. Info Básica.
  2. Actitudes con enfermos o asintomáticos con COVID-19
  3. Prácticas sobre COVID-19.
  4. Percepción sobre la pandemia.				
  5. Situación laboral y social.				
  6. Conocimiento sobre COVID-19.				
  """
  if number==1:
    return data.loc[:,'COD':'EN CASO DE HABER TOMADO MEDICAMENTOS CUÁLES TOMÓ?']
  elif number==2:
    return data.loc[:,'ALGUIEN EN LA FAMILIA O USTED A SIDO REPORTADO COMO ENFERMO DE COVID-19?':'USAN MASCARILLAS O CARETAS DENTRO DE LA VIVIENDA']
  elif number==3:
    return data.loc[:,'DURANTE LA PANDEMIA ME HE QUEDADO EN CASA':'OTRO CUAL?']
  elif number==4:
    return data.loc[:,'YO CREO QUE?':'ME HABRIA AISLADO VOLUNTARIAMENTE']
  elif number==5:
    return data.loc[:,'PERDÍ MI TRABAJO':'1 CAMBIÉ TENGO MÁS INGRESOS']
  elif number==6:
    return data.loc[:,'¿LA COVID -19 ES?':'DISTANCIAMIENTO SOCIAL']
  else:
    return data.loc[:,'CÓDIGO':]