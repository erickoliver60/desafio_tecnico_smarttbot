import pandas as pd
import datetime as dt

import io_lib
import financial_lib

#----------------------------------------------------------------------------
#Teste Desafio Smarttbot
def main(date_entry1,date_entry2):
	#Lendo o dataframe
	df = pd.read_csv('bitstampUSD_1-min_data_2012-01-01_to_2020-12-31.csv')
	df['Date'] = pd.to_datetime(df['Timestamp'],unit='s').apply(lambda x: x.date())
	df['Time'] = pd.to_datetime(df['Timestamp'],unit='s').apply(lambda x: x.time())

	#Retirando todos os valores NaN do dataframe
	df = df[df['Weighted_Price'].notna()]	
	
	#Recebendo a entrada de datas de inicio e fim
	initial_date, ending_date = io_lib.InputDate(date_entry1,date_entry2)	
	
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
	MME = financial_lib.MME(initial_date, ending_date, new_df)
		
	#Índice de Força Relativa (IFR)
	#IFR = financial_lib.IFR(initial_date, ending_date, new_df)
			
	#Bandas de Bollinger
	Sup_Bollinger, Inf_Bollinger = financial_lib.Bollinger(initial_date, ending_date, new_df)	

	print("Media Movel Exponencial = ", *MME)
	print("Banda Inferior de Bollinger = ", Inf_Bollinger)
	print("Banda Superior de Bollinger = ", Sup_Bollinger)	
	
	return MME, Inf_Bollinger, Sup_Bollinger

def test_1():
	errors = []
	MME, Inf, Sup  = main('2015-06-01','2015-07-01') 
	
	if not (MME == 269.37031471077415):
		errors.append("MME diferente do esperado")
	if not (Inf == 214.74678313115):
		errors.append("Banda Inferior de Bollinger diferente do esperado")
	if not (Sup == 261.4201979630435):
		errors.append("Banda Superior de Bollinger diferente do esperado")
		
	assert not errors, "Erros encontrados: \n{}".format("\n".join(errors))
	
def test_2():
	errors = []
	MME, Inf, Sup  = main('2013-04-11','2013-12-11') 
	
	if not (MME == 210.72042690171048):
		errors.append("MME diferente do esperado")
	if not (Inf == -294.1850124699172):
		errors.append("Banda Inferior de Bollinger diferente do esperado")
	if not (Sup == 703.5024124134519):
		errors.append("Banda Superior de Bollinger diferente do esperado")
		
	assert not errors, "Erros encontrados: \n{}".format("\n".join(errors))
	
def test_3():
	errors = []
	MME, Inf, Sup  = main('2017-01-01','2017-03-08') 
	
	if not (MME == 1077.516178660848):
		errors.append("MME diferente do esperado")
	if not (Inf == 740.6247898335114):
		errors.append("Banda Inferior de Bollinger diferente do esperado")
	if not (Sup == 1289.3824644599213):
		errors.append("Banda Superior de Bollinger diferente do esperado")
		
	assert not errors, "Erros encontrados: \n{}".format("\n".join(errors))

def test_4():
	errors = []
	MME, Inf, Sup  = main('2018-02-07','2018-02-17') 
	
	if not (MME == 12451.551740982724):
		errors.append("MME diferente do esperado")
	if not (Inf == 7028.804792352296):
		errors.append("Banda Inferior de Bollinger diferente do esperado")
	if not (Sup == 11040.617466502244):
		errors.append("Banda Superior de Bollinger diferente do esperado")
		
	assert not errors, "Erros encontrados: \n{}".format("\n".join(errors))

def test_5():
	errors = []
	MME, Inf, Sup  = main('2013-12-25','2014-12-25') 
	
	if not (MME == 537.3553184222754):
		errors.append("MME diferente do esperado")
	if not (Inf == 231.17201572772177):
		errors.append("Banda Inferior de Bollinger diferente do esperado")
	if not (Sup == 833.0580068039174):
		errors.append("Banda Superior de Bollinger diferente do esperado")
		
	assert not errors, "Erros encontrados: \n{}".format("\n".join(errors))
