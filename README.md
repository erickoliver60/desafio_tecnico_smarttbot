
# Desafio Técnico - Smarttbot
## 1 - Introdução
<right>O programa presente neste projeto tem como objetivo calcular os indicadores técnicos de Médias Móveis Exponeciais e as Bandas de Bollinger de um dataset que informa atualizações por minuto dos valores OHLC (Aberto, Alto, Baixo, Fechado), Volume(em Bitcoin e da moeda indicada), e o Preço Ponderado de Bitcoin do período de janeiro de 2012 a dezembro de 2020.</right>

Para escrever o programa, foram utilizadas a versão 3.8.5 do Python e as seguintes bibliotecas:
- pandas
- math
- datetime
- matplotlib


## 2 - O Desafio
Este desafio técnico proposto pela Smarttbot. O programa deverá calcular pelo menos dois indicadores técnicos abaixo para um período arbitrário contido no dataset: https://www.kaggle.com/mczielinski/bitcoin-historical-data/data#coinbaseUSD_1-min_data_2014-12-01_to_2019-01-09.csv.

Os indicadores técnicos que podem ser calculados são:
- Médias Móveis Exponenciais
- Índice de Força Relativa
- Bandas de Bollinger

O projeto do programa deverá ser criado e gerenciado usando git, podendo usar um provedor gratuito como Github, Gitlab e Bitbucket. O projeto deve estar como público ou fornecer as permissões necessárias para acesso.

O programa deverá ser escrito em Python 3.7+, rodar em Linux e ser compatível com os parâmetros de entrada e saída.

##### Parâmetros de Entrada
Juntamente com o dataset citado anteriormente, a aplicação receberá como input dois argumentos via linhas de comando:
- Data de início
- Data de fim

##### Parâmetros de Saída
O arquivo de saída será um arquivo CSV com o seguinte formato:
-timestamp,indicador-0,indicador-1,indicador-2,...

## 3 - Tomadas de decisão de implementação
O programa começa lendo via linha de comandos as variáveis referentes a <b>Data de início</b> e <b>Data de fim</b> do período, ambas no formato <b>"YYYY-MM-DD"</b>, e logo em seguida já faz uma autenticação para entrada válida. Feito isto, o programa então lê o dataset do arquivo .csv, guardando as informações do arquivo em um dataframe usando funções da biblioteca <i>pandas</i>. Com todas as entradas lidas, fazemos um tratamento dos dados do dataframe, criamos duas novas colunas 'Date' e 'Time', para guardar informações dos 'Timestamps' convertidos, e também retiramos todos os valores NaN da coluna dos Preço Ponderados('Weighted_Prices'), já que não poderíamos trabalhar com eles. Com o dataframe criado, usamos a entrada das datas de início e fim do usuário para determinar o período que iremos trabalhar no programa. 

Agora que o programa já tem todas suas entradas definidas, chegou a hora de trabalhar com os dois indicadores técnicos que iremos representar no programa. A definição de ambos indicadores pode ser encontrada nos links abaixo:

<a href="https://www.bussoladoinvestidor.com.br/media-movel-exponencial/">Médias Móveis Exponeciais</a> 

<a href="https://www.bussoladoinvestidor.com.br/bandas-de-bollinger/">Bandas de Bollinger</a>

Com o período definido por datas, resolvemos considerar nosso período em dias, e para isso tomamos um valor de Preço Ponderado para representar cada dia do período dado. Para definir qual seria esse valor do Preço Ponderado, primeiramente pensamos em tirar a média dos Preços Ponderados de cada dia, porém devido a valores NaN, e o fato de precisarmos do Timestamp referente ao valor, teríamos problemas. Pensamos também na possibilidade de pegar o valor da mediana dos Preços Ponderados, pois assim teríamos o Timestamp relacionado, mas lendo sobre os dois indicadores, achamos melhor escolher o último valor de Preço Ponderado de cada dia que fosse diferente de NaN, pois este seria o Preço Ponderado que a bitcoin teoricamente fechou o dia, e assim poderíamos ter as Timestamps de cada Preço da mesma forma.

Criamos então uma função <b>GetClosingPricePerDay</b> que nos entrega um novo dataframe apenas com os valores que iremos usar para ambos indicadores: Date, Time, Timestamp, e Weighted_Price. Agora temos um novo dataframe, mais enxuto apenas com as informações que escolhemos usar para nossos dois indicadores, que serão calculados em sequência.

Para calcular a <b>Média Móvel Exponecial</b>, agora que temos um valor por dia no dataframe, indexamos o dataframe por data, e selecionamos apenas os dias entre a Data de início e a Data de fim. Calculamos as três variáveis da fórmula do MME: Actual Price, MME Anterior(Média Móvel Simples até o dia anterior), e o multiplicador usando o número de dias do período. Com as varíaveis calculadas, apenas executamos a fórmula e retornamos o valor do MME para o período dado.

