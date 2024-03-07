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


def most_expensive_cuisines(df):
    lins = df['restaurant_id'] != 16608070
    df_aux = df.loc[lins, ['first_cuisines','average_cost_for_two_dolar','country_name']].groupby(['first_cuisines','country_name']).mean().sort_values('average_cost_for_two_dolar', ascending=False).reset_index()
    df_aux = df_aux.head(10)
    df_aux.columns=['Tipos_de_culinárias', 'Países', 'Custo_prato_para_dois']
    fig = px.bar(df_aux, x='Tipos_de_culinárias', y='Custo_prato_para_dois', color='Países', title='Média aparada do custo do prato para dois por tipo de culinária (dólar)', text_auto=True)
    return fig


def best_rating_cuisines(df):
    df_aux = df.loc[:, ['first_cuisines','aggregate_rating','restaurant_id','votes']].groupby(['first_cuisines','aggregate_rating']).agg({'restaurant_id':['count'],'votes':['sum']}.sort_values('aggregate_rating', ascending=False)
    df_aux.columns=['Tipos_de_culinárias', 'Média_notas_avaliações','Quantidade_restaurantes','Quantidade_avaliações']
    df_aux = df_aux.reset_index()
    df_aux = df_aux.head(10)
    fig = px.bar(df_aux, x='Tipos_de_culinárias', y='Média_notas_avaliações', title='Médias das notas das avaliações registradas por tipo de culinária')
    
    return df_aux


def cuisines_online_booking(df):
    lins = (df['has_table_booking'] == 1) & (df['has_online_delivery'] == 1)
    df_aux = df.loc[lins, ['first_cuisines','country_name','restaurant_id']].groupby(['first_cuisines','country_name']).count().sort_values('restaurant_id', ascending=False).reset_index()
    df_aux = df_aux.head(10)
    df_aux.columns=['Tipos_de_culinárias', 'Países', 'Quantidade_restaurantes']
    fig = px.bar(df_aux, x='Tipos_de_culinárias', y='Quantidade_restaurantes', color='Países', title='Tipos de culinárias com mais restaurantes que aceitam pedidos online e fazem entregas', text_auto=True)
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


# Filtros tipos de culinária
cuisines_list = list(df.loc[:,'first_cuisines'].unique())
lins = df['first_cuisines'].isin(cuisines_list)
df = df.loc[lins, :]

cuisines = st.sidebar.multiselect('Escolha os Tipos de Culinária', cuisines_list, default=cuisines_list)

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
        st.header(' 🍕 Visão Culinárias')
        st.markdown("""---""")    

# Tipos de Culinária


with st.container():
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        # 1. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do restaurante com a maior média de avaliação?
        lins = df['first_cuisines'] == 'Italian'
        df_aux = df.loc[lins, ['first_cuisines','restaurant_name','aggregate_rating']].sort_values('aggregate_rating', ascending=False).reset_index()
        col1.metric('Italiana: {}'.format(df_aux.loc[0, 'restaurant_name']), '{}/5.0'.format(df_aux.loc[0, 'aggregate_rating'])) 

    with col2:
        # 2. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do restaurante com a menor média de avaliação?
        lins = (df['first_cuisines'] == 'Italian') & (df['votes'] != 0)
        df_aux = df.loc[lins, ['first_cuisines','restaurant_name','aggregate_rating','votes']].sort_values('aggregate_rating', ascending=True).reset_index()
        col2.metric('Italiana: {}'.format(df_aux.loc[0, 'restaurant_name']), '{}/5.0'.format(df_aux.loc[0, 'aggregate_rating']))     
        
    with col3:
        # 3. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do restaurante com a maior média de avaliação?
        lins = (df['first_cuisines'] == 'American') & (df['votes'] != 0)
        df_aux = df.loc[lins, ['first_cuisines','restaurant_name','aggregate_rating','votes']].sort_values('aggregate_rating', ascending=False).reset_index()
        col3.metric('Americana: {}'.format(df_aux.loc[0, 'restaurant_name']), '{}/5.0'.format(df_aux.loc[0, 'aggregate_rating']))    


    with col4:
        # 4. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do restaurante com a menor média de avaliação?
        lins = (df['first_cuisines'] == 'American') & (df['votes'] != 0)
        df_aux = df.loc[lins, ['first_cuisines','restaurant_name','aggregate_rating','votes']].sort_values('aggregate_rating', ascending=True).reset_index()
        col4.metric('Americana: {}'.format(df_aux.loc[0, 'restaurant_name']), '{}/5.0'.format(df_aux.loc[0, 'aggregate_rating']))    

    with col5:
        # 5. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do restaurante com a maior média de avaliação?
        lins = (df['first_cuisines'] == 'Arabian') & (df['votes'] != 0)
        df_aux = df.loc[lins, ['first_cuisines','restaurant_name','aggregate_rating','votes']].sort_values('aggregate_rating', ascending=False).reset_index()
        col5.metric('Árabe: {}'.format(df_aux.loc[0, 'restaurant_name']), '{}/5.0'.format(df_aux.loc[0, 'aggregate_rating']))      


with st.container():
    col1, col2, col3, col4, col5= st.columns(5)

    with col1:
        col1.markdown(' ###### Restaurante de culinária italina com maior média de avaliações')
    with col2:
        col2.markdown(' ###### Restaurante de culinária italina com menor média de avaliações')
    with col3:
        col3.markdown(' ###### Restaurante de culinária americana com maior média de avaliações')
    with col4:
        col4.markdown(' ###### Restaurante de culinária americana com menor média de avaliações')
    with col5:
        col5.markdown(' ###### Restaurante de culinária árabe com maior média de avaliações')  

st.markdown("""---""")    


with st.container():
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        # 6. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do restaurante com a menor média de avaliação?
        lins = (df['first_cuisines'] == 'Arabian') & (df['votes'] != 0)
        df_aux = df.loc[lins, ['first_cuisines','restaurant_name','aggregate_rating']].sort_values('aggregate_rating', ascending=True).reset_index()
        col1.metric('Árabe: {}'.format(df_aux.loc[0, 'restaurant_name']), '{}/5.0'.format(df_aux.loc[0, 'aggregate_rating'])) 

    with col2:
        # 7. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do restaurante com a maior média de avaliação?
        lins = (df['first_cuisines'] == 'Japanese') & (df['votes'] != 0)
        df_aux = df.loc[lins, ['first_cuisines','restaurant_name','aggregate_rating','votes']].sort_values('aggregate_rating', ascending=False).reset_index()
        col2.metric('Japonesa: {}'.format(df_aux.loc[0, 'restaurant_name']), '{}/5.0'.format(df_aux.loc[0, 'aggregate_rating']))     
        
    with col3:
        # 8. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do restaurante com a menor média de avaliação?
        lins = (df['first_cuisines'] == 'Japanese') & (df['votes'] != 0)
        df_aux = df.loc[lins, ['first_cuisines','restaurant_name','aggregate_rating','votes']].sort_values('aggregate_rating', ascending=True).reset_index()
        col3.metric('Japonesa: {}'.format(df_aux.loc[0, 'restaurant_name']), '{}/5.0'.format(df_aux.loc[0, 'aggregate_rating']))    


    with col4:
        # 9. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do restaurante com a maior média de avaliação?
        lins = (df['first_cuisines'] == 'Home-made') & (df['votes'] != 0)
        df_aux = df.loc[lins, ['first_cuisines','restaurant_name','aggregate_rating','votes']].sort_values('aggregate_rating', ascending=False).reset_index()
        col4.metric('Caseira: {}'.format(df_aux.loc[0, 'restaurant_name']), '{}/5.0'.format(df_aux.loc[0, 'aggregate_rating']))    

    with col5:
        # 10. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do restaurante com a menor média de avaliação?
        lins = (df['first_cuisines'] == 'Home-made') & (df['votes'] != 0)
        df_aux = df.loc[lins, ['first_cuisines','restaurant_name','aggregate_rating','votes']].sort_values('aggregate_rating', ascending=True).reset_index()
        col5.metric('Caseira: {}'.format(df_aux.loc[0, 'restaurant_name']), '{}/5.0'.format(df_aux.loc[0, 'aggregate_rating']))      


with st.container():
    col1, col2, col3, col4, col5= st.columns(5)

    with col1:
        col1.markdown(' ###### Restaurante de culinária árabe com menor média de avaliações')
    with col2:
        col2.markdown(' ###### Restaurante de culinária japonesa com maior média de avaliações')
    with col3:
        col3.markdown(' ###### Restaurante de culinária japonesa com menor média de avaliações')
    with col4:
        col4.markdown(' ###### Restaurante de culinária caseira com maior média de avaliações')
    with col5:
        col5.markdown(' ###### Restaurante de culinária caseira com menor média de avaliações')  

st.markdown("""---""")    

with st.container():

    # 12. Qual o tipo de culinária que possui a maior nota média?   
    st.markdown(' #### Médias das notas das avaliações registradas por tipo de culinária')
    st.dataframe(best_rating_cuisines(df), use_container_width=True)

st.markdown("""---""")   

with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        # 11. Qual o tipo de culinária que possui o maior valor médio de um prato para duas pessoas?
        col1.plotly_chart(most_expensive_cuisines(df), use_container_width=True)
        col1.markdown(' ###### Informações do valor removido da média aparada \n País: Austrália Custo do prato para dois (dólar): 25.000.017,00 / ID do restaurante: 16608070 / Culinária: Modern Australian')

    with col2:
        # 13. Qual o tipo de culinária que possui mais restaurantes que aceitam pedidos online e fazem entregas?  
        col2.plotly_chart(cuisines_online_booking(df), use_container_width=True)

st.markdown("""---""")  










