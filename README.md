# Desafio Técnico - Smarttbot
## 1 - Introdução
Este problema é resultado de um desafio técnico proposto pela Smarttbot. 

O objetivo desta aplicação é calcular pelo menos dois indicadores técnicos abaixo para um período arbitrário contido no dataset: https://www.kaggle.com/mczielinski/bitcoin-historical-data/data#coinbaseUSD_1-min_data_2014-12-01_to_2019-01-09.csv.

Os indicadores técnicos que podem ser calculados são:
- Médias Móveis Exponenciais
- Índice de Força Relativa
- Bandas de Bollinger

O projeto deverá ser criado e gerenciado usando git, podendo usar um provedor gratuito como Github, Gitlab e Bitbucket. O projeto deve estar como público ou fornecer as permissões necessárias para acesso.

O programa deverá ser escrito em Python 3.7+, rodar em Linux e ser compatível com os parâmetros de entrada e saída.

##### Parâmetros de Entrada
Juntamente com o dataset citado anteriormente, a aplicação receberá como input dois argumentos via linhas de comando:
- Data de início
- Data de fim

##### Parâmetros de Saída
O arquivo de saída será um arquivo CSV com o seguinte formato:
-timestamp,indicador-0,indicador-1,indicador-2,...


