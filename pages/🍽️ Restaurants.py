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

st.set_page_config(page_title='Restaurants', page_icon='🍽️', layout='wide')

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

    # Removendo valores duplicados
    df = df.drop_duplicates().reset_index()
    
    return df

# Colunas necessárias: restaurant_name, restaurant_id, aggregate_rating, votes, average_cost_for_two_dolar, country_name, has_online_delivery, has_table_booking, first_cuisines

def renaming_columns(df):
     # Informações do valor removido  > País: Austrália / Custo do prato para dois (dólar): 25,000,017 / ID do restaurante: 16,608,070
    lins= (df['restaurant_id'] != 16608070) & (df['votes'] != 0)
    df_aux = df.loc[lins, ['restaurant_name', 'restaurant_id', 'aggregate_rating', 'votes', 'average_cost_for_two_dolar', 'country_name', 'has_online_delivery', 'has_table_booking', 'first_cuisines']]
    df_aux.columns = ['Nome_do_restaurante', 'Quantidade_de_restaurantes', 'Média_das_avaliações','Quantidade_de_avaliações','Média_de_custo_prato_para_dois_(dólar)','Países','Entrega_online','Faz_reservas','Tipos_de_culinárias']
    return df_aux


# 6. Os restaurantes que aceitam pedido online são também, na média, os restaurantes que mais possuem avaliações registradas? 

def restaurant_online_most_voted(df_aux):
    # Soma total das avaliações registradas dos restaurantes que fazem entrega online dividido pelo total de restaurantes que fazem entrega online
    lins = df_aux['Entrega_online'] == 1
    restaurants_online = df_aux.loc[lins, ['Nome_do_restaurante','Quantidade_de_restaurantes','Quantidade_de_avaliações','Tipos_de_culinárias','Entrega_online','Média_das_avaliações','Países']].sort_values('Quantidade_de_avaliações', ascending=False)
    restaurants_online = restaurants_online.head(10)
    mean_restaurants_online = np.round((restaurants_online['Quantidade_de_avaliações'].sum()) / (len(restaurants_online)),2)
    
    # Soma total das avaliações registradas dos restaurantes que não fazem entrega online dividido pelo total de restaurantes que não fazem entrega online
    lins = df_aux['Entrega_online'] == 0
    restaurants_not_online = df_aux.loc[lins, ['Nome_do_restaurante','Quantidade_de_restaurantes','Quantidade_de_avaliações','Tipos_de_culinárias','Entrega_online','Média_das_avaliações','Países']].sort_values('Quantidade_de_avaliações', ascending=False)
    restaurants_not_online = restaurants_not_online.head(10)
    mean_restaurants_not_online = np.round((restaurants_not_online['Quantidade_de_avaliações'].sum()) / len(restaurants_not_online), 2)
    
    # Gráfico de pizza
    data = {'Descrição_médias':['Média Com Pedido Online','Média Sem Pedido Online'] , 'Médias':[mean_restaurants_online, mean_restaurants_not_online]}
    mean_restaurants = pd.DataFrame(data)
    fig = px.pie(mean_restaurants, values='Médias', names='Descrição_médias', title='Top 10 - Restaurantes com mais avaliações' )
    
    return fig

# 7. Os restaurantes que fazem reservas são também, na média, os restaurantes que possuem o maior valor médio de um prato para duas pessoas?

def restaurant_booking_most_voted(df_aux):
    # Top 10 restaurantes com maior custo de pratos para dois que fazem reservas
    lins = df_aux['Faz_reservas'] == 1
    restaurant_booking = df_aux.loc[lins, ['Nome_do_restaurante','Tipos_de_culinárias','Faz_reservas','Média_de_custo_prato_para_dois_(dólar)','Países']].sort_values('Média_de_custo_prato_para_dois_(dólar)', ascending=False)
    restaurant_booking = restaurant_booking.head(10)
    mean_restaurant_booking= np.round(restaurant_booking['Média_de_custo_prato_para_dois_(dólar)'].sum() / len(restaurant_booking), 2)
    
    
    # Top 10 restaurantes com maior custo de pratos para dois que fazem reservas
    lins = df_aux['Faz_reservas'] == 0
    restaurant_not_booking = df_aux.loc[:, ['Nome_do_restaurante','Tipos_de_culinárias','Faz_reservas','Média_de_custo_prato_para_dois_(dólar)','Países']].sort_values('Média_de_custo_prato_para_dois_(dólar)', ascending=False)
    restaurant_not_booking = restaurant_not_booking.head(10)
    mean_restaurant_not_booking= np.round(restaurant_not_booking['Média_de_custo_prato_para_dois_(dólar)'].sum() / len(restaurant_not_booking), 2)
    
    # Gráfico de pizza
    data = {'Descrição_médias':['Média Fazem reservas','Média Não fazem reservas'] , 'Médias':[mean_restaurant_booking, mean_restaurant_not_booking]}
    mean_restaurants = pd.DataFrame(data)
    fig = px.pie(mean_restaurants, values='Médias', names='Descrição_médias', title='Top 10 - Restaurantes com maior custo prato para dois' )
    return fig

