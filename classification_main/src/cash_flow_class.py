import pandas  as pd
import numpy as np
from utils import yaml_parse
from fuzzywuzzy import fuzz
from datetime import datetime
import os,sys
import logging
global logger


def blockPrint():
	sys.stdout = open(os.devnull, 'w')

def normalize(a : str) -> float:
	"""
 
	To get the string and convert into float removing irrelevantchar value
 
	Parameters
	----------
	a : str
		string value   

	Returns
	-------
	float
		float number removing irrelevant char value
 
	""" 
	try:
		if len(a)==0 or len(a)>=15:
			return 0.0

		else:
			# a=[i.replace("(","-").replace(")","").replace("$","").replace(",","").replace("—","0").replace(" ","0") for i in a if "("]
			# a="".join(a)

			# return(float(a))

			a_temp= []
			for i in a:
				if "(":
					a_temp.append(i.replace("(","-").replace(")","").replace("$","").replace(",","").replace("—","").replace(' ',"0"))

			a_new ="".join(a_temp)

			return(float(a_new))
   
   
	except ValueError:

		return (a)
		raise
	except AttributeError:
		return (a)
		raise


def find_list(list_: list)-> list:
	"""
 
	To get the list of lineitems from extracted data
 
	Parameters
	----------
	list_ : list
		list of extracted dictionaries  

	Returns
	-------
	list
		list of lineitems
 
	"""

	i=sort_list(list_)
	return [each["particular"] for each in list_ ]

def sort_list(list_: list)-> list:
	"""
 
	To get the list of sorted lineitems and values with respect to keys from extracted data
 
	Parameters
	----------
	list_ : list
		list of extracted dictionaries  

	Returns
	-------
	list
		list of sorted lineitems and value with respect to keys
 
	"""
	if isinstance(list_, list):
		for each in list_:
			return [s for s in sorted(each.keys())]
	else:
		raise TypeError



def level_0(list_:list)-> list:
	"""
 
	To get the list of first level of metric from extracted data
 
	Parameters
	----------
	list_ : list
		list of lineitems  

	Returns
	-------
	list
		list of first level of metric
 
	"""
	# list_2=find_list(list_)
	# level =[list_2.index(each) for each in list_2 if "operating activities" in each ]       
	# return level
	level=[]
	list_2=find_list(list_)
	corpus=yaml_parse()
	corpus=corpus["cash_flow_CF"]["level_0"]
	for each in list_2:
		for c in corpus:
			if fuzz.token_set_ratio(each, c) > 90:
				level.append(list_2.index(each))
	return sorted(level)

def level_1(list_:list)-> list:
	"""
 
	To get the list of second level of metric from extracted data
 
	Parameters
	----------
	list_ : list
		list of lineitems  

	Returns
	-------
	list
		list of second level of metric
 
	"""
	# list_2=find_list(list_)
	# level =[list_2.index(each) for each in list_2 if "investing activities" in each ]       
	# return level
	level=[]
	list_2=find_list(list_)
	corpus=yaml_parse()
	corpus=corpus["cash_flow_CF"]["level_1"]
	for each in list_2:
		for c in corpus:
			if fuzz.token_set_ratio(each, c) > 90:
				level.append(list_2.index(each))
	return sorted(level)
def level_2(list_:list) -> list:
	"""
 
	To get the list of third level of metric from extracted data
 
	Parameters
	----------
	list_ : list
		list of lineitems  

	Returns
	-------
	list
		list of third level of metric
 
	"""
	# list_2=find_list(list_)
	# level =[list_2.index(each) for each in list_2 if "financing activities" or "fincing activities" or "ficing activities" in each ]       
	# return level
	level=[]
	list_2=find_list(list_)
	corpus=yaml_parse()
	corpus=corpus["cash_flow_CF"]["level_2"]
	for each in list_2:
		for c in corpus:
			if fuzz.token_set_ratio(each, c) > 90:
				level.append(list_2.index(each))
	return sorted(level)

def level_3(list_: list) -> list:
	"""
 
	To get the list of fourth level of metric from extracted data
 
	Parameters
	----------
	list_ : list
		list of lineitems  

	Returns
	-------
	list
		list of fourth level of metric
 
	"""
	# list_2=find_list(list_)
	# level =[list_2.index(each) for each in list_2 if "increase" in each and "decrease" in each or "(decrease)/increase" in each ]       
	# return level
	level=[]
	list_2=find_list(list_)
	corpus=yaml_parse()
	corpus=corpus["cash_flow_CF"]["level_3"]
	for each in list_2:
		for c in corpus:
			if fuzz.token_set_ratio(each, c) > 90:
				level.append(list_2.index(each))
	return sorted(level)


