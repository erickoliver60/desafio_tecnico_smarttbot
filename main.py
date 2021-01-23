import pandas as pd
import datetime as dt

import io_lib
import financial_lib

#----------------------------------------------------------------------------
#Main
def main():
	#Lendo o dataframe
	df = pd.read_csv('bitstampUSD_1-min_data_2012-01-01_to_2020-12-31.csv')
	df['Date'] = pd.to_datetime(df['Timestamp'],unit='s').apply(lambda x: x.date())
	df['Time'] = pd.to_datetime(df['Timestamp'],unit='s').apply(lambda x: x.time())

	#Retirando todos os valores NaN do dataframe
	df = df[df['Weighted_Price'].notna()]	
	
	#Recebendo a entrada de datas de inicio e fim
	initial_date, ending_date = io_lib.InputDate()	
	
	#Escolher o valor da condição entre preço médio do dia e último preço do dia
	#condition = 'meanprice'
	conditionvalue = 'lastprice'
	if (conditionvalue == 'lastprice'):
		#Criando um dataframe com as informações de Data, Hora e Preços Ponderados, onde mostra a Hora e o Valor do ÚLTIMO Preço Ponderado de cada dia	
		new_df = financial_lib.LastDailyPriceDF(initial_date, ending_date, df)
	
	elif(condition == 'meanprice'):
		#Criando um dataframe apenas com as informações de Data, Hora e Preços Ponderados, onde mostra a Hora e o Valor do Preço Ponderado MÉDIO de cada dia
		new_df = financial_lib.MeanDailyPriceDF(initial_date, ending_date, df)
	
	#Media movel exponencial (MME)
	financial_lib.MME(initial_date, ending_date, new_df)
		
	#Índice de Força Relativa (IFR)
	#financial_lib.IFR(initial_date, ending_date, new_df)
			
	#Bandas de Bollinger
	financial_lib.Bollinger(initial_date, ending_date, new_df)
		

if __name__ == "__main__":
	main()
