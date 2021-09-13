"""
Utility Module for graph related task 

"""
def find_list(list_: list) -> list:
	"""
 
	To get the list of lineitems from extracted data
 
	Parameters
	----------
	list_ : list
		List of extracted dictionaries  

	Returns
	-------
	list
		List of lineitems 
	"""
	list_particular=[]
	for each in list_:
		list_particular.append(each["particular"])

	return  list_particular


def get_financial_positions(graph_output):
	"""
	Retrieve financial term in graph_output
	"""
	financial_asset_position = -100
	non_financial_asset_position = -100
	financial_liability_position = -100
	non_financial_liability_position = -100
	equity_position = -100

	for item in graph_output:
		if item[2][1] == "FinancialAsset":
			financial_asset_position = graph_output.index(item)
		if item[2][1] == "NonFinancialAsset":
			non_financial_asset_position = graph_output.index(item)
		if item[2][1] == "FinancialLiabilities":
			financial_liability_position = graph_output.index(item)
		if item[2][1] == "NonFinancialLiabilities":
			non_financial_liability_position = graph_output.index(item)
		if item[2][1] == "Equity":
			equity_position = graph_output.index(item)

	return (financial_asset_position,non_financial_asset_position,financial_liability_position,non_financial_liability_position,equity_position)

def fix_class_overlap(graph_list, current_asset_pos, non_current_asset_pos, current_liability_pos, non_current_liability_pos, equity_pos):
	"""
	Check whether there is no overlap between Asset and Liability class items
	"""
	
	asset_pos = -100 # asset pos in graph list
	equity_liability_pos = -100 # equityliab pos in graph list

	try:
		asset_pos = graph_list.index(list(filter(lambda x: x[2][1] == 'Asset' and x[2][0] != 'Total', graph_list))[0])
	except:
		print("Warning::: Item named asset not found in graph")

	try:
		equity_liability_pos = graph_list.index(list(filter(lambda x: x[2][1] == 'EquityLiab' and x[2][0] != 'Total', graph_list))[0])
	except:
		print("Warning::: Item name equity_liability not found in graph")

	#Check overlap for Asset class. Check whether any asset class item misplaced in equityliability class
	if equity_liability_pos != -100 and asset_pos != -100:		
		if equity_liability_pos < asset_pos: # equityliability section is at top of the dataframe

			if current_asset_pos != -100 and current_asset_pos in range(equity_liability_pos, asset_pos+1):
				current_asset_pos = list(filter(lambda x: x[2][1] == 'CurrentAsset', graph_list[asset_pos:]))[0][1]
			if non_current_asset_pos != -100 and non_current_asset_pos in range(equity_liability_pos, asset_pos+1):
				non_current_asset_pos = list(filter(lambda x: x[2][1] == 'NonCurrentAsset', graph_list[asset_pos:]))[0][1]
			if current_liability_pos != -100 and current_liability_pos in range(asset_pos,graph_list[-1][1]+1):
				current_liability_pos = list(filter(lambda x: x[2][1] == 'CurrentLiabilities', graph_list[equity_liability_pos:asset_pos]))[0][1]
			if non_current_liability_pos != -100 and non_current_liability_pos in range(asset_pos,graph_list[-1][1]+1):
				non_current_liability_pos = list(filter(lambda x: x[2][1] == 'NonCurrentLiabilities', graph_list[equity_liability_pos:asset_pos]))[0][1]
			if equity_pos != -100 and equity_pos in range(asset_pos,graph_list[-1][1]+1):
				equity_pos = list(filter(lambda x: x[2][1] == 'Equity', graph_list[equity_liability_pos:asset_pos]))[0][1]

		else: # asset section is at top of dataframe
			if current_asset_pos != -100 and current_asset_pos in range(equity_liability_pos, graph_list[-1][1]+1):
				current_asset_pos = list(filter(lambda x: x[2][1] == 'CurrentAsset', graph_list[asset_pos:equity_liability_pos+1]))[0][1]
			if non_current_asset_pos != -100 and non_current_asset_pos in range(equity_liability_pos, graph_list[-1][1]+1):
				non_current_asset_pos = list(filter(lambda x: x[2][1] == 'NonCurrentAsset', graph_list[asset_pos:equity_liability_pos+1]))[0][1]
			if current_liability_pos != -100 and current_liability_pos in range(asset_pos,equity_liability_pos+1):
				current_liability_pos = list(filter(lambda x: x[2][1] == 'CurrentLiabilities', graph_list[equity_liability_pos:]))[0][1]
			if non_current_liability_pos != -100 and non_current_liability_pos in range(asset_pos,equity_liability_pos+1):
				non_current_liability_pos = list(filter(lambda x: x[2][1] == 'NonCurrentLiabilities', graph_list[equity_liability_pos:]))[0][1]
			if equity_pos != -100 and equity_pos in range(asset_pos,equity_liability_pos+1):
				equity_pos = list(filter(lambda x: x[2][1] == 'Equity', graph_list[equity_liability_pos:]))[0][1]

	return current_asset_pos, non_current_asset_pos, current_liability_pos, non_current_liability_pos, equity_pos


