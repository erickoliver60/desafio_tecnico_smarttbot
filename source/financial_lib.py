import pandas as pd
import math
import datetime as dt


#Função que retorna um novo dataframe com o último Preço Ponderado de cada dia
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
		
		
#Função que encontra a Média Móvel Exponencial
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
	
	
#Função que encontra as Bandas de Bollinger
def GetBollinger(initial_date, ending_date, new_df):	
	
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
