import pandas as pd
import math
import datetime as dt

#-----------------------------------------------------------------------
#Funções que geram dataframes novos de acordo com a condição do valor do dia escolhido
def LastDailyPriceDF(initial_date, ending_date, df):	
	aux_date = initial_date #variável auxiliar que vamos usar como contador de datas
	new_df = pd.DataFrame(columns=['Date','Time','Weighted_Price']) #criando novo dataframe apenas com Data, Hora e Preços Ponderados
	
	while (aux_date <= ending_date): #Laço que vai da data inicial até a final para construir o novo dataframe
		df_date = df[df['Date'] == aux_date] #Usando o aux_date para definir o dia que está sendo construido
		df_date_row = df_date[df_date['Time'] == df_date['Time'].max()] #Pegando o última de Hora do dia cujo Preço Ponderado é diferente de todos os NaN
		df_date_row = df_date_row[['Date', 'Time','Weighted_Price']] #Escrevendo a linha do referente ao dia da Data atual, com Hora e Preço Ponderado
		new_df = new_df.append(df_date_row, ignore_index=True) #Adicionando a linha ao novo dataframe
		aux_date = aux_date + dt.timedelta(1) #Aumentando nosso contador de datas em 1 dia
		
	return new_df
	
def MeanDailyPriceDF(initial_date, ending_date, df):	
	aux_date = initial_date #variável auxiliar que vamos usar como contador de datas
	new_df = pd.DataFrame(columns=['Date','Weighted_Price']) #criando novo dataframe apenas com Data, Hora e Preços Ponderados
	
	while (aux_date <= ending_date): #Laço que vai da data inicial até a final para construir o novo dataframe
		df_date = df[df['Date'] == aux_date] #Usando o aux_date para definir o dia que está sendo construido
		mean_price = df_date['Weighted_Price'].mean() #Pegando o valor da média do Preço Ponderado do dia
		df_date_row = pd.DataFrame({"Date":[aux_date], "Weighted_Price":[mean_price]}) 
		#df_date_row = df_date_row[['Date', 'Weighted_Price']] 				
		new_df = new_df.append(df_date_row, ignore_index = True)  #Adicionando a linha ao novo dataframe
		aux_date = aux_date + dt.timedelta(1) #Aumentando nosso contador de datas em 1 dia
		
	return new_df
	
	
#-----------------------------------------------------------------------
#Função que encontra a Média Móvel Exponencial
def MME(initial_date, ending_date, new_df):	
	#MME = [Preço Atual + MME(anterior)]*K + MME(anterior)
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

	print('Media Movel Exponencial = ', *MME) 

#-----------------------------------------------------------------------
#Função que encontra o Índice de Força Relativa (IFR)
#def IFR(initial_date, ending_date, new_df):	
	#IFR = (100 - (100/(1+(U/D)))
	#print(new_df)
	#U
	#D


#----------------------------------------------------------------------------
#Função que encontra as Bandas de Bollinger
def Bollinger(initial_date, ending_date, new_df):	
	new_df = new_df.set_index(['Date'])
	new_df = new_df.loc[initial_date:ending_date]
	new_df = new_df['Weighted_Price']

	#MMS
	MMS = new_df.mean()

	#Desvio Padrão
	number_days = (ending_date - initial_date).days

	if(number_days <= 10):
		std_deviation = (1.9)*new_df.std()
	elif(number_days >= 50):
		std_deviation = (2.1)*new_df.std()
	else:
		std_deviation = (2)*new_df.std()

	#Banda Superior = Média Móvel Simples (20 dias) + (2 x Desvio Padrão de 20 dias)
	Sup_Bollinger = MMS + std_deviation
	
	print('Banda Superior de Bollinger = ', Sup_Bollinger)
	#Banda Inferior = Média Móvel Simples (20 dias) – (2 x Desvio Padrão de 20 dias)
	Inf_Bollinger = MMS - std_deviation
	print('Banda Inferior de Bollinger = ', Inf_Bollinger)
