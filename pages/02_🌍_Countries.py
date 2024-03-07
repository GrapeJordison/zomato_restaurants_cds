# bibliotecas 
import pandas as pd
import haversine 
import plotly.express as px
import plotly.graph_objects as go
import streamlit  as st
import datetime as dt
from PIL import Image
import folium
from streamlit_folium import folium_static
import numpy as np
import inflection

st.set_page_config(page_title='Countries', page_icon='🌍', layout='wide')

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
    df['average_cost_for_two_real'] = np.round(df.apply(lambda row: row['average_cost_for_two'] * row['currencies_to_real'], axis=1), 2)

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
    df['average_cost_for_two_dolar'] = np.round(df.apply(lambda row: row['average_cost_for_two'] * row['currencies_to_dolar'], axis=1), 2)

    # Criando nova coluna com o nome das cores
    
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


# 1. Qual o nome do país que possui mais cidades registradas? 

def cities_by_country(df):
    
    df_aux = df.loc[:, ['country_name','city']].groupby('country_name').nunique().sort_values('city', ascending=False).reset_index()
    df_aux.columns=['Países', 'Quantidade de cidades']
    fig = px.bar(df_aux, x='Países', y='Quantidade de cidades', title='Cidades registradas por país', text_auto=True)
    
    return fig


# 2. Qual o nome do país que possui mais restaurantes registrados? 

def restaurants_by_country(df):
    
    df_aux = df.loc[:, ['country_name','restaurant_id']].groupby('country_name').nunique().sort_values('restaurant_id', ascending=False).reset_index()
    df_aux.columns=['Países', 'Quantidade de restaurantes']
    fig = px.bar(df_aux, x='Países', y='Quantidade de restaurantes', title='Restaurantes registrados por país', text_auto=True)
    
    return fig

# 3. Qual o nome do país que possui mais restaurantes com o nível de preço igual a 4 registrados?

def restaurants_by_country_price4(df):

    linhas_selecionadas = df['price_range'] == 4
    df_aux = df.loc[linhas_selecionadas, ['country_name','restaurant_id','price_range']].groupby('country_name').count().sort_values('restaurant_id', ascending=False).reset_index()
    df_aux.columns=['Países', 'Quantidade de restaurantes','Intervalo de Preço']
    fig = px.bar(df_aux, x='Países', y='Quantidade de restaurantes', title='Restaurantes registrados por país com nível de preço igual a 4', text_auto=True)
    
    return fig

# 4. Qual o nome do país que possui a maior quantidade de tipos de culinária distintos?

def cuisines_by_country(df):

    df_aux = df.loc[:, ['country_name','first_cuisines']].groupby('country_name').nunique().sort_values('first_cuisines', ascending=False).reset_index()
    df_aux.columns=['Países', 'Tipos de Culinária']
    fig = px.bar(df_aux, x='Países', y='Tipos de Culinária', title='Tipos de culinária distintos por país', text_auto=True)
    
    return fig

# 5. Qual o nome do país que possui a maior quantidade de avaliações feitas?

def rating_by_country(df):

    df_aux = df.loc[:, ['country_name','votes']].groupby('country_name').sum().sort_values('votes', ascending=False).reset_index()
    df_aux.columns=['Países', 'Quantidade de avaliações']
    fig = px.bar(df_aux, x='Países', y='Quantidade de avaliações', title='Quantidade de avaliações registradas por país', text_auto=True)
    
    return fig

# 6. Qual o nome do país que possui a maior quantidade de restaurantes que fazem entrega?

def delivery_restaurant_by_country(df):

    linhas_selecionadas = df['is_delivering_now'] == 1
    df_aux = df.loc[linhas_selecionadas, ['country_name','restaurant_id','is_delivering_now']].groupby('country_name').count().sort_values('restaurant_id', ascending=False).reset_index()
    df_aux.columns=['Países', 'Quantidade de restaurantes','Faz entregas']
    fig = px.bar(df_aux, x='Países', y='Quantidade de restaurantes', title='Restaurantes que fazem entrega por País', text_auto=True)
    
    return fig

# 7. Qual o nome do país que possui a maior quantidade de restaurantes que aceitam reservas?

def booking_restaurant_by_country(df):

    linhas_selecionadas = df['has_table_booking'] == 1
    df_aux = df.loc[linhas_selecionadas, ['country_name','restaurant_id','has_table_booking']].groupby('country_name').count().sort_values('restaurant_id', ascending=False).reset_index()
    df_aux.columns=['Países', 'Quantidade de restaurantes','Faz reservas']
    fig = px.bar(df_aux, x='Países', y='Quantidade de restaurantes',  title='Restaurantes que aceitam reservas por país', text_auto=True)
    
    return fig

# 8. Qual o nome do país que possui, na média, a maior quantidade de avaliações registradas?