Para calcular as <b>Bandas de Bollinger</b>, fazemos o mesmo inicialmente com o dataframe, indexamos por data, e selecionamos os dias entre a Data de início e Data de fim para ser o período. Para gerar as Bandas de Bollinger, precisamos calcular apenas o Média Móvel Simples do período e o desvio padrão dos N dias do período. A banda superior de Bollinger será dada pela soma do MMS com o dobro do Desvio padrão, a banda inferior de Bollinger será dada pela subtração do MMS pelo dobro do Desvio Padrão, e o Centro de Bollinger é dado apenas pelo MMS do período. Normalmente o período de Bollinger é dado por 20 períodos, mas neste programa tomamos o cálculo para o número de períodos que for definido pela entrada. Em casos maiores ou iguais a 50 períodos, o Desvio padrão é multiplicado por 2.1, e em casos menores ou iguais a 10 períodos, o Desvio Padrão é multiplicado por 1.9, ao invés de simplesmente usarmos o dobro do Desvio Padrão no cálculo.

Com os valores calculados, as funções retornam as variáveis para o programa, que executa a função de saída <b>OutputToCSV</b> onde cria um dataframe no formato definido pelo problema (timestamp,indicador-0,indicador-1,indicador-2,indicador-3) e o escreve em um arquivo de saída .csv.


## 4 - Explicando as funções do arquivo financial_lib.py

### Função GetClosingPricePerDay
	def GetClosingPricePerDay(initial_date, ending_date, df):	
	
		aux_date = initial_date 
		new_df = pd.DataFrame(columns=['Date','Time', 'Timestamp','Weighted_Price'])
		
		while (aux_date <= ending_date): 
			df_date = df[df['Date'] == aux_date] #Usando o aux_date para definir o dia de interesse da linha
			df_date_row = df_date[df_date['Time'] == df_date['Time'].max()] #Pegando o última de Hora do dia cujo Preço Ponderado é diferente de todos os NaN
			df_date_row = df_date_row[['Date', 'Time', 'Timestamp', 'Weighted_Price']] 
			new_df = new_df.append(df_date_row, ignore_index=True)
		
			aux_date = aux_date + dt.timedelta(1) 
		
		return new_df

A função <b>GetClosingPricePerDay</b> representada acima recebe a Data de início e a Data de fim dada pelo usuário, e o dataframe já tratado pela função control. Primeiramente criamos uma variável auxiliar que recebe o valor da Data de início, e em seguida criamos um novo dataframe vazio, apenas com 4 colunas que usaremos no programa: Date, Time, Timestamp e Weighted_Price. 

Fazemos um laço que vai da Data de início até a Data de fim. Linha por linha, vamos selecionando o Dia do momento, e pegamos o último horário do dia com Preço Ponderado disponível. Criamos então uma linha com a Data do dia, a Hora do último Preço Ponderado, o Timestamp referente a esta Data e Hora, e o valor do Preço Ponderado deste Timestamp. Adicionamos essa linha no dataframe novo, e iteramos, fazendo isso para todos os dias do período entre a Data de início e a Data de fim. Terminado o laço, retornamos o novo dataframe preenchido.


### Função MME
	def GetMME(initial_date, ending_date, new_df):
	
		new_df = new_df.set_index(['Date'])
		new_df = new_df.loc[initial_date:ending_date]

		#Preço atual
		actualprice = (new_df['Weighted_Price'].iloc[-1:]).values
 
		#MME(anterior) = MMS
		previous_day = ending_date - dt.timedelta(1)
		new_df_MMS = new_df.loc[initial_date:previous_day]
		new_df_MMS = new_df_MMS['Weighted_Price']
		MMS = new_df_MMS.mean()

		#Multiplicador K
		number_days = (ending_date - initial_date).days
		K = 2 / (1+number_days)

		#MME = [Preço Atual + MME(anterior)]*K + MME(anterior)
		MME = (actualprice + MMS)*K + MMS
	
		return MME

A função <b>MME</b> recebe a Data de início e a Data de fim dada pelo usuário, e o novo dataframe criado pela função GetClosingPricePerDay. Logo de inicio, já indexamos a coluna 'Date', e restringimos o dataframe no período entre as Datas de início e fim. Após isso, determinamos o valor das váriáveis que usaremos na fórmula do MME. Primeiro, a variavel do Preço Atual, depois calculamos o MMS da Data de início até o dia anterior da Data de fim, usando o valor dos Preços Ponderados deste período e tirando a média entre eles, e por último calculamos o multiplicador K, determinado por <i>2/(1 + número de períodos)</i>, e como nossos períodos são dias, logo fica <i>K = 2/(1 + número de dias)</i>.

