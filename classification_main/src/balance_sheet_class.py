import pandas as pd
import pprint
from datetime import datetime
import os
import logging
global getLogger
global logger
import yaml
import json
import tracemalloc

from src.balance_sheet_rules import *
from src.balance_sheet_graph import *
from src.graph_fS_classification import *

def convert_balance_sheet(dict_:dict)-> list:
    """
 
    To convert extraction json to list of dictionary for income statement classification
 
    Parameters
    ----------
    dict_ : dict
        dictionary of extraction   

    Returns
    -------
    list
        list of dictionaries
        
 
    """
    global  year_count
    balance_sheet=[]
    

    for idx, Bs in enumerate(dict_ ["Data"]["Financial Tables"][0]["Balance Sheet"]):

        balance_sheet.append({"particular":Bs["Label Name"]})

        z = [balance_sheet[idx].update({Bs["Year"+str(yc+1)]: normalize(Bs["Year"+str(yc+1)+" Value"])}) for yc in range(year_count)]

        balance_sheet[idx].update( {"Label Signage": positive_negative_sign([Bs["Year"+str(yc+1)+" Value"] for yc in range(year_count)] ) })

        balance_sheet[idx].update({"inner_outer": Bs["meta_year1"]})
        balance_sheet[idx].update({"id": idx})

    return balance_sheet 



def positive_negative_sign(num:list)->str:

    global year_count

    try:
        if all(True if isinstance(normalize(idx), float) else False for idx in num):
            if all(True if normalize(idx) == 0.0 else False for idx in num):
                return "H"
            elif any(True if normalize(idx) > 0.0 else False for idx in num):
                return "P"
            else:
                return "N"
        else: 
            return "E"
    except:
        return "E"


def getNext(l, no):
    i = l.index(no)
    print("Get Nxt ----------++++++++++>>>>>>>>>>>>",l[(i + 1) % len(l)])
    return  l[(i + 1) % len(l)]

def default_class(classification_bs, typ):
    classification_bs_after={}
    print(classification_bs_after)
    classification_bs_after.update({"Current Assets":[],"Non-current Assets":[],'Equity':[],'Non-Current Liabilities':[],'Current Liabilities':[],'Non-Current Liabilities':[]})
    flag=0

    for subclass in classification_bs: 
        print("----------",subclass,"-------")
        
        #classification_bs_after.update({"Current Assets":[],"Non-current Assets":[],'Equity':[],'Non-Current Liabilities':[],'Current Liabilities':[],'Non-Current Liabilities':[]})

        for sub_elements in classification_bs[subclass]:
            print(sub_elements)
            match =process.extractOne(sub_elements["particular"],avoid_calculated_field,scorer=fuzz.partial_ratio)
            if fuzz.partial_ratio(sub_elements["particular"],"over draft")>=85:
                #print(sub_elements,fuzz.partial_ratio(sub_elements["particular"],"over draft"))
                classification_bs_after["Current Liabilities"].append(sub_elements)

            elif (fuzz.partial_ratio(sub_elements["particular"],"profit & loss")>=85 or fuzz.partial_ratio(sub_elements["particular"],"opening")>=85) and subclass == "Current Liabilities" and typ == "T-form (Tally)":
                #print(sub_elements,fuzz.partial_ratio(sub_elements["particular"],"over draft"))
                #classification_bs_after["Current Liabilities"].append(sub_elements)
                classification_bs_after["Equity"].append(sub_elements)
                flag =1
                print(sub_elements,"Type detected: ",typ)


            elif (fuzz.partial_ratio(sub_elements["particular"],"profit & loss")>=85 or fuzz.partial_ratio(sub_elements["particular"],"opening")>=85) and subclass == "Current Liabilities" and typ == "Other vertical format" :
                #print(sub_elements,fuzz.partial_ratio(sub_elements["particular"],"over draft"))
                #classification_bs_after["Current Liabilities"].append(sub_elements)
                classification_bs_after["Equity"].append(sub_elements)
                flag =1
                print(sub_elements,"Type detected: ",typ)
            

            elif subclass == "Current Liabilities" and flag==1 and match[1]<90:

                classification_bs_after["Equity"].append(sub_elements)

            else:

                classification_bs_after[subclass].append(sub_elements)


    print("------------------after default class--------------------")
    pprint.pprint(classification_bs_after)
    classification_bs=classification_bs_after
    return classification_bs