def operating_activities(list_: list)-> list:
	"""
 
	To identify the list of operating activities section 
 
	Parameters
	----------
	list_ : list
		list of extracted dictionaries  

	Returns
	-------
	list:
		list of operating activities activities section with values
		
 
	"""
	if isinstance(list_, list):
		oa=pd.DataFrame(list_)
		oa=oa[(level_0(list_)[0])+1:level_0(list_)[-1]]
		oa=oa.T.to_dict()

		return [oa[i] for i in oa]
	else:
		raise TypeError
		return []


def investing_activities(list_ : list) -> list:
	"""
 
	To identify the list of investing activities section 
 
	Parameters
	----------
	list_ : list
		list of extracted dictionaries  

	Returns
	-------
	list:
		list of investing activities section with values
		
 
	"""
	if isinstance(list_, list):
		ia=pd.DataFrame(list_)
		ia=ia[(level_1(list_)[0])+1:level_1(list_)[-1]]
		ia=ia.T.to_dict()
		return [ia[i] for i in ia]
	else:
		raise TypeError
		return []

def financing_activities(list_ : list) -> list:
	"""
 
	To identify the list of financing activities section 
 
	Parameters
	----------
	list_ : list
		list of extracted dictionaries  

	Returns
	-------
	list:
		list of financing activities section with values
		
 
	"""
	if isinstance(list_, list):
		fa=pd.DataFrame(list_)
		fa=fa[(level_2(list_)[0])+1:level_2(list_)[-1]]
		fa=fa.T.to_dict()
		return [fa[i] for i in fa]
	else:
		raise TypeError
		return []


def increase_decrease(list_ : list) -> list:
	"""

	To identify the list of increase/decrease activities section

	Parameters
	----------
	list_ : list
		list of extracted dictionaries

	Returns
	-------
	list:
		list of increase/decrease activities activities section with values


	"""
	if isinstance(list_, list):
		i_d=pd.DataFrame(list_)
		i_d=i_d[level_3(list_)[-1]:(level_3(list_)[-1])+1]
		i_d=i_d.T.to_dict()
		i_d = {"Increase/Decrease":[i_d[i] for i in i_d]}
		print(i_d,"increase decrease --------")
		return i_d
	else:
		raise TypeError
		return []



def closing_cash(list_ : list) -> list:
	"""
 
	To identify the list of increase/decrease activities section 
 
	Parameters
	----------
	list_ : list
		list of extracted dictionaries  

	Returns
	-------
	list:
		list of increase/decrease activities section with values
		
 
	"""
	if isinstance(list_, list):
		cc=pd.DataFrame(list_)
		print(cc.tail(1).index.start )
		cc=cc[(level_3(list_)[-1])+1:cc.tail(1).index.start]
		cc=cc.T.to_dict()
		cc={[cc[i] for i in cc]}
		return cc
	else:
		raise TypeError
		return []



def cash_flow_lineitems(list_ : list) -> dict:
	"""
 
	To identify the list of cash flow section with class 
 
	Parameters
	----------
	list_ : list
		list of extracted dictionaries  

	Returns
	-------
	dict:
		dictionary of cash flow section with different class
		
 
	"""


	#uncomment to switch OFF print statement
	#blockPrint()

	
	a=[]
	if isinstance(list_, list):
		for each in list_:
			i=[s for s in sorted(each.keys())]
			if each[i[-1]] != '':

				a.append({i[-3]:normalize(str(each[i[-3]])),i[-2]:normalize(str(each[i[-2]])),i[-1]:str(each[i[-1]]).lower()})    
	else:
		raise TypeError
		return []
	outer=[]
	i=sort_list(a)
	#level0=level_0(a)

	print(pd.DataFrame(a))
	print("------level0------",level_0(a))
	print("------level1------",level_1(a))
	print("------level2------",level_2(a))
	print("------level3------",level_3(a))
	res = {}
	res['Operating Activities']=[]
	res['Investing Activities']=[]
	res['Financing Activities']=[]
	# res['Increase/Decrease']=[]
	# res['Cloing cash/End of year']=[]
	try: 
		res['Operating Activities']=operating_activities(a)
	except Exception as e:
		print(e ,"Error in operating activities")
		#logger.error(e )
		res['Operating Activities']=[]
	try:
		res['Investing Activities']=investing_activities(a)
	except Exception as e:
		print(e ,"Error in investing activities")
		#logger.error(e )
		res['Investing Activities']=[]


	try:
		res['Financing Activities']=financing_activities(a)
	except Exception as e:
		print(e ,"Error in financing activities")
		#logger.error(e)
		res['Financing Activities']=[]

	# res['Increase/Decrease']=increase_decrease(a)
	# res['Cloing cash/End of year']=closing_cash(a)
	#logger.info("initialize_service_logger has ended in CF")

	print(res,"result cash flow------------------")
	return res