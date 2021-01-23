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
	