def roman_number(lineitem : str) -> str:
    """
 
    To remove roman numbers from lineitem
 
    Parameters
    ----------
    lineitem : str
        Input string of lineitem


    Returns
    -------
    Sentance : str
        
    """
    # roman=["","I","II","III","IV","V","VI","VII","VIII","IX","X"]
    # remove_items=[".","-","+","/","(",")","*"]
    # remove=[c for c in lineitem if c in remove_items]
    # # print(remove)
    # if remove != []:
    #     for each in remove:
    #         str_=lineitem.replace(each," ")
    # else :
    #     str_=lineitem
    # sentance=""
    # for i in str_.split():
    #     if i.upper() in roman:
    #         pass
    #     else:
    #         sentance+=i+" "
    # # print(sentance,"print sentance")
    # return sentance
    return lineitem.lower()


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
        # print("2ndProblem::",each)
        list_particular.append(each["particular"])

    return  list_particular

def sort_list(list_ : list)-> list:
    """
 
    To get the list of sorted lineitems and values with respect to keys from extracted data
 
    Parameters
    ----------
    list_ : list
        List of extracted dictionaries  

    Returns
    -------
    list
        List of sorted lineitems and value with respect to keys 
    """
    for each in list_:
        return [s for s in sorted(each.keys())]
    

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


def get_graph_output(input_list:list)-> list:
    """
    graph calling function
    """
    lineitem_list=[]
    for each in input_list:
        lineitem_list.append(each["particular"])

    d = {"query_type": "classification", "branch_name": "BS", "lineitem_list": lineitem_list}

    graph_list = start_graph_process(d)
    if graph_list:
        graph_list.sort(key = lambda x: x[1])
        return graph_list
    else:
        return []

def get_rule_output(input_list:list)-> dict:
    """
    rule calling function
    """
    rule_dict = start_bs_rule_processing(input_list)
    return rule_dict

def merge_graph_rule_dict(rule_dict, graph_dict, graph_output):
    """
    consolidate graph and rule dict output into a single dict if any subclass or class
    is missing in graph
    """
    asset_g_item_names = [y["item_name"] for y in graph_dict["Asset"]]
    asset_diff = [x for x in rule_dict["Asset"] if x["item_name"] not in asset_g_item_names]
    for asset_item in asset_diff:
        graph_dict["Asset"].append(asset_item)
    graph_dict["Asset"].sort(key = lambda x: x["start_pos"])

    liability_g_item_names = [y["item_name"] for y in graph_dict["Equity_Liability"]]
    liability_diff = [x for x in rule_dict["Equity_Liability"] if x["item_name"] not in liability_g_item_names]
    for liability_item in liability_diff:
        graph_dict["Equity_Liability"].append(liability_item)
    graph_dict["Equity_Liability"].sort(key = lambda x: x["start_pos"])

    del asset_g_item_names
    del liability_g_item_names
    del asset_diff
    del liability_diff
    return graph_dict

