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

	#Criando um dataframe com as informações de Data, Hora e Preços Ponderados, onde mostra a Hora e o Valor do ÚLTIMO Preço Ponderado de cada dia	
	new_df = financial_lib.LastDailyPriceDF(initial_date, ending_date, df)
		
	#Media movel exponencial (MME)
	MME = financial_lib.MME(initial_date, ending_date, new_df)

	#Bandas de Bollinger
	Sup_Bollinger, Center_Bollinger, Inf_Bollinger = financial_lib.Bollinger(initial_date, ending_date, new_df)
	
	#Salvando o timestamp do último período
	Timestamp = new_df['Timestamp'].iloc[-1]
		
	#Escrevendo saída encontrada no arquivo .csv
	io_lib.OutputToCSV(Timestamp, MME, Inf_Bollinger, Center_Bollinger, Sup_Bollinger)
	
	print('Timestamp de Bollinger = ', Timestamp)
	print('MME de Bollinger = ', *MME)
	print('Banda Inferior de Bollinger = ', Inf_Bollinger)
	print('Centro de Bollinger = ', Center_Bollinger)
	print('Banda Superior de Bollinger = ', Sup_Bollinger)
	
	
if __name__ == "__main__":
	main()
