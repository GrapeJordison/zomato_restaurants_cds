  # zomato_restaurants_cds 
  This dashboard was a student project using a public dataset from kaggle > https://www.kaggle.com/datasets/akashram/zomato-restaurants-autoupdated-dataset?resource=download&amp;select=zomato.csv
  
  ## Projeto de conclusão do curso:
  ## Fast Track Course: analisando dados com Python pela Comunidade DS
  
  Cenário fictício usado para criação do dashboard para o projeto.
  
  **Link para acessar o dashboard > https://zomato-restaurants-cds.streamlit.app/**
  
  ### **Indíce:**
  
  **1. Problema de negócio** <br>
  **2. Premissas do negócio** <br>
  **3. Estratégia da solução** <br>
  **4. Top 3 Insights de dados** <br>
  **5. O produto final do projeto** <br>
  **6. Conclusão** <br>
  **7. Próximo passos** <br>
  
  ### **1. Problema de negócio**
  
  <br><br>
  A Zomato restaurants é uma rede de restaurantes que serve 
  os mais diversos tipos de culinárias e possui filiais no mundo todo.
  <br><br>
  Para facilitar a visualização dos KPIs da empresa foi construído 
  um painel gerencial usando o streamlit.  
  <br><br>
  Para acompanhar o crescimento do negócio, o CEO solicitou as seguintes métricas de crescimento:

  #### Visão Geral
  1. Quantos restaurantes únicos estão registrados?
  2. Quantos países únicos estão registrados?
  3. Quantas cidades únicas estão registradas?
  4. Qual o total de avaliações feitas?
  5. Qual o total de tipos de culinária registrados?

  #### Vĩsão Países
  1. Qual o nome do país que possui mais cidades registradas?
  2. Qual o nome do país que possui mais restaurantes registrados?
  3. Qual o nome do país que possui mais restaurantes com o nível de preço igual a 4 registrados?
  4. Qual o nome do país que possui a maior quantidade de tipos de culinária distintos?
  5. Qual o nome do país que possui a maior quantidade de avaliações feitas?
  6. Qual o nome do país que possui a maior quantidade de restaurantes que fazem entrega?
  7. Qual o nome do país que possui a maior quantidade de restaurantes que aceitam reservas?
  8. Qual o nome do país que possui, na média, a maior quantidade de avaliações registrada?
  9. Qual o nome do país que possui, na média, a maior nota média registrada?
  10. Qual o nome do país que possui, na média, a menor nota média registrada?
  11. Qual a média de preço de um prato para dois por país?
     
  #### Visão Cidades
  1. Qual o nome da cidade que possui mais restaurantes registrados?
  2. Qual o nome da cidade que possui mais restaurantes com nota média acima de 4?
  3. Qual o nome da cidade que possui mais restaurantes com nota média abaixo de 2.5?
  4. Qual o nome da cidade que possui o maior valor médio de um prato para dois?
  5. Qual o nome da cidade que possui a maior quantidade de tipos de culinária distintas?
  6. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem reservas?
  7. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem entregas?
  8. Qual o nome da cidade que possui a maior quantidade de restaurantes que aceitam pedidos online?

  #### Visão Restaurantes
  1. Qual o nome do restaurante que possui a maior quantidade de avaliações?
  2. Qual o nome do restaurante com a maior nota média?
  3. Qual o nome do restaurante que possui o maior valor de uma prato para duas pessoas?
  4. Qual o nome do restaurante de tipo de culinária brasileira que possui a menor média de avaliação?
  5. Qual o nome do restaurante de tipo de culinária brasileira, e que é do Brasil, que possui a maior média de avaliação?
  6. Os restaurantes que aceitam pedido online são também, na média, os restaurantes que mais possuem avaliações registradas?
  7. Os restaurantes que fazem reservas são também, na média, os restaurantes que possuem o maior valor médio de um prato para duas pessoas?
  8. Os restaurantes do tipo de culinária japonesa dos Estados Unidos da América possuem um valor médio de prato para duas pessoas maior que as churrascarias americanas (BBQ)?
  
  #### Visão Culinárias
  1. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do restaurante com a maior média de avaliação?
  2. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do restaurante com a menor média de avaliação?
  3. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do restaurante com a maior média de avaliação?
  4. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do restaurante com a menor média de avaliação?
  5. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do restaurante com a maior média de avaliação?
  6. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do restaurante com a menor média de avaliação?
  7. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do restaurante com a maior média de avaliação?
  8. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do restaurante com a menor média de avaliação?
  9. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do restaurante com a maior média de avaliação?
  10. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do restaurante com a menor média de avaliação?
  11. Qual o tipo de culinária que possui o maior valor médio de um prato para duas pessoas?
  12. Qual o tipo de culinária que possui a maior nota média?
  13. Qual o tipo de culinária que possui mais restaurantes que aceitam pedidos online e fazem entregas?

  O objetivo desse projeto é criar um conjunto de gráficos e/ou tabelas que exibam essas métricas da melhor forma possível para o CEO.<br>
  
  ### 2. Premissas assumidas para a análise
  1. A base de dados utilizada é pública e está disponível na plataforma Kaggle através do link:https://www.kaggle.com/datasets/akashram/zomato-restaurants-autoupdated-dataset?resource=download&select=zomato.csv
  2. Cada linha da base de dados foi assumida como representante de uma filial, possuindo um ID do restaurante que a representa, as linhas com valores repetidos foram removidas;
  3. As linhas que possuem valores zerados permaneceram para preservar ao máximo a conexão com a realidade;
  4. Marketplace foi o modelo de negócio assumido;
  5. Foram construídos cinco painéis interativos para facilitar a visualização das principais métricas do negócio, sendo elas:
  -  A visão geral dos dados cadastrados e localização geográfica dos restaurantes;
  -  A visão por países;
  -  A visão por cidades;
  -  A visão por restaurantes;
  -  A visão por tipo de culinárias;

  ### 3. Estratégia da solução

  O painel estratégico foi desenvolvido utilizando as métricas que
  refletem as principais visões do modelo de negócio da empresa:<br>
  <br>

  #### 1. Visão Geral
  - Total de filiais disponíveis pelo mundo <br>
  - Países atendidos <br>
  - Cidades atendidas <br>
  - Total de avaliações realizadas <br>  
  - Total de tipos de culinárias que as filiais disponibilizam <br>
  - Mapa com a localização geográfica dos restaurantes cadastrados <br>
  
  #### 2. Visão Países
  - O número de restaurantes cadastrados por país
  - O número de cidades atendidas por país
  - Os tipos de culinárias oferecidas por país
  - A média de avaliações na plataforma por país
  - A média aparada do custo de refeições para duas pessoas por país (Informações do valor removido da média aparada > País: Austrália / Custo do prato para dois (dólar): 25.000.017,00 / ID do restaurante: 16608070)

  #### 3. Visão Cidades
 - O número de restaurantes cadastrados por cidade
 - Cidades com mais restaurantes avaliados acima de 4.0
 - Cidades com mais restaurantes avaliados abaixo de 2.5
 - Cidades com maiores custo médio de refeições para duas pessoas
 - Cidades com mais tipos de culinárias disponíveis
 - Cidades com mais restaurantes que fazem reservas
 - Cidades com mais restaurantes que fazem entregas  
 
  #### 3. Visão Restaurantes
  - Restaurante com a maior quantidade de avaliações
  - Restaurante com a maior nota média
  - Restaurante com maior valor de uma prato para dois
  - Restaurante com culinária brasileira com menor avaliação média
  - Restaurante brasileiro com culinária brasileira com maior avaliação média
  - Top 10 restaurantes com mais avaliações que fazem entregas e que não fazem entregas
  - Top 10 restaurantes com maior custo do prato para dois que fazem reservas e que não fazem reservas
  - Top 10 restaurantes estadunidenses com custo do prato para dois que servem comida japonesa e churrasco

  #### 3. Visão Culinárias
  - Restaurante de culinária italina com maior média de avaliações
  - Restaurante de culinária italina com menor média de avaliações
  - Restaurante de culinária americana com maior média de avaliações
  - Restaurante de culinária americana com menor média de avaliações
  - Restaurante de culinária árabe com maior média de avaliações
  - Restaurante de culinária árabe com menor média de avaliações
  - Restaurante de culinária japonesa com maior média de avaliações
  - Restaurante de culinária japonesa com menor média de avaliações
  - Restaurante de culinária caseira com maior média de avaliações
  - Restaurante de culinária caseira com menor média de avaliações
  - Média aparada do custo do prato para dois (dólar) (Informações do valor removido da média aparada > País: Austrália / Custo do prato para dois (dólar): 25.000.017,00 / ID do restaurante: 16608070)
  - Média das notas das avaliações registradas por tipo de culinária
  - Tipos de culinárias com mais restaurantes  