def final_postprocessing(input_dict, input_list, graph_output):
    """
    1. If a subclass T is present after subclass U and  T.endpos - U.startpos > 1 then shift U.start_pos just after T.endpos
    2. If a subclass of different class comes between "continuation of a class belonging to subclass" delete that different class.
        # For example non-current-liability coming under current asset continuation, delete ncl. Check graph for continuation. 
    3. Subclass is present before main class then delete the subclass
    """
    
    asset_start = -100
    current_asset_start = -100
    current_asset_start_pos_list = -100
    current_asset_end = -100
    non_current_asset_start = -100
    non_current_asset_start_pos_list = -100
    non_current_asset_end = -100
    current_liability_start = -100
    current_liability_end = -100
    non_current_liability_start = -100
    non_current_liability_end = -100
    equity_start = -100
    equity_end = -100
    position_graph = {}

    lineitem_list=[]
    for each in input_list:
        lineitem_list.append(each["particular"])

    for asset_item in input_dict["Asset"]:
        if asset_item["item_name"] == "asset":
            asset_start= asset_item["start_pos"]
        if asset_item["item_name"] == "current_asset":
            current_asset_start = asset_item["start_pos"]
        if asset_item["item_name"] == "total_current_asset":
            current_asset_end = asset_item["start_pos"]
        if asset_item["item_name"] == "non_current_asset":
            non_current_asset_start = asset_item["start_pos"]
            non_current_asset_start_pos_list = input_dict["Asset"].index(asset_item)
        if asset_item["item_name"] == "total_non_current_asset":
            non_current_asset_end = asset_item["start_pos"]

    for liability_item in input_dict["Equity_Liability"]:
        if liability_item["item_name"] == "current_liabilities":
            current_liability_start = liability_item["start_pos"]
        if liability_item["item_name"] == "non_current_liabilities":
            non_current_liability_start = liability_item["start_pos"]
        if liability_item["item_name"] == "equity":
            equity_start = liability_item["start_pos"]

    for g_item in graph_output:
        position_graph.setdefault(g_item[2][1], []).append(g_item[1])

    # Logic 1: For Non current asset
    # Check diff between total_current_asset and non_current_asset if non_current_asset is present after total_current_asset
    if current_asset_end != -100 and current_asset_end < non_current_asset_start:
        if (non_current_asset_start - current_asset_end) > 1:
            del input_dict["Asset"][non_current_asset_start_pos_list]
            input_dict["Asset"].append({"class_id":1,"sub_class_id":2,"hiererchy":"sub","level":"class","item_name":"non_current_asset","matched_with":lineitem_list[current_asset_end+1],"start_pos": current_asset_end+1,"end_position":-100})


    # Logic 2: For NCL coming under current asset continuation
    #if non_current_liability_start in range()
    if "CurrentAsset" in position_graph and non_current_liability_start in range(min(position_graph["CurrentAsset"]),max(position_graph["CurrentAsset"])):
        input_dict["Equity_Liability"] = list(filter(lambda x: x["start_pos"] != non_current_liability_start, input_dict["Equity_Liability"]))


    # Logic 3: Current asset present before asset

    if asset_start != -100 and current_asset_start != -100:
        if asset_start > current_asset_start:
            input_dict["Asset"] = list(filter(lambda x: x["start_pos"] != current_asset_start, input_dict["Asset"]))


    input_dict["Asset"].sort(key = lambda x: x["start_pos"])
    input_dict["Equity_Liability"].sort(key = lambda x: x["start_pos"])
    return input_dict

def process_graph_rule(input_list:list):
    """
    main method
    """
    print("============================= Graph output =============================")
    graph_output = get_graph_output(input_list)
    print(graph_output)
    print("============================= Rule output =============================")
    rule_output = get_rule_output(input_list)
    print(rule_output)

    fin_asset_pos,non_fin_asset_pos,fin_liability_pos,non_fin_liability_pos,equity_pos = get_financial_positions(graph_output)
    if fin_asset_pos != -100 and fin_liability_pos != -100 and non_fin_asset_pos != -100 and non_fin_liability_pos != -100 and equity_pos != 100:
        final_dict_graph = subclass_based_on_financial_positions(input_list, graph_output, rule_output, fin_asset_pos, non_fin_asset_pos, fin_liability_pos, non_fin_liability_pos,equity_pos)
        final_dict = merge_graph_rule_dict(rule_output, final_dict_graph, graph_output)
        return graph_output, final_dict
    else:
        final_dict_graph = subclass(input_list, graph_output, rule_output)
        final_dict = merge_graph_rule_dict(rule_output, final_dict_graph, graph_output)
        final_dict = final_postprocessing(final_dict,input_list,graph_output)
        return graph_output, final_dict


def balance_sheet_lineitems(list_:list):
    """ 
    To identify and group sequence from list of lineitem index
 
    Parameters
    ----------
    list_ : list
        list of index of lineitems 


    Returns
    -------
    dict :
        dictionary of balance sheet classification
 
    """
    a=[]
    for each in list_:
        i=[s for s in sorted(each.keys())]

        a.append({i[-3]:normalize(str(each[i[-3]])),i[-2]:normalize(str(each[i[-2]])),i[-1]:str(each[i[-1]]).lower()})

    print(pd.DataFrame(a).head(60))

    graph_output, final_classification_output = process_graph_rule(a)
    print("============================= Final Output =============================")
    print(final_classification_output)

    return graph_output, final_classification_output

