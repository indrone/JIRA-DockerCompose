import glob
import json
import pandas as pd
import numpy as np
from numpy import median
from fuzzywuzzy import fuzz,process
import re
import pprint
import requests
import ssl
from operator import itemgetter
from functools import reduce
import traceback
import ast
from utils import *
from itertools import islice
from itertools import groupby

import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
nlp = en_core_web_sm.load()

import re
import nltk
from nltk.corpus import stopwords
stop = stopwords.words('english')
from nltk.corpus import wordnet
from datetime import datetime
from nested_lookup import nested_lookup
# pd.set_option("display.max_rows", None, "display.max_columns", None)

#ClassCode = { "IS": { "Revenue": "CCREVENUE", "Cost of goods sold / Cost of Sales": "CCCOGS", "Operating expenses": "CCOPERATINGEXP", "Depreciation": "CCDEPRECIATION", "Non-operating or Other Income / Expenses": "CCNONOPERATINGEXP", "Other Income": "CCOTHERINC", "Finance cost": "CCFINANCECOST", "Tax": "CCTAX" }, "BS": { "Current Assets": "CCCURRENTASSET", "Non-current Assets": "CCNONCURRENTASSET", "Current Liabilities": "CCCURRENTLIABILITIES", "Non-Current Liabilities": "CCNONCURRENTLIABILITIES", "Equity": "CCEQUITY" }, "CF": { "Operating Activities": "OPERATINGACTIVITIES", "Investing Activities": "INVESTINGACTIVITIES", "Financing Activities": "FINANCINGACTIVITIES", "Net Change": "NETCHANGE", "Closing Cash": "CLOSINGCASH" } }
IS_Stopwords = {'CACL': ['receivable','receivables','payable','payables'], 'Revenue': ['less', ''], 'Operating expenses': ['expense', 'charge', 'printer', 'less', 'cost'], 'Non-operating or Other Income / Expenses': ['expense', 'charge', 'printer', 'less', 'cost']}

is_cal_index, bs_cal_index, year_count_bs, year_count_is = [], [], 2, 2
scenario_flag_bs = 0
bs_graph_output = []
scenario_flag_is = 0
KM1, KM4, KM5, SIGNAGE, IS_GRAPH_OUTPUT, All_NEG = -1, -1, -1, -1, [], False

tradepayable_pos = []
total_msme_pos = []
match__ = []
is_header_mapping_dict = {'Cost of goods sold / Cost of Sales': []}

def remove_stopwords(lineitem: str, class_: str)->str:

    ''' Remove stopwords based on class'''

    if class_ in 'Operating expenses':
        REMOVE_LIST = IS_Stopwords['Operating expenses']
    elif class_ in 'Non-operating or Other Income / Expenses':
        REMOVE_LIST = IS_Stopwords['Non-operating or Other Income / Expenses']
    elif class_ in 'Revenue':
        REMOVE_LIST = IS_Stopwords['Revenue']
    elif class_ in ['Current Assets', 'Current Liabilities']:
        REMOVE_LIST = IS_Stopwords['CACL']
    else:
        REMOVE_LIST = []

    if REMOVE_LIST:
        remove_all = '|'.join(REMOVE_LIST[:-1])
        remove_last = '|'.join(REMOVE_LIST[-1:])

        regex_all = re.compile(r''+remove_all+r'', flags=re.IGNORECASE)
        regex_last = re.compile(r''+remove_last+r'$', flags=re.IGNORECASE)

        out = regex_all.sub("", lineitem.strip())
        out = regex_last.sub("", out.strip())
    else:
        out = lineitem

    return out.strip()

def num_checking(num:float)->float:
    if num < 0:
        return num * -1
    return num

# def subset_sum_(numbers:list, target:int, percent:int, partial=[])->list:

#     ''' A recursive combinations of all possible sums filtering out those that reach the target '''
#     s = sum(partial)

#     # check if the partial sum is equals to target
#     if abs(int(round(s*percent/100))) == target and target!=0: 
#         print ("sum(%s)=%s" % (partial, target))
#         return partial

        

#     for i in range(len(numbers)):
#         n = numbers[i]
#         remaining = numbers[i+1:]
#         output = subset_sum_(remaining, target, percent, partial + [n]) 
#         if output:
#             return output
        
#     return []


def subset_sum_(set_ints:list, sum_val:int)->list:
    test_subset = []
    filtered_ints = list(filter(lambda x:x<=sum_val,set_ints))
#     print(filtered_ints)
    while sum(test_subset) < sum_val and len(set_ints) > 0:
#         print('test_subset:: ',test_subset)
        remainder = sum_val - sum(test_subset)
#         print('remainder:: ', remainder)
        filtered_ints = list(filter(lambda x:x<=remainder,filtered_ints))
#         print('filtered_ints:: ', filtered_ints)
        if len(filtered_ints) == 0:
            set_ints.remove(max(set_ints))

            if abs(int(round(sum(test_subset)))) == sum_val:
                return test_subset

            test_subset = []
            filtered_ints = list(filter(lambda x:x<=sum_val,set_ints))
            if sum(set_ints) < sum_val:
                # return []
                pass
            continue
        test_subset.append(max(filtered_ints))
        filtered_ints.remove(test_subset[-1])
        
    if abs(int(round(sum(test_subset)))) == sum_val:
        return test_subset
    else:
        return []

def subset_sum(numbers:list, target:int, percent:int)->list:
    ''' len(numbers) == len(diff) '''
    # print(list(filter(lambda a: a != 0, numbers)), abs(int(round(target/percent*100))))
    return subset_sum_(list(filter(lambda a: a != 0, numbers)), abs(int(round(target/percent*100))))


def scenario_subset_sum(numbers:list, original:list, outerl:list, current_time:str, partial=[])->int:

    ''' A recursive combinations of all possible sums filtering out those that reach the target '''
    s = sum(partial)
    # print("Partial Search:: ",partial)

    # check if the partial sum is equals to target
    if s in outerl: 
        print ("Matched:: ",(partial,s))
        
        if original.index(partial[0]) > original.index(s):
            return 1
        elif original.index(partial[0]) < original.index(s):
            return 2
        else:
            return -1
        

    for i in range(len(numbers)):
        # print("Time::: ", datetime.now(), int(datetime.now().strftime('%S')), int(current_time))
        if int(datetime.now().strftime('%S'))-int(current_time) > 20:
            print("Timeout...")
            break
        n = numbers[i]
        remaining = numbers[i+1:]
        output = scenario_subset_sum(remaining, original, outerl, current_time, partial + [n]) 
        # print("Output::", output)
        if output > 0:
            return output
        
    return -1

def check_calculatedf_scenario(data_:object)->int:

    if data_.shape[0] > 1:
        if data_['Label Signage'].iloc[0] == 'H':
            data_ = data_.iloc[1:].reset_index(drop=True)

        data_.drop(data_[(data_['particular'] == '') & (data_['Label Signage'] == 'H')].index, inplace=True)

        if fuzz.partial_ratio("".join(data_['particular'].iloc[-1].strip()), 'total') > 85:
            data_ = data_.iloc[:-1].reset_index(drop=True)

        data_['sign']=list(map(lambda x: -1 if x == '-' else +1, data_['Label Signage'].to_list())) 
        data_[list(data_.columns)[1]] = data_[list(data_.columns)[1]].to_list()*data_['sign']

        # print(data_)
        req_list_inner = [data_[data_.columns[1]].to_list()[idx] for idx,each in enumerate(data_['inner_outer'].to_list()) if each == 'inner']
        req_list_outer = [data_[data_.columns[1]].to_list()[idx] for idx,each in enumerate(data_['inner_outer'].to_list()) if each == 'outer']

        print("original:: ",  data_[data_.columns[1]].to_list())
        print("Inner:: ", req_list_inner)
        print("Outer:: ", req_list_outer)

        if data_['inner_outer'].to_list().count('outer') > 1 and data_['inner_outer'].to_list()[-1] == 'outer':
            return scenario_subset_sum(req_list_inner, data_[data_.columns[1]].to_list(), req_list_outer, datetime.now().strftime('%S'))
            # return 2

        if data_['inner_outer'].iloc[0] == 'outer' and data_['inner_outer'].iloc[-1] == 'inner':
            return 1

        elif data_['inner_outer'].iloc[0] == 'inner' and data_['inner_outer'].iloc[-1] == 'outer':
            return scenario_subset_sum(req_list_inner, data_[data_.columns[1]].to_list(), req_list_outer, datetime.now().strftime('%S'))
            # return 2

    return -1

def profit_loss_account_check(data_:object)->int:
    
    ''' For T Form, if there is Profit & Loss Account, treat that as outer if Reserves and Surplus (calculated field) is not prsent.'''
    # print(dict(data_))
    score1 = process.extractOne('profit & loss account',dict(data_['particular']),scorer=fuzz.token_set_ratio)
    score2 = process.extractOne('reserves and surplus',dict(data_['particular'][0:score1[2]]),scorer=fuzz.token_set_ratio)

    if score1 and score2:
        if score1[1] > 85 and score2[1] < 85:
            return score1[2]

    return -1

def year_count_(dict_:dict)->int:
    ''' Return the number of year present in extraction json'''
    if dict_ == {}:
        return 0
    name = ' '.join(list(dict_.keys()))

    m = re.findall("(Year[0-9] Value)", name)
    return len(m)


def check_header(dict_:dict, year_count)->bool:
    ''' Return True if header else False'''

    if year_count == 2 and [normalize(dict_['Year1 Value']), normalize(dict_['Year2 Value'])].count(0.0) == 2:
        return True
    elif year_count == 1 and [normalize(dict_['Year1 Value'])].count(0.0) == 1:
        return True
    elif year_count == 3 and [normalize(dict_['Year1 Value']), normalize(dict_['Year2 Value']), normalize(dict_['Year3 Value'])].count(0.0) == 3:
        return True

    return False


def find_tradepayable_pos(data_:object):
    ''' Return trade payable indexe for BS'''
    
    global tradepayable_pos
    tradepayable_pos = []
    try:    
        for each_lineitem in ['trade payable']:
            score_ =  process.extractOne(each_lineitem, data_['particular'].to_dict(), scorer=fuzz.token_set_ratio)
            # print('********************####################',score_)
            if score_[1] >= 85:
                tradepayable_pos.append(score_[2])
    except Exception as e:
        print('Issue in find_tradepayable_pos:::::',e)
        pass


def find_total_msme(data_:object):
    ''' Under Current Liability class, if "Total" row index has micro, medium, small, MSME, outstanding, dues (OR condition) then that is NOT a calculated field '''
    ''' B/W 0 to first total if trade payble or sundry creditor present then it will be mapeed as calculated field '''
    
    global total_msme_pos, tradepayable_pos, match__
    temp = True
    total_msme_pos = []
    match__ = []
    try:    
        for idx, each_lineitem in enumerate(data_['particular']):
            score_ =  process.extractOne(each_lineitem, ['micro', 'medium', 'small', 'MSME', 'outstanding', 'dues'], scorer=fuzz.token_set_ratio)
            # print('total_msme_pos score::::',score_)
            # print('INDEX:::::::', data_['Label Signage'].iloc[idx])
            if score_[1] >= 85 and fuzz.partial_ratio("".join(each_lineitem.split()), 'total') >= 85 and not data_['Label Signage'].iloc[idx] is 'H':
                total_msme_pos.append(each_lineitem)
                if temp:
                    temp = False
                    if tradepayable_pos:
                        if idx > tradepayable_pos[0]:
                            match__.append(data_['particular'][tradepayable_pos[0]])
                        else:
                            sc = process.extractOne('sundry creditor', data_['particular'].to_dict(), scorer=fuzz.token_set_ratio)
                            if sc[1] > 85:
                                match__.append(data_['particular'][sc[2]])


            
    except Exception as e:
        print('Issue in find_total_msme_pos:::::',e)
        pass


def calculated_field_bs(data : dict, balance_sheet_cls: dict)-> dict:
    """
 
    To find calculated field in lineitems 
 
    Parameters
    ----------
    data : dict
        Input dict of income statement lineitems

    balance_sheet_cls: dict
        Classification of Balance sheet

    Returns
    -------
    data : dict
        
    """
    # print(balance_sheet_cls)
    match = []
    print(balance_sheet_cls)

    global year_count_bs, bs_cal_index, bs_graph_output
    global scenario_flag_bs, total_msme_pos, match__
    bs_cal_index = []

    bs_graph_output = balance_sheet_cls['graph_output']
    # print("BS GRAPH OUTPUT:::", bs_graph_output)
    level2 = [list(e1)[1] for e1 in bs_graph_output if 'Level2.0' in list(e1)[2]]
    level3 = [list(e2)[1] for e2 in bs_graph_output if 'Level3.0' in list(e2)[2] and fuzz.token_set_ratio('net', e2[0]) > 85]
    del balance_sheet_cls['graph_output']

    year_count_bs = year_count_(data['Data']['Financial Tables'][0]['Balance Sheet'][0])
    print('year count bs::::', year_count_bs)

    try:
        '''if non current asset class has net fixed asset corpus and -1 index = depreciation
        -2 index = gross fixed assset corpus then  cal field =True'''
        corpus=yaml_parse()
        net_fixed_asset_corpus=corpus["balance_sheet_BS"]["net_fixed_asset"]
        gross_fixed_assset_corpus=corpus["balance_sheet_BS"]["gross_fixed_assset"]
        # match = ""
        if balance_sheet_cls['Non-current Assets']:
            found = list(filter(lambda each: process.extractOne(each["particular"],net_fixed_asset_corpus, scorer=fuzz.token_sort_ratio)[1] >= 85,\
             balance_sheet_cls['Non-current Assets']))[0]
            
            if fuzz.partial_token_set_ratio(balance_sheet_cls['Non-current Assets'][balance_sheet_cls['Non-current Assets'].index(found)-1]\
                ['particular'], 'depreciation') >= 85: 

                if process.extractOne(balance_sheet_cls['Non-current Assets'][balance_sheet_cls['Non-current Assets'].index(found)-2]\
                    ['particular'],gross_fixed_assset_corpus, scorer=fuzz.token_sort_ratio)[1] >= 85:
                    # match = found["particular"]
                    # match.append(found["particular"])
                    match.append(int(balance_sheet_cls['Non-current Assets'][nested_lookup('particular', balance_sheet_cls['Non-current Assets']).index(found["particular"])]["id"]))
    except:
        print('Net block is not here')
        # print(traceback.print_exc())
        pass

    ''' "equity attributable", under equity class should be claculated field. '''
    try:
        print("Entry1:::")
        lt_ =[l_['particular'] for l_ in balance_sheet_cls['Equity']]

        ea = process.extractOne('attributable', {idx: el for idx, el in enumerate(lt_)}, scorer=fuzz.token_set_ratio)
        print(ea)

        if fuzz.token_set_ratio('equity', ea[0]) > 85 and ea[1] > 85:
            print(ea[0],'$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$::')
            # match.append(ea[0])
            match.append(int(balance_sheet_cls['Equity'][lt_.index(ea[0])]["id"]))
    except:
        pass


    ''' Within BS class(Equity and NCA), if expression contains Closing or Cl (len 2) AND within index -3 there is Opening or OP (len 2), then the expression with Closing or Cl is a calculated field '''
    try:
        print("Entry2(Closing balance):::")
        lt_ =[l_['particular'] for l_ in balance_sheet_cls['Equity']]
        lt__ =[l__['particular'] for l__ in balance_sheet_cls['Non-current Assets']]

        ea = process.extractOne('closing', {idx: el for idx, el in enumerate(lt_)}, scorer=fuzz.token_set_ratio)
        ea_ = process.extractOne('opening', {idx: el for idx, el in enumerate(lt_)}, scorer=fuzz.token_set_ratio)

        nca = process.extractOne('closing', {idx: el for idx, el in enumerate(lt__)}, scorer=fuzz.token_set_ratio)
        nca_ = process.extractOne('opening', {idx: el for idx, el in enumerate(lt__)}, scorer=fuzz.token_set_ratio)

        print(ea, ea_)
        print(nca, nca_)

        if ea[1] > 85 and ea_[1] > 85 and ea[2] > ea_[2] and ea_[2] - ea[2] < 4:
 
            print('Equity Cal filed:::', ea[0])
            # match.append(ea[0])
            match.append(int(balance_sheet_cls['Equity'][lt_.index(ea[0])]["id"]))

        if nca[1] > 85 and nca_[1] > 85 and nca[2] > nca_[2] and nca_[2] - nca[2] < 4:
 
            print('NCA Cal filed:::', ea[0])
            # match.append(nca[0])
            match.append(int(balance_sheet_cls['Non-current Assets'][lt__.index(nca[0])]["id"]))

    except:
        pass

    print('\n\n\n')

    ''' Inner outer calculated filed---> If one outer is present and it is the first index of that class, considered as calculated filed'''

    scenario_flag = 0

    try:
        # for each in balance_sheet_cls:
        for each in ['Equity', 'Non-Current Liabilities', 'Current Liabilities', 'Current Assets', 'Non-current Assets']:
            data_ = pd.DataFrame(balance_sheet_cls[each])
            # print(balance_sheet_cls[each])
            scenario_flag = check_calculatedf_scenario(data_)
            if scenario_flag >= 0:
                break
    except Exception as e:
        print('Exception occured in scenario ...', e)
        print(traceback.print_exc())
        pass

    if scenario_flag == -1:
        print('No SCENARIO found, default 0')   
        scenario_flag = 0

    print('SCENARIO::::$$$$$$$$$:',scenario_flag)
    scenario_flag_bs = scenario_flag

    for each in balance_sheet_cls:
        try:
            if len(balance_sheet_cls[each]) > 0:
                data_ = pd.DataFrame(balance_sheet_cls[each])

                if data['Source']['annualReportType'] == 'T-form (Tally)' and each == 'Equity' and balance_sheet_cls[each]:

                    index_ = profit_loss_account_check(data_.copy())
                    print('INDEX::::::::::::::', index_)

                    if not index_ is -1:
                        print('profit_loss_account_check ACTIVATED::: ')
                        data_['inner_outer'].iloc[index_] = 'outer'


                if each == 'Current Liabilities':
                    find_tradepayable_pos(data_)
                    find_total_msme(data_)
                    if not total_msme_pos:
                        total_msme_pos.append('e')
                    match = match + match__
                    print("total_msme_pos:::::::::::",total_msme_pos, match__)

                print("################################" + each + "####################################")
                # outer_len = len(list(filter(lambda each: True if each=="outer" else False, pd.DataFrame(balance_sheet_cls[each])['inner_outer'] )))
                outer_len = list(data_.apply(lambda x: 1 if x['inner_outer'] == 'outer' and not fuzz.partial_ratio("".join(x['particular'].split()), 'total') > 85 else 0, axis=1)).count(1)
                inner_len = list(data_.apply(lambda x: 1 if x['inner_outer'] == 'inner' and not fuzz.partial_ratio("".join(x['particular'].split()), 'total') > 85 else 0, axis=1)).count(1)

                if outer_len == 1 and data_['inner_outer'].iloc[0] == 'outer' and inner_len > 0 and not any(data_['inner_outer'].iloc[i]==data_['inner_outer'].iloc[i+1] and data_['inner_outer'].iloc[i] == 'outer' for i in range(len(data_['inner_outer'])-1)) and abs(int(data_['id'].iloc[0]) - int(data_['id'].iloc[1])) < 2:
                    print('Inner Outer Found----------------------------------------->', pd.DataFrame(balance_sheet_cls[each])['particular'].iloc[0])
                    # match.append(data_['particular'].iloc[0])
                    match.append(int(balance_sheet_cls[each][nested_lookup('particular', balance_sheet_cls[each]).index(data_['particular'].iloc[0])]["id"]))


                #Disabled XREV-293
                # Multiple outers exists
                else: 
                    if data_['Label Signage'].iloc[0] == 'H':
                        data_ = data_.iloc[1:].reset_index(drop=True)

                    if fuzz.partial_ratio("".join(data_['particular'].iloc[-1].strip()), 'total') > 85 and not data_['inner_outer'].iloc[-2] == 'outer':
                        data_ = data_.iloc[:-1].reset_index(drop=True)

                    if scenario_flag == 1:

                        print('----------------------------CASE 2.1-------------------------')
                        valid_row = [int(data_['id'].iloc[row]) for row in range(0,len(data_['inner_outer'])-1) if data_['inner_outer'].iloc[row]=='outer' and data_['inner_outer'].iloc[row+1]=='inner' and not data_['inner_outer'].iloc[row+1]=='outer' and not data_['Label Signage'].iloc[row] is 'H' and not data_['Label Signage'].iloc[row+1] is 'H' and abs(int(data_['id'].iloc[row]) - int(data_['id'].iloc[row+1])) < 2]
                        print(each, valid_row)
                        match = match + valid_row

                    elif scenario_flag == 2:
                        print('----------------------------CASE 2.2-------------------------')
                        valid_row = [int(data_['id'].iloc[row+1]) for row in range(0,len(data_['inner_outer'])-1) if data_['inner_outer'].iloc[row]=='inner' and data_['inner_outer'].iloc[row+1]=='outer' and not data_['inner_outer'].iloc[row]=='outer' and not data_['Label Signage'].iloc[row] is 'H' and not data_['Label Signage'].iloc[row+1] is 'H']
                        print(each, valid_row)
                        match = match + valid_row

        except:
            print(traceback.print_exc())
            print('No Inner Outer Found----------------------------------------->')

    print('\n\n\n')
    print("CALS INDEX::: ", match)

    for i,BS in enumerate(data["Data"]["Financial Tables"][0]["Balance Sheet"]):

        lineitem_bs=roman_number(BS["Label Name"])
        print(lineitem_bs)

        if (fuzz.partial_ratio("".join(lineitem_bs.split()), 'total') >= 85 and not fuzz.token_sort_ratio(lineitem_bs, 'total comprehensive income') >= 85 and not process.extractOne(lineitem_bs, total_msme_pos, scorer=fuzz.token_sort_ratio)[1] >= 85 )\
        or (lineitem_bs is '' and not check_header(BS, year_count_bs)) or check_header(BS, year_count_bs) or i in match or lineitem_bs is '' or fuzz.token_sort_ratio(lineitem_bs, 'closing balance') >= 85 or i in level2 or i in level3:

            print('----------------------------------Calculated Filed111111------------------------------------------------')
            data['Data']['Financial Tables'][0]['Balance Sheet'][i].update({"Calculated Field":True})
            bs_cal_index.append(i)

            '''If any line item contains net it will be checked in all classes. With position no. >1 of individual class considered as calculated filed'''
        elif lineitem_bs.startswith('net') or lineitem_bs.endswith('net'):
            for dic in balance_sheet_cls:
                try:
                    found = list(filter(lambda each: fuzz.token_sort_ratio(lineitem_is, each['particular']) >= 95, balance_sheet_cls[dic]))[0]

                    if balance_sheet_cls[dic].index(found) > 1 or fuzz.token_sort_ratio(lineitem_bs, 'Net Current Assets') >= 85:
                        print('--------------------------------Calculated Filed22222----------------------------------------')
                        data['Data']['Financial Tables'][0]['Balance Sheet'][i].update({"Calculated Field":True})
                        bs_cal_index.append(i)
                        break

                except Exception as e:
                    # print(e)
                    pass
        else:
            data['Data']['Financial Tables'][0]['Balance Sheet'][i].update({"Calculated Field":False})
 
    return data