def get_first_pos_graph(graph_list):
	"""
	return initial position of subclass from graph
	"""
	current_asset_pos = -100
	non_current_asset_pos = -100
	current_liability_pos = -100
	mis_expense_pos = -100
	non_current_liability_pos = -100
	equity_pos = -100

	# Find position with level3
	######for label3 or label2 positions######
	for each in graph_list:
		if each[2][1] == "CurrentAsset" and ("Level3" in each[2][0] or "Level2" in each[2][0]) and "Total" not in each[2][0] and current_asset_pos == -100:
			current_asset_pos = graph_list.index(each)
		if each[2][1] == "NonCurrentAsset" and ("Level3" in each[2][0] or "Level2" in each[2][0]) and "Total" not in each[2][0] and non_current_asset_pos == -100:
			non_current_asset_pos = graph_list.index(each)
		if each[2][1] == "MiscellaneousExp" and ("Level3" in each[2][0] or "Level2" in each[2][0]) and "Total" not in each[2][0] and mis_expense_pos == -100:
			mis_expense_pos = graph_list.index(each)
		if each[2][1] == "CurrentLiabilities" and ("Level3" in each[2][0] or "Level2" in each[2][0]) and "Total" not in each[2][0] and current_liability_pos == -100:
			current_liability_pos = graph_list.index(each)
		if each[2][1] == "NonCurrentLiabilities" and ("Level3" in each[2][0] or "Level2" in each[2][0]) and "Total" not in each[2][0] and non_current_liability_pos == -100:
			non_current_liability_pos = graph_list.index(each)
		if each[2][1] == "Equity" and ("Level3" in each[2][0] or "Level2" in each[2][0]) and "Total" not in each[2][0] and equity_pos == -100:
			equity_pos = graph_list.index(each)


	######for other labels######
	for each in graph_list:
		if each[2][1] == "CurrentAsset" and "Total" not in each[2][0] and current_asset_pos == -100:
			current_asset_pos = graph_list.index(each)
		if each[2][1] == "NonCurrentAsset" and "Total" not in each[2][0] and non_current_asset_pos == -100:
			non_current_asset_pos = graph_list.index(each)
		if each[2][1] == "MiscellaneousExp" and "Total" not in each[2][0] and mis_expense_pos == -100:
			mis_expense_pos = graph_list.index(each)
		if each[2][1] == "CurrentLiabilities" and "Total" not in each[2][0] and current_liability_pos == -100:
			current_liability_pos = graph_list.index(each)
		if each[2][1] == "NonCurrentLiabilities" and "Total" not in each[2][0] and non_current_liability_pos == -100:
			non_current_liability_pos = graph_list.index(each)
		if each[2][1] == "Equity" and "Total" not in each[2][0] and equity_pos == -100:
			equity_pos = graph_list.index(each)

	current_asset_pos, non_current_asset_pos, current_liability_pos, non_current_liability_pos, equity_pos = fix_class_overlap(graph_list,current_asset_pos, non_current_asset_pos, current_liability_pos, non_current_liability_pos, equity_pos)	
	return (current_asset_pos, non_current_asset_pos, mis_expense_pos, current_liability_pos, non_current_liability_pos, equity_pos)