Com os valores calculados, é efetuado o cálculo da fórmula do MME, e então a função retorna o valor da Média Móvel Exponencial.
 
 
### Função Bollinger
	def GetBollinger(initial_date, ending_date, new_df):	
	
		new_df = new_df.set_index(['Date'])
		new_df = new_df.loc[initial_date:ending_date]		

		#MMS
		new_df = new_df['Weighted_Price']
		MMS = new_df.mean()

		#Desvio Padrão
		number_days = (ending_date - initial_date).days

		#Curto prazo, usar 10 dias
		if(number_days <= 10):
			std_deviation = (1.9)*new_df.std()
		#Longo prazo, usar 50 dias
		elif(number_days >= 50):
			std_deviation = (2.1)*new_df.std()
		#Prazo padrão, usar 20 dias
		else:
			std_deviation = (2)*new_df.std()

		#Banda Superior = Média Móvel Simples (20 dias) + (2 x Desvio Padrão de 20 dias)
		Sup_Bollinger = MMS + std_deviation
	
		#Centro de Bollinger = Média Móvel Simples (20 dias)
		Center_Bollinger = MMS
	
		#Banda Inferior = Média Móvel Simples (20 dias) – (2 x Desvio Padrão de 20 dias)
		Inf_Bollinger = MMS - std_deviation
	
		return Sup_Bollinger, Center_Bollinger, Inf_Bollinger

A função <b>Bollinger</b> também recebe a Data de início e a Data de fim dada pelo usuário, e o novo dataframe criado pela função GetClosingPricePerDay. Como na função MME, indexamos a coluna 'Date' e determinamos que o dataframe será apenas o período entre a Data de início e a Data de fim. Para calcular as bandas de Bollinger, a primeira coisa que fazemos é tirar a média dos Preços Ponderados de todos os dias do período, achando assim o MMS do período. Depois calculamos o desvio padrão deste mesmo período. Com o MMS e o desvio padrão, podemos agora calcular Bollinger, porém antes vamos analisar os casos em que o período é menor que 10 dias e maior que 50 dias. Neste caso, a fórmula que tem mudança no multiplicador do desvio padrão. Caso o período seja maior que 50 dias, então o multiplicador 2 se torna 2.1, e caso seja menor que 10 dias, o multiplicador se torna 1.9. Após analisar as condições, nós efetuamos a fórmula para a Banda Superior, <i>Banda Superior = MMS + (Multplicador x Desvio Padrão)</i>, para o Centro de Bollinger, <i>Centro = MMS</i>, e para Banda Inferior de Bollinger, <i>Banda Inferior = MMS - (Multplicador x Desvio Padrão)</i>.

Com os cálculos executados, a função retorna os três valores, Banda Superior de Bollinger, Centro de Bollinger e Banda Inferior de Bollinger.

    
## 5 - Saída
A função <b>OutputToCSV</b> gera como saída do programa um arquivo .csv com o header: (timestamp, indicador-0, indicador-1, indicador-2, indicador-3). Os indicadores que aparecem na saída remetem a:
- Timestamp: É o valor da coluna Timestamp que já é fornecido pelo dataset de entrada. O Timestamp está em formato Unix, e refere-se ao Timestamp do último dia do período.
- indicador-0: É a Média Móvel Exponencial do período, e é um valor numérico no formato float64.
- indicador-1: É a Banda Inferior de Bollinger do período, e é um valor numérico no formato float64.
- indicador-2: É o Centro de Bollinger do período, e é um valor numérico no formato float64.
- indicador-3: É a Banda Superior de Bollinger do período, e é um valor numérico no formato float64.


## 6 - Testes Automáticos

Foram feitos um total de 4 testes para verificar se o programa trata os possíveis erros que possam ocorrer. O arquivo de testes <b>index_test.py</b> foi feito usando o framework de testes <i>pytest</i> e todos os testes passaram, segue abaixo uma explicação sobre cada um deles.

No primeiro teste, fazemos um teste básico para verificarmos se o programa, com uma entrada válida de período pequeno, gera uma saída a esperada. No segundo teste, verificamos se o programa trata o caso onde a entrada é vazia ou se a entrada passa um valor de tipo de variável diferente do esperado. No terceiro teste, verificamos se o programa trata o erro do caso em que a Data de início é maior que a Data de fim. E por fim no quarto teste, temos novamente outro teste para verificarmos se o programa gera saída esperada com entrada vália, porém desta vez com um período maior. 







###### - Contato
Para quaisquer dúvidas e/ou erros presentes sobre o código, entre em contato comigo pelo e-mail: <b>erick.oliver60@gmail.com</b>
