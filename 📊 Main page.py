# bibliotecas 
import pandas as pd
import haversine 
import plotly.express as px
import plotly.graph_objects as go
import streamlit  as st
import datetime as dt
from PIL import Image
import folium
from folium.plugins import MarkerCluster, FastMarkerCluster
from streamlit_folium import folium_static
import numpy as np
import inflection

st.set_page_config(page_title='Main page', page_icon='📊', layout='wide')

# ====================================================
# Import dataset
# ====================================================
df_raw = pd.read_csv('zomato.csv')

# Fazendo uma cópia do dataframe lido:
df = df_raw.copy()

# ====================================================
# Funções
# ====================================================

def clean_code(df):    
    """ Esta função tem a responsabilidade de limpar o dataframe

        Tipos de limpeza:
        1. Remoçao dos dados NaN
        2. Mudança do tipo de coluna de dados 
        3. Remoçao dos espaços das variáveis de texto
        4. Formatação da coluna de datas e etc 
    
        Input: Dataframe
        Output: Dataframe
    """
    # Remoção da coluna 'Switch to order menu' que estava vazia
    df = df.drop('Switch to order menu', axis=1)

    # Renomeando colunas
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(' ', '')
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new

    # Criando nova coluna com apenas o primeiro tipo de culinária de cada restaurante   
    df['cuisines'] = df['cuisines'].astype('str')
    df['first_cuisines'] = df.cuisines.apply(lambda x: x.split(',')[0])

    # Criando uma nova coluna com a quantidade de tipos de culinária
    df['num_of_cuisines'] = df.cuisines.apply(lambda x: len(x.split(',')))

    # Criando nova coluna com o nome dos países
    COUNTRIES = {
    1: 'India',
    14: 'Australia',
    30: 'Brazil',
    37: 'Canada',
    94: 'Indonesia',
    148: 'New Zeland',
    162: 'Philippines',
    166: 'Qatar',
    184: 'Singapure',
    189: 'South Africa',
    191: 'Sri Lanka',
    208: 'Turkey',
    214: 'United Arab Emirates',
    215: 'England',
    216: 'United States of America',
    }
    
    df['country_name'] = df['country_code'].map(COUNTRIES)

    # Criar coluna de tag do range do preço
    
    df['price_range'] = df['price_range'].astype('int')

    PRICE_TAGS = {
    1: 'cheap',
    2: 'normal',
    3: 'expensive',
    4: 'gourmet'
    }

    df['price_tag'] = df['price_range'].map(PRICE_TAGS)

    # Criando colunas de conversão dos preços para Reais e Dolares (Criar botão na barra lateral)

    df['average_cost_for_two'] = df['average_cost_for_two'].astype('float')

    CURRENCIES_TO_REAL = {
    'Botswana Pula(P)': 0.36,
    'Brazilian Real(R$)': 1,
    'Dollar($)': 4.98,
    'Emirati Diram(AED)': 0.74,
    'Indian Rupees(Rs.)': 0.060,
    'Indonesian Rupiah(IDR)': 0.00032,
    'NewZealand($)': 3.08,
    'Pounds(£)': 6.30,
    'Qatari Rial(QR)': 1.37,
    'Rand(R)': 0.26,
    'Sri Lankan Rupee(LKR)': 0.016,
    'Turkish Lira(TL)': 0.16
    }

    df['currencies_to_real'] = df['currency'].map(CURRENCIES_TO_REAL)
    df['average_cost_for_two_real'] = df.apply(lambda row: row['average_cost_for_two'] * row['currencies_to_real'], axis=1)

    CURRENCIES_TO_DOLAR = {
    'Botswana Pula(P)': 0.073,
    'Brazilian Real(R$)': 0.20,
    'Dollar($)': 1,
    'Emirati Diram(AED)': 0.27,
    'Indian Rupees(Rs.)': 0.012,
    'Indonesian Rupiah(IDR)': 0.000064,
    'NewZealand($)': 0.62,
    'Pounds(£)': 1.27,
    'Qatari Rial(QR)': 0.27,
    'Rand(R)': 0.052,
    'Sri Lankan Rupee(LKR)': 0.0032,
    'Turkish Lira(TL)': 0.032
    }

    df['currencies_to_dolar'] = df['currency'].map(CURRENCIES_TO_DOLAR)   
    df['average_cost_for_two_dolar'] = df.apply(lambda row: row['average_cost_for_two'] * row['currencies_to_dolar'], axis=1)


    # Função para renomear as cores
    
    COLORS = {
    "3F7E00": "darkgreen",
    "5BA829": "green",
    "9ACD32": "lightgreen",
    "CDD614": "orange",
    "FFBA00": "red",
    "CBCBC8": "darkred",
    "FF7800": "darkred",
    }
    
    df['rating_color_name'] = df['rating_color'].map(COLORS)

    # Criação coluna quantidade de filiais cada restaturante
    # df['qtde_restaurants'] = df.restaurant_id.apply(lambda x: x.count(x))
    
    return df

