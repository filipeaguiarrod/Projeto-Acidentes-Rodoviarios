import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from geopy.geocoders import Nominatim
from math import sin, pi
import pickle
from PIL import Image



st.title('CrashIA')

image = Image.open('crashia.png')

st.image(image,use_column_width=True)

st.write('Com o CrashIA você pode passar a localização de um acidente rodoviário, tente passar o máximo de informações possíveis e a hora aproximada, e o CrashIA te passa a classificação do acidente.')

user_input = st.text_area("Localização do acidente, Exemplo: BR-101, Km 51 - Timbó, Abreu e Lima - PE")

try:

    # Busca no Nominatim qual é a latitude e longitude do ponto em questão.
    
    geolocator = Nominatim(user_agent="Acidente")
    location = geolocator.geocode(user_input)
    
    # Desenha pro usuario onde é o ponto em questão até pra ele saber se é o ponto esperado
    
    lat = location.latitude
    lon = location.longitude
    
    map_data = pd.DataFrame({'lat': [lat], 'lon': [lon]})
    
    st.map(map_data) 
    
    st.write('latitude:',lat,'longitude:',lon)

except:
    
    pass

# Coleta do horário do acidente e transformação em horario_sin

user_input_2 = st.text_area("Horário do Acidente - Formato (HH:MM)")

try:
    
    # Trabalhar na transformação para float:!!!!!!!!!
    
    list_h = user_input_2.split(':') # Cria lista com Hora, Minuto
    hor_flt = float(list_h[0]) + float(list_h[1])/60 # Transforma hora e minuto em um float
    horario_sin=np.sin(2.*np.pi*hor_flt/24.) # Transforma o horário em sin.
    
    #st.write(horario_sin)
    
except:
    
    pass

# Criando Dataframe que será utilizado no modelo de ML:

# df = horario_sin	latitude	longitude

try:
          
    df = pd.DataFrame({'horario_sin':[horario_sin],'latitude':[lat],'longitude':[lon]})
    
except:
    
    pass

# Alimentando o modelo com os dados

try:

    model = pickle.load(open('finalized_model.sav', 'rb'))
    result = model.predict(df)
    
    st.write('A previsão de gravidade para o acidente é:',result)
    
except:
    
    pass