def mean_votes_country(df):
    
    df_aux = df.loc[:, ['country_name','votes']].groupby('country_name').mean().sort_values('votes', ascending=False).reset_index()
    df_aux.columns=['Países', 'Quantidade de avaliações']
    fig = px.bar(df_aux, x='Países', y='Quantidade de avaliações', title='Média da quantidade avaliações registradas por país', text_auto=True)
    
    return fig

# 9. Qual o nome do país que possui, na média, a maior nota média registrada?

# 10. Qual o nome do país que possui, na média, a menor nota média registrada?

def mean_rating_country(df):
    
    df_aux = df.loc[:, ['country_name','aggregate_rating']].groupby('country_name').mean().sort_values('aggregate_rating', ascending=False).reset_index()
    df_aux.columns=['Países', 'Média das avaliações']
    fig = px.bar(df_aux, x='Países', y='Média das avaliações', title='Média das avaliações registradas por países', text_auto=True)
    
    return fig


# 11. Qual a média de preço de um prato para dois por país?

def mean_average_cost_for_two_dolar_country(df):
    # Informações do valor removido da média aparada > País: Austrália / Custo do prato para dois (dólar): 25,000,017 / ID do restaurante: 16,608,070
    lins= df['restaurant_id'] != 16608070
    df_aux = np.round(df.loc[lins, ['country_name','average_cost_for_two_dolar']].groupby('country_name').mean().sort_values('average_cost_for_two_dolar', ascending=False).reset_index(), 2)
    df_aux.columns=['Países', 'Custo do prato para dois']
    fig = px.bar(df_aux, x='Países', y='Custo do prato para dois', title='Média aparada de preço de um prato para dois por país (dólar)', text_auto=True)
    return fig


def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


# ============ Inicio estrutura lógica ===============
# ====================================================
# Limpando os dados
# ====================================================

df = clean_code(df)


# ====================================================
# Front-end CSS
# ====================================================


list_of_tables = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6']

# Add CSS styles for the containers
container_style = """
    <style>
        .container1 {
            border: 2px solid #3498db;
            border-radius: 8px;
            padding: 10px;
            margin-bottom: 20px;
        }
        .container2 {
            /* Add styles for Container 2 if needed */
        }
    </style>
"""

# ====================================================
# Inicio códigos Streamlit
# ====================================================

# ====================================================
# Barra Lateral Streamlit
# ====================================================

with st.sidebar.container():
           
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


# Países - Perguntas
st.header(' 🌍  Visão Países')
st.markdown("""---""")    

with st.container():
    col1, col2 = st.columns(2)

    with col1:    
        # 1. Qual o nome do país que possui mais cidades registradas?
        col1.plotly_chart(cities_by_country(df), use_content_width=True)

    with col2:
        # 2. Qual o nome do país que possui mais restaurantes registrados?
        col2.plotly_chart(restaurants_by_country(df), use_content_width=True)

with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        # 3. Qual o nome do país que possui mais restaurantes com o nível de preço igual a 4 registrados?
        col1.plotly_chart(restaurants_by_country_price4(df), use_content_width=True)

    with col2:
        # 4. Qual o nome do país que possui a maior quantidade de tipos de culinária distintos?    
        col2.plotly_chart(cuisines_by_country(df), use_content_width=True)

with st.container():
    col1, col2 = st.columns(2)

    with col1:
        # 5. Qual o nome do país que possui a maior quantidade de avaliações feitas?
        col1.plotly_chart(rating_by_country(df), use_content_width=True)
        
    with col2:
        # 6. Qual o nome do país que possui a maior quantidade de restaurantes que fazem entrega?
        col2.plotly_chart(delivery_restaurant_by_country(df), use_content_width=True)

with st.container():
    col1, col2 = st.columns(2)

    with col1:
        # 7. Qual o nome do país que possui a maior quantidade de restaurantes que aceitam reservas?
        col1.plotly_chart(booking_restaurant_by_country(df), use_content_width=True)
        
    with col2:
        # 8. Qual o nome do país que possui, na média, a maior quantidade de avaliações registradas? 
        col2.plotly_chart(mean_votes_country(df), use_content_width=True)

with st.container():
    col1, col2 = st.columns(2)

    with col1:
        # 9. Qual o nome do país que possui, na média, a maior nota média registrada?
        # 10. Qual o nome do país que possui, na média, a menor nota média registrada?
        col1.plotly_chart(mean_rating_country(df), use_content_width=True)
    
    with col2:
        # 11. Qual a média de preço de um prato para dois por país?
        col2.plotly_chart(mean_average_cost_for_two_dolar_country(df), use_content_width=True)
        col2.markdown(' ###### Informações do valor removido da média aparada \n País: Austrália / Custo do prato para dois (dólar): 25.000.017,00 / ID do restaurante: 16608070')