# Desenhando mapa da página principal

def country_map(df):
    # # Separando linhas e colunas
    cols = ['longitude', 'latitude', 'rating_color_name', 'restaurant_name','average_cost_for_two','first_cuisines','aggregate_rating','currency','country_name']
    df_aux = df.loc[:, cols]
    
    # Desenhando o map
    map = folium.Map(location=[0, 0], zoom_start=2)
    
    # Agrupamento dos pontos em bolinhas
    marker_cluster = MarkerCluster().add_to(map)

    # Adicionar marcadores com popups personalizados
    for idx, row in df_aux.iterrows():
        color = (row['rating_color_name'])
        popup_text = (f"<b>{row['restaurant_name']}</b><br><br>Preço: {row['average_cost_for_two']} {row['currency']} para dois <br> País: {row['country_name']}<br>Tipo de culinária: {row['first_cuisines']}<br>Avaliações: {row['aggregate_rating']}")
        folium.Marker(location=[row['latitude'], row['longitude']], icon=folium.Icon(color=color, icon='home'), popup=popup_text).add_to(marker_cluster)

    folium_static(map, width=1024, height=600)
    
    # Agrupamento dos pontos em polígonos
    #fast_marker_cluster = FastMarkerCluster(data=list(zip(df['latitude'], df['longitude']))).add_to(map)

def columns_types(df):
    df_aux = df.loc[1, :]
    df_aux = df_aux.reset_index()
    df_aux.columns = ['columns_name','columns_examples']
    lista= []
    for i in df_aux['columns_examples']:
        tipo = type(i)
        lista.append(tipo)
    df_aux['columns_type'] = lista
    df_aux = df_aux.loc[:, ['columns_name','columns_type']]
    
    return df_aux

def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

# ============ Inicio estrutura lógica ===============
# ====================================================
# Limpando os dados
# ====================================================

df = clean_code(df)

# ====================================================
# Inicio códigos Streamlit
# ====================================================

# ====================================================
# Barra Lateral Streamlit
# ====================================================


with st.sidebar.container():
    
    with st.sidebar.container():

        # Informações barra lateral
        st.sidebar.write('# Fome Zero')
        # Imagem da barra lateral
        image = Image.open('logo.png')
        st.sidebar.image(image, width=80)
        st.sidebar.markdown("""---""")   

            
    with st.sidebar.container():
        
        #Filtro dos países
        st.sidebar.markdown('### Filtros')
        
        countries_list = list(df.loc[:,'country_name'].unique())
        countries = st.sidebar.multiselect('Escolha os Paises que Deseja visualizar os Restaurantes',
        countries_list, default=countries_list)
        
        linhas_selecionadas = df['country_name'].isin(countries)
        df = df.loc[linhas_selecionadas, :]
        
        st.sidebar.markdown("""---""")    


    with st.sidebar.container():
        
         # Criar botão de baixar os dados
        st.sidebar.markdown(' ### Dados Tratados')

        csv = convert_df(df)
        
        st.sidebar.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='df.csv',
            mime='text/csv',
        )

        
       
        
        st.sidebar.markdown("""---""")    
        st.sidebar.markdown(' ### Powered by DS')

# ====================================================
# Layout Sreamlit
# ====================================================

st.markdown(' # Projeto Fome Zero')
st.markdown('###### Fonte: Zomato Restaurants - Autoupdated dataset - Kaggle Dataset')
st.markdown("""---""")   
st.markdown('#### Temos as seguintes marcas dentro da nossa plataforma:') 

with st.container():
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    # Geral
    with col1:
        # 1. Quantos restaurantes únicos estão registrados?
        restaurants = df.loc[:,'restaurant_id'].nunique()
        col1.metric('Restaurantes Cadastrados', restaurants)
    
    with col2:
        # 2. Quantos países únicos estão registrados?
        countries = df.loc[:,'country_name'].nunique()
        col2.metric('Países Cadastrados', countries)
    
    with col3:
        # 3. Quantas cidades únicas estão registradas?
        cities = df.loc[:,'city'].nunique()
        col3.metric('Cidades Cadastradas', cities)
    
    with col4:
        # 4. Qual o total de avaliações feitas? Soma da coluna 'Votes'
        ratings = df.loc[:,'votes'].sum()
        col4.metric('Avaliações Realizadas', ratings)
    
    with col5:
        # 5. Qual o total de tipos de culinária registrados? Realizar agrupamento por categorias (Limpeza)
        cuisines = df.loc[:,'first_cuisines'].nunique()
        col5.metric('Tipos de Culinárias', cuisines)

with st.container():
    # Mapa com as informações dos indicadores
    country_map(df)
