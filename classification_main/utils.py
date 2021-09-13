import pandas as pd
#import xlrd
import json
from fuzzywuzzy import fuzz 
from fuzzywuzzy import process 
#import difflib
import yaml





def yaml_parse()-> dict:
	"""
 
	To parse yaml file

	Parameters
	----------
	None
		   

	Returns
	-------
	dict
		to get corpus of different class
		
 
	"""
	with open("corpus.yaml", 'r') as stream:
		try:
			corpus=yaml.safe_load(stream)
			#print(corpus)
			return(corpus)
		except yaml.YAMLError as exc:
			print(exc)
			return(exc)
			raise


def find_url_template(data: dict)-> str:
	"""
 
	To get dynamic mapping template
 
	Parameters
	----------
	data : dict
		meta dictionary including templateid
		   

	Returns
	-------
	str
		
 
	"""
	# if not isinstance(data, dict):
	# 	raise TypeError

	# if "Source" not in data:
	# 	raise KeyError

	# else:
	if data['Source']['templateUrl']:
		print("Template URL ",data['Source']['templateUrl'])
		return data['Source']['templateUrl']

	else:
		return "Template URL Not found"







