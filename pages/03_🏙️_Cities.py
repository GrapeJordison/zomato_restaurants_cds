# bibliotecas 
import pandas as pd
import haversine 
import plotly.express as px
import streamlit  as st
import datetime as dt
from PIL import Image
import folium
from streamlit_folium import folium_static
import numpy as np
import inflection

st.set_page_config(page_title='Cities', page_icon='🏙️', layout='wide')

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
    
    return df


# 1. Qual o nome da cidade que possui mais restaurantes registrados?
def restaurants_by_city(df):
    df_aux = df.loc[:, ['city','restaurant_id','country_name']].groupby(['city','country_name']).count().sort_values('restaurant_id', ascending=False).reset_index()
    df_aux.columns=['Cidades','Países', 'Quantidade de restaurantes']
    df_aux = df_aux.head(25)
    fig = px.bar(df_aux, x='Cidades', y='Quantidade de restaurantes', title='Restaurantes por cidade', color='Países')
    return fig

# 2. Qual o nome da cidade que possui mais restaurantes com nota média acima de 4?
def restaurant_price_tag_4_by_city(df):
    lins = df['aggregate_rating'] >= 4
    df_aux = df.loc[lins, 
['city','restaurant_id','aggregate_rating','country_name']].groupby(['city','country_name']).count().sort_values('aggregate_rating', ascending=False).reset_index()
    df_aux.columns=['Cidades','Países', 'Quantidade de restaurantes','Média das avaliações']
    df_aux = df_aux.head(7)
    fig = px.bar(df_aux, x='Cidades', y='Quantidade de restaurantes', title='Restaurantes com nota média acima de 4 por cidade', color='Países')
    return fig


# 3. Qual o nome da cidade que possui mais restaurantes com nota média abaixo de 2.5?
def restaurant_price_tag_2_5_by_city(df):
    lins = df['aggregate_rating'] <= 2.5
    df_aux = df.loc[lins, ['city','aggregate_rating','restaurant_id','country_name']].groupby(['city','country_name']).count().sort_values('aggregate_rating', ascending=False).reset_index()
    df_aux.columns=['Cidades','Países', 'Quantidade de restaurantes','Média das avaliações']
    df_aux = df_aux.head(7)
    fig = px.bar(df_aux, x='Cidades', y='Quantidade de restaurantes', title='Restaurantes com nota média abaixo de 2.5 por cidade', color='Países')
    return fig


# 4. Qual o nome da cidade que possui o maior valor médio de um prato para dois?
def expensiver_average_cost_for_two_city(df):
    # Informações do valor removido da média aparada > País: Austrália / Custo do prato para dois (dólar): 25,000,017 / ID do restaurante: 16,608,070
    lins= df['restaurant_id'] != 16608070
    df_aux = df.loc[lins, 
['city','average_cost_for_two_dolar','country_name']].groupby(['city','country_name']).mean('average_cost_for_two_dolar').sort_values('average_cost_for_two_dolar', ascending=False).reset_index()
    df_aux.columns=['Cidades','Países', 'Média custo prato para dois (dólar)']    
    df_aux = df_aux.head(10)
    fig = px.bar(df_aux, x='Cidades', y='Média custo prato para dois (dólar)', title='Maiores preços médios de pratos para dois por cidade (dólar)', color='Países')
    return fig


# 5. Qual o nome da cidade que possui a maior quantidade de tipos de culinária distintas?

def cuisines_by_city(df):
    df_aux = df.loc[:, ['city','first_cuisines','country_name']].groupby(['city','country_name']).nunique().sort_values('first_cuisines', ascending=False).reset_index()
    df_aux.columns=['Cidades','Países', 'Tipos de culinária']
    df_aux = df_aux.head(10)
    fig = px.bar(df_aux, x='Cidades', y='Tipos de culinária', title='Tipos de culinária por cidade', color='Países')
    return fig


# 6. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem reservas?
# 7. Qual o nome da cidade que possui a menor quantidade de restaurantes que fazem entregas?

def restaurants_has_booking_by_city(df):
    lins = df['has_table_booking'] == 1
    df_aux = df.loc[lins, ['has_table_booking','city','restaurant_id','country_name']].groupby(['city','country_name']).count().sort_values('restaurant_id', ascending=False).reset_index()   
    df_aux.columns=['Cidades','Países', 'Faz reservas','Quantidade de restaurantes']
    df_aux = df_aux.head(10)
    fig = px.bar(df_aux, x='Cidades', y='Quantidade de restaurantes', title='Restaurantes que fazem reservas por cidade', color='Países')
    return fig

#8. Qual o nome da cidade que possui a maior quantidade de restaurantes que aceitam pedidos online?

def restaurants_has_online_delivery_by_city(df):
    lins = df['has_online_delivery'] == 1
    df_aux = df.loc[lins, ['has_online_delivery','city','country_name']].groupby(['city','country_name']).count().sort_values('has_online_delivery', ascending=False).reset_index()  
    df_aux.columns=['Cidades','Países', 'Faz entregas online']
    df_aux = df_aux.head(10)
    fig = px.bar(df_aux, x='Cidades', y='Faz entregas online', title='Restaurantes que fazem entregas online por cidade', color='Países')
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
# Inicio códigos Streamlit
# ====================================================

# ====================================================
# Barra Lateral Streamlit
# ====================================================

# Informações barra lateral
st.sidebar.markdown('### Filtros')

#Filtro dos países
countries_list = list(df.loc[:,'country_name'].unique())
countries = st.sidebar.multiselect('Escolha os Paises que Deseja visualizar os Restaurantes',
countries_list, default=countries_list)

lins = df['country_name'].isin(countries)
df = df.loc[lins, :]

st.sidebar.markdown("""---""")  

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
st.sidebar.markdown(' ### Powered by Marina Sá')

# ====================================================
# Layout Sreamlit
# ====================================================


with st.container():
    with st.container():
        # Cidade
        st.header(' 🏙️  Visão Cidades')
        st.markdown("""---""")      
        
        # 1. Qual o nome da cidade que possui mais restaurantes registrados?
        st.plotly_chart(restaurants_by_city(df), use_content_width=True)

    with st.container():
        col1, col2 = st.columns(2)
        
        with col1:
            # 2. Qual o nome da cidade que possui mais restaurantes com nota média acima de 4?
            col1.plotly_chart(restaurant_price_tag_4_by_city(df), use_content_width=True)
    
        with col2:
            # 3. Qual o nome da cidade que possui mais restaurantes com nota média abaixo de 2.5?
            col2.plotly_chart(restaurant_price_tag_2_5_by_city(df), use_content_width=True)

    with st.container():
        with col1:
            # 4. Qual o nome da cidade que possui o maior valor médio de um prato para dois?
            col1.plotly_chart(expensiver_average_cost_for_two_city(df), use_content_width=True)
            col1.markdown(' ###### Informações do valor removido da média aparada \n País: Austrália / Custo do prato para dois (dólar): 25.000.017,00 / ID do restaurante: 16608070')

        with col2:
            # 5. Qual o nome da cidade que possui a maior quantidade de tipos de culinária distintas?
            col2.plotly_chart(cuisines_by_city(df), use_content_width=True)

        with col1:
            # 6. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem reservas?
            # 7. Qual o nome da cidade que possui a menor quantidade de restaurantes que fazem entregas?
            col1.plotly_chart(restaurants_has_booking_by_city(df), use_content_width=True)

        with col2:
            #8. Qual o nome da cidade que possui a maior quantidade de restaurantes que aceitam pedidos online?
            col2.plotly_chart(restaurants_has_online_delivery_by_city(df), use_content_width=True)
    