def get_position_graph(item1:str,item2:str,graph_output:list,index1:int,index2:int,item3="Equity",index3="") -> tuple:
	"""
	Find position of lineitems from graph if two indexes are present

	Parameters
	----------
	item1 : string
		Name of lineitem (currentasset/currentliability)
	item2 : string
		Name of lineitem (noncurrentasset/noncurrentliability)
	graph_output : list
		sorted output from graph
	index1 : int
		Index of Financial Asset/Liability in graph_output list
	index2 : int
		Index of non Financial Asset/Liability in graph_output list

	Returns
	--------
	pos_tup: tuple
		tuple containing either asset/liability items
	"""
	item1_pos1 = -100
	item1_pos2 = -100
	item2_pos1 = -100
	item2_pos2 = -100
	item3_pos1 = -100
	
	for item in graph_output[index1:index2]:
		if item[2][1] == item1 and "Total" not in item[2][0] and item1_pos1 == -100:
			item1_pos1 = item[1]
		if item[2][1] == item2 and "Total" not in item[2][0] and item2_pos1 == -100:
			item2_pos1 = item[1]
			
	for item in graph_output[index2:]:
		if item[2][1] == item1 and "Total" not in item[2][0] and item1_pos2 == -100:
			item1_pos2 = item[1]
		if item[2][1] == item2  and "Total" not in item[2][0] and item2_pos2 == -100:
			item2_pos2 = item[1]
		if item[2][1] == str(item3) and "Total" not in item[2][0] and item3_pos1 == -100:
			item3_pos1 = item[1]
		
	pos_tup = (item1_pos1,item2_pos1,item1_pos2,item2_pos2,item3_pos1)
	return pos_tup

def preprocess_class_list(class_list):
	"""
	1. list items containing 'matched_with -100' will be discarded
	"""
	l = []

	for each in class_list:
		if each["matched_with"] != -100:
			l.append(each)

	return l

def gen_subclass_list_based_on_financial_positions(input_list:list, item1_pos1: int, item2_pos1:int, item1_pos2:int, item2_pos2:int, non_fin_pos:int, main_class:str,item3_pos1:int) -> list:
	"""
	generate list for asset/liability subclass items based on position if financial/non financial term is present
	"""
	current_asset_dict1 = {"class_id":1,"sub_class_id":1,"hiererchy":"sub","level":"class","item_name":"current_asset","matched_with":"","start_pos":-100,"end_position":-100}
	non_current_asset_dict1 = {"class_id":1,"sub_class_id":2,"hiererchy":"sub","level":"class","item_name":"non_current_asset","matched_with":"","start_pos":-100,"end_position":-100}
	current_liabilities_dict1 = {"class_id":2,"sub_class_id":2,"hiererchy":"sub","level":"class","item_name":"current_liabilities","matched_with":"","start_pos":-100,"end_position":-100}
	non_current_liabilities_dict1 = {"class_id":2,"sub_class_id":3,"hiererchy":"sub","level":"class","item_name":"non_current_liabilities","matched_with":"","start_pos":-100,"end_position":-100}
	current_asset_dict2 = {"class_id":1,"sub_class_id":1,"hiererchy":"sub","level":"class","item_name":"current_asset","matched_with":"","start_pos":-100,"end_position":-100}
	non_current_asset_dict2 = {"class_id":1,"sub_class_id":2,"hiererchy":"sub","level":"class","item_name":"non_current_asset","matched_with":"","start_pos":-100,"end_position":-100}
	current_liabilities_dict2 = {"class_id":2,"sub_class_id":2,"hiererchy":"sub","level":"class","item_name":"current_liabilities","matched_with":"","start_pos":-100,"end_position":-100}
	non_current_liabilities_dict2 = {"class_id":2,"sub_class_id":3,"hiererchy":"sub","level":"class","item_name":"non_current_liabilities","matched_with":"","start_pos":-100,"end_position":-100}
	equity_dict = {"class_id":1,"sub_class_id":1,"hiererchy":"sub","level":"class","item_name":"equity","matched_with":"","start_pos":-100,"end_position":-100}


	lineitem_list = []
	for each in input_list:
		lineitem_list.append(each["particular"])

	if main_class == "Asset":
		current_asset_dict1["matched_with"] = lineitem_list[item1_pos1] if item1_pos1 != -100 else item1_pos1
		current_asset_dict1["start_pos"] = item1_pos1
		non_current_asset_dict1["matched_with"] = lineitem_list[item2_pos1] if item2_pos1 != -100 else item2_pos1
		non_current_asset_dict1["start_pos"] = item2_pos1

		current_asset_dict2["matched_with"] = lineitem_list[item1_pos2] if item1_pos2 != -100 else item1_pos2
		current_asset_dict2["start_pos"] = item1_pos2
		non_current_asset_dict2["matched_with"] = lineitem_list[item2_pos2] if item2_pos2 != -100 else item2_pos2
		non_current_asset_dict2["start_pos"] = item2_pos2
	
		asset_list_unprocessed = [current_asset_dict1,non_current_asset_dict1,current_asset_dict2,non_current_asset_dict2]
		asset_list = preprocess_class_list(asset_list_unprocessed)
		return asset_list

	if main_class == "Liability":
		current_liabilities_dict1["matched_with"] = lineitem_list[item1_pos1] if item1_pos1 != -100 else item1_pos1
		current_liabilities_dict1["start_pos"] = item1_pos1
		non_current_liabilities_dict1["matched_with"] = lineitem_list[item2_pos1] if item2_pos1 != -100 else item2_pos1
		non_current_liabilities_dict1["start_pos"] = item2_pos1

		current_liabilities_dict2["matched_with"] = lineitem_list[item1_pos2] if item1_pos2 != -100 else item1_pos2
		current_liabilities_dict2["start_pos"] = item1_pos2
		non_current_liabilities_dict2["matched_with"] = lineitem_list[item2_pos2] if item2_pos2 != -100 else item2_pos2
		non_current_liabilities_dict2["start_pos"] = item2_pos2
		equity_dict["matched_with"] = lineitem_list[item3_pos1] if item3_pos1 != -100 else item3_pos1
		equity_dict["start_pos"] = item3_pos1

		liability_list_unprocessed = [current_liabilities_dict1,non_current_liabilities_dict1,current_liabilities_dict2,non_current_liabilities_dict2,equity_dict]
		liability_list = preprocess_class_list(liability_list_unprocessed)

		return liability_list

