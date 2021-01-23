import datetime as dt

#Função de Entrada de Dados
def InputDate():
	#Entrada da data de início
	date_entry = input()
	year, month, day = map(int, date_entry.split('-'))
	initial_date = dt.date(year, month, day)
	
	#Entrada da data de fim
	date_entry = input()
	year, month, day = map(int, date_entry.split('-'))
	ending_date = dt.date(year, month, day)
	
	return initial_date,ending_date