def year_count_(dict_:dict)->int:
    import re
    ''' Return the number of year present in extraction json'''

    name = ' '.join(list(dict_.keys()))

    m = re.findall("(Year[0-9] Value)", name)
    return len(m)


# if __name__ == "__main__": 
#   filename="/home/user/Downloads/Bombay Oxygen Annual Report 2019-2020.pdf.json"
#   # filename= "Extraction_18_May_2020/ASX_BAP_2015/extraction.json"
#   with open(filename, 'rb') as outfile:
#       data=json.load(outfile)

#   DATA = data[1]

def balance_sheet_lineitems_(dict_:dict , typ: str, datasource: str)-> dict:
    global year_count

    year_count = year_count_(dict_['Data']['Financial Tables'][0]["Balance Sheet"][0])
    print("TYPE::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::", type(dict_))
    DATA = convert_balance_sheet(dict_)
    print("TYPE::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::", type(DATA))
    # a=preprocessing_BS_input(DATA)


    graph_output, final_classification_output = balance_sheet_lineitems(DATA)


    print ("====================================POST PROCESSING========================================")
    pprint.pprint(final_classification_output)

    BS_pos=final_classification_output
    BS=DATA
    pos_list=[]
    sub_class=[]
    secondary_start_pos_ = -100

    for class_pos in BS_pos:
        #print(class_pos)
        for sub_class_pos in BS_pos[class_pos]:
            if sub_class_pos['hiererchy']== 'sub' or sub_class_pos['hiererchy']== 'main':
                sub_class.append({sub_class_pos['item_name']:sub_class_pos['start_pos']})
                pos_list.append(sub_class_pos['start_pos'])

                if 'secondary_start_pos' in sub_class_pos.keys():
                    if sub_class_pos['secondary_start_pos'] !=-100:
                        secondary_start_pos_ = sub_class_pos['secondary_start_pos']
                        pos_list.append(sub_class_pos['secondary_start_pos'])
                        sub_class.append({sub_class_pos['item_name']+"2nd":sub_class_pos['secondary_start_pos']})
                

    res = {'Current Assets':[], 'Non-current Assets':[], 'Current Liabilities':[], 'Non-Current Liabilities':[], 'Equity':[]} 
    pos_list.append(len(DATA))
    
    pos_list = list(set(pos_list))
    pos_list=sorted(pos_list)
    print('pos_list----------->>>>')
    print(pos_list) 
    print(sub_class)
    sub_class_ = [dict([(value, key) for key, value in each.items()]) for each in sub_class]
    print(sub_class_)
    req_dict = {k1:v1 for list_item in sub_class_ for (k1,v1) in list_item.items()}
    req_dict_rev = {k2:v2 for list_item in sub_class for (k2,v2) in list_item.items()}

    cur_noncur_last = {'current_asset':'Current Assets', 'non_current_asset':'Non-current Assets'}
    clia_nonclia_last = {'current_liabilities': 'Current Liabilities', 'non_current_liabilities':'Non-Current Liabilities', 'equity':'Equity'}

    for idx, each in enumerate(sub_class):
        for k,v in each.items():
            # print(k,v)
            print("============================================================================")
            if k == 'current_asset':
                #print(pos_list,v)
                print(k,v)
                end=getNext(pos_list,v)
                #print(end,"current asset end",pos_list,v)
                if end:
                    res['Current Assets'] = res['Current Assets'] + [each for each in BS[v:end]]
                else :
                    res['Current Assets'] =BS[v:len(a)]

                cur_noncur_last = {'current_asset':'Current Assets'}


            elif k == 'non_current_asset':
                print(k,v)
                end=getNext(pos_list,v)
                # print(end)
                if end:
                    res['Non-current Assets'] = res['Non-current Assets'] + [each for each in BS[v:end]]
                else:
                    res['Non-current Assets'] =BS[v:len(a)]

                cur_noncur_last = {'non_current_asset':'Non-current Assets'}

            elif k == 'miscellaneous_exp':
                print(k,v)
                end=getNext(pos_list,v)
                # print(end)
                if end:
                    res['Current Assets'] = res['Current Assets'] + [each for each in BS[v:end]]
                else :
                    res['Current Assets'] =BS[v:len(a)]

                cur_noncur_last = {'current_asset':'Current Assets'}

            elif k == 'total_current_asset':
                print(k,v)
                end=getNext(pos_list,v)
                if end:
                    res[cur_noncur_last[list(cur_noncur_last.keys())[0]]] = res[cur_noncur_last[list(cur_noncur_last.keys())[0]]] + [each for each in BS[v:end]]
                else :
                    res[cur_noncur_last] =BS[v:len(a)]

            elif k == 'total_non_current_asset':
                print(k,v)
                end=getNext(pos_list,v)
                if end:
                    res[cur_noncur_last[list(cur_noncur_last.keys())[0]]] = res[cur_noncur_last[list(cur_noncur_last.keys())[0]]] + [each for each in BS[v:end]]
                else :
                    res[cur_noncur_last] =BS[v:len(a)]


            elif k == 'total_asset':
                print(k,v)
                end=getNext(pos_list,v)
                if end:
                    res[cur_noncur_last[list(cur_noncur_last.keys())[0]]] = res[cur_noncur_last[list(cur_noncur_last.keys())[0]]] + [each for each in BS[v:end]]
                else :
                    res[cur_noncur_last] =BS[v:len(a)]



            elif k == 'current_liabilities':
                print(k,v)
                end=getNext(pos_list,v)
                if end:
                    res['Current Liabilities'] = res['Current Liabilities'] + [each for each in BS[v:end]]
                else :
                    res['Current Liabilities'] =BS[v:len(a)]

                clia_nonclia_last = {'current_liabilities': 'Current Liabilities'}

                
            elif k == 'non_current_liabilities':
                print(k,v)
                end=getNext(pos_list,v)

                if end:
                    res['Non-Current Liabilities'] = res['Non-Current Liabilities'] + [each for each in BS[v:end]]
                else:
                    res['Non-Current Liabilities'] =BS[v:len(a)]

                clia_nonclia_last = {'non_current_liabilities':'Non-Current Liabilities'}
                
            elif k == 'equity' or k == 'equity2nd':
                print(k,v)
                end=getNext(pos_list,v)

                if end:
                    res['Equity'] = res['Equity'] + [each for each in BS[v:end]]
                else:
                    res['Equity'] =BS[v:len(a)]

                clia_nonclia_last = {'equity':'Equity'}


            elif k == 'total_current_liabilities':
                print(k,v)
                end=getNext(pos_list,v)
                if end:
                    res[clia_nonclia_last[list(clia_nonclia_last.keys())[0]]] = res[clia_nonclia_last[list(clia_nonclia_last.keys())[0]]] + [each for each in BS[v:end]]
                else :
                    res[clia_nonclia_last] =BS[v:len(a)]

            elif k == 'total_non_current_liabilities':
                print(k,v)
                end=getNext(pos_list,v)
                if end:
                    res[clia_nonclia_last[list(clia_nonclia_last.keys())[0]]] = res[clia_nonclia_last[list(clia_nonclia_last.keys())[0]]] + [each for each in BS[v:end]]
                else :
                    res[clia_nonclia_last] =BS[v:len(a)]

            elif k == 'total_liabilities':
                print(k,v)
                end=getNext(pos_list,v)
                if end:
                    res[clia_nonclia_last[list(clia_nonclia_last.keys())[0]]] = res[clia_nonclia_last[list(clia_nonclia_last.keys())[0]]] + [each for each in BS[v:end]]
                else :
                    res[clia_nonclia_last] =BS[v:len(a)]


            elif k == 'total_equity':
                print(k,v)
                end=getNext(pos_list,v)
                if end:
                    res[clia_nonclia_last[list(clia_nonclia_last.keys())[0]]] = res[clia_nonclia_last[list(clia_nonclia_last.keys())[0]]] + [each for each in BS[v:end]]
                else :
                    res[clia_nonclia_last] =BS[v:len(a)]

            elif k == 'total_equity_liabilities':
                print(k,v)
                end=getNext(pos_list,v)
                if end:
                    res[clia_nonclia_last[list(clia_nonclia_last.keys())[0]]] = res[clia_nonclia_last[list(clia_nonclia_last.keys())[0]]] + [each for each in BS[v:end]]
                else :
                    res[clia_nonclia_last] =BS[v:len(a)]


    #pprint.pprint(res)
    print("res----",res)
    res= default_class(res,datasource)
    res['graph_output'] = graph_output

    return res