import pandas as pd
import datetime as dt

def GetInputData(date_entry1="", date_entry2=""):
	
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

	output_df = pd.DataFrame(columns=['timestamp','indicador-0', 'indicador-1','indicador-2', 'indicador-3']) 	
	output_df_row = pd.DataFrame({"timestamp":[Timestamp], "indicador-0":[*MME], "indicador-1":[Inf], "indicador-2":[Center], "indicador-3":[Sup]}) 
	output_df = output_df.append(output_df_row, ignore_index = True)
	
	output_df.to_csv('out.csv', index=False)