def subclass_based_on_financial_positions(input_list, graph_output, rule_output, fin_asset_pos, non_fin_asset_pos, fin_liability_pos, non_fin_liability_pos,equity_pos):

		non_fin_asset_list_pos = graph_output[non_fin_asset_pos][1]
		non_fin_liability_list_pos = graph_output[non_fin_liability_pos][1]

		# get asset positions from graph
		current_asset_pos1, non_current_asset_pos1, current_asset_pos2, non_current_asset_pos2,_ = get_position_graph("CurrentAsset","NonCurrentAsset",graph_output,fin_asset_pos,non_fin_asset_pos)
		# get liability positions from graph
		current_liability_pos1, non_current_liability_pos1, current_liability_pos2, non_current_liability_pos2,equity_pos_1= get_position_graph("CurrentLiabilities","NonCurrentLiabilities",graph_output,fin_liability_pos,non_fin_liability_pos,"Equity",equity_pos)
		# ============================= Asset Position preprocessing =============================
		asset_list = rule_output["Asset"]
		final_asset_list = [e for e in asset_list if e["item_name"] not in ('current_asset', 'non_current_asset')]
		sub_class_asset_list = 	gen_subclass_list_based_on_financial_positions(input_list, current_asset_pos1, non_current_asset_pos1, current_asset_pos2, non_current_asset_pos2, non_fin_asset_list_pos, "Asset",-100)
		final_asset_list += sub_class_asset_list
		final_asset_list.sort(key = lambda x: x["start_pos"])

		# ============================= Liability Position preprocessing =============================
		liability_list = rule_output["Equity_Liability"]
		final_liability_list = [e for e in liability_list if e["item_name"] not in ('current_liabilities', 'non_current_liabilities','equity')]
		sub_class_liability_list = 	gen_subclass_list_based_on_financial_positions(input_list, current_liability_pos1, non_current_liability_pos1, current_liability_pos2, non_current_liability_pos2, non_fin_liability_list_pos, "Liability",equity_pos_1)
		final_liability_list += sub_class_liability_list
		final_liability_list.sort(key = lambda x: x["start_pos"])

		final_dict = {"Asset":final_asset_list,"Equity_Liability":final_liability_list}

		return final_dict