# 8. Os restaurantes do tipo de culinária japonesa dos Estados Unidos da América possuem um valor médio de prato para duas pessoas maior que as churrascarias americanas (BBQ)?

def restaurants_japanese_bbq_usa(df_aux):
    # Top 10 Restaurantes Estadunidenses que servem comida japonesa com maior custo do prato para dois
    lins = (df_aux['Tipos_de_culinárias'] == 'Japanese') & (df_aux['Países'] == 'United States of America')
    restaurants_japanese_usa = df_aux.loc[lins, ['Nome_do_restaurante','Média_de_custo_prato_para_dois_(dólar)','Tipos_de_culinárias','Países']].sort_values('Média_de_custo_prato_para_dois_(dólar)', ascending=False)
    restaurants_japanese_usa = restaurants_japanese_usa.head(10)
    mean_restaurants_japanese_usa= np.round(restaurants_japanese_usa['Média_de_custo_prato_para_dois_(dólar)'].sum() / len(restaurants_japanese_usa), 2)
    
    # Top 10 Restaurantes Estadunidenses que servem churrasco com maior custo do prato para dois
    lins = (df_aux['Tipos_de_culinárias'] == 'BBQ') & (df_aux['Países'] == 'United States of America')
    restaurants_bbq_usa = df_aux.loc[lins, ['Nome_do_restaurante','Média_de_custo_prato_para_dois_(dólar)','Tipos_de_culinárias','Países']].sort_values('Média_de_custo_prato_para_dois_(dólar)', ascending=False)
    restaurants_bbq_usa = restaurants_bbq_usa.head(10)
    mean_restaurants_bbq_usa= np.round(restaurants_bbq_usa['Média_de_custo_prato_para_dois_(dólar)'].sum() / len(restaurants_bbq_usa), 2)
    
    # Gráfico de pizza
    data = {'Descrição_médias':['Média Comida Japondes','Média Churrasco'] , 'Médias':[mean_restaurants_japanese_usa, mean_restaurants_bbq_usa]}
    mean_restaurants = pd.DataFrame(data)
    fig = px.pie(mean_restaurants, values='Médias', names='Descrição_médias', title='Top 10 - Restaurantes Estadunidenses com maior custo prato para dois' )
    
    return fig


def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


# ============ Inicio estrutura lógica ===============
# ====================================================
# Limpando os dados
# ====================================================

df = clean_code(df)
df_aux = renaming_columns(df)

# ====================================================
# Inicio códigos Streamlit
# ====================================================

# ====================================================
# Barra Lateral Streamlit
# ====================================================

# Informações barra lateral
st.sidebar.markdown('### Filtros')

#Filtro dos países
countries_list = list(df_aux.loc[:,'Países'].unique())
countries = st.sidebar.multiselect('Escolha os Paises que Deseja visualizar os Restaurantes',
countries_list, default=countries_list)

lins = df_aux['Países'].isin(countries)
df_aux = df_aux.loc[lins, :]

st.sidebar.markdown("""---""")  

# Filtro da quantidade de restaurantes
st.sidebar.markdown('##### Selecione a quantidade de Restaurantes que deseja visualizar')

date_slider = st.sidebar.slider(
    '',
    value=(6942),
    min_value=(1),
    max_value=(6942))