def find_first_header(df_:object):

    """
    To find the first header of any lineitem of a class.
    """
    header = []
    
    outer_len = len(list(filter(lambda each: True if each=="outer" else False, df_['inner_outer'] )))

    if outer_len == 1 and df_['inner_outer'].iloc[0] == 'outer':
        print('first_header is the outer----------------------------------------->')
        header.append(0) 
    else:
        print('No Inner Outer Found-------Checking other headers---------------------------------->')
        header = list(set([idx if each == 'H' else False for idx,each in enumerate(df_['Label Signage'])]))

    if isinstance(header[0],bool) and len(header)==1:
        header = []

    return header


def OTHRNCA_pos(df_:object, classes: list):

    df_.set_index("Class",  inplace = True)
    # print(classes)
    df_ = df_.loc[['Non-current Assets']]
    df_ = df_.loc[classes]
    df_ = df_.apply(lambda s: s.fillna({i: [] for i in df_.index}))
    # print(df_)
    df_['combined']= df_.apply(lambda x: [x['Lineitem']]+ x['Corpus'] ,axis=1)

    line_score = [process.extractOne('Other Non-Current Assets', each, scorer=fuzz.token_sort_ratio)[1] for each in df_['combined']]

    onca_lineitem = df_['Lineitem'].iloc[line_score.index(max(line_score))]
    onca_label = df_['chart_of_accounts'].iloc[line_score.index(max(line_score))]
    onca_corpus = df_['combined'].iloc[line_score.index(max(line_score))]

    onca_subclass = df_['Subclass'].iloc[line_score.index(max(line_score))]
    onca_subclasscode = df_['SubClasscode'].iloc[line_score.index(max(line_score))]

    return onca_lineitem, onca_label, onca_corpus, onca_subclass, onca_subclasscode

def secured_loan_pos(df_:object, classes: list):

    df_.set_index("Class",  inplace = True)
    # print(classes)
    # df_ = df_.loc[classes]
    df_ = df_.loc[['Non-Current Liabilities']]
    df_ = df_.apply(lambda s: s.fillna({i: [] for i in df_.index}))
    # print(df_)
    df_['combined']= df_.apply(lambda x: [x['Lineitem']]+ x['Corpus'] ,axis=1)

    line_score = [process.extractOne('secured loan', each, scorer=fuzz.token_sort_ratio)[1] for each in df_['combined']]

    sl_lineitem = df_['Lineitem'].iloc[line_score.index(max(line_score))]
    sl_label = df_['chart_of_accounts'].iloc[line_score.index(max(line_score))]
    sl_corpus = df_['combined'].iloc[line_score.index(max(line_score))]

    sl_subclass = df_['Subclass'].iloc[line_score.index(max(line_score))]
    sl_subclasscode = df_['SubClasscode'].iloc[line_score.index(max(line_score))]

    return sl_lineitem, sl_label, sl_corpus, sl_subclass, sl_subclasscode


def machinary_pos(df_:object, classes: list):

    df_.set_index("Class",  inplace = True)
    # print(classes)
    df_ = df_.loc[classes]
    df_ = df_.apply(lambda s: s.fillna({i: [] for i in df_.index}))
    # print(df_)
    df_['combined']= df_.apply(lambda x: [x['Lineitem']]+ x['Corpus'] ,axis=1)

    line_score = [process.extractOne('Loan against Machinery', each, scorer=fuzz.token_sort_ratio)[1] for each in df_['combined']]

    machinary_lineitem = df_['Lineitem'].iloc[line_score.index(max(line_score))]
    machinary_label = df_['chart_of_accounts'].iloc[line_score.index(max(line_score))]
    machinary_corpus = df_['combined'].iloc[line_score.index(max(line_score))]

    machinary_subclass = df_['Subclass'].iloc[line_score.index(max(line_score))]
    machinary_subclasscode = df_['SubClasscode'].iloc[line_score.index(max(line_score))]

    return machinary_lineitem, machinary_label, machinary_corpus, machinary_subclass, machinary_subclasscode

def unsecured_loan_pos(df_:object, classes: list):

    df_.set_index("Class",  inplace = True)
    # print(classes)
    # df_ = df_.loc[classes]
    df_ = df_.loc[['Non-Current Liabilities']]
    df_ = df_.apply(lambda s: s.fillna({i: [] for i in df_.index}))
    # print(df_)
    df_['combined']= df_.apply(lambda x: [x['Lineitem']]+ x['Corpus'] ,axis=1)

    line_score = [process.extractOne('unsecured loan', each, scorer=fuzz.token_sort_ratio)[1] for each in df_['combined']]

    usl_lineitem = df_['Lineitem'].iloc[line_score.index(max(line_score))]
    usl_label = df_['chart_of_accounts'].iloc[line_score.index(max(line_score))]

    usl_subclass = df_['Subclass'].iloc[line_score.index(max(line_score))]
    usl_subclasscode = df_['SubClasscode'].iloc[line_score.index(max(line_score))]

    return usl_lineitem, usl_label, usl_subclass, usl_subclasscode


def other_fixed_asset_pos(df_:object, classes: list):

    df_.set_index("Class",  inplace = True)
    # print(classes)
    df_ = df_.loc[classes]
    df_ = df_.apply(lambda s: s.fillna({i: [] for i in df_.index}))
    # print(df_)
    df_['combined']= df_.apply(lambda x: [x['Lineitem']]+ x['Corpus'] ,axis=1)

    line_score = [process.extractOne('Other Fixed Assets (Net Block)', each, scorer=fuzz.token_sort_ratio)[1] for each in df_['combined']]

    ofa_lineitem = df_['Lineitem'].iloc[line_score.index(max(line_score))]
    ofa_label = df_['chart_of_accounts'].iloc[line_score.index(max(line_score))]

    ofa_subclass = df_['Subclass'].iloc[line_score.index(max(line_score))]
    ofa_subclasscode = df_['SubClasscode'].iloc[line_score.index(max(line_score))]

    return ofa_lineitem, ofa_label, ofa_subclass, ofa_subclasscode

def cash_bank_pos(df_:object, classes: list):

    df_.set_index("Class",  inplace = True)
    # print(classes)
    df_ = df_.loc[classes]
    df_ = df_.apply(lambda s: s.fillna({i: [] for i in df_.index}))
    # print(df_)
    df_['combined']= df_.apply(lambda x: [x['Lineitem']]+ x['Corpus'] ,axis=1)

    line_score = [process.extractOne('Cash & Bank Balance', each, scorer=fuzz.token_sort_ratio)[1] for each in df_['combined']]

    cb_lineitem = df_['Lineitem'].iloc[line_score.index(max(line_score))]
    cb_label = df_['chart_of_accounts'].iloc[line_score.index(max(line_score))]

    cb_subclass = df_['Subclass'].iloc[line_score.index(max(line_score))]
    cb_subclasscode = df_['SubClasscode'].iloc[line_score.index(max(line_score))]

    return cb_lineitem, cb_label, cb_subclass, cb_subclasscode

def ownmoney_pos(df_:object, classes: list):

    df_.set_index("Class",  inplace = True)
    # print(classes)
    df_ = df_.loc[['Non-Current Liabilities']]
    df_ = df_.apply(lambda s: s.fillna({i: [] for i in df_.index}))
    # print(df_)
    df_['combined']= df_.apply(lambda x: [x['Lineitem']]+ x['Corpus'] ,axis=1)

    line_score = [process.extractOne('ownmoney', each, scorer=fuzz.token_sort_ratio)[1] for each in df_['combined']]

    om_lineitem = df_['Lineitem'].iloc[line_score.index(max(line_score))]
    om_label = df_['chart_of_accounts'].iloc[line_score.index(max(line_score))]

    om_subclass = df_['Subclass'].iloc[line_score.index(max(line_score))]
    om_subclasscode = df_['SubClasscode'].iloc[line_score.index(max(line_score))]

    return om_lineitem, om_label, om_subclass, om_subclasscode

def land_pos(df_:object, classes: list):

    df_.set_index("Class",  inplace = True)
    # print(classes)
    df_ = df_.loc[classes]
    df_ = df_.apply(lambda s: s.fillna({i: [] for i in df_.index}))
    # print(df_)
    df_['combined']= df_.apply(lambda x: [x['Lineitem']]+ x['Corpus'] ,axis=1)

    line_score = [process.extractOne('land', each, scorer=fuzz.token_sort_ratio)[1] for each in df_['combined']]

    land_lineitem = df_['Lineitem'].iloc[line_score.index(max(line_score))]
    land_label = df_['chart_of_accounts'].iloc[line_score.index(max(line_score))]

    land_subclass = df_['Subclass'].iloc[line_score.index(max(line_score))]
    land_subclasscode = df_['SubClasscode'].iloc[line_score.index(max(line_score))]

    return land_lineitem, land_label, land_subclass, land_subclasscode

def capitalacc_pos(df_:object, classes: list):

    df_.set_index("Class",  inplace = True)
    # print(classes)
    df_ = df_.loc[classes]
    df_ = df_.apply(lambda s: s.fillna({i: [] for i in df_.index}))
    # print(df_)
    df_['combined']= df_.apply(lambda x: [x['Lineitem']]+ x['Corpus'] ,axis=1)

    line_score = [process.extractOne('Capital Account', each, scorer=fuzz.token_sort_ratio)[1] for each in df_['combined']]

    capital_lineitem = df_['Lineitem'].iloc[line_score.index(max(line_score))]
    capital_label = df_['chart_of_accounts'].iloc[line_score.index(max(line_score))]

    capital_subclass = df_['Subclass'].iloc[line_score.index(max(line_score))]
    capital_subclasscode = df_['SubClasscode'].iloc[line_score.index(max(line_score))]

    return capital_lineitem, capital_label, capital_subclass, capital_subclasscode

def capitalreserve_pos(df_:object, classes: list):

    df_.set_index("Class",  inplace = True)
    # print(classes)
    df_ = df_.loc[classes]
    df_ = df_.apply(lambda s: s.fillna({i: [] for i in df_.index}))
    # print(df_)
    df_['combined']= df_.apply(lambda x: [x['Lineitem']]+ x['Corpus'] ,axis=1)

    line_score = [process.extractOne('Capital Reserve', each, scorer=fuzz.token_sort_ratio)[1] for each in df_['combined']]

    capitalres_lineitem = df_['Lineitem'].iloc[line_score.index(max(line_score))]
    capitalres_label = df_['chart_of_accounts'].iloc[line_score.index(max(line_score))]

    capitalres_subclass = df_['Subclass'].iloc[line_score.index(max(line_score))]
    capitalres_subclasscode = df_['SubClasscode'].iloc[line_score.index(max(line_score))]

    return capitalres_lineitem, capitalres_label, capitalres_subclass, capitalres_subclasscode


def capitalsubsidy_pos(df_:object, classes: list):

    df_.set_index("Class",  inplace = True)
    # print(classes)
    df_ = df_.loc[classes]
    df_ = df_.apply(lambda s: s.fillna({i: [] for i in df_.index}))
    # print(df_)
    df_['combined']= df_.apply(lambda x: [x['Lineitem']]+ x['Corpus'] ,axis=1)

    line_score = [process.extractOne('Capital Subsidy', each, scorer=fuzz.token_sort_ratio)[1] for each in df_['combined']]

    capitalsub_lineitem = df_['Lineitem'].iloc[line_score.index(max(line_score))]
    capitalsub_label = df_['chart_of_accounts'].iloc[line_score.index(max(line_score))]

    capitalsub_subclass = df_['Subclass'].iloc[line_score.index(max(line_score))]
    capitalsub_subclasscode = df_['SubClasscode'].iloc[line_score.index(max(line_score))]

    return capitalsub_lineitem, capitalsub_label, capitalsub_subclass, capitalsub_subclasscode


def partner_salary_pos(df_:object, classes: list):

    df_.set_index("Class",  inplace = True)
    print(classes)
    df_ = df_.loc[classes]
    df_ = df_.apply(lambda s: s.fillna({i: [] for i in df_.index}))
    # print(df_)
    df_['combined']= df_.apply(lambda x: [x['Lineitem']]+ x['Corpus'] ,axis=1)

    line_score = [process.extractOne("Partner's Remuneration", each, scorer=fuzz.token_sort_ratio)[1] for each in df_['combined']]

    partner_salary_lineitem = df_['Lineitem'].iloc[line_score.index(max(line_score))]
    partner_salary_label = df_['chart_of_accounts'].iloc[line_score.index(max(line_score))]

    partner_salary_subclass = df_['Subclass'].iloc[line_score.index(max(line_score))]
    partner_salary_subclasscode = df_['SubClasscode'].iloc[line_score.index(max(line_score))]

    return partner_salary_lineitem, partner_salary_label, partner_salary_subclass, partner_salary_subclasscode


def partner_capital_pos(df_:object, classes: list):

    df_.set_index("Class",  inplace = True)
    # print(classes)
    df_ = df_.loc[classes]
    df_ = df_.apply(lambda s: s.fillna({i: [] for i in df_.index}))
    # print(df_)
    df_['combined']= df_.apply(lambda x: [x['Lineitem']]+ x['Corpus'] ,axis=1)

    line_score = [process.extractOne("Interest on Partner's Capital", each, scorer=fuzz.token_sort_ratio)[1] for each in df_['combined']]

    partner_capital_lineitem = df_['Lineitem'].iloc[line_score.index(max(line_score))]
    partner_capital_label = df_['chart_of_accounts'].iloc[line_score.index(max(line_score))]

    partner_capital_subclass = df_['Subclass'].iloc[line_score.index(max(line_score))]
    partner_capital_subclasscode = df_['SubClasscode'].iloc[line_score.index(max(line_score))]

    return partner_capital_lineitem, partner_capital_label, partner_capital_subclass, partner_capital_subclasscode


def interest_expense_pos(df_:object, classes: list):

    df_.set_index("Class",  inplace = True)
    # print(classes)
    df_ = df_.loc[classes]
    df_ = df_.apply(lambda s: s.fillna({i: [] for i in df_.index}))
    # print(df_)
    df_['combined']= df_.apply(lambda x: [x['Lineitem']]+ x['Corpus'] ,axis=1)

    line_score = [process.extractOne("Interest Expense", each, scorer=fuzz.token_sort_ratio)[1] for each in df_['combined']]

    interest_expense_lineitem = df_['Lineitem'].iloc[line_score.index(max(line_score))]
    interest_expense_label = df_['chart_of_accounts'].iloc[line_score.index(max(line_score))]

    interest_expense_subclass = df_['Subclass'].iloc[line_score.index(max(line_score))]
    interest_expense_subclasscode = df_['SubClasscode'].iloc[line_score.index(max(line_score))]

    return interest_expense_lineitem, interest_expense_label, interest_expense_subclass, interest_expense_subclasscode


def creditors_pos(df_:object, classes: list):

    df_.set_index("Class",  inplace = True)
    # print(classes)
    df_ = df_.loc[classes]
    df_ = df_.apply(lambda s: s.fillna({i: [] for i in df_.index}))
    # print(df_)
    df_['combined']= df_.apply(lambda x: [x['Lineitem']]+ x['Corpus'] ,axis=1)

    line_score = [process.extractOne("creditors", each, scorer=fuzz.token_sort_ratio)[1] for each in df_['combined']]

    creditors_lineitem = df_['Lineitem'].iloc[line_score.index(max(line_score))]
    creditors_label = df_['chart_of_accounts'].iloc[line_score.index(max(line_score))]

    creditors_expense_subclass = df_['Subclass'].iloc[line_score.index(max(line_score))]
    creditors_expense_subclasscode = df_['SubClasscode'].iloc[line_score.index(max(line_score))]

    return creditors_lineitem, creditors_label, creditors_expense_subclass, creditors_expense_subclasscode


def overdraft_pos(df__:object, classes: list):

    df__.set_index("Class",  inplace = True)
    # print(classes)
    df_ = df__.loc[['Non-Current Liabilities']]
    df1_ = df__.loc[['Current Liabilities']]

    df_ = df_.apply(lambda s: s.fillna({i: [] for i in df_.index}))
    # print(df_)
    df_['combined']= df_.apply(lambda x: [x['Lineitem']]+ x['Corpus'] ,axis=1)

    df1_ = df1_.apply(lambda s: s.fillna({i: [] for i in df1_.index}))
    # print(df_)
    df1_['combined']= df1_.apply(lambda x: [x['Lineitem']]+ x['Corpus'] ,axis=1)

    line_score = [process.extractOne("CC / OD / BD / Packing-Credit / Factoring - Non Current", each, scorer=fuzz.token_sort_ratio)[1] for each in df_['combined']]
    line_score2 = [process.extractOne("CC / OD / BD / Packing-Credit / Factoring - Current", each, scorer=fuzz.token_sort_ratio)[1] for each in df1_['combined']]

    overdraft_noncurrent_lineitem = df_['Lineitem'].iloc[line_score.index(max(line_score))]
    overdraft_noncurrent_label = df_['chart_of_accounts'].iloc[line_score.index(max(line_score))]

    overdraft_current_lineitem = df1_['Lineitem'].iloc[line_score2.index(max(line_score2))]
    overdraft_current_label = df1_['chart_of_accounts'].iloc[line_score2.index(max(line_score2))]

    overdraft_noncurrent_subclass = df_['Subclass'].iloc[line_score.index(max(line_score))]
    overdraft_noncurrent_subclasscode = df_['SubClasscode'].iloc[line_score.index(max(line_score))]

    overdraft_current_subclass = df1_['Subclass'].iloc[line_score2.index(max(line_score2))]
    overdraft_current_subclasscode = df1_['SubClasscode'].iloc[line_score2.index(max(line_score2))]

    return overdraft_noncurrent_lineitem, overdraft_noncurrent_label, overdraft_current_lineitem, overdraft_current_label, overdraft_noncurrent_subclass, overdraft_noncurrent_subclasscode, overdraft_current_subclass, overdraft_current_subclasscode


def openingclosingstock_pos(df_:object, classes: list):

    df_.set_index("Class",  inplace = True)
    # print(classes)
    df_ = df_.loc[classes]
    df_ = df_.apply(lambda s: s.fillna({i: [] for i in df_.index}))
    # print(df_)
    df_['combined']= df_.apply(lambda x: [x['Lineitem']]+ x['Corpus'] ,axis=1)

    line_score = [process.extractOne("Opening Stock", each, scorer=fuzz.token_sort_ratio)[1] for each in df_['combined']]
    line_score2 = [process.extractOne("Closing Stock", each, scorer=fuzz.token_sort_ratio)[1] for each in df_['combined']]

    openingstock_lineitem = df_['Lineitem'].iloc[line_score.index(max(line_score))]
    openingstock_label = df_['chart_of_accounts'].iloc[line_score.index(max(line_score))]

    closingstock_lineitem = df_['Lineitem'].iloc[line_score2.index(max(line_score2))]
    closingstock_label = df_['chart_of_accounts'].iloc[line_score2.index(max(line_score2))]

    openingstock_subclass = df_['Subclass'].iloc[line_score.index(max(line_score))]
    openingstock_subclasscode = df_['SubClasscode'].iloc[line_score.index(max(line_score))]

    closingstock_subclass = df_['Subclass'].iloc[line_score2.index(max(line_score2))]
    closingstock_subclasscode = df_['SubClasscode'].iloc[line_score2.index(max(line_score2))]

    return openingstock_lineitem, openingstock_label, closingstock_lineitem, closingstock_label, openingstock_subclass, openingstock_subclasscode, closingstock_subclass, closingstock_subclasscode


def make_suggestion(lineitem:str, confidence:int, class_:str, subclass:str, subclasscode:str, label:str, labelitem:str, classcode:str)-> dict:
    

    suggestion = {"lineitem" : str, "confidence"  : int, "class" : str, "subclass" : str, "subclasscode" : str, "label" : str, "labelitem" : str, "classcode" : str}
    # print(lineitem, confidence, class_, label, labelitem)
    
    suggestion["lineitem"] = lineitem
    suggestion["confidence"] = confidence
    suggestion["class"] = class_

    suggestion["subclass"] = subclass
    suggestion["subclasscode"] = subclasscode
    
    suggestion["classcode"] = classcode

    suggestion["label"] = label
    suggestion["labelitem"] = labelitem

    return suggestion


# def add_label_signage(DATA, data):



def BS_mapping_override(lineitem:str)->bool:
    
    """
 
    Many to many mapping for Income Statement
 
    Parameters
    ----------
    lineitem: str
        Requested lineitem from extraction

    Returns
    -------
    bool:
        Returns True if matched with corpus else False
        
 
    """
    corpus=yaml_parse()
    secured_loans_domain_corpus=corpus["balance_sheet_BS"]["secured_loans_domain"]



    if any(fuzz.partial_token_set_ratio(lineitem.lower(), c.lower()) >= 85 for c in secured_loans_domain_corpus):

        if fuzz.partial_token_set_ratio(lineitem.lower(), 'finance') >= 85 and fuzz.partial_token_set_ratio(lineitem.lower(), 'other') >= 85:
            return False
        return True
    else:
        return False

