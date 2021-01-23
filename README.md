
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
O programa começa lendo o arquivo .csv e guardando as informações do arquivo em um dataframe usando funções da biblioteca pandas. Após isso, escolhemos fazer um tratamento dos dados, criamos duas novas colunas Date e Time, para guardar informações dos Timestamps convertidos, e também retiramos todos os valores NaN da coluna do Preço Ponderado, já que não poderíamos trabalhar com eles. 

Com o dataframe criado, é hora de receber a entrada do usuário que determinará o período que iremos trabalhar no programa, o programa então lê via linha de comandos as variáveis referentes a Data de início e Data de fim do período, ambas no formato "YYYY-MM-DD".

Agora que o programa já tem todas suas entradas definidas, chegou a hora de trabalhar com os dois indicadores técnicos que iremos representar no programa. A definição de ambos indicadores pode ser encontrada nos links abaixo:

<a href="https://www.bussoladoinvestidor.com.br/media-movel-exponencial/">Médias Móveis Exponeciais</a> 

<a href="https://www.bussoladoinvestidor.com.br/bandas-de-bollinger/">Bandas de Bollinger</a>

Com o período definido por datas, resolvemos considerar nosso período em dias, e para isso tomamos um valor de Preço Ponderado para representar cada dia do período dado. Para definir qual seria esse valor do Preço Ponderado, primeiramente pensamos em tirar a média dos Preços Ponderados de cada dia, porém devido a valores NaN, e o fato de precisarmos do Timestamp referente ao valor, teríamos problemas. Pensamos também na possibilidade de pegar o valor da mediana dos Preços Ponderados, pois assim teríamos o Timestamp relacionado, mas lendo sobre os dois indicadores, achamos melhor escolher o último valor de Preço Ponderado de cada dia que fosse diferente de NaN, pois este seria o Preço Ponderado que a bitcoin teoricamente fechou o dia, e assim poderíamos ter as Timestamps de cada Preço da mesma forma.

Criamos então uma função LastDailyPriceDF que nos entrega um novo dataframe apenas com os valores que iremos usar para ambos indicadores: Date, Time, Timestamp, e Weighted_Price. Agora temos um novo dataframe, mais enxuto apenas com as informações que escolhemos usar para nossos dois indicadores, que serão calculados em sequência.

Para calcular a Média Móvel Exponecial, agora que temos um valor por dia no dataframe, indexamos o dataframe por data, e selecionamos apenas os dias entre a Data de início e a Data de fim. Calculamos as três variáveis da fórmula do MME: Actual Price, MME Anterior(Média Móvel Simples até o dia anterior), e o multiplicador usando o número de dias do período. Com as varíaveis calculadas, apenas executamos a fórmula e retornamos o valor do MME para o período dado.

Para calcular as Bandas de Bollinger, fazemos o mesmo inicialmente com o dataframe, indexamos por data, e selecionamos os dias entre a Data de início e Data de fim para ser o período. Para gerar as Bandas de Bollinger, precisamos calcular apenas o Média Móvel Simples do período e o desvio padrão dos N dias do período. A banda superior de Bollinger será dada pela soma do MMS com o dobro do Desvio padrão, a banda inferior de Bollinger será dada pela subtração do MMS pelo dobro do Desvio Padrão, e o Centro de Bollinger é dado apenas pelo MMS do período. Normalmente o período de Bollinger é dado por 20 períodos, mas neste programa tomamos o cálculo para o número de períodos que for definido pela entrada. Em casos maiores ou iguais a 50 períodos, o Desvio padrão é multiplicado por 2,1, e em casos menores ou iguais a 10 períodos, o Desvio Padrão é multiplicado por 1.9, ao invés de simplesmente usarmos o dobro do Desvio Padrão no cálculo.

Com os valores calculados, as funções retornam as variáveis para o programa, que executa uma função de saída onde cria um dataframe no formato definido pelo problema (timestamp,indicador-0,indicador-1,indicador-2,...) e o escreve em um arquivo de saída .csv.

## 4 - Explicando as funções MME e  do programa

### Função MME

    def MME(initial_date, ending_date, new_df):	
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
	
	    #print('Media Movel Exponencial = ', *MME) 
    return MME

### Função Bollinger
      def Bollinger(initial_date, ending_date, new_df):	
	    new_df = new_df.set_index(['Date'])
	    new_df = new_df.loc[initial_date:ending_date]
	    new_df = new_df['Weighted_Price']

	    #MMS
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

    
## 5 - Saída

## 6 - Testes 