### 4. Top 3 Insights de dados
  1. A Zomato está presente nos cinco continentes;
  2. A maioria dos restaurantes está localizado na Índia ou Estados Unidos;
  3. Índia e Emirados Arábes possuem a maior diversidade de culinárias;
  4. Poucos restaurantes fazem entregas ou aceitam reservas de mesa;
  5. Indonésia, Philipinas e Singapura tem as maiores médias das avaliações registradas;
  6. Singapura possui o maior média de custo de um prato para dois (141.04 dólares)
  7. Existe um outlier na base de dados que é um restaurante da Austrália com a média do custo do prato para dois em (Informações do valor removido da média aparada > País: Austrália / Custo do prato para dois (dólar): 25.000.017,00 / ID do restaurante: 16608070)
  8. Os restaurantes com mais avaliações fazem pedido online;
  9. Os restaurantes com maior custo do prato para dois são os que não fazem reservas;
  10. Os restaurantes estadunidenses com maior custo do prato para dois são os que vendem comida japonesa e não churrasco;
  11. Indonésia e Índia são os países com maior quantidade média de avaliações.
  12. Com execessão do Brasil todos os outros 14 países cadastrados tem a média de avaliações acima dos 4.0 pontos.
  13. Qatar, Inglaterra e Canadá possuem as cidades que oferecem a maior diversidade de culinárias.
  14. Três das dez cidades com mais restaurantes avaliados em média abaixo de 2.5 estão no Brasil.
  15. A maior parte dos restaurantes cadastrados não fazem entregas on-line (64,7%) e não reservam mesas (93,9%).
  16. As culinárias com maior número de avaliações e com maior média de avalição são: Continental, Européia, Barbecue, Indiana, Sushi e Cafeteria.


### 5. O produto final do projeto
  Um conjunto de paineis interativose  online, hospedado em um Cloud e disponível para acesso em qualquer dispositivo conectado à internet.<br>
  O painel pode ser acessado através desse link: https://zomato-restaurants-cds.streamlit.app/
  
### 6. Conclusão
  O objetivo desse projeto é criar um conjunto de gráficos e/ou tabelas
  que exibem essas métricas da melhor forma possível para o CEO.<br>
  Da visão da Empresa, podemos concluir que o número de pedidos
  Cresceu entre a semana 06 e a semana 13 do ano de 2022.<br>

### 7. Próximo passos
  1. Otimizar o código colocando as funções em um arquivo a parte;
  2. Reduzir o número de métricas.<br>
  3. Criar novos filtros.<br>
  4. Adicionar novas visões de negócio<br>
  5. Otimizar o banco de dados, eliminando colunas irrelevantes e adicionando colunas com dados originais e derivados que gerem maior valor ao negócio.
  6. A partir da coleta de dados dos clientes, implementar modelos de aprendizado de máquina preditivos e de recomendações.
  7. Adicionar novas visões de negócio.