def check_unsecured_loan_previous_immediate_header(df_:object, idx:int)->bool:
    ''' For non current liability if previous immediate header is unsecured loan then it will be mapped to previous immediate header mapping'''

    header = find_first_header(df_)
    print('headers===>', header)

    try:
        if header:
            if len(header) >1:
                nearest_header = [el for el in header if el < idx][-1]
            else:
                nearest_header = header[0]

            print('@@@@@@@@@@@@@@check_unsecured_loan_previous_immediate_header===>', df_['particular'].iloc[nearest_header])
            if fuzz.token_set_ratio('unsecured loan', df_['particular'].iloc[nearest_header]) > 95:
                return False

            return True
    except:
        return True


def check_person(name:str)->bool:

    doc = nlp(name)
    split_name = name.split(' ')

    for X in doc.ents:
        if X.label_ == 'PERSON' and not 'cc' in split_name and not 'od' in split_name:
            return True

    return False



def BS_mapping(DATA:dict, df_temp:object, bs_data:dict)->dict:
    """
 
    Many to many mapping for Income Statement
 
    Parameters
    ----------
    DATA : dict 
        Requested dict from extraction

    df_temp : object
        Template in dataframe format

    is_data : dict
        Income statement classification

    Returns
    -------
    dict:
        Income Statement Mapping attached with extraction dict 
        
 
    """
    # print(bs_data)
    global year_count_bs
    global scenario_flag_bs, tradepayable_pos, bs_graph_output

    template_code = DATA['Source']['templateUrl'].split('/')[-2]
    print('----------------------BS classes-------------------')
    classes = list(bs_data.keys())

    onca_lineitem, onca_label, onca_corpus, onca_subclass, onca_subclasscode = OTHRNCA_pos(df_temp.copy(), classes)
    sl_lineitem, sl_label, sl_corpus, sl_subclass, sl_subclasscode = secured_loan_pos(df_temp.copy(), classes)
    machinary_lineitem, machinary_label, machinary_corpus, machinary_subclass, machinary_subclasscode = machinary_pos(df_temp.copy(), classes)
    
    usl_lineitem, usl_label, usl_subclass, usl_subclasscode = unsecured_loan_pos(df_temp.copy(), classes)
    ofa_lineitem, ofa_label, ofa_subclass, ofa_subclasscode = other_fixed_asset_pos(df_temp.copy(), classes)
    cb_lineitem, cb_label, cb_subclass, cb_subclasscode = cash_bank_pos(df_temp.copy(), classes)
    om_lineitem, om_label, om_subclass, om_subclasscode = ownmoney_pos(df_temp.copy(), classes)
    land_lineitem, land_label, land_subclass, land_subclasscode = land_pos(df_temp.copy(), classes)
    capital_lineitem, capital_label, capital_subclass, capital_subclasscode = capitalacc_pos(df_temp.copy(), classes)
    capitalsub_lineitem, capitalsub_label, capitalsub_subclass, capitalsub_subclasscode = capitalsubsidy_pos(df_temp.copy(), classes)
    capitalres_lineitem, capitalres_label, capitalres_subclass, capitalres_subclasscode = capitalreserve_pos(df_temp.copy(), classes)
    creditors_lineitem, creditors_label, creditor_subclass, creditor_subclasscode = creditors_pos(df_temp.copy(), classes)
    overdraft_noncurrent_lineitem, overdraft_noncurrent_label, overdraft_current_lineitem, overdraft_current_label, overdraft_noncurrent_subclass, overdraft_noncurrent_subclasscode, overdraft_current_subclass, overdraft_current_subclasscode = overdraft_pos(df_temp.copy(), classes)

    print(onca_lineitem, onca_label, "++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(sl_lineitem, sl_label, "++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(machinary_lineitem, machinary_label, "++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(usl_lineitem, usl_label, "++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(ofa_lineitem, ofa_label, "++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(cb_lineitem, cb_label, "++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(om_lineitem, om_label, "++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(land_lineitem, land_label, "++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(capital_lineitem, capital_label, "++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(capitalsub_lineitem, capitalsub_label, "++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(capitalres_lineitem, capitalres_label, "++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(overdraft_noncurrent_lineitem, overdraft_noncurrent_label, overdraft_current_lineitem, overdraft_current_label, "++++++++++++++++++++++++++++++++++")


    T1 = 55
    T2 = 0

    equity_header_mapped_lineitem = []

    print(classes)
    print(df_temp['Class'].to_list())

    # print(data['Profit and Loss_IS'])
    lineitems = [roman_number(a.strip()) for a in list(map(itemgetter('Label Name'), DATA['Data']['Financial Tables'][0]["Balance Sheet"]))]

    year1_values = list(map(itemgetter('Year1 Value'), DATA['Data']['Financial Tables'][0]["Balance Sheet"]))
    year1_ = DATA['Data']['Financial Tables'][0]["Balance Sheet"][0]['Year1']


    print('^^^^^^^^^^^^^^^^^^^^^lineitems^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
    print(lineitems)
    print(year1_values)

    for each in classes:
        if each in df_temp['Class'].to_list() and bs_data[each]: 
    
            print('###############################################',each,'##################################################')
            # new_df = pd.concat([pd.DataFrame(bs_data[each])['particular'], pd.DataFrame(bs_data[each]).iloc[:,1] ,pd.DataFrame(bs_data[each])['inner_outer'], \
            #     df_temp[df_temp['Class'].str.contains(each)]['Lineitem'].reset_index(drop=True), df_temp[df_temp['Class'].str.contains(each)]['Corpus'].reset_index(drop=True)\
            #     , df_temp[df_temp['Class'].str.contains(each)]['chart_of_accounts'].reset_index(drop=True),pd.DataFrame(bs_data[each])['Label Signage'],df_temp[df_temp['Class']\
            #     .str.contains(each)]['Residual'].reset_index(drop=True)], axis=1, sort=False)

            new_df = pd.concat([pd.DataFrame(bs_data[each])['particular'], pd.DataFrame(bs_data[each])[year1_] ,pd.DataFrame(bs_data[each])['inner_outer'], \
                df_temp[df_temp['Class']==each]['Lineitem'].reset_index(drop=True), df_temp[df_temp['Class']==each]['Corpus'].reset_index(drop=True)\
                , df_temp[df_temp['Class']==each]['chart_of_accounts'].reset_index(drop=True),pd.DataFrame(bs_data[each])['Label Signage'],df_temp[df_temp['Class']\
                ==each]['Residual'].reset_index(drop=True), df_temp[df_temp['Class']==each]['Classcode'].reset_index(drop=True), df_temp[df_temp['Class']==each]['Subclass'].reset_index(drop=True), df_temp[df_temp['Class']==each]['SubClasscode'].reset_index(drop=True), pd.DataFrame(bs_data[each])['id']], axis=1, sort=False)

            new_df["id"] = new_df["id"].apply(lambda x: int(x) if x == x else "")
            print(new_df)
            scores = []
            line_score = []
            # suggestion = {"lineitem" : str, "confidence"  : int, "class" : str, "label" : str, "labelitem" : str}
            suggestion = {}
            previous_suggestion = {}
            map_ = []

            for idx, each2 in enumerate(new_df['particular'].to_list()):
                if isinstance(each2, str):

                    print('Previous###  ', each2)
                    each2 = remove_stopwords(each2, each)
                    print('After Stopword removal###  ', each2)

                    for idx2, each3 in enumerate(new_df['Lineitem'].to_list()):
                        
                        if isinstance(each3, str):
                            # print(each3, idx2, "####################", each2, idx)
                    
                            if isinstance(new_df['Corpus'].iloc[idx2], list):
                                corpus = new_df['Corpus'].iloc[idx2]
                                corpus.append(each3)
                            else:
                                corpus = [each3]

                            line_score.append(process.extractOne(each2, corpus, scorer=fuzz.token_sort_ratio)[1])

                    print(line_score)
                    
                    pos = line_score.index(max(line_score))
                    max_score = max(line_score)

                    # print(new_df['Lineitem'].dropna().unique().tolist())

                    if len(new_df['Lineitem'].dropna().unique().tolist()) == 1:
                        threshold = T2
                    else:
                        threshold = T1

                    # match = process.extract(new_df['particular'].iloc[idx].strip(), lineitems_dict, scorer=fuzz.ratio)
                    # lineitems_dict = {idx: el for idx, el in enumerate(lineitems)}
                    # print(match)
                    match = new_df['id'].iloc[idx]

                    print('\nAfter Signage:::')
                    ''' ************************* BALANCE SHEET SIGNAGE *************************************'''

                    for yc in range(year_count_bs):

                        sign = 1

                        if each in ['Non-current Assets']:
                            sign =  -1 if new_df['Label Signage'].iloc[idx] == '-'  else 1

                        elif each in ['Equity']:

                            if (fuzz.token_set_ratio(new_df['particular'].iloc[idx].strip().lower(), 'drawings') > 90 or match in [list(e1)[1] for e1 in bs_graph_output if 'Level6a' in list(e1)[2]]):

                                if normalize(DATA['Data']['Financial Tables'][0]["Balance Sheet"][match]['Year'+str(yc+1)+' Value']) < 0:
                                    pass

                                elif normalize(DATA['Data']['Financial Tables'][0]["Balance Sheet"][match]['Year'+str(yc+1)+' Value']) > 0 and new_df['Label Signage'].iloc[idx] == '+':
                                    sign =  -1

                                else:
                                    sign =  -1 if new_df['Label Signage'].iloc[idx] == '-'  else 1

                            else:
                                sign =  -1 if new_df['Label Signage'].iloc[idx] == '-'  else 1

                        print('Year'+str(yc+1)+' Value OLD::: ', normalize(DATA['Data']['Financial Tables'][0]["Balance Sheet"][match]['Year'+str(yc+1)+' Value']))
                        value = normalize(DATA['Data']['Financial Tables'][0]["Balance Sheet"][match]['Year'+str(yc+1)+' Value']) * sign
                        print('Year'+str(yc+1)+' Value NEW::: ', value)

                        DATA['Data']['Financial Tables'][0]["Balance Sheet"][match]['Year'+str(yc+1)+' Value'] = str(value)
                        bs_data[each][idx][list(bs_data[each][idx].keys())[1]] = value
                        DATA['Data']['Financial Tables'][0]["Balance Sheet"][match].update({DATA['Data']['Financial Tables'][0]["Balance Sheet"][match]['Year'+str(yc+1)+' Value']: value})


                    DATA['Data']['Financial Tables'][0]["Balance Sheet"][match].update({'particular':new_df['particular'].iloc[idx].strip()})
                    DATA['Data']['Financial Tables'][0]["Balance Sheet"][match].update({'Label Signage':new_df['Label Signage'].iloc[idx].strip()})

                    # print('------------equity_header_mapped_lineitem--------', equity_header_mapped_lineitem)

                    if max_score >= threshold and not new_df['particular'].iloc[idx].strip() is '' and not check_person(new_df['particular'].iloc[idx].strip()) and not fuzz.token_set_ratio(new_df['particular'].iloc[idx].strip(),'land') > 95:
                        suggestion = make_suggestion(new_df['Lineitem'].iloc[pos], max_score, each, new_df['Subclass'].iloc[pos], new_df['SubClasscode'].iloc[pos], new_df['chart_of_accounts'].iloc[pos], new_df['particular'].iloc[idx].strip(), new_df['Classcode'].iloc[0].strip())
                              
                        ''' If contains land then it should be mapped to Land and Building / Property'''      
                    if fuzz.token_set_ratio(new_df['particular'].iloc[idx].strip(),'land') > 95:

                        suggestion = make_suggestion(land_lineitem, max_score, each, land_subclass, land_subclasscode, land_label, new_df['particular'].iloc[idx].strip(), new_df['Classcode'].iloc[0].strip())


                        ''' If class is Equity and should contain “Subsidy” should be mapped to Capital Subsidy'''      
                    if fuzz.token_set_ratio(new_df['particular'].iloc[idx].strip(),'subsidy') > 95 and each.lower() == 'equity':

                        suggestion = make_suggestion(capitalsub_lineitem, max_score, each, capitalsub_subclass, capitalsub_subclasscode, capitalsub_label, new_df['particular'].iloc[idx].strip(), new_df['Classcode'].iloc[0].strip())


                        ''' If class is Equity and should contain “reserve” should be mapped to Capital Reserve'''      
                    if fuzz.token_set_ratio(new_df['particular'].iloc[idx].strip(),'reserve') > 95 and each.lower() == 'equity':

                        suggestion = make_suggestion(capitalres_lineitem, max_score, each, capitalres_subclass, capitalres_subclasscode, capitalres_label, new_df['particular'].iloc[idx].strip(), new_df['Classcode'].iloc[0].strip())


                        ''' If class is Equity and should contain “Capital” but not “Subsidy” or “Reserve” should be mapped to capital acc'''      
                    if fuzz.token_set_ratio(new_df['particular'].iloc[idx].strip(),'capital') > 95 and process.extractOne(new_df['particular'].iloc[idx].strip(), ['subsidy', 'reserve'], scorer=fuzz.token_sort_ratio)[1] < 80 and each.lower() == 'equity':

                        suggestion = make_suggestion(capital_lineitem, max_score, each, capital_subclass, capital_subclasscode, capital_label, new_df['particular'].iloc[idx].strip(), new_df['Classcode'].iloc[0].strip())


                        '''Threshold doesnot match so overriding will work for secured and unsecured loans'''
                    elif each in ['Non-Current Liabilities', 'Current Liabilities'] and not new_df['particular'].iloc[idx].strip() is '':

                    #'''If contains secured then map to secured loans'''
                        if fuzz.token_set_ratio('secured', new_df['particular'].iloc[idx].strip().lower()) >= 95:
                            print('-------------- MATCHED to SECURED LOANS---------------')
                            suggestion = make_suggestion(sl_lineitem, max_score, each, sl_subclass, sl_subclasscode, sl_label, new_df['particular'].iloc[idx].strip(), new_df['Classcode'].iloc[0].strip())

                            

                    #'''If contains unsecured then map to unsecured loans'''
                        elif fuzz.token_set_ratio('unsecured', new_df['particular'].iloc[idx].strip().lower()) >= 95:
                            print('--------------MATCHED to UNSECURED LOANS---------------')
                            suggestion = make_suggestion(usl_lineitem, max_score, each, usl_subclass, usl_subclasscode, usl_label, new_df['particular'].iloc[idx].strip(), new_df['Classcode'].iloc[0].strip())


                    #'''If Non-Current Liabilities contains 'CC / OD / BD' then map to CC / OD / BD / Packing-Credit / Factoring - Non Current'''
                        elif any(ind in new_df['particular'].iloc[idx].strip().lower().split() for ind in ['od','cc','bd']) and each in ['Non-Current Liabilities']:

                            print("-------------- MATCHED to 'CC / OD / BD' then map to CC / OD / BD / Packing-Credit / Factoring - Non Current---------------")
                            suggestion = make_suggestion(overdraft_noncurrent_lineitem, max_score, each, overdraft_noncurrent_subclass, overdraft_noncurrent_subclasscode, overdraft_noncurrent_label, new_df['particular'].iloc[idx].strip(), new_df['Classcode'].iloc[0].strip())

                    #'''If Current Liabilities contains 'CC / OD / BD' then map to CC / OD / BD / Packing-Credit / Factoring - Current'''
                        elif any(ind in new_df['particular'].iloc[idx].strip().lower().split() for ind in ['od','cc','bd']) and each in ['Current Liabilities']:

                            print("-------------- MATCHED to 'CC / OD / BD' then map to CC / OD / BD / Packing-Credit / Factoring - Current---------------")
                            suggestion = make_suggestion(overdraft_current_lineitem, max_score, each, overdraft_current_subclass, overdraft_current_subclasscode, overdraft_current_label, new_df['particular'].iloc[idx].strip(), new_df['Classcode'].iloc[0].strip())




                    #'''If Domain Corpus matches mapped to secured loans for Non-Current Liabilities or unsecured loans for Current Liabilities'''
                        elif BS_mapping_override(new_df['particular'].iloc[idx].strip()) and fuzz.token_set_ratio(new_df['particular'].iloc[idx].strip(), 'derivative') < 85:
        
                            if each in ['Non-Current Liabilities'] and check_unsecured_loan_previous_immediate_header(new_df, idx):
                                print(sl_corpus)
                                print(machinary_corpus)
                                sl_score = process.extractOne(new_df['particular'].iloc[idx].strip() , sl_corpus, scorer=fuzz.token_sort_ratio)[1]
                                machinary_score = process.extractOne(new_df['particular'].iloc[idx].strip() , machinary_corpus, scorer=fuzz.token_sort_ratio)[1]
                                print(sl_score)
                                print(machinary_score)

                                if sl_score < machinary_score:
                                    print('-------------- MATCHED to Loan against Machinery(overriding)---------------')
                                    suggestion = make_suggestion(machinary_lineitem, max_score, each, machinary_subclass, machinary_subclasscode, machinary_label, new_df['particular'].iloc[idx].strip(), new_df['Classcode'].iloc[0].strip())
                                else:
                                    print('-------------- MATCHED to SECURED LOANS(overriding)---------------')
                                    suggestion = make_suggestion(sl_lineitem, max_score, each, sl_subclass, sl_subclasscode, sl_label, new_df['particular'].iloc[idx].strip(), new_df['Classcode'].iloc[0].strip())

                            elif each in 'Current Liabilities':
                                print('--------------MATCHED to UNSECURED LOANS(overriding)---------------')
                                suggestion = make_suggestion(usl_lineitem, max_score, each, usl_subclass, usl_subclasscode, usl_label, new_df['particular'].iloc[idx].strip(), new_df['Classcode'].iloc[0].strip())
                            else:
                                suggestion = {}


                    if each in ['Non-current Assets'] and not new_df['particular'].iloc[idx].strip() is '':

                    #'''If DEPRECIATION found in Non-current Assets then it will be mapped to the previous suggestion'''
                        if (any(fuzz.token_set_ratio(new_df['particular'].iloc[idx].strip().lower(), c.lower()) >= 85 for c in ['dep', 'depn' ,'depreciation']) and len(new_df['particular'].iloc[idx].strip().lower().split(' ')) <= 3)\
                        or process.extractOne(new_df['particular'].iloc[idx].strip().lower().replace(':',' '),['add this year', 'addition during the year', 'capitalized'], scorer=fuzz.token_set_ratio)[1] > 90:
                            
                            print('@@@@@@@@@@@@@@@ DEPRECIATION / ADD @@@@@@@@@@@@@@@@')

                            suggestion = make_suggestion(previous_suggestion['lineitem'], max_score, each, previous_suggestion['subclass'], previous_suggestion['subclasscode'], previous_suggestion['label'], new_df['particular'].iloc[idx].strip(), new_df['Classcode'].iloc[0].strip())

                    #'''In non current asset, if land, flat, property found then should be mapped to Other Fixed Assets.'''
                        if process.extractOne(new_df['particular'].iloc[idx].strip().lower(), ['land', 'flat', 'property', 'properties'], scorer=fuzz.token_set_ratio)[1] > 90 and \
                         process.extractOne(new_df['particular'].iloc[idx].strip().lower(), ['plant', 'equipment'], scorer=fuzz.token_set_ratio)[1] < 90 and template_code.lower() in ['t_sc_efl_sme']:

                            print('@@@@@@@@@@@@@@@ land, flat, property @@@@@@@@@@@@@@@@')

                            suggestion = make_suggestion('Other Fixed Assets', max_score, each, '','', 'OTHRFA', new_df['particular'].iloc[idx].strip(), new_df['Classcode'].iloc[0].strip())


                    # if each in ['Equity', 'Non-Current Liabilities', 'Current Liabilities'] and not new_df['particular'].iloc[idx].strip() is '':
                    # #'''In current asset, if cash, bank found then should be mapped to Cash & Bank Balance.'''
                    #   if process.extractOne(new_df['particular'].iloc[idx].strip().lower(), ['cash', 'bank'], scorer=fuzz.token_set_ratio)[1] > 90:

                    #       print('@@@@@@@@@@@@@@@ cash OR bank @@@@@@@@@@@@@@@@')

                    #       suggestion = make_suggestion(cb_lineitem, max_score, each, cb_subclass, cb_subclasscode, cb_label, new_df['particular'].iloc[idx].strip(), new_df['Classcode'].iloc[0].strip())



                    if tradepayable_pos and each in ['Current Liabilities']:
                        
                        if tradepayable_pos[0]+1 == idx or tradepayable_pos[0]+2 == idx:
                            #Mapped to creditors
                            score_ =  process.extractOne(new_df['particular'].iloc[idx].strip(), ['micro', 'Small' ,'medium enterprises', 'msme', 'due', 'others'], scorer=fuzz.token_set_ratio)
                            
                            if score_[1] >= 85 and fuzz.token_set_ratio(new_df['particular'].iloc[idx].strip(), 'provisions') < 85:
                                print('Goes to creditors')
                                suggestion = make_suggestion(creditors_lineitem, max_score, each, creditor_subclass, creditor_subclasscode, creditors_label, new_df['particular'].iloc[idx].strip(), new_df['Classcode'].iloc[0].strip())

                        if tradepayable_pos[0]+2 == idx and [new_df['Residual'].to_list().index('Y')]:
                            #Mapped to residual
                            score_ =  process.extractOne(new_df['particular'].iloc[idx].strip(), ['liabilities'], scorer=fuzz.token_set_ratio)
                            if score_[1] >= 85:
                                print('Goes to liability')
                                try:
                                    residual_pos = [new_df['Residual'].to_list().index('Y')]
                                    suggestion = make_suggestion(new_df['Lineitem'].iloc[residual_pos[0]], max_score, each, new_df['Subclass'].iloc[residual_pos[0]], new_df['SubClasscode'].iloc[residual_pos[0]], new_df['chart_of_accounts'].iloc[residual_pos[0]], new_df['particular'].iloc[idx].strip(), new_df['Classcode'].iloc[0].strip())
                                except:
                                    residual_pos = []
                                



                        #If any person name found on 'Non-Current Liabilities' and also found in 'Equity' then it will always map to 'OWNMONEY'
                    if each in ['Non-Current Liabilities'] and equity_header_mapped_lineitem:

                        print('equity_header_mapped_lineitem#########', equity_header_mapped_lineitem)

                        break_lineitem = new_df['particular'].iloc[idx].strip().split(' ')
                        domain = False

                        for word in break_lineitem:
                            for c in equity_header_mapped_lineitem:
                                
                                if fuzz.token_set_ratio(word.lower(), c.lower()) >= 85:
                                    print('@@@@@@@@@@@@@@@ Domain Matched @@@@@@@@@@@@@@@@@@@@')
                                    print(word.lower(), '-->', c.lower(), fuzz.token_set_ratio(word.lower(), c.lower()))
                                    # return [idx+index]
                                    domain = True
                                    break
                            else:
                                continue  
                            break

                        if domain:
                            print('@@@@@@@@@@@@@@@ Overwrites the mapping to equity header @@@@@@@@@@@@@@@@@@@')
                            suggestion = make_suggestion(om_lineitem, max_score, each, om_subclass, om_subclasscode, om_label, new_df['particular'].iloc[idx].strip(), new_df['Classcode'].iloc[0].strip())

                    if suggestion:
                        if suggestion['label'] == 'CAPITALRESERVE' and suggestion['class'].lower() in ['equity'] and (fuzz.partial_ratio("".join(suggestion['labelitem'].split()), 'capital') <= 85 or fuzz.partial_ratio("".join(suggestion['labelitem'].split()), 'reserve') <= 85):
                            suggestion = {}

                    if suggestion:
                        if suggestion['class'] in ['Non-current Assets'] and fuzz.partial_ratio("".join(suggestion['labelitem'].split()), 'financial') >= 85:
                            suggestion['lineitem']= onca_lineitem
                            suggestion['label'] = onca_label

                        print(suggestion)
                        previous_suggestion = suggestion
                        map_.append(suggestion)

                        DATA['Data']['Financial Tables'][0]["Balance Sheet"][match].update({'suggestion':suggestion})



                        
                    if not suggestion and not new_df['particular'].iloc[idx].strip() is '':
                        try:
                            residual_pos = [new_df['Residual'].to_list().index('Y')]
                        except:
                            residual_pos = []

                        print("###################RESIDUAL POS########################", residual_pos)

                        if residual_pos:

                            suggestion = make_suggestion(new_df['Lineitem'].iloc[residual_pos[0]], max_score, each, new_df['Subclass'].iloc[residual_pos[0]], new_df['SubClasscode'].iloc[residual_pos[0]], new_df['chart_of_accounts'].iloc[residual_pos[0]], new_df['particular'].iloc[idx].strip(), new_df['Classcode'].iloc[0].strip())
                            previous_suggestion = suggestion
                            map_.append(suggestion)
                            print(suggestion)
                            
                            if not each.lower() in ['equity', 'current assets', 'non-current liabilities'] or DATA['Source']['annualReportType'] in ['Schedule-III']: 
                                DATA['Data']['Financial Tables'][0]["Balance Sheet"][match].update({'suggestion':suggestion})

                            elif each.lower() == 'equity':
                                print('$$$$$$$$$$$$$$$$$$$$$  Mapped to previous nearest header @@@@@@@@@@@@@@@@@@@@@')
                                header = find_first_header(new_df)
                                print('headers===>', header)

                                if not header:
                                    print("Didn't find the header...by default 0........")
                                    # header.append(0)

                                try:
                                    if header:
                                        if len(header) >1:
                                            nearest_header = [el for el in header if el < idx][-1]
                                        else:
                                            nearest_header = header[0]

                                        print('nearest_header===>', nearest_header)

                                        suggestion = make_suggestion(map_[nearest_header]['lineitem'], max_score, each, map_[nearest_header]['subclass'], map_[nearest_header]['subclasscode'], map_[nearest_header]['label'], new_df['particular'].iloc[idx].strip(), new_df['Classcode'].iloc[0].strip())
                                        previous_suggestion = suggestion
                                        # map_[nearest_header] = suggestion
                                        map_[-1] = suggestion
                                        print(suggestion)
                                        if idx <=3 and fuzz.token_set_ratio('as per', new_df['particular'].iloc[idx].strip()) <= 85:
                                            equity_header_mapped_lineitem.append(new_df['particular'].iloc[idx].strip())

                                        DATA['Data']['Financial Tables'][0]["Balance Sheet"][match].update({'suggestion':suggestion})
                                    else:
                                        '''If the first lineitem(Person Name) is not header and inner column, should be mapped Capital Account'''
                                        if new_df['inner_outer'].iloc[0] == 'inner' and not new_df['Label Signage'].iloc[0] is 'H' and idx == 0:

                                            suggestion = make_suggestion(capital_lineitem, max_score, each, capital_subclass, capital_subclasscode, capital_label, new_df['particular'].iloc[idx].strip(), new_df['Classcode'].iloc[0].strip())
                                            previous_suggestion = suggestion
                                            map_[-1] = suggestion
                                            if idx <=3 and fuzz.token_set_ratio('as per', new_df['particular'].iloc[idx].strip()) <= 85:
                                                equity_header_mapped_lineitem.append(new_df['particular'].iloc[idx].strip())
                                            print(suggestion)

                                            DATA['Data']['Financial Tables'][0]["Balance Sheet"][match].update({'suggestion':suggestion})

                                        DATA['Data']['Financial Tables'][0]["Balance Sheet"][match].update({'suggestion':suggestion})
                                except:
                                    print('@@@@@@@@@@@@@@@@ FIRST line item does not have the header @@@@@@@@@@@@')
                                    DATA['Data']['Financial Tables'][0]["Balance Sheet"][match].update({'suggestion':suggestion})


                            elif each.lower() == 'current assets':
                                print('$$$$$$$$$$$$$$$$$$$$$  Mapped to previous nearest header @@@@@@@@@@@@@@@@@@@@@')
                                header = find_first_header(new_df)
                                print('headers===>', header)

                                try:
                                    if header:
                                        if len(header) >1:
                                            nearest_header = [el for el in header if el < idx][-1]
                                        else:
                                            nearest_header = header[0]

                                        print('nearest_header===>', nearest_header)
                                        # print(map_,nearest_header, "%%%%%%%%%%%%%%%%%%%%%")
                                        suggestion = make_suggestion(map_[nearest_header]['lineitem'], max_score, each, map_[nearest_header]['subclass'], map_[nearest_header]['subclasscode'], map_[nearest_header]['label'], new_df['particular'].iloc[idx].strip(), new_df['Classcode'].iloc[0].strip())
                                        previous_suggestion = suggestion
                                        map_[nearest_header] = suggestion
                                        print(suggestion)
                                        #equity_header_mapped_lineitem.append(new_df['particular'].iloc[idx].strip())

                                        DATA['Data']['Financial Tables'][0]["Balance Sheet"][match].update({'suggestion':suggestion})
                                    else:
                                        DATA['Data']['Financial Tables'][0]["Balance Sheet"][match].update({'suggestion':suggestion})
                                except:
                                    print('@@@@@@@@@@@@@@@@ FIRST line item does not have the header @@@@@@@@@@@@')
                                    DATA['Data']['Financial Tables'][0]["Balance Sheet"][match].update({'suggestion':suggestion})


                            elif each.lower() == 'non-current liabilities':
                                print('$$$$$$$$$$$$$$$$$$$$$  Mapped to previous nearest header @@@@@@@@@@@@@@@@@@@@@')
                                header = find_first_header(new_df)
                                print('headers===>', header)

                                try:
                                    if header:
                                        if len(header) >1:
                                            nearest_header = [el for el in header if el < idx][-1]
                                        else:
                                            nearest_header = header[0]

                                        print('nearest_header===>', nearest_header)

                                        suggestion = make_suggestion(map_[nearest_header]['lineitem'], max_score, each, map_[nearest_header]['subclass'], map_[nearest_header]['subclasscode'], map_[nearest_header]['label'], new_df['particular'].iloc[idx].strip(), new_df['Classcode'].iloc[0].strip())
                                        previous_suggestion = suggestion
                                        map_[nearest_header] = suggestion
                                        print(suggestion)
                                        #equity_header_mapped_lineitem.append(new_df['particular'].iloc[idx].strip())

                                        DATA['Data']['Financial Tables'][0]["Balance Sheet"][match].update({'suggestion':suggestion})
                                    else:
                                        suggestion = make_suggestion(sl_lineitem, max_score, each, sl_subclass, sl_subclasscode, sl_label, new_df['particular'].iloc[idx].strip(), new_df['Classcode'].iloc[0].strip())
                                        print(suggestion)
                                        DATA['Data']['Financial Tables'][0]["Balance Sheet"][match].update({'suggestion':suggestion})
                                except:
                                    print('@@@@@@@@@@@@@@@@ FIRST line item does not have the header @@@@@@@@@@@@')
                                    DATA['Data']['Financial Tables'][0]["Balance Sheet"][match].update({'suggestion':suggestion})


                    elif not suggestion:
                        map_.append({})

                        # DATA['Data']['Financial Tables'][0]["Balance Sheet"][match].update({'suggestion':suggestion})
                    line_score = []
                    suggestion = {}
                    print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n')

    '''For upmapped data year and year value will be attached'''
    for i, itr in enumerate(DATA['Data']['Financial Tables'][0]["Balance Sheet"]):
        if not 'particular' in itr:

            for yc in range(year_count_bs):
                DATA['Data']['Financial Tables'][0]["Balance Sheet"][i].update({DATA['Data']['Financial Tables'][0]["Balance Sheet"][i]['Year'+str(yc+1)+' Value']: normalize(DATA['Data']['Financial Tables'][0]["Balance Sheet"][i]['Year'+str(yc+1)+' Value'])})

    try:

        print('\n\n\nBS DECIAMAL CHECKING::::::::::::')
        if scenario_flag_bs == 0:

            for count in range(year_count_bs):
                DATA = scenario_zero_decimal_check_bs_individual_class(DATA, bs_data, count+1)
                DATA = scenario_zero_decimal_check_bs(DATA, bs_data, count+1)

        if scenario_flag_bs == 1:

            for count in range(year_count_bs):
                DATA = scenario_one_decimal_check_bs(DATA, bs_data, count+1)

        if scenario_flag_bs == 2:

            for count in range(year_count_bs):
                DATA = scenario_two_decimal_check_bs(DATA, bs_data, count+1)


    except Exception as e:
        print(e)
        print(traceback.print_exc())

    print('\n\n\n==========================================================================================\n\n\n')

    return DATA


def scenario_zero_decimal_check_bs_individual_class(DATA:dict, bs_data:dict, year_pos:int)->dict:

    '''
        Scenario = 0, check the rule on every class.
    '''

    print('-------------------------------------------scenario_zero_decimal_check_bs_individual_class--------------------------------')
    for key,value in bs_data.items():

        data = pd.DataFrame(bs_data[key])
        if len(data) > 0:
        
            year_col = data.columns[year_pos]
            print('YEAR::::::::', year_col)


            lineitems = [roman_number(a.strip()) for a in list(map(itemgetter('Label Name'), DATA['Data']['Financial Tables'][0]["Balance Sheet"]))]

            year_values = list(map(itemgetter('Year'+str(year_pos)+' '+'Value'), DATA['Data']['Financial Tables'][0]["Balance Sheet"]))

            total_index = list(np.nonzero(list(data.apply(lambda x: float(x[year_col]) if process.extractOne("".join(x['particular'].lower().split()) ,[''], scorer=fuzz.partial_ratio)[1] > 85 else 0, axis=1)))[0])

            if total_index:

                diff = abs(int(round(data[year_col].iloc[total_index[-1]] - sum(data[year_col].iloc[0:total_index[-1]]))))
                
                diff_len = len(str(diff))

                # print("CLass::::::::", key)
                # print("Total Sum and Inner Sum:::::", data[year_col].iloc[total_index[-1]], sum(data[year_col].iloc[0:total_index[-1]]))
                for idx2 in range(0,total_index[-1]):
    
                    # if len(str(abs(int(data[year_col].iloc[idx2])))) == diff_len:
                    # if True:
                    if sum(data[year_col].iloc[0:total_index[-1]]) > data[year_col].iloc[total_index[-1]]:

                        # if abs(int((data[year_col].iloc[idx2] * 90)/100)) == diff and not diff is 0:
                        # print(subset_sum(data[year_col].iloc[0:total_index[-1]].to_list(), diff, 90))
                        if float(data[year_col].iloc[idx2]) in subset_sum(data[year_col].iloc[0:total_index[-1]].to_list(), diff, 90) and not diff is 0 and len(subset_sum(data[year_col].iloc[0:total_index[-1]].to_list(), diff, 90)) < 3:

                            print('diff:::::', diff)
                            print('diff_len:::::',diff_len)

                            print('One decimal error found::::',data[year_col].iloc[idx2],idx2)

                            for en, value in enumerate(year_values):
                           
                                if data[year_col].iloc[idx2] == normalize(value) and fuzz.ratio(data['particular'].iloc[idx2].strip().lower(), lineitems[en].lower()) ==100:
                                    print('match::::::',data['particular'].iloc[idx2].strip().lower(), en)
                                    match = en
                                    print(str(float(data[year_col].iloc[idx2])/10))
                                    DATA['Data']['Financial Tables'][0]["Balance Sheet"][match].update({'Year'+str(year_pos)+' '+'Value':str(float(data[year_col].iloc[idx2])/10)})

                            print('-------------------------------------------------------------')

                        # if abs(int((data[year_col].iloc[idx2] * 99)/100)) == diff and not diff is 0:
                        elif float(data[year_col].iloc[idx2]) in subset_sum(data[year_col].iloc[0:total_index[-1]].to_list(), diff, 99) and not diff is 0:

                            print('TWO decimal error found::::',data[year_col].iloc[idx2],idx2)

                            print('diff:::::', diff)
                            print('diff_len:::::',diff_len)

                            for en, value in enumerate(year_values):
                           
                                if data[year_col].iloc[idx2] == normalize(value) and fuzz.ratio(data['particular'].iloc[idx2].strip().lower(), lineitems[en].lower()) ==100:
                                    print('match::::::',data['particular'].iloc[idx2].strip().lower(), en)
                                    match = en
                                    print(str(float(data[year_col].iloc[idx2])/100))
                                    DATA['Data']['Financial Tables'][0]["Balance Sheet"][match].update({'Year'+str(year_pos)+' '+'Value':str(float(data[year_col].iloc[idx2])/100)})

                            print('-------------------------------------------------------------')
            

    return DATA

def scenario_zero_decimal_check_bs(DATA:dict, bs_data:dict, year_pos:int)->dict:

    ''' Scenario = 0 and no outer columns then divide the BS in asset= CA+NCA and liability= Equity+CL+NCL. 
        Run the rule in asset and liability. This rule will not work if there are two different decimal errors in asset or liability
    '''

    global bs_cal_index
    print('-------------------------------------------scenario_zero_decimal_check_bs---------------------------------------------------')
    print('Asset Side:::::::::::')
    data_ca = pd.DataFrame(bs_data['Current Assets'])
    data_nca = pd.DataFrame(bs_data['Non-current Assets'])
    # print(data_ca)
    # print(data_nca)
    data_asset = pd.concat([data_ca, data_nca],ignore_index=True)
    year_col = data_asset.columns[year_pos]
    print('YEAR::::::::', year_col)

    lineitems = [roman_number(a.strip()) for a in list(map(itemgetter('Label Name'), DATA['Data']['Financial Tables'][0]["Balance Sheet"]))]

    year_values = list(map(itemgetter('Year'+str(year_pos)+' '+'Value'), DATA['Data']['Financial Tables'][0]["Balance Sheet"]))

    year_values_float = [float(each5) for each5 in year_values]
    total_asset_liability_frequency = [(k, len(list(g))) for k, g in groupby(sorted(year_values_float))]
    total_asset_liability_frequency_ = max([each7 for each7 in total_asset_liability_frequency if each7[1]==2] , default=[])
    #Taking the maximum total which has two occurrence
    print("total_asset_liability_frequency:::::: ", total_asset_liability_frequency_)

    if list(data_asset.inner_outer).count('outer') == 0 and total_asset_liability_frequency_:

        total_sum = total_asset_liability_frequency_[0]

        #Checking the asset sum is in the asset side or not, if Yes then right Asset total
        # print(data_asset)
        # print("*********************************", year_values_float[:data_asset.shape[0]])
        if total_sum in year_values_float[:data_asset.shape[0]+4]:

            elimanated_cal_rows = [float(v7) for id7,v7 in enumerate(year_values) if not id7 in bs_cal_index and id7 <= year_values_float.index(total_sum)]
            #Inner rows without calculated fields.
            print("elimanated_cal_rows::: ", elimanated_cal_rows)

            inner_sum = sum(elimanated_cal_rows)
            print('total_sum, inner_sum::::::', total_sum, inner_sum)

            diff = abs(int(round(total_sum-inner_sum)))
            # print('diff:::::',diff)
            diff_len = len(str(diff))
            # print('diff_len:::::',diff_len)

            for idx2 in range(len(data_asset)):
                if inner_sum > total_sum:

                    if float(data_asset[year_col].iloc[idx2]) in subset_sum(elimanated_cal_rows, diff, 90) and not diff is 0:
                        print('total_sum, inner_sum::::::', total_sum, inner_sum)
                        print('diff:::::',diff)
                        print('diff_len:::::',diff_len)
                        print('One decimal error found::::',data_asset[year_col].iloc[idx2],idx2)

                        for en, value in enumerate(year_values):
                       
                            if data_asset[year_col].iloc[idx2] == normalize(value) and fuzz.ratio(data_asset['particular'].iloc[idx2].strip().lower(), lineitems[en].lower()) ==100:
                                print('match::::::',data_asset['particular'].iloc[idx2].strip().lower(), en)
                                match = en
                                print(str(float(data_asset[year_col].iloc[idx2])/10))
                                DATA['Data']['Financial Tables'][0]["Balance Sheet"][match].update({'Year'+str(year_pos)+' '+'Value':str(float(data_asset[year_col].iloc[idx2])/10)})


                    # if abs(int((data_asset[year_col].iloc[idx2] * 99)/100)) == diff and not diff is 0:
                    elif float(data_asset[year_col].iloc[idx2]) in subset_sum(elimanated_cal_rows, diff, 99) and not diff is 0:
                        print('total_sum, inner_sum::::::', total_sum, inner_sum)
                        print('diff:::::',diff)
                        print('diff_len:::::',diff_len)
                        print('Two decimal error found::::',data_asset[year_col].iloc[idx2],idx2)

                        for en, value in enumerate(year_values):
                       
                            if data_asset[year_col].iloc[idx2] == normalize(value) and fuzz.ratio(data_asset['particular'].iloc[idx2].strip().lower(), lineitems[en].lower()) ==100:
                                print('match::::::',data_asset['particular'].iloc[idx2].strip().lower(), en)
                                match = en
                                print(str(float(data_asset[year_col].iloc[idx2])/100))
                                DATA['Data']['Financial Tables'][0]["Balance Sheet"][match].update({'Year'+str(year_pos)+' '+'Value':str(float(data_asset[year_col].iloc[idx2])/100)})



    print('Liability Side:::::::::::')
    data_el = pd.DataFrame(bs_data['Equity'])
    data_ncl = pd.DataFrame(bs_data['Non-Current Liabilities'])
    data_cl = pd.DataFrame(bs_data['Current Liabilities'])

    data_liability = pd.concat([data_el, data_ncl, data_cl],ignore_index=True)

    if total_asset_liability_frequency_:
        liability_start_pos = year_values_float.index(total_sum) + 1
    else:
        liability_start_pos = data_asset.shape[0]+1

    print("liability_start_pos:::: ",liability_start_pos)

    # print(data_ca)
    # print(data_nca)
    year_col = data_liability.columns[year_pos]
    print('YEAR::::::::', year_col)

    if list(data_liability.inner_outer).count('outer') == 0 and total_asset_liability_frequency_:
        
        total_sum = total_asset_liability_frequency_[0]

        #The Total sum occurrence should be one in liability side else will not be executed.
        if data_liability[year_col].to_list().count(total_sum) == 1:

            liability_inner_col = data_liability[year_col].to_list()
            print("liability_inner_col::::", liability_inner_col)
            print("bs_cal_index:::::", bs_cal_index)

            elimanated_cal_rows = [v2 for id2,v2 in enumerate(year_values_float[:[i for i, v in enumerate(year_values_float) if v == total_sum][1]]) if not id2 in bs_cal_index and id2 >= liability_start_pos]
            print("elimanated_cal_rows::: ", elimanated_cal_rows)

            inner_sum = sum(elimanated_cal_rows)
            print('total_sum, inner_sum::::::', total_sum, inner_sum)

            diff = abs(int(round(total_sum-inner_sum)))
            # print('diff:::::',diff)
            diff_len = len(str(diff))
            # print('diff_len:::::',diff_len)

            for idx2 in range(len(data_liability)):

                if inner_sum > total_sum:

                    if float(data_liability[year_col].iloc[idx2]) in subset_sum(elimanated_cal_rows, diff, 90) and not diff is 0:
                        print('total_sum, inner_sum::::::', total_sum, inner_sum)
                        print('diff:::::',diff)
                        print('diff_len:::::',diff_len)
                        print('One decimal error found::::',data_liability[year_col].iloc[idx2],idx2)

                        for en, value in enumerate(year_values):

                            if data_liability[year_col].iloc[idx2] == normalize(value) and fuzz.ratio(data_liability['particular'].iloc[idx2].strip().lower(), lineitems[en].lower()) ==100:
                                print('match::::::',data_liability['particular'].iloc[idx2].strip().lower(), en)
                                match = en
                                print(str(float(data_liability[year_col].iloc[idx2])/10))
                                DATA['Data']['Financial Tables'][0]["Balance Sheet"][match].update({'Year'+str(year_pos)+' '+'Value':str(float(data_liability[year_col].iloc[idx2])/10)})


                    # if abs(int((data_liability[year_col].iloc[idx2] * 99)/100)) == diff and not diff is 0:
                    elif float(data_liability[year_col].iloc[idx2]) in subset_sum(elimanated_cal_rows, diff, 99) and not diff is 0:
                        print('total_sum, inner_sum::::::', total_sum, inner_sum)
                        print('diff:::::',diff)
                        print('diff_len:::::',diff_len)
                        print('Two decimal error found::::',data_liability[year_col].iloc[idx2],idx2)

                        for en, value in enumerate(year_values):

                            if data_liability[year_col].iloc[idx2] == normalize(value) and fuzz.ratio(data_liability['particular'].iloc[idx2].strip().lower(), lineitems[en].lower()) ==100:
                                print('match::::::',data_liability['particular'].iloc[idx2].strip().lower(), en)
                                match = en
                                print(str(float(data_liability[year_col].iloc[idx2])/100))
                                DATA['Data']['Financial Tables'][0]["Balance Sheet"][match].update({'Year'+str(year_pos)+' '+'Value':str(float(data_liability[year_col].iloc[idx2])/100)})
                        

    return DATA



def scenario_one_decimal_check_bs(DATA:dict, bs_data:dict, year_pos:int)->dict:

    '''
        Scenario = 1, check the rule on every class.
    '''

    global year_count_bs

    for key,value in bs_data.items():

        data = pd.DataFrame(bs_data[key])
        if len(data) > 0:

            if year_count_bs == 1:
                data.loc[len(data)]=['',0.0,'H','outer']

            elif year_count_bs == 2:
                data.loc[len(data)]=['',0.0,0.0,'H','outer']
            else:
                data.loc[len(data)]=['',0.0,0.0,0.0,'H','outer']
        
            year_col = data.columns[year_pos]
            print('YEAR::::::::', year_col)


            lineitems = [roman_number(a.strip()) for a in list(map(itemgetter('Label Name'), DATA['Data']['Financial Tables'][0]["Balance Sheet"]))]

            year_values = list(map(itemgetter('Year'+str(year_pos)+' '+'Value'), DATA['Data']['Financial Tables'][0]["Balance Sheet"]))

            outer_index = list(filter(lambda v: v is not None, [nth_index(data['inner_outer'].to_list(), 'outer', each+1) for each in range(len(data))]))
            # print(data)
            # print(outer_index)

            if outer_index:

                for each_outer in range(len(outer_index)-1):
                    # print(data[year_col].iloc[outer_index[each_outer]+1:outer_index[each_outer+1]].to_list())
                    diff = abs(int(round(data[year_col].iloc[outer_index[each_outer]] - sum(data[year_col].iloc[outer_index[each_outer]+1:outer_index[each_outer+1]]))))
                    # print(diff)

                    diff_len = len(str(diff))
                    # print(diff_len)

                    for idx2 in range(outer_index[each_outer],outer_index[each_outer+1]):
        
                        # if len(str(abs(int(data[year_col].iloc[idx2])))) == diff_len:
                        # if True:
                        if sum(data[year_col].iloc[outer_index[each_outer]+1:outer_index[each_outer+1]]) > data[year_col].iloc[outer_index[each_outer]]:

                            # print(data[year_col].iloc[idx2] ,data[year_col].iloc[outer_index[each_outer]+1:outer_index[each_outer+1]].to_list(), diff, 90)
                            # if abs(int((data[year_col].iloc[idx2] * 90)/100)) == diff and not diff is 0:
                            if float(data[year_col].iloc[idx2]) in subset_sum(data[year_col].iloc[outer_index[each_outer]+1:outer_index[each_outer+1]].to_list(), diff, 90) and not diff is 0:

                                print('diff:::::', diff)
                                print('diff_len:::::',diff_len)

                                print('One decimal error found::::',data[year_col].iloc[idx2],idx2)

                                for en, value in enumerate(year_values):
                               
                                    if data[year_col].iloc[idx2] == normalize(value) and fuzz.ratio(data['particular'].iloc[idx2].strip().lower(), lineitems[en].lower()) ==100:
                                        print('match::::::',data['particular'].iloc[idx2].strip().lower(), en)
                                        match = en
                                        print(str(float(data[year_col].iloc[idx2])/10))
                                        DATA['Data']['Financial Tables'][0]["Balance Sheet"][match].update({'Year'+str(year_pos)+' '+'Value':str(float(data[year_col].iloc[idx2])/10)})

                                print('-------------------------------------------------------------')


                            # if abs(int((data[year_col].iloc[idx2] * 99)/100)) == diff and not diff is 0:
                            elif float(data[year_col].iloc[idx2]) in subset_sum(data[year_col].iloc[outer_index[each_outer]+1:outer_index[each_outer+1]].to_list(), diff, 99) and not diff is 0:

                                print('TWO decimal error found::::',data[year_col].iloc[idx2],idx2)

                                print('diff:::::', diff)
                                print('diff_len:::::',diff_len)

                                for en, value in enumerate(year_values):
                               
                                    if data[year_col].iloc[idx2] == normalize(value) and fuzz.ratio(data['particular'].iloc[idx2].strip().lower(), lineitems[en].lower()) ==100:
                                        print('match::::::',data['particular'].iloc[idx2].strip().lower(), en)
                                        match = en
                                        print(str(float(data[year_col].iloc[idx2])/100))
                                        DATA['Data']['Financial Tables'][0]["Balance Sheet"][match].update({'Year'+str(year_pos)+' '+'Value':str(float(data[year_col].iloc[idx2])/100)})

                                print('-------------------------------------------------------------')
            

    return DATA


def scenario_two_decimal_check_bs(DATA:dict, bs_data:dict, year_pos:int)->dict:

    '''
        Scenario = 1, check the rule on every class.
    '''

    global year_count_bs

    for key,value in bs_data.items():

        data = pd.DataFrame(bs_data[key])
        # print(data)
        if len(data) > 0:

            if year_count_bs == 1:
                data.loc[-1]=['',0.0,'H','outer']
            elif year_count_bs == 2:
                data.loc[-1]=['',0.0,0.0,'H','outer']
            else:
                data.loc[-1]=['',0.0,0.0,0.0,'H','outer']

            data.index = data.index + 1  # shifting index
            data.sort_index(inplace=True)
        
            year_col = data.columns[year_pos]
            print('YEAR::::::::', year_col)


            lineitems = [roman_number(a.strip()) for a in list(map(itemgetter('Label Name'), DATA['Data']['Financial Tables'][0]["Balance Sheet"]))]

            year_values = list(map(itemgetter('Year'+str(year_pos)+' '+'Value'), DATA['Data']['Financial Tables'][0]["Balance Sheet"]))

            outer_index = list(filter(lambda v: v is not None, [nth_index(data['inner_outer'].to_list(), 'outer', each+1) for each in range(len(data))]))

            # print(data)
            # print(outer_index)

            if outer_index:

                for each_outer in range(len(outer_index)-1):

                    diff = abs(int(round(data[year_col].iloc[outer_index[each_outer+1]] - sum(data[year_col].iloc[outer_index[each_outer]+1:outer_index[each_outer+1]]))))
                    
                    diff_len = len(str(diff))

                    # print(outer_index[each_outer], outer_index[each_outer+1])
                    # print("each_outer::::", each_outer)
                    # print(data[year_col].iloc[outer_index[each_outer]+1:outer_index[each_outer+1]].to_list(), data[year_col].iloc[outer_index[each_outer+1]])
                    # print('diff:::::', diff)
                    # print('diff_len:::::',diff_len)

                    for idx2 in range(outer_index[each_outer],outer_index[each_outer+1]):
        
                        # if len(str(abs(int(data[year_col].iloc[idx2])))) == diff_len:
                        # if True:
                        # print(sum(data[year_col].iloc[outer_index[each_outer]+1:outer_index[each_outer+1]]) ,"----------->", data[year_col].iloc[outer_index[each_outer+1]])
                        if sum(data[year_col].iloc[outer_index[each_outer]+1:outer_index[each_outer+1]]) > data[year_col].iloc[outer_index[each_outer+1]]:

                            # if abs(int((data[year_col].iloc[idx2] * 90)/100)) == diff and not diff is 0:
                            if float(data[year_col].iloc[idx2]) in subset_sum(data[year_col].iloc[outer_index[each_outer]+1:outer_index[each_outer+1]].to_list(), diff, 90) and not diff is 0:

                                print('diff:::::', diff)
                                print('diff_len:::::',diff_len)

                                print('One decimal error found::::',data[year_col].iloc[idx2],idx2)

                                for en, value in enumerate(year_values):
                               
                                    if data[year_col].iloc[idx2] == normalize(value) and fuzz.ratio(data['particular'].iloc[idx2].strip().lower(), lineitems[en].lower()) ==100:
                                        print('match::::::',data['particular'].iloc[idx2].strip().lower(), en)
                                        match = en
                                        print(str(float(data[year_col].iloc[idx2])/10))
                                        DATA['Data']['Financial Tables'][0]["Balance Sheet"][match].update({'Year'+str(year_pos)+' '+'Value':str(float(data[year_col].iloc[idx2])/10)})

                                print('-------------------------------------------------------------')


                            # if abs(int((data[year_col].iloc[idx2] * 99)/100)) == diff and not diff is 0:
                            elif float(data[year_col].iloc[idx2]) in subset_sum(data[year_col].iloc[outer_index[each_outer]+1:outer_index[each_outer+1]].to_list(), diff, 99) and not diff is 0:

                                print('TWO decimal error found::::',data[year_col].iloc[idx2],idx2)

                                print('diff:::::', diff)
                                print('diff_len:::::',diff_len)

                                for en, value in enumerate(year_values):
                               
                                    if data[year_col].iloc[idx2] == normalize(value) and fuzz.ratio(data['particular'].iloc[idx2].strip().lower(), lineitems[en].lower()) ==100:
                                        print('match::::::',data['particular'].iloc[idx2].strip().lower(), en)
                                        match = en
                                        print(str(float(data[year_col].iloc[idx2])/100))
                                        DATA['Data']['Financial Tables'][0]["Balance Sheet"][match].update({'Year'+str(year_pos)+' '+'Value':str(float(data[year_col].iloc[idx2])/100)})

                                print('-------------------------------------------------------------')
            

    return DATA



def nth_index(iterable:list, value:bool, n:int):
    matches = (idx for idx, val in enumerate(iterable) if val == value)
    return next(islice(matches, n-1, n), None)


def check_is_header_mapping(data_:object, class_:str):
    ''' Return the header mapping indexes for IS'''
    
    global is_header_mapping_dict

    try:
        data_.loc[len(data_)]=['','0.0','0.0','H','outer'] 
        if class_ == 'Cost of goods sold / Cost of Sales':
            
            for each_lineitem in ['opening stock', 'purchase', 'closing stock']:
                score_ =  process.extractOne(each_lineitem, data_['particular'].to_dict(), scorer=fuzz.token_set_ratio)
                if score_[1] >= 85 and data_['inner_outer'].iloc[score_[2]] == 'outer':
                    stop_index = nth_index(data_['inner_outer'][score_[2]:], 'outer', 2)
                    if isinstance(stop_index,int):
                        stop_index = score_[2] + stop_index
                        is_header_mapping_dict['Cost of goods sold / Cost of Sales'] = is_header_mapping_dict['Cost of goods sold / Cost of Sales'] + [dx for dx in range(score_[2]+1,stop_index)] 
    except Exception as e:
        print('Issue in check_is_header_mapping:::::',e)
        pass


def calculated_field_is(data : dict, income_statement_cls: dict)-> dict:
    """
 
    To find calculated field in lineitems 
 
    Parameters
    ----------
    data : dict
        Input dict of income statement lineitems

    income_statement_cls: dict
        Classification of Income statement
        
    Returns
    -------
    data : dict
        
    """
    global is_cal_index, year_count_is, is_header_mapping_dict, KM1, KM4, KM5, SIGNAGE, IS_GRAPH_OUTPUT, All_NEG
    global scenario_flag_is

    is_header_mapping_dict['Cost of goods sold / Cost of Sales'] = []

    print(income_statement_cls)

    year_count_is = year_count_(data['Data']['Financial Tables'][1]['Income Statement'][0])
    print('year count is::::', year_count_is)

    match = []
    # print(data['Data']['Financial Tables'][1]['Income Statement'])
    
    if not income_statement_cls['finance_cost_index']:
        income_statement_cls['finance_cost_index'] = [9999]
    print('finance_cost_index=======================>>',income_statement_cls['finance_cost_index'])

    # if not income_statement_cls['km_index']:
    #     income_statement_cls['km_index']=[99999]
    # print('km=======================>>',income_statement_cls['km_index'])

    if income_statement_cls['km_index'][2] == -1:
        km3 = 99999
    else:
        km3 = income_statement_cls['km_index'][2]

    if income_statement_cls['km_index'][4] == -1:
        km4 = -1
    else:
        km4 = income_statement_cls['km_index'][4]

    KM1 = income_statement_cls['km_index'][0]
    KM4 = income_statement_cls['km_index'][3]
    KM5 = income_statement_cls['km_index'][4]
    SIGNAGE = income_statement_cls['signage_index'][0]
    IS_GRAPH_OUTPUT = income_statement_cls['graph_output']
    # print(IS_GRAPH_OUTPUT)
    all_km = [list(e3)[0] for e3 in IS_GRAPH_OUTPUT if 'KM1' in list(e3)[2] or 'KM2' in list(e3)[2] or 'KM3' in list(e3)[2] or 'KM4' in list(e3)[2] or 'KM5' in list(e3)[2]]
    # all_km.sort()
    print("ALL KM:::: ",all_km)
    not_calf = [list(e3)[1] for e3 in IS_GRAPH_OUTPUT if 'Level10.0' in list(e3)[2] and list(e3)[1] in income_statement_cls['km_index'][5]['classified_index']]
    print("not_calf:::: ",not_calf)

    try:
        '''If cogs and OE have all the negative values then revenue, cogs, OE, NOE, FC and DEP will be in positive figure'''
        All_NEG = False
        if income_statement_cls['Cost of goods sold / Cost of Sales'] or income_statement_cls['Operating expenses']:
            if sum([0 if int(list(e.values())[1]) <= 0 else 1 for e in income_statement_cls['Cost of goods sold / Cost of Sales']+income_statement_cls['Operating expenses']]) == 0:
                All_NEG =  True
    except:
        print(traceback.print_exc())
        pass

    print("All_NEG:::", All_NEG)

    # try:
    #     '''If Net Revenue is there in Revenue class AND there are other line items before that, then Net Revenue is calculated field NOT to be mapped'''

    #     if income_statement_cls['Revenue']:
    #         found = list(filter(lambda each: 'net' in each["particular"], income_statement_cls['Revenue']))
    #         if found:
    #             if income_statement_cls['Revenue'].index(found[0]) > 0:
    #                 print('Net found in Revenue')
    #                 match.append(found[0]["particular"])
    # except:
    #     print('Net is not in Revenue')
    #     print(traceback.print_exc())
    #     pass


    try:
        '''Finance cost has more than 1 line item and one has Net, then the Net label is calculated'''

        if income_statement_cls['Finance cost']:
            found = list(filter(lambda each: 'net' in each["particular"], income_statement_cls['Finance cost']))
            if found:
                if income_statement_cls['Finance cost'].index(found[0]) > 0:
                    print('Net found in Finance cost')
                    match.append(found[0]["particular"])
    except:
        print('Net is not in Finance cost')
        print(traceback.print_exc())
        pass



    ''' (If there is "Net" AND "Revenue") AND (there is Revenue in earlier index within Revenue class), then index with "Net" AND "Revenue" is a calculated field. '''
    try:
        match_=[]
        list_ = [l_['particular'] for l_ in income_statement_cls['Revenue']]
        net_score_ = process.extractOne('net', list_, scorer=fuzz.token_set_ratio)
        if net_score_[1] > 95:
            # if fuzz.token_set_ratio('revenue', net_score_[0]) > 95: 
            if process.extractOne(net_score_[0], ['Revenue', 'sales', 'operating income', 'operations', 'fees', 'turnover', 'contract receipt'], scorer=fuzz.token_set_ratio)[1] > 85:
                req_list_ = list_[0:list_.index(net_score_[0])]
                rev_index = process.extractOne('revenue', req_list_, scorer=fuzz.token_set_ratio)
    
                # print("1st rev value:::",list(income_statement_cls['Revenue'][list_.index(rev_index[0])].items())[1][1])
                if rev_index[1] >= 85 and list(income_statement_cls['Revenue'][list_.index(rev_index[0])].items())[1][1] > 0:
                    match_.append(net_score_[0])
    except:
        pass


    ''' if index < Level 1 index contains "sales" OR "services" Or "income" AND Level 1 label does not have "Other", then Level 1 is calculated field. '''
    try:
        level1 = [each2[1] for each2 in IS_GRAPH_OUTPUT if '.' in  list(each2)[2][0] and list(each2)[2][0].replace(list(each2)[2][0][list(each2)[2][0].find('.'):],'') == 'Level1'] 
        if level1:
            level1 = level1[-1]

            list_ = [l_['particular'] for l_ in income_statement_cls['Revenue']]
            level1_ = [level1  for i_, e_ in enumerate(list_) if process.extractOne(e_, ["sales", "services", "income"], scorer=fuzz.token_set_ratio)[1] > 90 and i_ < level1 and fuzz.token_set_ratio(list_[level1], "other") < 85]
            if level1_:
                match_.append(list_[level1_[0]])
    except:
        pass


    ''' (If there is "Gross" AND "Revenue") AND (there is Revenue in after index within Revenue class), then index with "Revenue" but not "Net" is a calculated field. '''
    try:
        # match_=[]
        list_ = [l_['particular'] for l_ in income_statement_cls['Revenue']]
        gross_score_ = process.extractOne('gross', list_, scorer=fuzz.token_set_ratio)
        if gross_score_[1] > 95:
            # if fuzz.token_set_ratio('revenue', net_score_[0]) > 95: 
            if process.extractOne(gross_score_[0], ['Revenue', 'sales', 'operating income', 'operations', 'fees', 'turnover', 'contract receipt'], scorer=fuzz.token_set_ratio)[1] > 85:
                req_list_ = list_[list_.index(gross_score_[0])+1:]
                rev_index = [fu for fu in process.extract('revenue', req_list_, scorer=fuzz.token_set_ratio) if process.extractOne(fu[0], ['net'],scorer=fuzz.token_set_ratio)[1]<= 85 and fu[1] >= 85]
                rev_index = rev_index[0]
    
                # print(rev_index, "@@@@@@@@@@@@@@@@@@@@@santanu")
                if rev_index[1] >= 85:
                    match_.append(rev_index[0])
    except:
        pass

    ''' In Tax Class, (If there is "Net" AND "Current") AND (there is Current Tax in earlier index within Tax class), then index with "Net" AND "Current" is a calculated field '''
    try:
        # match_=[]
        list_ = [l_['particular'] for l_ in income_statement_cls['Tax']]
        net_score = process.extractOne('net', list_, scorer=fuzz.token_set_ratio)
        if net_score[1] > 95 and not fuzz.token_set_ratio('earlier', net_score[0]) > 85:
            if fuzz.token_set_ratio('current', net_score[0]) > 95: 
                req_list = list_[0:list_.index(net_score[0])]
                c_tax = process.extractOne('current tax', req_list, scorer=fuzz.token_set_ratio)
                #print(c_tax, d_tax)
                if c_tax[1] >= 85:
                    match_.append(net_score[0])
    except:
        pass

    ''' In Tax Class, (If there is "Net" AND "Deferred") AND (there is Deferred Tax in earlier index within Tax class) then index with "Net" AND "Deferred" is a calculated field '''
    try:
        # match_=[]
        list_ = [l_['particular'] for l_ in income_statement_cls['Tax']]
        net_score = process.extractOne('net', list_, scorer=fuzz.token_set_ratio)
        if net_score[1] > 95:
            if fuzz.token_set_ratio('deferred', net_score[0]) > 95: 
                req_list = list_[0:list_.index(net_score[0])]
                d_tax = process.extractOne('deferred tax', req_list, scorer=fuzz.token_set_ratio)
                #print(c_tax, d_tax)
                if d_tax[1] >= 85:
                    match_.append(net_score[0])
    except:
        pass

    ''' Expression between KM4 and KM5 contains "Tax Expense" and index > index of Current Tax, then it is calculated field '''
    try:
        print("Entry::::::::::::::::::::::")
        lt_ =[l_['particular'] for l_ in income_statement_cls['Tax'] and len(l_['particular'].split()) == 2]

        tax_exp= process.extractOne('tax expenses', {idx: el for idx, el in enumerate(lt_)}, scorer=fuzz.token_set_ratio)
        # exp = process.extractOne('expense', lt_, scorer=fuzz.token_set_ratio)
        ctax = process.extractOne('current tax', {idx: el for idx, el in enumerate(lt_)}, scorer=fuzz.token_sort_ratio)
        print(tax_exp,ctax)

        if tax_exp[2] > ctax[2]:
            if tax_exp[1] > 85  and ctax[1] > 85:
                print(tax_exp[0],'$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$::')
                match_.append(tax_exp[0])
    except:
        pass


    ''' Inner outer calculated filed---> If one outer is present and it is the first index of that class, considered as calculated filed'''
    scenario_flag = 0

    try:
        for each in dict(list(income_statement_cls.items())[0: -3]):
            data_ = pd.DataFrame(income_statement_cls[each])

            if each == 'Cost of goods sold / Cost of Sales':
                data_ = data_[data_['particular'].map(lambda x: x.strip().startswith('to'))]

            scenario_flag = check_calculatedf_scenario(data_)
            if scenario_flag >= 0:
                break
    except Exception as e:
        print('Exception occured in scenario ...', e)
        print(traceback.print_exc())
        pass

    if scenario_flag == -1:
        print('No SCENARIO found, default 0')   
        scenario_flag = 0

    print('SCENARIO::::$$$$$$$$$:',scenario_flag)
    scenario_flag_is = scenario_flag

    for each in income_statement_cls:
        try:
            data_ = pd.DataFrame(income_statement_cls[each])

            if each == 'Cost of goods sold / Cost of Sales':

                check_is_header_mapping(data_, each)

                print('IS HEADER MAPPING:::', is_header_mapping_dict)
                if data_[data_['particular'].map(lambda x: x.strip().startswith('by'))].shape[0] == 1:
                    data_ = data_[data_['particular'].map(lambda x: x.strip().startswith('to'))]

            # outer_len = len(list(filter(lambda each: True if each=="outer" else False, pd.DataFrame(income_statement_cls[each])['inner_outer'] )))
            outer_len = list(data_.apply(lambda x: 1 if x['inner_outer'] == 'outer' and not fuzz.partial_ratio("".join(x['particular'].split()), 'total') > 85 else 0, axis=1)).count(1)
            inner_len = list(data_.apply(lambda x: 1 if x['inner_outer'] == 'inner' and not fuzz.partial_ratio("".join(x['particular'].split()), 'total') > 85 else 0, axis=1)).count(1)

            if outer_len == 1 and data_['inner_outer'].iloc[0] == 'outer' and inner_len > 0:
                ''' for inner outer sequence, outer will be calculated field only if inner column value > 0 '''

                if not data_.iloc[1][1] == 0 and data_['inner_outer'].iloc[1] == 'inner' and abs(data_['id'].iloc[0] - data_['id'].iloc[1]) < 2:

                    print('Inner Outer Found----------------------------------------->',data_['particular'].iloc[0])
                    match.append(data_['particular'].iloc[0])


            elif outer_len == 1 and data_['inner_outer'].iloc[-1] == 'outer' and inner_len > 0:
                ''' for inner outer sequence, outer will be calculated field only if inner column value > 0 '''

                if not data_.iloc[-2][1] == 0 and data_['inner_outer'].iloc[-2] == 'inner':
                    print('Inner Outer Found----------------------------------------->', data_['particular'].iloc[-1])
                    match.append(data_['particular'].iloc[-1])

            #Disabled XREV-293
            # Multiple outers exists
            else: 
                if data_['Label Signage'].iloc[0] == 'H':
                    data_ = data_.iloc[1:].reset_index(drop=True)

                if fuzz.partial_ratio("".join(data_['particular'].iloc[-1].strip()), 'total') > 85:
                    data_ = data_.iloc[:-1].reset_index(drop=True)

                if scenario_flag == 0:

                    print('----------------------------CASE 2.0-------------------------')
                    valid_row = [data_['particular'].iloc[row+1] for row in range(0,len(data_['inner_outer'])-1) if data_['inner_outer'].iloc[row]=='inner' and data_['inner_outer'].iloc[row+1]=='outer' and not data_.iloc[row][1] == 0]
                    print(each, valid_row)
                    match = match + valid_row

                if scenario_flag == 1:

                    print('----------------------------CASE 2.1-------------------------')
                    valid_row = [data_['particular'].iloc[row] for row in range(0,len(data_['inner_outer'])-1) if data_['inner_outer'].iloc[row]=='outer' and data_['inner_outer'].iloc[row+1]=='inner' and not data_['Label Signage'].iloc[row] is 'H' and not data_['Label Signage'].iloc[row+1] is 'H' and abs(data_['id'].iloc[row] - data_['id'].iloc[row+1]) < 2]
                    print(each, valid_row)
                    match = match + valid_row

                # elif scenario_flag == 2:
                #     print('----------------------------CASE 2.2-------------------------')
                #     valid_row = [data_['particular'].iloc[row+1] for row in range(0,len(data_['inner_outer'])-1) if data_['inner_outer'].iloc[row]=='inner' and data_['inner_outer'].iloc[row+1]=='outer' and not data_['Label Signage'].iloc[row] is 'H' and not data_['Label Signage'].iloc[row+1] is 'H']
                #     print(each, valid_row)
                #     match = match + valid_row

        except:
            print('No Inner Outer Found----------------------------------------->')
    # print(income_statement_cls)
    # classified_items = [roman_number(key['particular']) for each in dict(list(income_statement_cls.items())[0: -4]) for key in income_statement_cls[each]]
    classified_items = [each for each in income_statement_cls['km_index'][6]['classified_items_']]
    # print(classified_items)
    print('MATCH:::', match, match_)
    try:
        classified_items = list(set(classified_items) - set(match + match_))
    except:
        print("ERROR IN SUBTRACTING")
    print("income_statement_cls['km_index']::", income_statement_cls['km_index'])
    print("classified_items::", classified_items)
    print("all_km::", all_km)
    print("\n\n\n")

    for i,IS in enumerate(data["Data"]["Financial Tables"][1]["Income Statement"]):

        lineitem_is= IS["Label Name"]
        # print(lineitem_is)
        
        
        if fuzz.partial_ratio("".join(lineitem_is.split()), 'total') >= 85 or i in income_statement_cls['km_index'] or not lineitem_is in classified_items or \
         (lineitem_is is '' and not check_header(IS, year_count_is)) or check_header(IS, year_count_is)\
         or (any(fuzz.token_sort_ratio(lineitem_is, mt) >= 95 for mt in match) and IS['meta_year1'] == 'outer') or lineitem_is is '' or any(fuzz.token_sort_ratio(lineitem_is, mt_) >= 95 for mt_ in match_) or (fuzz.token_set_ratio(lineitem_is, 'expenditure') >= 85 and fuzz.token_set_ratio(lineitem_is, 'before') >= 85) \
         or ((fuzz.partial_token_set_ratio(lineitem_is, 'profit') >= 85 or fuzz.partial_token_set_ratio(lineitem_is, 'earnings') >= 85) and fuzz.partial_token_set_ratio(lineitem_is, 'before') >= 85 \
            and (fuzz.partial_token_set_ratio(lineitem_is, 'interest') >= 85 or fuzz.partial_token_set_ratio(lineitem_is, 'finance') >= 85)) or fuzz.token_set_ratio(lineitem_is, 'ebitda') >= 85 or any(fuzz.token_sort_ratio(lineitem_is, mt1) >= 95 for mt1 in all_km):

            if not i in not_calf:
                print('\n===========> ',lineitem_is,' => CL')
                data['Data']['Financial Tables'][1]['Income Statement'][i].update({"Calculated Field":True})
                is_cal_index.append(i)

            '''If any line item contains net it will be checked in all classes. With position no. >1 of individual class consided as calculated filed'''
        elif (lineitem_is.startswith('net') or lineitem_is.endswith('net')) and fuzz.token_set_ratio(lineitem_is, "exceptional") <= 85 and not i in not_calf:
            for dic in income_statement_cls:
                try:
                    found = list(filter(lambda each: fuzz.token_sort_ratio(lineitem_is, each['particular']) >= 95, income_statement_cls[dic]))[0]
                    if income_statement_cls[dic].index(found) > 1:
                        print('\n===========> ',lineitem_is,' => CL**')
                        data['Data']['Financial Tables'][1]['Income Statement'][i].update({"Calculated Field":True})
                        is_cal_index.append(i)
                        break
                except Exception as e:
                    # print(e)
                    pass

        else:
            print('\n',lineitem_is)
            data['Data']['Financial Tables'][1]['Income Statement'][i].update({"Calculated Field":False})
 
    return data

def check_person_2(name:str)->list:

    if name.startswith('to '):
        name = name[3:]

    sentences = nltk.sent_tokenize(name)
    Tokens = []
    for Sent in sentences:
        Tokens.append(nltk.word_tokenize(Sent)) 
    Words_List = [nltk.pos_tag(Token) for Token in Tokens]

    Nouns_List = []

    for List in Words_List:
        for Word in List:
            if re.match('[NN.*]', Word[1]):
                Nouns_List.append(Word[0])

    Names = []
    for Nouns in Nouns_List:
        if not wordnet.synsets(Nouns):
            Names.append(Nouns)

    return Names


def salary_wages_mapping(tem_code:str, name:str)->bool:

    '''Tempalte specific mapping'''
    ''' If salary is present before wages then it should be mapped with it's residual'''
    try:
        if re.search('salar', name).start() < re.search('wages', name).start() and tem_code.lower() in ['t_sc_efl_sme']:
        # if re.search('salar', name).start() < re.search('wages', name).start():
            return False
        else:
            return True
    except:
        return True


def signage_inner_outer(in_out:str, match_:int, km4_:int)->bool:

    '''Less signage rule for Operating and non operating items will apply Only if they have inner and before km4'''
    if in_out == 'outer' and match_ < km4_ and km4_ != -1:
        return False

    return True
               

def Signage_Exceptional_Extraordinary_(data_:dict, is_data:dict, year_pos:int)->dict:
    '''Level 10 OR anything between Level 9 and (Level 11 or 13 or 15) is exceptional item. Similarly Level 12 OR anything between Level 11 and (Level 13 or 15) is extraordinary item. Level 14 OR anything between Level 13 and Level 15 is prior period item.'''
    '''XREV-1169'''

    global IS_GRAPH_OUTPUT, KM4, KM5, is_cal_index
    # print(IS_GRAPH_OUTPUT)

    data__ = pd.DataFrame(data_['Data']['Financial Tables'][1]['Income Statement'])

    col = ["Label Name"]
    col_ = ["Year"+str(yc+1)+" Value" for yc in range(year_pos)]
    col = col+col_+["Calculated Field"]
    data = data__[col]

    # data = data__[["Label Name","Year1 Value","Year2 Value","Calculated Field"]]
    lineitem = []
    print(["".join(each1['particular'].split()) for each1 in is_data['Non-operating or Other Income / Expenses']])

    if not is_data['Non-operating or Other Income / Expenses']:
        lineitems = [{'particular':''}]
    else:
        lineitems = is_data['Non-operating or Other Income / Expenses']

    year_value = 'Year'+str(year_pos)+' '+'Value'

    levels = [list(each2)[2][0] for each2 in IS_GRAPH_OUTPUT]
    levels = [ each15.replace(each15[each15.find('.'):],'') if '.' in each15 else each15 for each15 in levels]
    print("levels::::::::",levels)
    if 'Level10' in levels:
        lineitem.append([IS_GRAPH_OUTPUT[levels.index('Level10')][1]])
    if 'Level9' in levels and 'Level11' in levels:
        lineitem.append([each3 for each3 in range(IS_GRAPH_OUTPUT[levels.index('Level9')][1]+1,IS_GRAPH_OUTPUT[levels.index('Level11')][1])])
    if 'Level9' in levels and 'Level13' in levels:
        lineitem.append([each4 for each4 in range(IS_GRAPH_OUTPUT[levels.index('Level9')][1]+1,IS_GRAPH_OUTPUT[levels.index('Level13')][1])])
    if 'Level9' in levels and 'Level15' in levels:
        lineitem.append([each5 for each5 in range(IS_GRAPH_OUTPUT[levels.index('Level9')][1]+1,IS_GRAPH_OUTPUT[levels.index('Level15')][1])])

    if 'Level12' in levels:
        # if IS_GRAPH_OUTPUT[levels.index('Level12')][1] not in sum(lineitem,[]):
        lineitem.append([IS_GRAPH_OUTPUT[levels.index('Level12')][1]])

    if 'Level11' in levels and 'Level13' in levels:
        lineitem.append([each6 for each6 in range(IS_GRAPH_OUTPUT[levels.index('Level11')][1]+1,IS_GRAPH_OUTPUT[levels.index('Level13')][1]) ])
    if 'Level11' in levels and 'Level15' in levels:
        lineitem.append([each7 for each7 in range(IS_GRAPH_OUTPUT[levels.index('Level11')][1]+1,IS_GRAPH_OUTPUT[levels.index('Level15')][1]) ])
    if 'Level11' in levels and 'Level17' in levels:
        lineitem.append([each7 for each7 in range(IS_GRAPH_OUTPUT[levels.index('Level11')][1]+1,IS_GRAPH_OUTPUT[levels.index('Level17')][1]) ])

    if 'Level14' in levels:
        # if IS_GRAPH_OUTPUT[levels.index('Level14')][1] not in sum(lineitem,[]):
        lineitem.append([IS_GRAPH_OUTPUT[levels.index('Level14')][1]])


    if 'Level13' in levels and 'Level15' in levels:
        lineitem.append([each8 for each8 in range(IS_GRAPH_OUTPUT[levels.index('Level13')][1]+1,IS_GRAPH_OUTPUT[levels.index('Level15')][1]) ])


    # if 'Level16' in levels:
    #   # if IS_GRAPH_OUTPUT[levels.index('Level14')][1] not in sum(lineitem,[]):
    #   lineitem.append([IS_GRAPH_OUTPUT[levels.index('Level16')][1]])

    tax_idx = []
    Tax_Execution = True
    MAT_Credit = 0
    Current_Tax = 0
    Current_Sign = False
    Current_Flag = True

    if 'Level16' in levels and 'Level17' in levels:
        lineitem.append([each11 for each11 in range(IS_GRAPH_OUTPUT[levels.index('Level16')][1],IS_GRAPH_OUTPUT[levels.index('Level17')][1]) ])
        tax_idx = [each12 for each12 in range(IS_GRAPH_OUTPUT[levels.index('Level16')][1],IS_GRAPH_OUTPUT[levels.index('Level17')][1]) ]

    elif 'Level15' in levels and 'Level17' in levels:
        lineitem.append([each11 for each11 in range(IS_GRAPH_OUTPUT[levels.index('Level15')][1]+1,IS_GRAPH_OUTPUT[levels.index('Level17')][1]) ])
        tax_idx = [each12 for each12 in range(IS_GRAPH_OUTPUT[levels.index('Level15')][1]+1,IS_GRAPH_OUTPUT[levels.index('Level17')][1]) ]

    print('li:::',lineitem)
    print('tax_idx::::', tax_idx)
    print("****************************************************************")

    if pd.DataFrame(is_data['Tax']).shape[0] == 1:
        ''' If tax expense has line item which contains both “expense” AND “benefit”, multiply reported amount by -1 '''
        if fuzz.token_set_ratio(data_['Data']['Financial Tables'][1]['Income Statement'][tax_idx[0]]['Label Name'], "expense") > 85 and fuzz.token_set_ratio(data_['Data']['Financial Tables'][1]['Income Statement'][tax_idx[0]]['Label Name'], "benefit") > 85:
            
            data_['Data']['Financial Tables'][1]['Income Statement'][tax_idx[0]][year_value] = str(normalize(data_['Data']['Financial Tables'][1]['Income Statement'][tax_idx[0]][year_value]) * -1) 
            print('\n\n************ If tax expense has line item which contains both “expense” AND “benefit”, multiply reported amount by -1 *************')
            Tax_Execution = False

    done = []

    for each20 in tax_idx:

        if process.extractOne("".join(data_['Data']['Financial Tables'][1]['Income Statement'][each20]['Label Name'].split()), ['current', 'income tax', 'Label Name', 'Provision', 'earlier'], scorer=fuzz.partial_ratio)[1] > 85 and process.extractOne("".join(data_['Data']['Financial Tables'][1]['Income Statement'][each20]['Label Name'].split()), ["MAT", "Credit", "deferred"], scorer=fuzz.partial_ratio)[1] < 85 and Tax_Execution and each20 not in is_cal_index:
                        
            if normalize(data_['Data']['Financial Tables'][1]['Income Statement'][each20][year_value]) != 0:

                print("Current Tax:::", data_['Data']['Financial Tables'][1]['Income Statement'][each20]['Label Name'])
                Current_Tax = Current_Tax + normalize(data_['Data']['Financial Tables'][1]['Income Statement'][each20][year_value])

    print("Current_Tax SUM::::", Current_Tax)

    print('\n\n')

    for each in lineitem:
        for idx in range(len(each)):
            previous_calf = -1
            after_calf = -1
            sign = 0
            # check_lineitem = each[idx]
            # print("check_lineitem::::",check_lineitem)
            # print("min(each):::::", min(each))
            # print("type of min(each):::::", type(min(each)))

            if each[idx] not in tax_idx:
                previous_calf = float(data[year_value].iloc[min(each)-1])
                after_calf = float(data[year_value].iloc[max(each)+1])
            else:
                previous_calf = float(data[year_value].iloc[KM4])
                after_calf = float(data[year_value].iloc[KM5])

    
            # print("Index::::", each[idx])
            # print(data)
            sum_ = float(reduce(lambda x,y: float(x)+float(y),data[year_value][each[0]:each[-1]+1]))
            # print("sum:::",sum_)

            if after_calf > previous_calf and after_calf!= -1 and previous_calf != -1 and process.extractOne("".join(data_['Data']['Financial Tables'][1]['Income Statement'][each[idx]]['Label Name'].split()), ["".join(each9['particular'].split()) for each9 in lineitems], scorer=fuzz.partial_ratio)[1] > 90 and each[idx] not in done and each[idx] not in tax_idx and each[idx] not in is_cal_index:

                sign = 1 if sum_ < 0  else -1


            elif after_calf < previous_calf and after_calf!= -1 and previous_calf != -1 and each[idx] not in done and each[idx] not in tax_idx and each[idx] not in is_cal_index:

                if process.extractOne("".join(data_['Data']['Financial Tables'][1]['Income Statement'][each[idx]]['Label Name'].split()), ["".join(each10['particular'].split()) for each10 in is_data['Non-operating or Other Income / Expenses']], scorer=fuzz.partial_ratio)[1] > 90:
                    sign = -1 if sum_ < 0  else 1
                else:
                    sign = 1 if sum_ < 0  else -1

                
            #XREV-1223
            elif each[idx] not in done and each[idx] in tax_idx and Tax_Execution and each[idx] not in is_cal_index:

                if process.extractOne("".join(data_['Data']['Financial Tables'][1]['Income Statement'][each[idx]]['Label Name'].split()), ["Income tax expense", "Income tax benefit/(expense)", "current", "Provision", "earlier"], scorer=fuzz.partial_ratio)[1] > 85:
                    
                    if Current_Sign:
                        sign = Current_Sign
                    else:
                        sign = -1 if normalize(data_['Data']['Financial Tables'][1]['Income Statement'][each[idx]][year_value]) < 0  else 1
                    
                    if fuzz.token_set_ratio(data_['Data']['Financial Tables'][1]['Income Statement'][each[idx]]['Label Name'], 'current') > 85 or fuzz.token_set_ratio(data_['Data']['Financial Tables'][1]['Income Statement'][each[idx]]['Label Name'], 'income tax') > 85 or fuzz.token_set_ratio(data_['Data']['Financial Tables'][1]['Income Statement'][each[idx]]['Label Name'], 'Provision') > 85 or fuzz.token_set_ratio(data_['Data']['Financial Tables'][1]['Income Statement'][each[idx]]['Label Name'], 'earlier') > 85 and fuzz.token_set_ratio(data_['Data']['Financial Tables'][1]['Income Statement'][each[idx]]['Label Name'], 'prior') < 85:
                        
                        if normalize(data_['Data']['Financial Tables'][1]['Income Statement'][each[idx]][year_value]) != 0:

                            # Current_Tax = Current_Tax + normalize(data_['Data']['Financial Tables'][1]['Income Statement'][each[idx]][year_value])
                            print('*********************Current TAX*******************************')
                            if Current_Flag:
                                Current_Sign = sign
                                Current_Flag = False

                elif process.extractOne("".join(data_['Data']['Financial Tables'][1]['Income Statement'][each[idx]]['Label Name'].split()), ["MAT", "Credit"], scorer=fuzz.partial_ratio)[1] > 90 and process.extractOne("".join(data_['Data']['Financial Tables'][1]['Income Statement'][each[idx]]['Label Name'].split()), ["deferred"], scorer=fuzz.partial_ratio)[1] < 90 and Tax_Execution and each[idx] not in is_cal_index:
                    
                    sign = 1 if normalize(data_['Data']['Financial Tables'][1]['Income Statement'][each[idx]][year_value]) < 0  else -1
                    MAT_Credit = normalize(data_['Data']['Financial Tables'][1]['Income Statement'][each[idx]][year_value])

                elif process.extractOne("".join(data_['Data']['Financial Tables'][1]['Income Statement'][each[idx]]['Label Name'].split()), ["deferred"], scorer=fuzz.partial_ratio)[1] > 90 and Tax_Execution and each[idx] not in is_cal_index:
                    print('km+1:::',after_calf , 'mat:::',abs(int(round(MAT_Credit))), 'ct:::',abs(int(round(Current_Tax))), 'km-1::',previous_calf)

                    if after_calf - abs(int(round(MAT_Credit))) + abs(int(round(Current_Tax))) > previous_calf and after_calf!= -1 and previous_calf != -1:
                        sign = 1 if normalize(data_['Data']['Financial Tables'][1]['Income Statement'][each[idx]][year_value]) < 0  else -1

                    elif after_calf - abs(int(round(MAT_Credit))) + abs(int(round(Current_Tax))) <= previous_calf and after_calf!= -1 and previous_calf != -1:
                        sign = -1 if normalize(data_['Data']['Financial Tables'][1]['Income Statement'][each[idx]][year_value]) < 0  else 1

                
            if sign != 0:

                print("Index::::", each[idx])
                print("sum:::",sum_)

                print(data_['Data']['Financial Tables'][1]['Income Statement'][each[idx]]['Label Name'],'=======>',"Multipled by:::", sign)
                print("original value:::::", normalize(data_['Data']['Financial Tables'][1]['Income Statement'][each[idx]][year_value]))

                data_['Data']['Financial Tables'][1]['Income Statement'][each[idx]][year_value] = str(normalize(data_['Data']['Financial Tables'][1]['Income Statement'][each[idx]][year_value]) * sign) 
                print("new value:::::", data_['Data']['Financial Tables'][1]['Income Statement'][each[idx]][year_value])
                done.append(each[idx])
                print('-------------------------------------------------------------------------------\n')

    return data_

def check_revenue(req_item:list)->bool:
    ''' If revenue corpus present then return True else False '''
    
    for each in req_item:
        if process.extractOne(each, ['Revenue', 'sales', 'operating income', 'operations', 'fees', 'turnover', 'contract receipt'],scorer=fuzz.token_set_ratio)[1] >= 85:
            return True

    for each in req_item:
        if process.extractOne(each, ["opening stock", "closing stock", "opening wip", 'finished goods', "closing work in progress", "contract expenses","cost of operation", \
            "opening work in progress","cost of materials consumed", "cost of goods sold", "direct material", "direct labour", "direct cost", "cost of sales", \
            "cost of raw materials and packing materials consumed", "excise duty", 'consumption of material', 'raw material consumed','direct expenses', 'changes in inventories', \
            'stock in trade', 'purchases', 'purchase', 'construction meterials consumption', "cost of construction", "cost of stock sold"],scorer=fuzz.token_set_ratio)[1] >= 85:
            return True

    return False

def IS_mapping(DATA:dict, df_temp:object, is_data:dict)->dict:
    """
 
    Many to many mapping for Income Statement
 
    Parameters
    ----------
    DATA : dict 
        Requested dict from extraction

    df_temp : object
        Template in dataframe format

    is_data : dict
        Income statement classification

    Returns
    -------
    dict:
        Income Statement Mapping attached with extraction dict 
        
 
    """
    # print(is_data)
    global is_cal_index, year_count_is, is_header_mapping_dict, All_NEG
    global scenario_flag_is
    print('----------------------IS classes-------------------')
    classes = list(is_data.keys())

    T1 = 55
    T2 = 0

    template_code = DATA['Source']['templateUrl'].split('/')[-2]
    print("TEMPLATE CODE::: ", template_code)
    print(classes)

    # lineitems = list(map(itemgetter('Label Name'), DATA['Data']['Financial Tables'][1]['Income Statement']))
    classes_ = classes[:-4]
    classes_.remove('KM4')

    ps_lineitem, ps_label, ps_subclass, ps_subclasscode = partner_salary_pos(df_temp.copy(), classes_)
    pc_lineitem, pc_label, pc_subclass, pc_subclasscode = partner_capital_pos(df_temp.copy(), classes_)
    ie_lineitem, ie_label, ie_subclass, ie_subclasscode = interest_expense_pos(df_temp.copy(), classes_)
    openingstock_lineitem, openingstock_label, closingstock_lineitem, closingstock_label, openingstock_subclass, openingstock_subclasscode, closingstock_subclass, closingstock_subclasscode = openingclosingstock_pos(df_temp.copy(), classes_)

    print(ps_lineitem, ps_label, '&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
    print(pc_lineitem, pc_label, '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
    print(openingstock_lineitem, openingstock_label, closingstock_lineitem, closingstock_label, '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')

    lineitems = [roman_number(a.strip()) for a in list(map(itemgetter('Label Name'), DATA['Data']['Financial Tables'][1]['Income Statement']))]

    year1_values = list(map(itemgetter('Year1 Value'), DATA['Data']['Financial Tables'][1]['Income Statement']))

    print(lineitems)
    print(year1_values)
    year1_ = DATA['Data']['Financial Tables'][1]['Income Statement'][0]['Year1']

    for each in classes:
        if each in df_temp['Class'].to_list() and is_data[each]: 
    
            print('###############################################',each,'##################################################')
            # new_df = pd.concat([pd.DataFrame(is_data[each])['particular'], pd.DataFrame(is_data[each]).iloc[:,1], pd.DataFrame(is_data[each])['inner_outer'], df_temp[df_temp['Class'].str.contains(each)]\
            #     ['Lineitem'].reset_index(drop=True), df_temp[df_temp['Class'].str.contains(each)]['Corpus'].reset_index(drop=True), df_temp[df_temp['Class']\
            #     .str.contains(each)]['chart_of_accounts'].reset_index(drop=True),pd.DataFrame(is_data[each])['Label Signage'],df_temp[df_temp['Class']\
            #     .str.contains(each)]['Residual'].reset_index(drop=True)], axis=1, sort=False)

            new_df = pd.concat([pd.DataFrame(is_data[each])['particular'], pd.DataFrame(is_data[each])[year1_], pd.DataFrame(is_data[each])['inner_outer'], df_temp[df_temp['Class']==each]\
                ['Lineitem'].reset_index(drop=True), df_temp[df_temp['Class']==each]['Corpus'].reset_index(drop=True), df_temp[df_temp['Class']\
                ==each]['chart_of_accounts'].reset_index(drop=True),pd.DataFrame(is_data[each])['Label Signage'],df_temp[df_temp['Class']\
                ==each]['Residual'].reset_index(drop=True), df_temp[df_temp['Class']==each]['Classcode'].reset_index(drop=True), df_temp[df_temp['Class']==each]['Subclass'].reset_index(drop=True), df_temp[df_temp['Class']==each]['SubClasscode'].reset_index(drop=True), pd.DataFrame(is_data[each])['id']], axis=1, sort=False)

            new_df["id"] = new_df["id"].apply(lambda x: int(x) if x == x else "")
            print(new_df)
            scores = []
            line_score = []
            # suggestion = {"lineitem" : str, "confidence"  : int, "class" : str, "label" : str, "labelitem" : str}
            suggestion = {}
            previous_suggestion_is = []
            

            for idx, each2 in enumerate(new_df['particular'].to_list()):
                if isinstance(each2, str):

                    print('Previous###  ', each2)
                    each2 = remove_stopwords(each2, each)
                    print('After Stopword removal###  ', each2)

                    for idx2, each3 in enumerate(new_df['Lineitem'].to_list()):
                        
                        if isinstance(each3, str):
                            # print(each3, idx2, "####################", each2, idx)
                    
                            if isinstance(new_df['Corpus'].iloc[idx2], list):
                                corpus = new_df['Corpus'].iloc[idx2]
                                corpus.append(each3)
                            else:
                                corpus = [each3]

                            corpus = [remove_stopwords(word, each) for word in corpus]
                            # print(corpus)
                            line_score.append(process.extractOne(each2, corpus, scorer=fuzz.token_sort_ratio)[1])

                    print(line_score)
                    pos = line_score.index(max(line_score))
                    max_score = max(line_score)

                    # print(new_df['Lineitem'].dropna().unique().tolist())

                    if len(new_df['Lineitem'].dropna().unique().tolist()) == 1:
                        threshold = T2
                    else:
                        threshold = T1

                    match = new_df['id'].iloc[idx]

                    '''**********************************INCOME STATEMENT SIGNAGE***************************************'''
                    print('\nAfter Signage:::')
                    # print("All_NEG::::", All_NEG)
                    if each in ['Depreciation', 'Finance cost'] and len(is_data[each]) == 1:

                        print('Taking the absolute value....')

                        for yc in range(year_count_is):

                            print('Year'+str(yc+1)+' Value OLD::: ', normalize(str(DATA['Data']['Financial Tables'][1]['Income Statement'][match]['Year'+str(yc+1)+' Value'])))
                            value = abs(normalize(str(DATA['Data']['Financial Tables'][1]['Income Statement'][match]['Year'+str(yc+1)+' Value'])))
                            print('Year'+str(yc+1)+' Value NEW::: ', value)

                            DATA['Data']['Financial Tables'][1]['Income Statement'][match]['Year'+str(yc+1)+' Value'] = str(value)
                            is_data[each][idx][list(is_data[each][idx].keys())[1]] = value
                            DATA['Data']['Financial Tables'][1]['Income Statement'][match].update({DATA['Data']['Financial Tables'][1]['Income Statement'][match]['Year'+str(yc+1)+' Value']: value})

                    elif (each in ['Revenue', 'Cost of goods sold / Cost of Sales', 'Operating expenses', 'Non-operating or Other Income / Expenses', 'Depreciation', 'Finance cost'] and new_df['Label Signage'].iloc[idx] == '-' and signage_inner_outer(new_df['inner_outer'].iloc[idx], match, is_data['km_index'][4])) or ( fuzz.partial_ratio("".join(new_df['particular'].iloc[idx].split()), 'return') > 90 and new_df['Label Signage'].iloc[idx] == '+' and check_revenue(new_df['particular'].to_list()[0:idx])) or (new_df['particular'].iloc[idx].strip().lower().startswith('by') and each in ['Cost of goods sold / Cost of Sales'] and template_code.lower() not in ['t_sc_efl_sme']) or (All_NEG and each in ['Cost of goods sold / Cost of Sales', 'Operating expenses', 'Non-operating or Other Income / Expenses', 'Finance cost', 'Depreciation']) and not fuzz.partial_ratio("".join(new_df['particular'].iloc[idx].split()), 'total') >= 85:
                        
                        # print('Negetive signage line item should be mapped as negative******')

                        for yc in range(year_count_is):

                            print('Year'+str(yc+1)+' Value OLD::: ', normalize(DATA['Data']['Financial Tables'][1]['Income Statement'][match]['Year'+str(yc+1)+' Value']))
                            value = normalize(DATA['Data']['Financial Tables'][1]['Income Statement'][match]['Year'+str(yc+1)+' Value']) * 1 if process.extractOne("".join(new_df['particular'].iloc[idx].split()), ['allowances', 'return'], scorer=fuzz.partial_ratio)[1] > 90 and template_code.lower() not in ['t_sc_efl_sme'] and each in ['Revenue'] else normalize(DATA['Data']['Financial Tables'][1]['Income Statement'][match]['Year'+str(yc+1)+' Value']) * -1
                            print('Year'+str(yc+1)+' Value NEW::: ', value)

                            DATA['Data']['Financial Tables'][1]['Income Statement'][match]['Year'+str(yc+1)+' Value'] = str(value)
                            is_data[each][idx][list(is_data[each][idx].keys())[1]] = value
                            DATA['Data']['Financial Tables'][1]['Income Statement'][match].update({DATA['Data']['Financial Tables'][1]['Income Statement'][match]['Year'+str(yc+1)+' Value']: value})
                        
                    else:

                        for yc in range(year_count_is):

                            if (each in ["Other Income"] and float(DATA['Data']['Financial Tables'][1]['Income Statement'][match]['Year'+str(yc+1)+' Value']) < 0 and new_df['Label Signage'].iloc[idx] == '-') or (each in ['Non-operating or Other Income / Expenses' , 'Finance cost'] and float(DATA['Data']['Financial Tables'][1]['Income Statement'][match]['Year'+str(yc+1)+' Value']) > 0 and fuzz.token_set_ratio(new_df['particular'].iloc[idx], 'income') >= 85)\
                                 or (each in ['Non-operating or Other Income / Expenses'] and float(DATA['Data']['Financial Tables'][1]['Income Statement'][match]['Year'+str(yc+1)+' Value']) > 0 and fuzz.token_set_ratio(new_df['particular'].iloc[idx], 'income') > 85 and ((fuzz.token_set_ratio(new_df['particular'].iloc[idx], 'prior') > 85 or fuzz.token_set_ratio(new_df['particular'].iloc[idx], 'earlier') > 85) and fuzz.token_set_ratio(new_df['particular'].iloc[idx], 'period') > 85) and fuzz.token_set_ratio(new_df['particular'].iloc[idx], 'tax') < 85):

                                # print('Negetive signage line item should be mapped as negative OI1')

                                value = normalize(DATA['Data']['Financial Tables'][1]['Income Statement'][match]['Year'+str(yc+1)+' Value']) * -1
                                
                            else:
                                value = normalize(DATA['Data']['Financial Tables'][1]['Income Statement'][match]['Year'+str(yc+1)+' Value'])

                            print('Year'+str(yc+1)+' Value OLD::: ', normalize(DATA['Data']['Financial Tables'][1]['Income Statement'][match]['Year'+str(yc+1)+' Value']))
                            print('Year'+str(yc+1)+' Value NEW::: ', value)

                            DATA['Data']['Financial Tables'][1]['Income Statement'][match]['Year'+str(yc+1)+' Value'] = str(value)
                            is_data[each][idx][list(is_data[each][idx].keys())[1]] = value
                            DATA['Data']['Financial Tables'][1]['Income Statement'][match].update({DATA['Data']['Financial Tables'][1]['Income Statement'][match]['Year'+str(yc+1)+' Value']: value})



                    DATA['Data']['Financial Tables'][1]['Income Statement'][match].update({'particular':new_df['particular'].iloc[idx].strip()})
                    DATA['Data']['Financial Tables'][1]['Income Statement'][match].update({'Label Signage':new_df['Label Signage'].iloc[idx].strip()})

                    if fuzz.token_set_ratio(new_df['particular'].iloc[idx].strip(), 'interest on') > 85 and each.lower() in ['finance cost']:

                        suggestion = make_suggestion(ie_lineitem, max_score, each, ie_subclass, ie_subclasscode, ie_label, new_df['particular'].iloc[idx].strip(), new_df['Classcode'].iloc[0].strip())
                        print(suggestion)
                        
                        DATA['Data']['Financial Tables'][1]['Income Statement'][match].update({'suggestion':suggestion})
                        previous_suggestion_is.append(suggestion)

                    elif max_score > threshold and salary_wages_mapping(template_code, new_df['particular'].iloc[idx].strip()):
                        
                        if each == 'Cost of goods sold / Cost of Sales' and new_df['chart_of_accounts'].iloc[pos] == 'OPSTOCK' and new_df['particular'].iloc[idx].strip().startswith('to'):
                            print('111111111111111111111111111111111')
                            suggestion = make_suggestion(openingstock_lineitem, max_score, each, openingstock_subclass, openingstock_subclasscode, openingstock_label, new_df['particular'].iloc[idx].strip(), new_df['Classcode'].iloc[0].strip())

                        elif each == 'Cost of goods sold / Cost of Sales' and new_df['chart_of_accounts'].iloc[pos] == 'OPSTOCK' and new_df['particular'].iloc[idx].strip().startswith('by'):
                            print('222222222222222222222222222222222222')
                            suggestion = make_suggestion(closingstock_lineitem, max_score, each, closingstock_subclass, closingstock_subclasscode, closingstock_label, new_df['particular'].iloc[idx].strip(), new_df['Classcode'].iloc[0].strip())

                        else:
                            # print('3333333333333333333333333333333333333')
                            suggestion = make_suggestion(new_df['Lineitem'].iloc[pos], max_score, each, new_df['Subclass'].iloc[pos], new_df['SubClasscode'].iloc[pos], new_df['chart_of_accounts'].iloc[pos], new_df['particular'].iloc[idx].strip(), new_df['Classcode'].iloc[0].strip()) 
                        print(suggestion)
                        
                        if each in is_header_mapping_dict.keys():
                            if idx in is_header_mapping_dict[each]:
                                print('Header mapping----------->')
                                suggestion = make_suggestion(previous_suggestion_is[-1]['lineitem'], max_score, each, previous_suggestion_is[-1]['subclass'], previous_suggestion_is[-1]['subclasscode'], previous_suggestion_is[-1]['label'], new_df['particular'].iloc[idx].strip(), new_df['Classcode'].iloc[0].strip())
                                print(suggestion)

                        DATA['Data']['Financial Tables'][1]['Income Statement'][match].update({'suggestion':suggestion})
                        previous_suggestion_is.append(suggestion)

                    else:
                        try:
                            residual_pos = [new_df['Residual'].to_list().index('Y')]
                        except:
                            residual_pos = []
                        print("###################RESIDUAL POS########################", residual_pos)

                        print('NAME:::', check_person_2(new_df['particular'].iloc[idx].strip()))
                        residual = True


                        if each in is_header_mapping_dict.keys():
                            print('idx::::::::', idx)
                            if idx in is_header_mapping_dict[each]:
                                print('Header mapping----------->')
                                suggestion = make_suggestion(previous_suggestion_is[-1]['lineitem'], max_score, each, previous_suggestion_is[-1]['subclass'], previous_suggestion_is[-1]['subclasscode'], previous_suggestion_is[-1]['label'], new_df['particular'].iloc[idx].strip(), new_df['Classcode'].iloc[0].strip())
                                print(suggestion)
                                DATA['Data']['Financial Tables'][1]['Income Statement'][match].update({'suggestion':suggestion})
                                previous_suggestion_is.append(suggestion)
                                residual = False

                        if (check_person(new_df['particular'].iloc[idx].strip()) or check_person_2(new_df['particular'].iloc[idx].strip())) and each.lower() in ['operating expenses', 'non-operating or other income / expenses']:
                            # print(is_cal_index, match)
                            '''If a person name found in the mentioned class, check the previous calculated field matches with the relevant words. if yes, then map'''
                            nearest_header_cal = max([each_ for each_ in is_cal_index if each_ < match], default=0)
                            # print(nearest_header_cal)
                            print('Nearest Header/Calculated Field::: ', lineitems[nearest_header_cal].strip())

                            if process.extractOne(lineitems[nearest_header_cal].strip(),["salary", "remuneration"], scorer=fuzz.token_set_ratio)[1] > 85:

                                residual = False
                                suggestion = make_suggestion(ps_lineitem, max_score, each, ps_subclass, ps_subclasscode, ps_label, new_df['particular'].iloc[idx].strip(), new_df['Classcode'].iloc[0].strip())
                                print(suggestion)
                                
                                DATA['Data']['Financial Tables'][1]['Income Statement'][match].update({'suggestion':suggestion})
                                previous_suggestion_is.append(suggestion)

                            elif process.extractOne(lineitems[nearest_header_cal].strip(),["interest"], scorer=fuzz.token_set_ratio)[1] > 85:

                                residual = False
                                suggestion = make_suggestion(pc_lineitem, max_score, each, pc_subclass, pc_subclasscode, pc_label, new_df['particular'].iloc[idx].strip(), new_df['Classcode'].iloc[0].strip())
                                print(suggestion)
                                
                                DATA['Data']['Financial Tables'][1]['Income Statement'][match].update({'suggestion':suggestion})
                                previous_suggestion_is.append(suggestion)


                        if residual_pos and residual:

                            suggestion = make_suggestion(new_df['Lineitem'].iloc[residual_pos[0]], max_score, each, new_df['Subclass'].iloc[residual_pos[0]], new_df['SubClasscode'].iloc[residual_pos[0]], new_df['chart_of_accounts'].iloc[residual_pos[0]], new_df['particular'].iloc[idx].strip(), new_df['Classcode'].iloc[0].strip())
                            print(suggestion)
                            
                            DATA['Data']['Financial Tables'][1]['Income Statement'][match].update({'suggestion':suggestion})
                            previous_suggestion_is.append(suggestion)


                    line_score = []
                    suggestion = {}
                    print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n')

    '''For upmapped data year and year value will be attached'''
    for i, itr in enumerate(DATA['Data']['Financial Tables'][1]['Income Statement']):
        if not 'particular' in itr:

            for yc in range(year_count_is):
                DATA['Data']['Financial Tables'][1]['Income Statement'][i].update({DATA['Data']['Financial Tables'][1]['Income Statement'][i]['Year'+str(yc+1)+' Value']: normalize(DATA['Data']['Financial Tables'][1]['Income Statement'][i]['Year'+str(yc+1)+' Value'])})

    try:
        print("\n\n\nSignage_Exceptional_Extraordinary Checking::::")

        if DATA["Source"]["annualReportType"] in ['Schedule-III', 'Other vertical format']:
            for count in range(year_count_is):
                print('**********************************************YEAR '+str(count+1)+'********************************************************\n\n')
                DATA = Signage_Exceptional_Extraordinary_(DATA.copy(), is_data, count+1)

    except:
        print(traceback.print_exc())
        pass


    ''' Decimal Check'''
    print('\n\n\nDECIMAL ISSUE CHECKING(If any line item value is exceeded the total value)::: ')
    try:
        if DATA['Source']['annualReportType'] == 'T-form (Tally)':
            # print(DATA['Data']['Financial Tables'][0]['Balance Sheet'])
            df = pd.DataFrame(DATA['Data']['Financial Tables'][1]['Income Statement'])
            df = df[['Label Name', 'Year1 Value', 'Year2 Value']]
            total_index = np.nonzero(list(df.apply(lambda x: float(x['Year1 Value']) if process.extractOne("".join(x['Label Name'].lower().split()) ,['total', ''], scorer=fuzz.partial_ratio)[1] > 85 else 0, axis=1)))

            by_total = float(df['Year1 Value'].iloc[total_index[0][0]])
            to_total = float(df['Year1 Value'].iloc[total_index[-1][-1]])
            print("by_total, to_total::::", by_total, to_total)


            if by_total > to_total:
                max_total = by_total
            elif by_total < to_total:
                max_total = to_total
            else:
                max_total = by_total

            for ix ,each in enumerate(DATA['Data']['Financial Tables'][1]['Income Statement']):
                if str(max_total).find('.') - each['Year1 Value'].find('.') == -1:

                    print(each['Year1 Value'], normalize(each['Year1 Value'])/10)
                    DATA['Data']['Financial Tables'][1]['Income Statement'][ix].update({"Year1 Value": str(normalize(each['Year1 Value'])/10)})

                elif str(max_total).find('.') - each['Year1 Value'].find('.') == -2:

                    print(each['Year1 Value'], normalize(each['Year1 Value'])/100)
                    DATA['Data']['Financial Tables'][1]['Income Statement'][ix].update({"Year1 Value": str(normalize(each['Year1 Value'])/100)})
    except:
        print('GOT ISSUE WITH DECIMAL ISSUE CHECKING::: ')


    print('\n\n\nIS DECIAMAL CHECKING::::::::::::')
    try:
        if scenario_flag_is == 0:

            for count in range(year_count_is):
                DATA = scenario_zero_decimal_check_is(DATA, is_data,count+1) 

        if scenario_flag_is == 1:

            for count in range(year_count_is):
                DATA = scenario_one_decimal_check_is(DATA, is_data,count+1) 

    except Exception as e:
        print(e)
        print(traceback.print_exc())

    print('\n\n==========================================================================================\n\n')

    is_cal_index = []

    return DATA


def scenario_zero_decimal_check_is(DATA:dict, is_data:dict, year_pos:int)->dict:

    ''' Scenario = 0 and no outer columns then divide the IS into income = all BY or before expense and expense = upto km5. 
        Run the rule in income and expense. This rule will not work if there are two different decimal errors in income and expense
    '''

    global KM1, KM4, KM5, SIGNAGE, is_cal_index

    fixed = []

    data = pd.DataFrame(DATA['Data']['Financial Tables'][1]['Income Statement'])

    print('YEAR::::::::', 'Year'+str(year_pos)+' '+'Value')

    # if list(data['meta_year'+str(year_pos)]).count('outer') == 0:

    lineitems = [roman_number(a.strip()) for a in list(map(itemgetter('Label Name'), DATA['Data']['Financial Tables'][1]['Income Statement']))]

    year_values = list(map(itemgetter('Year'+str(year_pos)+' '+'Value'), DATA['Data']['Financial Tables'][1]['Income Statement']))   

    print('INCOME SIDE STARTING...........')

    income_total_index = list(np.nonzero(list(data.apply(lambda x: float(x['Year'+str(year_pos)+' '+'Value']) if process.extractOne("".join(x['Label Name'].lower().split()) ,['total', ''], scorer=fuzz.partial_ratio)[1] > 85 and float(x['Year'+str(year_pos)+' '+'Value'])!= 0.0 else 0, axis=1)))[0])

    if income_total_index:
        print('INCOME TOTAL and INDEX:::', income_total_index[0], float(data['Year'+str(year_pos)+' '+'Value'].iloc[income_total_index[0]]))

        total_sum_income = float(data['Year'+str(year_pos)+' '+'Value'].iloc[income_total_index[0]])
        inner_sum_income = sum([float(num) for num in data['Year'+str(year_pos)+' '+'Value'][0:income_total_index[0]]])
        # print('total_sum_income, inner_sum_income::::::', total_sum_income, inner_sum_income)
        # print([float(num) for num in data['Year'+str(year_pos)+' '+'Value'][0:income_total_index[0]]])

        diff = abs(int(round(total_sum_income-inner_sum_income)))
        # print('diff:::::',diff)
        diff_len = len(str(diff))
        # print('diff_len:::::',diff_len)

#         # decimal_error = []
        for idx2 in range(0,income_total_index[0]+1):
            # if len(str(abs(int(float(data['Year'+str(year_pos)+' '+'Value'].iloc[idx2]))))) == diff_len:
            # if True:
            if inner_sum_income > total_sum_income:

                # if abs(int((float(data['Year'+str(year_pos)+' '+'Value'].iloc[idx2]) * 90)/100)) == diff and not diff is 0:
                if float(data['Year'+str(year_pos)+' '+'Value'].iloc[idx2]) in subset_sum([float(num) for num in data['Year'+str(year_pos)+' '+'Value'][0:income_total_index[0]]], diff, 90) and not diff is 0:
                    print('total_sum_income, inner_sum_income::::::', total_sum_income, inner_sum_income)
                    print('diff:::::',diff)
                    print('diff_len:::::',diff_len)

                    print('One decimal error found::::',data['Year'+str(year_pos)+' '+'Value'].iloc[idx2],idx2)

                    for en, value in enumerate(year_values):
                   
                        if normalize(data['Year'+str(year_pos)+' '+'Value'].iloc[idx2]) == normalize(value) and fuzz.ratio(data['Label Name'].iloc[idx2].strip().lower(), lineitems[en].lower()) ==100:
                            print('match::::::',data['Label Name'].iloc[idx2].strip().lower(), en)
                            match = en
                            print(str(float(data['Year'+str(year_pos)+' '+'Value'].iloc[idx2])/10))
                            DATA['Data']['Financial Tables'][1]['Income Statement'][match].update({'Year'+str(year_pos)+' '+'Value':str(float(data['Year'+str(year_pos)+' '+'Value'].iloc[idx2])/10)})


                # if abs(int((float(data['Year'+str(year_pos)+' '+'Value'].iloc[idx2]) * 99)/100)) == diff and not diff is 0:
                elif float(data['Year'+str(year_pos)+' '+'Value'].iloc[idx2]) in subset_sum([float(num) for num in data['Year'+str(year_pos)+' '+'Value'][0:income_total_index[0]]], diff, 99) and not diff is 0:
                    print('Two decimal error found::::',data['Year'+str(year_pos)+' '+'Value'].iloc[idx2],idx2)

                    for en, value in enumerate(year_values):
                   
                        if normalize(data['Year'+str(year_pos)+' '+'Value'].iloc[idx2]) == normalize(value) and fuzz.ratio(data['Label Name'].iloc[idx2].strip().lower(), lineitems[en].lower()) ==100:
                            print('match::::::',data['Label Name'].iloc[idx2].strip().lower(), en)
                            match = en
                            print(str(float(data['Year'+str(year_pos)+' '+'Value'].iloc[idx2])/100))
                            DATA['Data']['Financial Tables'][1]['Income Statement'][match].update({'Year'+str(year_pos)+' '+'Value':str(float(data['Year'+str(year_pos)+' '+'Value'].iloc[idx2])/100)})


        print('----------------------------------------------------------')


    print('EXPENSE SIDE STARTING............')

    if income_total_index:
        expense_starting_index = income_total_index[0]+1
        if DATA['Source']['annualReportType'] == 'T-form (Tally)':
            expense_starting_index = SIGNAGE

    else:
        expense_starting_index = 0

    expense_total_index = list(np.nonzero(list(data[expense_starting_index:].apply(lambda x: float(x['Year'+str(year_pos)+' '+'Value']) if process.extractOne("".join(x['Label Name'].lower().split()) ,['total', ''], scorer=fuzz.partial_ratio)[1] > 85 and float(x['Year'+str(year_pos)+' '+'Value'])!= 0.0 else 0, axis=1)))[0])
    expense_total_index = [expense_starting_index + in_ for in_ in expense_total_index]

    if KM1!=-1:
        expense_total_index = [d_ for d_ in expense_total_index if d_ > KM1]

    if expense_total_index:
        print('EXPENSE TOTAL and INDEX:::', expense_total_index[0], float(data['Year'+str(year_pos)+' '+'Value'].iloc[expense_total_index[0]]))

        total_sum_expense = float(data['Year'+str(year_pos)+' '+'Value'].iloc[expense_total_index[0]])
        inner_sum_expense = sum([float(num) for num in data['Year'+str(year_pos)+' '+'Value'][expense_starting_index:expense_total_index[0]]])
        # print('total_sum_expense, inner_sum_expense::::::', total_sum_expense, inner_sum_expense)

        diff = abs(int(round(total_sum_expense-inner_sum_expense)))
        # print('diff:::::',diff)
        diff_len = len(str(diff))
        # print('diff_len:::::',diff_len)

        for idx2 in range(expense_starting_index, expense_total_index[0]):

            # if len(str(abs(int(float(data['Year'+str(year_pos)+' '+'Value'].iloc[idx2]))))) == diff_len:
            # if True:
            if inner_sum_expense > total_sum_expense:

                # if abs(int((float(data['Year'+str(year_pos)+' '+'Value'].iloc[idx2]) * 90)/100)) == diff and not diff is 0:
                if float(data['Year'+str(year_pos)+' '+'Value'].iloc[idx2]) in subset_sum([float(num) for num in data['Year'+str(year_pos)+' '+'Value'][expense_starting_index:expense_total_index[0]]], diff, 90) and not diff is 0:
                    print('total_sum_expense, inner_sum_expense::::::', total_sum_expense, inner_sum_expense)
                    print('diff:::::',diff)
                    print('diff_len:::::',diff_len)

                    print('One decimal error found::::',data['Year'+str(year_pos)+' '+'Value'].iloc[idx2],idx2)

                    for en, value in enumerate(year_values):
                   
                        if normalize(data['Year'+str(year_pos)+' '+'Value'].iloc[idx2]) == normalize(value) and fuzz.ratio(data['Label Name'].iloc[idx2].strip().lower(), lineitems[en].lower()) ==100:
                            print('match::::::',data['Label Name'].iloc[idx2].strip().lower(), en)
                            match = en
                            print(str(float(data['Year'+str(year_pos)+' '+'Value'].iloc[idx2])/10))
                            DATA['Data']['Financial Tables'][1]['Income Statement'][match].update({'Year'+str(year_pos)+' '+'Value':str(float(data['Year'+str(year_pos)+' '+'Value'].iloc[idx2])/10)})
                            fixed.append(idx2)

                # if abs(int((float(data['Year'+str(year_pos)+' '+'Value'].iloc[idx2]) * 99)/100)) == diff and not diff is 0:
                elif float(data['Year'+str(year_pos)+' '+'Value'].iloc[idx2]) in subset_sum([float(num) for num in data['Year'+str(year_pos)+' '+'Value'][expense_starting_index:expense_total_index[0]]], diff, 99) and not diff is 0:
                    print('Two decimal error found::::',data['Year'+str(year_pos)+' '+'Value'].iloc[idx2],idx2)

                    for en, value in enumerate(year_values):
                   
                        if normalize(data['Year'+str(year_pos)+' '+'Value'].iloc[idx2]) == normalize(value) and fuzz.ratio(data['Label Name'].iloc[idx2].strip().lower(), lineitems[en].lower()) ==100:
                            print('match::::::',data['Label Name'].iloc[idx2].strip().lower(), en)
                            match = en
                            print(str(float(data['Year'+str(year_pos)+' '+'Value'].iloc[idx2])/100))
                            DATA['Data']['Financial Tables'][1]['Income Statement'][match].update({'Year'+str(year_pos)+' '+'Value':str(float(data['Year'+str(year_pos)+' '+'Value'].iloc[idx2])/100)})
                            fixed.append(idx2)

        print('----------------------------------------------------------')


    # print(DATA)
    print('Operting and Non-Operating SIDE STARTING............')

    if expense_total_index:
        if len(data) - expense_total_index[0] > 5:
            op_starting_index = expense_total_index[0]+1
        else:
            op_starting_index = expense_starting_index
    else:
        op_starting_index = int(len(data)/2)

    op_total_index = list(np.nonzero(list(data[op_starting_index:].apply(lambda x: float(x['Year'+str(year_pos)+' '+'Value']) if process.extractOne("".join(x['Label Name'].lower().split()) ,['total', ''], scorer=fuzz.partial_ratio)[1] > 85 and float(x['Year'+str(year_pos)+' '+'Value'])!= 0.0 else 0, axis=1)))[0])
    op_total_index = [op_starting_index + in_ for in_ in op_total_index]

    if op_total_index:
        print('OPERATING and Non-OPERATING TOTAL and INDEX:::', op_total_index[0], float(data['Year'+str(year_pos)+' '+'Value'].iloc[op_total_index[0]]))

        total_sum_op = float(data['Year'+str(year_pos)+' '+'Value'].iloc[op_total_index[0]])

        inner_sum_op = sum([float(num) for num in data['Year'+str(year_pos)+' '+'Value'][op_starting_index: op_total_index[0]]])
        # print('total_sum_op, inner_sum_op::::::', total_sum_op, inner_sum_op)

        diff = abs(int(round(total_sum_op - inner_sum_op)))
        # print('diff:::::',diff)
        diff_len = len(str(diff))
        # print('diff_len:::::',diff_len)

#         # decimal_error = []
        for idx2 in range(op_starting_index, len(data)):
            # print(data['Year'+str(year_pos)+' '+'Value'].iloc[idx2])
            if len(str(abs(int(float(data['Year'+str(year_pos)+' '+'Value'].iloc[idx2]))))) == diff_len and idx2 not in fixed:

                # if abs(int((float(data['Year'+str(year_pos)+' '+'Value'].iloc[idx2]) * 90)/100)) == diff and not diff is 0:
                if float(data['Year'+str(year_pos)+' '+'Value'].iloc[idx2]) in subset_sum([float(num) for num in data['Year'+str(year_pos)+' '+'Value'][op_starting_index: op_total_index[0]]], diff, 99) and not diff is 0:
                    print('total_sum_op, inner_sum_op::::::', total_sum_op, inner_sum_op)
                    print('diff:::::',diff)
                    print('diff_len:::::',diff_len)

                    print('One decimal error found::::',data['Year'+str(year_pos)+' '+'Value'].iloc[idx2],idx2)

                    for en, value in enumerate(year_values):
                   
                        if normalize(data['Year'+str(year_pos)+' '+'Value'].iloc[idx2]) == normalize(value) and fuzz.ratio(data['Label Name'].iloc[idx2].strip().lower(), lineitems[en].lower()) ==100:
                            print('match::::::',data['Label Name'].iloc[idx2].strip().lower(), en)
                            match = en
                            print(str(float(data['Year'+str(year_pos)+' '+'Value'].iloc[idx2])/10))
                            DATA['Data']['Financial Tables'][1]['Income Statement'][match].update({'Year'+str(year_pos)+' '+'Value':str(float(data['Year'+str(year_pos)+' '+'Value'].iloc[idx2])/10)})


                # if abs(int((float(data['Year'+str(year_pos)+' '+'Value'].iloc[idx2]) * 99)/100)) == diff and not diff is 0:
                elif float(data['Year'+str(year_pos)+' '+'Value'].iloc[idx2]) in subset_sum([float(num) for num in data['Year'+str(year_pos)+' '+'Value'][op_starting_index: op_total_index[0]]], diff, 90) and not diff is 0:
                    print('Two decimal error found::::',data['Year'+str(year_pos)+' '+'Value'].iloc[idx2],idx2)

                    for en, value in enumerate(year_values):
                   
                        if normalize(data['Year'+str(year_pos)+' '+'Value'].iloc[idx2]) == normalize(value) and fuzz.ratio(data['Label Name'].iloc[idx2].strip().lower(), lineitems[en].lower()) ==100:
                            print('match::::::',data['Label Name'].iloc[idx2].strip().lower(), en)
                            match = en
                            print(str(float(data['Year'+str(year_pos)+' '+'Value'].iloc[idx2])/100))
                            DATA['Data']['Financial Tables'][1]['Income Statement'][match].update({'Year'+str(year_pos)+' '+'Value':str(float(data['Year'+str(year_pos)+' '+'Value'].iloc[idx2])/100)})

        print('----------------------------------------------------------')



    if DATA['Source']['annualReportType'] in ['Schedule III', 'Other vertical format', 'Schedule-III']:
        print('TAX SIDE STARTING............')
        print("is_cal_index:::::::::::: ",is_cal_index)
        print(KM4,KM5)
        if not KM4 is -1 and not KM5 is -1:

            total_sum_tax = float(data['Year'+str(year_pos)+' '+'Value'].iloc[KM4]) - num_checking(float(data['Year'+str(year_pos)+' '+'Value'].iloc[KM5]))
            elimanated_cal_rows = [0 if idx in is_cal_index else each for idx, each in enumerate(data['Year'+str(year_pos)+' '+'Value'])]
            print("elimanated_cal_rows::: ", elimanated_cal_rows)
            # inner_sum_tax = sum([float(num) for num in data['Year'+str(year_pos)+' '+'Value'][KM4+1: KM5]])
            inner_sum_tax = sum([float(num) for num in elimanated_cal_rows[KM4+1: KM5]])
            # print('total_sum_tax, inner_sum_tax::::::', total_sum_tax, inner_sum_tax)

            diff = abs(int(round(total_sum_tax-inner_sum_tax)))
            # print('diff:::::',diff)
            diff_len = len(str(diff))
            # print('diff_len:::::',diff_len)

    #         # decimal_error = []
            for idx2 in range(KM4+1,KM5):
                # if len(str(abs(int(float(data['Year'+str(year_pos)+' '+'Value'].iloc[idx2]))))) == diff_len:
                # if True:
                if inner_sum_tax > total_sum_tax:

                    # if abs(int((float(data['Year'+str(year_pos)+' '+'Value'].iloc[idx2]) * 90)/100)) == diff and not diff is 0:
                    if float(data['Year'+str(year_pos)+' '+'Value'].iloc[idx2]) in subset_sum([float(num) for num in data['Year'+str(year_pos)+' '+'Value'][KM4+1: KM5]], diff, 90) and not diff is 0:   
                        print('total_sum_tax, inner_sum_tax::::::', total_sum_tax, inner_sum_tax)
                        print('diff:::::',diff)
                        print('diff_len:::::',diff_len)

                        print('One decimal error found::::',data['Year'+str(year_pos)+' '+'Value'].iloc[idx2],idx2)

                        for en, value in enumerate(year_values):
                       
                            if normalize(data['Year'+str(year_pos)+' '+'Value'].iloc[idx2]) == normalize(value) and fuzz.ratio(data['Label Name'].iloc[idx2].strip().lower(), lineitems[en].lower()) ==100:
                                print('match::::::',data['Label Name'].iloc[idx2].strip().lower(), en)
                                match = en
                                print(str(float(data['Year'+str(year_pos)+' '+'Value'].iloc[idx2])/10))
                                DATA['Data']['Financial Tables'][1]['Income Statement'][match].update({'Year'+str(year_pos)+' '+'Value':str(float(data['Year'+str(year_pos)+' '+'Value'].iloc[idx2])/10)})


                    # if abs(int((float(data['Year'+str(year_pos)+' '+'Value'].iloc[idx2]) * 99)/100)) == diff and not diff is 0:
                    elif float(data['Year'+str(year_pos)+' '+'Value'].iloc[idx2]) in subset_sum([float(num) for num in data['Year'+str(year_pos)+' '+'Value'][KM4+1: KM5]], diff, 99) and not diff is 0:   
                        print('Two decimal error found::::',data['Year'+str(year_pos)+' '+'Value'].iloc[idx2],idx2)

                        for en, value in enumerate(year_values):
                       
                            if normalize(data['Year'+str(year_pos)+' '+'Value'].iloc[idx2]) == normalize(value) and fuzz.ratio(data['Label Name'].iloc[idx2].strip().lower(), lineitems[en].lower()) ==100:
                                print('match::::::',data['Label Name'].iloc[idx2].strip().lower(), en)
                                match = en
                                print(str(float(data['Year'+str(year_pos)+' '+'Value'].iloc[idx2])/100))
                                DATA['Data']['Financial Tables'][1]['Income Statement'][match].update({'Year'+str(year_pos)+' '+'Value':str(float(data['Year'+str(year_pos)+' '+'Value'].iloc[idx2])/100)})
                        
                print('----------------------------------------------------------')


    return DATA



def scenario_one_decimal_check_is(DATA:dict, is_data:dict, year_pos:int)->dict:

    '''
        Scenario = 1, check the rule on every class.
    '''
    # for key in list(is_data.keys())[:-3]:
    #     print(key)
    #     print(pd.DataFrame(is_data[key]))
    global year_count_is

    for key in list(is_data.keys())[:-4]:

        if key in ['Operating expenses']:

            if is_data['Operating expenses']:
                if is_data['Operating expenses'][0]['inner_outer'] == 'outer':
                    data = pd.DataFrame(is_data['Operating expenses']+is_data['Non-operating or Other Income / Expenses'] + is_data['Finance cost'] + is_data['Depreciation'])
                else:
                    data = pd.DataFrame(is_data[key])

        elif key in ['Non-operating or Other Income / Expenses']:

            if is_data['Non-operating or Other Income / Expenses']:
                if is_data['Non-operating or Other Income / Expenses'][0]['inner_outer'] == 'outer':
                    data = pd.DataFrame(is_data['Non-operating or Other Income / Expenses'] + is_data['Operating expenses'] + is_data['Finance cost'] + is_data['Depreciation'])
                else:
                    data = pd.DataFrame(is_data[key])

        else:
            data = pd.DataFrame(is_data[key])
        # print(key, type(data),'@@@@@@@@@@@@@@@@@@@@@@@@')

        # print(data)

        if len(data) > 0:
            temp = ['']
            z = [temp.append(0.0) for yc in range(year_count_is)]
            temp.append('H')
            temp.append(0)
            temp.append('outer')
            # print("temp::: ",temp)
            data.loc[len(data)] = temp
        
            year_col = data.columns[year_pos]
            print('YEAR::::::::', year_col)


            lineitems = [roman_number(a.strip()) for a in list(map(itemgetter('Label Name'), DATA['Data']['Financial Tables'][1]['Income Statement']))]

            year_values = list(map(itemgetter('Year'+str(year_pos)+' '+'Value'), DATA['Data']['Financial Tables'][1]['Income Statement']))
            
            outer_index = list(filter(lambda v: v is not None, [nth_index(data['inner_outer'].to_list(), 'outer', each+1) for each in range(len(data))]))

            if outer_index:

                for each_outer in range(len(outer_index)-1):

                    diff = abs(int(round(data[year_col].iloc[outer_index[each_outer]] - sum(data[year_col].iloc[outer_index[each_outer]+1:outer_index[each_outer+1]]))))
                    
                    diff_len = len(str(diff))


                    for idx2 in range(outer_index[each_outer],outer_index[each_outer+1]):
        
                        # if len(str(abs(int(data[year_col].iloc[idx2])))) == diff_len:
                        # if True:
                        if sum(data[year_col].iloc[outer_index[each_outer]+1:outer_index[each_outer+1]]) > data[year_col].iloc[outer_index[each_outer]]:

                            # if abs(int((data[year_col].iloc[idx2] * 90)/100)) == diff and not diff is 0:
                            # print(float(data[year_col].iloc[idx2]), data[year_col].iloc[outer_index[each_outer]+1:outer_index[each_outer+1]].to_list(), diff, 90)
                            if float(data[year_col].iloc[idx2]) in subset_sum(data[year_col].iloc[outer_index[each_outer]+1:outer_index[each_outer+1]].to_list(), diff, 90) and not diff is 0:

                                print('diff:::::', diff)
                                print('diff_len:::::',diff_len)

                                print('One decimal error found::::',data[year_col].iloc[idx2],idx2)

                                for en, value in enumerate(year_values):
                               
                                    if data[year_col].iloc[idx2] == normalize(value) and fuzz.ratio(data['particular'].iloc[idx2].strip().lower(), lineitems[en].lower()) ==100:
                                        print('match::::::',data['particular'].iloc[idx2].strip().lower(), en)
                                        match = en
                                        print(str(float(data[year_col].iloc[idx2])/10))
                                        DATA['Data']['Financial Tables'][1]['Income Statement'][match].update({'Year'+str(year_pos)+' '+'Value':str(float(data[year_col].iloc[idx2])/10)})

                                print('-------------------------------------------------------------')


                            # if abs(int((data[year_col].iloc[idx2] * 99)/100)) == diff and not diff is 0:
                            elif float(data[year_col].iloc[idx2]) in subset_sum(data[year_col].iloc[outer_index[each_outer]+1:outer_index[each_outer+1]].to_list(), diff, 99) and not diff is 0:

                                print('TWO decimal error found::::',data[year_col].iloc[idx2],idx2)

                                print('diff:::::', diff)
                                print('diff_len:::::',diff_len)

                                for en, value in enumerate(year_values):
                               
                                    if data[year_col].iloc[idx2] == normalize(value) and fuzz.ratio(data['particular'].iloc[idx2].strip().lower(), lineitems[en].lower()) ==100:
                                        print('match::::::',data['particular'].iloc[idx2].strip().lower(), en)
                                        match = en
                                        print(str(float(data[year_col].iloc[idx2])/100))
                                        DATA['Data']['Financial Tables'][1]['Income Statement'][match].update({'Year'+str(year_pos)+' '+'Value':str(float(data[year_col].iloc[idx2])/100)})

                                print('-------------------------------------------------------------')
            
    return DATA