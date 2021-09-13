from src import balance_sheet_class
from src import income_statement_class
from src import cash_flow_class

from utils import *

import traceback

# from utils import convert_cash_flow, convert_balance_sheet


def roman_number(lineitem: str) -> str:
	"""
 
	To remove roman numbers from lineitem

	Parameters
	----------
	lineitem : str
		Input string of lineitem


	Returns
	-------
	sentance : str

	"""
	roman = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]
	remove_items = [".", "-", "+", "/", "(", ")", "*"]
	str_ = ''.join([c for c in lineitem if c not in remove_items])
	print(str_)
	sentance = ""
	for i in str_.split():
		if i.upper() in roman:
			pass
		else:
			sentance += i + " "
	return sentance





def balance_sheet_service(DATA: dict, input_filename: str, dynamic_data: dict) -> dict:
	"""
 
	To find balance sheet lineitems

	Parameters
	----------
	Data : dict
		Input dictionary of balance sheet
	input_filename:
		Input fileanme
	dynamic_data: dict
		Input for dynamic template


	Returns
	-------
	balance_sheet :  dict

	"""
	type_=""

	if not isinstance(DATA, dict) and not isinstance(input_filename,str) and not isinstance(dynamic_data,dict):
			raise TypeError


	try:
		
		# logger.info("balance_sheet started")
		print("TEST DATA-------------------------------------")
		# print (DATA)
		print(input_filename)
		# print(dynamic_data)



		if DATA['Source']['annualReportType'] in 'T-form (Tally)' or DATA['Source']['annualReportType'] in 'T-form (Others)':
			print("Document type ",'T-form_Tally')
			type_ = 'T-form_Tally'

		elif 'schedule'  in DATA['Source']['annualReportType'].lower() or DATA['Source']['annualReportType'] in 'Other vertical format':
			print("Document type",'Schedule-III')
			type_ = 'Schedule-III'
		datasource= DATA['Source']['annualReportType']

		print(type_,DATA['Source'])

		# balance_sheet = convert_balance_sheet(DATA)
		# balance_sheet_cls = balance_sheet_class.balance_sheet_lineitems(balance_sheet,type_,datasource)
		balance_sheet_cls = balance_sheet_class.balance_sheet_lineitems_(DATA,type_,datasource)

	except Exception as e:
		print(traceback.print_exc())
		print(e)
		# logger.error(e)
		balance_sheet_cls=[]

	# print (balance_sheet,"ENNNNNNNNNNNNNNNNNNNNNNNNN BS")
	return balance_sheet_cls


def income_statement_service(DATA: dict, input_filename: str, dynamic_data: dict) -> dict:
	"""
 
	To find income_statement lineitems

	Parameters
	----------
	Data : dict
		Input dictionary of income statement
	input_filename:
		Input fileanme
	dynamic_data: dict
		Input for dynamic template


	Returns
	-------
	income_statement :  dict

	"""
	type_=""

	if not isinstance(DATA, dict) and not isinstance(input_filename,str) and not isinstance(dynamic_data,dict):
		raise TypeError

	try:
		#income_statement,source= convert_income_statement(DATA)
		print("HELLO-------------------------------------")
		# try:
		if DATA['Source']['annualReportType'] in 'T-form (Tally)' or DATA['Source']['annualReportType'] in 'T-form (Others)':
			print('T-form_Tally')
			type_ = 'T-form_Tally'

		elif 'schedule'  in DATA['Source']['annualReportType'].lower() or DATA['Source']['annualReportType'] in 'Other vertical format':
			print('Schedule-III')
			type_ = 'Schedule-III'
		datasource= DATA['Source']['annualReportType']
		print(type_,DATA['Source'])
		income_statement_cls = income_statement_class.income_statement_lineitems(DATA,type_,datasource)
		#income_statement_cls = signage_rule_IS(income_statement_cls)
		#DATA_IS = calculated_field_is(DATA)

		#print(income_statement_cls, "ENNNNNNNNNNNNNNNNNNNNNN IS")

	except Exception as e:
		print(traceback.print_exc())
		print(e)
		income_statement_cls = []
	# 	logger.error(e)

	return income_statement_cls


def cash_flow_service(DATA: dict, input_filename: str, dynamic_data: dict) -> dict:
	"""
 
	To find cash flow lineitems

	Parameters
	----------
	Data : dict
		Input dictionary of cash flow
	input_filename:
		Input fileanme
	dynamic_data: dict
		Input for dynamic template


	Returns
	-------
	cash_flow :  dict

	"""
	if not isinstance(DATA, dict) and not isinstance(input_filename,str) and not isinstance(dynamic_data,dict):
		raise TypeError
	try:

		# cash_flow = convert_cash_flow(DATA)
		# print(cash_flow)
		# cash_flow_cls = cash_flow_class.cash_flow_lineitems(cash_flow)
		# print(cash_flow_cls,"class nei")
		# cash_flow_cls = signage_rule_CF(cash_flow_cls)
		#DATA_CF = calculated_field_cf(DATA)

		print("NO CF")
		cash_flow_cls = []

	except Exception as e:
		print(traceback.print_exc())
		print(e)
		# logger.error(e)
		cash_flow = []

	# print (cash_flow,"ENNNNNNNNNNNNNNNNNNNNNNNN CF")
	return cash_flow_cls
