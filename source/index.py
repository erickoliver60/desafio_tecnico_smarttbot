import pandas as pd
import datetime as dt
import io_lib
import financial_lib

def main():
	df = pd.read_csv('bitstampUSD_1-min_data_2012-01-01_to_2020-12-31.csv')
	df['Date'] = pd.to_datetime(df['Timestamp'],unit='s').apply(lambda x: x.date())
	df['Time'] = pd.to_datetime(df['Timestamp'],unit='s').apply(lambda x: x.time())

	#Retirando todos os valores NaN do dataframe
	df = df[df['Weighted_Price'].notna()]	
	
	initial_date, ending_date = io_lib.GetInputData()	

	#Criando um dataframe com as informações de Data, Hora e Preços Ponderados, onde mostra a Hora e o Valor do ÚLTIMO Preço Ponderado de cada dia	
	new_df = financial_lib.GetClosingPricePerDay(initial_date, ending_date, df)
		
	MME = financial_lib.GetMME(initial_date, ending_date, new_df)

	Sup_Bollinger, Center_Bollinger, Inf_Bollinger = financial_lib.GetBollinger(initial_date, ending_date, new_df)
	
	#Salvando o timestamp do último período
	Timestamp = new_df['Timestamp'].iloc[-1]
		
	io_lib.OutputToCSV(Timestamp, MME, Inf_Bollinger, Center_Bollinger, Sup_Bollinger)
	
if __name__ == "__main__":
	main()
