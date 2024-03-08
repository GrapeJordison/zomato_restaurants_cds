# fome_zero_cds
This dashboard was a student project mine using a dataset from kaggle > https://www.kaggle.com/datasets/akashram/zomato-restaurants-autoupdated-dataset?resource=download&amp;select=zomato.csv

Cenário fictício usado para criação do dashboard durante a aula.

**Link para acessar o dashboard > https://fome-zero-cds.streamlit.app/**

### **Indíce:**

**1. Problema de negócio** <br>
**2. Premissas do negócio** <br>
**3. Estratégia da solução** <br>
**4. Top 3 Insights de dados** <br>
**5. O produto final do projeto** <br>
**6. Conclusão** <br>
**7. Próximo passos** <br>
  
  ### **1. Problema de negócio**
  A Cury Company é uma empresa de tecnologia que criou um
  aplicativo que conecta restaurantes, entregadores e pessoas.
  Através desse aplicativo, é possível realizar o pedido de uma refeição,
  em qualquer restaurante cadastrado, e recebê-lo no conforto da sua
  casa por um entregador também cadastrado no aplicativo da Cury
  Company.
  <br><br>
  A empresa realiza negócios entre restaurantes, entregadores e
  pessoas, e gera muitos dados sobre entregas, tipos de pedidos,
  condições climáticas, avaliação dos entregadores e etc. Apesar da
  entrega estar crescento, em termos de entregas, o CEO não tem
  visibilidade completa dos KPIs de crescimento da empresa.
  Você foi contratado como um Cientista de Dados para criar soluções
  de dados para entrega, mas antes de treinar algoritmos, a
  necessidade da empresa é ter um os principais KPIs estratégicos
  organizados em uma única ferramenta, para que o CEO possa
  consultar e conseguir tomar decisões simples, porém importantes.
  <br><br>
  A Cury Company possui um modelo de negócio chamado
  Marketplace, que fazer o intermédio do negócio entre três clientes
  principais: Restaurantes, entregadores e pessoas compradoras. Para
  acompanhar o crescimento desses negócios, o CEO gostaria de ver
  as seguintes métricas de crescimento:

  #### Do lado da empresa:
  1. Quantidade de pedidos por dia.<br>
  2. Quantidade de pedidos por semana.<br>
  3. Distribuição dos pedidos por tipo de tráfego.<br>
  4. Comparação do volume de pedidos por cidade e tipo de tráfego.<br>
  4. A quantidade de pedidos por entregador por semana.<br>
  5. A localização central de cada cidade por tipo de tráfego.<br>

  #### Do lado do entregador:
  1. A menor e maior idade dos entregadores.<br>
  2. A pior e a melhor condição de veículos.<br>
  3. A avaliação médida por entregador.<br>
  4. A avaliação média e o desvio padrão por tipo de tráfego.<br>
  5. A avaliação média e o desvio padrão por condições climáticas.<br>
  6. Os 10 entregadores mais rápidos por cidade.<br>
  7. Os 10 entregadores mais lentos por cidade.<br>
     
  #### Do lado do restaurantes:
  1. A quantidade de entregadores únicos.<br>
  2. A distância média dos resturantes e dos locais de entrega.<br>
  3. O tempo médio e o desvio padrão de entrega por cidade.<br>
  4. O tempo médio e o desvio padrão de entrega por cidade e tipo de
  pedido.<br>
  5. O tempo médio e o desvio padrão de entrega por cidade e tipo de
  tráfego.<br>
  6. O tempo médio de entrega durantes os Festivais.<br>
  <br>
  O objetivo desse projeto é criar um conjunto de gráficos e/ou tabelas
  que exibam essas métricas da melhor forma possível para o CEO.<br>
  


### 2. Premissas assumidas para a análise
  1. A análise foi realizada com dados entre 11/02/2022 e 06/04/2022.<br>
  2. Marketplace foi o modelo de negócio assumido.<br>
  3. Os 3 principais visões do negócio foram: Visão transação de
  pedidos, visão restaurante e visão entregadores.<br>


### 3. Estratégia da solução

  O painel estratégico foi desenvolvido utilizando as métricas que
  refletem as 3 principais visões do modelo de negócio da empresa:<br>
  <br>
    1. Visão do crescimento da empresa<br>
    2. Visão do crescimento dos restaurantes<br>
    3. Visão do crescimento dos entregadores<br>   
  Cada visão é representada pelo seguinte conjunto de métricas.
  
  #### 1. Visão do crescimento da empresa
  a. Pedidos por dia<br>
  b. Porcentagem de pedidos por condições de trânsito<br>
  c. Quantidade de pedidos por tipo e por cidade.<br>
  d. Pedidos por semana<br>
  e. Quantidade de pedidos por tipo de entrega<br>
  f. Quantidade de pedidos por condições de trânsito e tipo de Cidade<br>
  
  #### 2. Visão do crescimento dos restaurantes
  a. Quantidade de pedidos únicos.<br>
  b. Distância média percorrida.<br>
  c. Tempo médio de entrega durante festival e dias normais.<br>
  d. Desvio padrão do tempo de entrega durante festivais e dias
  normais.<br>
  e. Tempo de entrega médio por cidade.<br>
  f. Distribuição do tempo médio de entrega por cidade.<br>
  g. Tempo médio de entrega por tipo de pedido.<br>

  #### 3. Visão do crescimento dos entregadores
  a. Idade do entregador mais velho e do mais novo.<br>
  b. Avaliação do melhor e do pior veículo.<br>
  c. Avaliação média por entregador.<br>
  d. Avaliação média por condições de trânsito.<br>
  e. Avaliação média por condições climáticas.<br>
  f. Tempo médido do entregador mais rápido.<br>
  g. Tempo médio do entregador mais rápido por cidade.<br>

### 4. Top 3 Insights de dados
  1. A sazonalidade da quantidade de pedidos é diária. Há uma
  variação de aproximadamente 10% do número de pedidos em dia
  sequenciais.<br>
  2. As cidades do tipo Semi-Urban não possuem condições baixas de
  trânsito.<br>
  3. As maiores variações no tempo de entrega, acontecem durante o
  clima ensolarado.<br>

### 5. O produto final do projeto
  Painel online, hospedado em um Cloud e disponível para acesso em
  qualquer dispositivo conectado à internet.<br>
  O painel pode ser acessado através desse link: https://fome-zero-cds.streamlit.app/

### 6. Conclusão
  O objetivo desse projeto é criar um conjunto de gráficos e/ou tabelas
  que exibem essas métricas da melhor forma possível para o CEO.<br>
  Da visão da Empresa, podemos concluir que o número de pedidos
  Cresceu entre a semana 06 e a semana 13 do ano de 2022.<br>

### 7. Próximo passos
  1. Reduzir o número de métricas.<br>
  2. Criar novos filtros.<br>
  3. Adicionar novas visões de negócio<br>
