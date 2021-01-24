import pandas as pd
import datetime as dt
import io_lib
import financial_lib


#Teste 
def main(date_entry1,date_entry2):

	df = pd.read_csv('bitstampUSD_1-min_data_2012-01-01_to_2020-12-31.csv')
	df['Date'] = pd.to_datetime(df['Timestamp'],unit='s').apply(lambda x: x.date())
	df['Time'] = pd.to_datetime(df['Timestamp'],unit='s').apply(lambda x: x.time())

	#Retirando todos os valores NaN do dataframe
	df = df[df['Weighted_Price'].notna()]	
	
	initial_date, ending_date = io_lib.GetInputData(date_entry1,date_entry2)	
	
	#Criando um dataframe com as informações de Data, Hora e Preços Ponderados, onde mostra a Hora e o Valor do ÚLTIMO Preço Ponderado de cada dia	
	new_df = financial_lib.GetClosingPricePerDay(initial_date, ending_date, df)
		
	MME = financial_lib.GetMME(initial_date, ending_date, new_df)

	Sup_Bollinger, Center_Bollinger, Inf_Bollinger = financial_lib.GetBollinger(initial_date, ending_date, new_df)
	
	#Salvando o timestamp do último período
	Timestamp = new_df['Timestamp'].iloc[-1]
		
	io_lib.OutputToCSV(Timestamp, MME, Inf_Bollinger, Center_Bollinger, Sup_Bollinger)
	
	return Timestamp, MME, Inf_Bollinger, Center_Bollinger, Sup_Bollinger

def test_1():
	errors = []
	Timestamp, MME, Inf, Center, Sup = main('2015-06-01','2015-07-01') 
	
	if not (Timestamp == 1435795140):
		errors.append("Timestamp diferente do esperado")
	if not (MME == 269.37031471077415):
		errors.append("MME diferente do esperado")
	if not (Inf == 214.74678313115):
		errors.append("Banda Inferior de Bollinger diferente do esperado")
	if not (Center == 238.08349054709674):
		errors.append("Centro de Bollinger diferente do esperado")
	if not (Sup == 261.4201979630435):
		errors.append("Banda Superior de Bollinger diferente do esperado")
		
	assert not errors, "Erros encontrados: \n{}".format("\n".join(errors))
	
def test_2():
	errors = []
	Timestamp, MME, Inf, Center, Sup = main('2013-04-11','2013-12-11') 
	
	if not (Timestamp == 1386806340):
		errors.append("Timestamp diferente do esperado")
	if not (MME == 210.72042690171048):
		errors.append("MME diferente do esperado")
	if not (Inf == -294.1850124699172):
		errors.append("Banda Inferior de Bollinger diferente do esperado")
	if not (Center == 204.65869997176736):
		errors.append("Centro de Bollinger diferente do esperado")
	if not (Sup == 703.5024124134519):
		errors.append("Banda Superior de Bollinger diferente do esperado")
		
	assert not errors, "Erros encontrados: \n{}".format("\n".join(errors))
	
def test_3():
	errors = []
	Timestamp, MME, Inf, Center, Sup = main('2017-01-01','2017-03-08') 
	if not (Timestamp == 1489017540):
		errors.append("Timestamp diferente do esperado")
	if not (MME == 1077.516178660848):
		errors.append("MME diferente do esperado")
	if not (Inf == 740.6247898335114):
		errors.append("Banda Inferior de Bollinger diferente do esperado")
	if not (Center == 1015.0036271467163):
		errors.append("Centro de Bollinger diferente do esperado")
	if not (Sup == 1289.3824644599213):
		errors.append("Banda Superior de Bollinger diferente do esperado")
		
	assert not errors, "Erros encontrados: \n{}".format("\n".join(errors))

def test_4():
	errors = []
	Timestamp, MME, Inf, Center, Sup = main('2018-02-07','2018-02-17') 
	if not (Timestamp == 1518911940):
		errors.append("Timestamp diferente do esperado")
	if not (MME == 12451.551740982724):
		errors.append("MME diferente do esperado")
	if not (Inf == 7028.804792352296):
		errors.append("Banda Inferior de Bollinger diferente do esperado")
	if not (Center == 9034.71112942727):
		errors.append("Centro de Bollinger diferente do esperado")
	if not (Sup == 11040.617466502244):
		errors.append("Banda Superior de Bollinger diferente do esperado")
		
	assert not errors, "Erros encontrados: \n{}".format("\n".join(errors))

def test_5():
	errors = []
	Timestamp, MME, Inf, Center, Sup  = main('2013-12-25','2014-12-25') 
	
	if not (Timestamp == 1419551820):
		errors.append("Timestamp diferente do esperado")
	if not (MME == 537.3553184222754):
		errors.append("MME diferente do esperado")
	if not (Inf == 231.17201572772177):
		errors.append("Banda Inferior de Bollinger diferente do esperado")
	if not (Center == 532.1150112658196):
		errors.append("Centro de Bollinger diferente do esperado")
	if not (Sup == 833.0580068039174):
		errors.append("Banda Superior de Bollinger diferente do esperado")
		
	assert not errors, "Erros encontrados: \n{}".format("\n".join(errors))