df_aux = df_aux.sort_values('Média_das_avaliações', ascending=False)
df_aux = df_aux.head(date_slider)


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
    # Restaurantes
        st.header(' 🍽️  Visão Restaurantes')
        st.markdown("""---""")    

with st.container():
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        # 1. Qual o nome do restaurante que possui a maior quantidade de avaliações?
        most_votes = df_aux.loc[:, ['Nome_do_restaurante','Quantidade_de_avaliações']].sort_values('Quantidade_de_avaliações', ascending=False).reset_index()
        col1.metric(most_votes.loc[0, 'Nome_do_restaurante'], most_votes.loc[0, 'Quantidade_de_avaliações'])

    with col2:
        # 2. Qual o nome do restaurante com a maior nota média?
        most_rating = df_aux.loc[:, ['Nome_do_restaurante','Média_das_avaliações']].sort_values('Média_das_avaliações', ascending=False).reset_index()
        col2.metric(most_rating.loc[0, 'Nome_do_restaurante'], '{}/5.0'.format(most_rating.loc[0, 'Média_das_avaliações']))         
        
    with col3:
        # 3. Qual o nome do restaurante que possui o maior valor de uma prato para duas pessoas?
        most_cost = df_aux.loc[:, ['Nome_do_restaurante','Média_de_custo_prato_para_dois_(dólar)']].sort_values('Média_de_custo_prato_para_dois_(dólar)', ascending=False).reset_index()
        col3.metric(most_cost.loc[0, 'Nome_do_restaurante'], most_cost.loc[0, 'Média_de_custo_prato_para_dois_(dólar)'])    

    with col4:
        #4. Qual o nome do restaurante de tipo de culinária brasileira que possui a menor média de avaliação?
        lins = df_aux['Tipos_de_culinárias'] == 'Brazilian'        
        brazilian_worse_rating = df_aux.loc[lins, ['Nome_do_restaurante','Média_das_avaliações','Quantidade_de_avaliações']].sort_values('Média_das_avaliações', ascending=True).reset_index()
        col4.metric(brazilian_worse_rating.loc[0, 'Nome_do_restaurante'], '{}/5.0'.format(brazilian_worse_rating.loc[0, 'Média_das_avaliações']))

    with col5:
# 5. Qual o nome do restaurante de tipo de culinária brasileira, e que é do Brasil, que possui a maior média de avaliação?
        lins = (df_aux['Tipos_de_culinárias'] == 'Brazilian') & (df_aux['Países'] == 'Brazil')    
        brazilian_best_rating = df_aux.loc[lins, ['Nome_do_restaurante','Média_das_avaliações','Quantidade_de_avaliações']].sort_values('Média_das_avaliações', ascending=False).reset_index()
        col5.metric(brazilian_best_rating.loc[0, 'Nome_do_restaurante'], '{}/5.0'.format(brazilian_best_rating.loc[0, 'Média_das_avaliações']))   


with st.container():
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        col1.markdown(' ###### Restaurante com maior quantidade de avaliações')
    with col2:
        col2.markdown(' ###### Restaurante com maior nota média')
    with col3:
        col3.markdown(' ###### Restaurante com maior valor de uma prato para dois')
    with col4:
        col4.markdown(' ###### Restaurante com culinária brasileira com menor avaliação média')
    with col5:
        col5.markdown(' ###### Restaurante brasileiro com culinária brasileira com maior avaliação média')  


st.markdown("""---""")    


with st.container():
    
    col1, col2, col3 = st.columns(3)

    with col1:
        # 6. Os restaurantes que aceitam pedido online são também, na média, os restaurantes que mais possuem avaliações registradas? 
        col1.plotly_chart(restaurant_online_most_voted(df_aux), use_content_width=True)
    
    with col2:
        # 7. Os restaurantes que fazem reservas são também, na média, os restaurantes que possuem o maior valor médio de um prato para duas pessoas?
        col2.plotly_chart(restaurant_booking_most_voted(df_aux), use_content_width=True)
    
    with col3:
        # 8. Os restaurantes do tipo de culinária japonesa dos Estados Unidos da América possuem um valor médio de prato para duas pessoas maior que as churrascarias americanas (BBQ)?
        col3.plotly_chart(restaurants_japanese_bbq_usa(df_aux), use_content_width=True)


st.markdown("""---""")  











