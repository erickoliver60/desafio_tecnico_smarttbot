import pandas as pd
import datetime as dt
import io_lib
import financial_lib
from index import control 
from error_lib import InputTypeError, InvalidInputError

def test_Valid_SmallInput():

	initial_date = dt.date(2015, 6, 1)
	end_date = dt.date(2015, 7, 1)
	
	errors = []
	Timestamp, MME, Inf, Center, Sup = control(initial_date, end_date) 
	
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
	
def test_Invalid_EmptyInput():
		
	try:
		control('','')		
		assert False
	except InputTypeError:
		assert True
		
	
def test_Invalid_InvalidInput():
	initial_date = dt.date(2018, 1, 1)
	end_date = dt.date(2017, 3, 8)	
	
	try:
		control(initial_date,end_date)
		assert False
	except InvalidInputError:
		assert True

		
def test_Valid_BigInput():
	initial_date = dt.date(2013, 12, 25)
	end_date = dt.date(2014, 12, 25)
	
	errors = []
	Timestamp, MME, Inf, Center, Sup = control(initial_date, end_date) 
	
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