def gen_subclass_list(graph_list:list, input_list:list, main_class:str, item1_pos: int, item2_pos:int, item3_pos:int = -100) -> list:
	"""
	generate list for asset/liability subclass items based on position if financial/non financial term is not present
	"""
	current_asset_dict = {"class_id":1,"sub_class_id":1,"hiererchy":"sub","level":"class","item_name":"current_asset","matched_with":"","start_pos":-100,"end_position":-100}
	non_current_asset_dict = {"class_id":1,"sub_class_id":2,"hiererchy":"sub","level":"class","item_name":"non_current_asset","matched_with":"","start_pos":-100,"end_position":-100}
	mis_expense_dict = {"class_id":1,"sub_class_id":2,"hiererchy":"sub","level":"class","item_name":"miscellaneous_exp","matched_with":"","start_pos":-100,"end_position":-100}
	current_liabilities_dict = {"class_id":2,"sub_class_id":2,"hiererchy":"sub","level":"class","item_name":"current_liabilities","matched_with":"","start_pos":-100,"end_position":-100}
	non_current_liabilities_dict = {"class_id":2,"sub_class_id":3,"hiererchy":"sub","level":"class","item_name":"non_current_liabilities","matched_with":"","start_pos":-100,"end_position":-100}
	equity_dict = {"class_id":2,"sub_class_id":1,"hiererchy":"sub","level":"class","item_name":"equity","matched_with":"","start_pos":-100,"secondary_start_pos":-100,"secondary_matched_with":"","end_position":-100}

	lineitem_list = []
	for each in input_list:
		lineitem_list.append(each["particular"])

	if main_class == "Asset":
		current_asset_dict["matched_with"] = lineitem_list[graph_list[item1_pos][1]] if item1_pos != -100 else item1_pos
		current_asset_dict["start_pos"] = graph_list[item1_pos][1] if item1_pos != -100 else item1_pos
		non_current_asset_dict["matched_with"] = lineitem_list[graph_list[item2_pos][1]] if item2_pos != -100 else item2_pos
		non_current_asset_dict["start_pos"] = graph_list[item2_pos][1] if item2_pos != -100 else item2_pos
		mis_expense_dict["matched_with"] = lineitem_list[graph_list[item3_pos][1]] if item3_pos != -100 else item3_pos
		mis_expense_dict["start_pos"] = graph_list[item3_pos][1] if item3_pos != -100 else item3_pos

		asset_list_unprocessed = [current_asset_dict,non_current_asset_dict,mis_expense_dict]
		asset_list = preprocess_class_list(asset_list_unprocessed)
		return asset_list

	if main_class == "Liability":
		current_liabilities_dict["matched_with"] = lineitem_list[graph_list[item1_pos][1]] if item1_pos != -100 else item1_pos
		current_liabilities_dict["start_pos"] = graph_list[item1_pos][1] if item1_pos != -100 else item1_pos
		non_current_liabilities_dict["matched_with"] = lineitem_list[graph_list[item2_pos][1]] if item2_pos != -100 else item2_pos
		non_current_liabilities_dict["start_pos"] = graph_list[item2_pos][1] if item2_pos != -100 else item2_pos
		equity_dict["matched_with"] = lineitem_list[graph_list[item3_pos][1]] if item3_pos != -100 else item3_pos
		equity_dict["start_pos"] = graph_list[item3_pos][1] if item3_pos != -100 else item3_pos
	
		liability_list_unprocessed = [current_liabilities_dict,non_current_liabilities_dict,equity_dict]
		liability_list = preprocess_class_list(liability_list_unprocessed)
		return liability_list

def subclass(input_list, graph_output, rule_output):
	"""
	"""
	current_asset_pos, non_current_asset_pos, mis_expense_pos, current_liability_pos, non_current_liability_pos, equity_pos = get_first_pos_graph(graph_output)
	
	# ============================= Asset Position preprocessing =============================
	asset_list = rule_output["Asset"]
	final_asset_list = [e for e in asset_list if e["item_name"] not in ('current_asset', 'non_current_asset')]
	sub_class_asset_list = 	gen_subclass_list(graph_output, input_list, "Asset", current_asset_pos, non_current_asset_pos,  mis_expense_pos)
	final_asset_list += sub_class_asset_list
	final_asset_list.sort(key = lambda x: x["start_pos"])

	# ============================= Liability Position preprocessing =============================
	liability_list = rule_output["Equity_Liability"]
	final_liability_list = [e for e in liability_list if e["item_name"] not in ('current_liabilities', 'non_current_liabilities','equity')]
	sub_class_liability_list = 	gen_subclass_list(graph_output, input_list, "Liability", current_liability_pos, non_current_liability_pos, equity_pos)
	final_liability_list += sub_class_liability_list
	final_liability_list.sort(key = lambda x: x["start_pos"])

	final_dict = {"Asset":final_asset_list,"Equity_Liability":final_liability_list}

	return final_dict


	