import pandas as pd
import datetime as dt

#Função de Entrada de Dados
def InputDate(date_entry1="", date_entry2=""):
	#Entrada da data de início
	if(date_entry1 == ""):
		date_entry1 = input()	
	year, month, day = map(int, date_entry1.split('-'))
	initial_date = dt.date(year, month, day)
	
	#Entrada da data de fim
	if(date_entry2 == ""):
		date_entry2 = input()
	year, month, day = map(int, date_entry2.split('-'))
	ending_date = dt.date(year, month, day)
	
	return initial_date,ending_date

def OutputToCSV(Timestamp, MME, Inf, Center, Sup):
	
	output_df = pd.DataFrame(columns=['Timestamp','MME', 'Inferior Bollinger','Center Bollinger', 'Superior Bollinger']) #Criando dataframe de saída	
	output_df_row = pd.DataFrame({"Timestamp":[Timestamp], "MME":[*MME], "Inferior Bollinger":[Inf], "Center Bollinger":[Center], "Superior Bollinger":[Sup]}) #Escrevendo a linha com os valores encontrados
	output_df = output_df.append(output_df_row, ignore_index = True)  #Adicionando a linha ao novo dataframe
	
	output_df.to_csv('out.csv', index=False)
