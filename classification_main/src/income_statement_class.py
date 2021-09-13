import glob
import json
import pandas as pd
from numpy import median
from fuzzywuzzy import fuzz,process
import re
import pprint
import os,sys
import traceback
from iteration_utilities import unique_everseen
import copy
pd.set_option("display.max_rows", None, "display.max_columns", None)
from src.graph_fS_classification import *
from utils import *





l1,l2,l3,l4,exp_head,signage,cost,km1,km2,km3,km4,km5,classfi_format,operating_items_end_index,dep,global_df,type_,exclude_tax_index, rev_idx, tax_index, operating_idx, remove_item, by_grosss_proft_index, year_count, nonoperating_idx, dep_index = [],[],[],[],[],-1,[],[],[],[],[],[],{},-1,[],[],'',[],[],[], [],[],[], 2, [], []

income_statement_IS = {
    "KM_1": ["gross profit", "to gross profit", "gross profit/(loss)", 'gross profit c/d', 'gross loss c/d', 'gross profit carried down', 'gross profit to profit & loss account', 'gross profit transfered to profit & loss account'],

    "KM_2": ['operating profit','profit from operations' ,'profit before net financing costs','profit before income tax and finance costs','loss from continuing operations','earnings before interest and income tax expense','earnings before interest and tax','loss from operations','operating loss','loss before net financing costs','loss before income tax and finance costs','(loss)/profit before net finance costs and tax', 'operating profit/(loss)','operating profit/(loss) before financing costs', 'operating profit loss before financing costs'],

    "KM_3": ['profit before exceptional items', 'profit before finance cost depreciation amortisation exceptional', 'net profit loss before depreciation and tax','profit loss before exceptional and extraordinary items', 'profit before exceptional extraordinary items', 'profit loss before exceptional and extraordinary items and tax', 'excess of income over expenditure before depreciation and finance charges', 'profit before exceptional items, share of net profits/(losses) of investment accounted for using equity method and tax','profit before exceptional items and tax','profit before contribution to wppf','profit before share of profit/(loss) of an associate and a joint venture and exceptional item and tax','loss before exceptional items and tax','loss before contribution to wppf','loss before share of loss/(loss) of an associate and a joint venture and exceptional item and tax', 'loss before exceptional items and tax from continuing operations','Profit Before Exceptional and Extra Ordinary ltems & Tax'],

    "KM_4": ['profit before tax','profit before income tax expense', 'profit loss before tax from continuing operations' ,'profit / (loss) before income tax','loss before income tax', 'Excess Of Income Over Expenditure  Transferred to Capital Account','loss before income tax expense','loss / (loss) before income tax','loss before taxation','profit before taxation','Profit before taxes on income','profit / (loss) before tax', 'profit loss before prior period expense & tax'],

    "KM_5": ['profit after tax','profit for the period after tax', 'net income', 'book profit', 'profit for the financial year','balance carried to balance sheet','profit for the year', 'excess of income over expenditure','excess of expenditure over income' ,'excess of income over expenditure for the year', 'excess of expenditure over income for the year','profit loss for the period', 'profit loss for the period from continuing operations', 'profit loss from ordinary activities after tax', 'profit from continuing operations', 'profit for the period','profit','net profit for the period','net profit','nett profit','profit / (loss) for the year','surplus/(deficit) for the year', 'surplus/(deficit)','surplus','deficit','total comprehensive income for the year','total comprehensive income','loss for the period','loss','loss after tax','net loss for the period','net loss','loss / (loss) for the year','profit/(loss) after income tax','profit / (Loss) for the year','NET PROFIT AFTER TAX ATTRIBUTABLE TO EQUITY HOLDERS','net profit/(loss) after tax','profit for the financial year','loss for the financial year','profit / (loss) for the financial year','profit / (loss) for the period','loss for the financial year',"Profit c/d to Appropriation Account", "Profit c/d to PL Appropriation Account", "Profit transferred to Capital Ac", "Profit transferred to Proprietor's Capital Ac", "Profit transferred to Partner's Capital Ac", "Profit carried to Partner's Capital Ac", "Profit carried to Proprietor's Capital Ac", "Net Profit transferred to Capital", "Net Profit tr to Cap Ac", "profit for the year from continuing operations", "net profit before tax", 'loss for the year from continuing operations discontinued operations'],
    
    "other_income": ["other income", "otherincome", "other income and revenue", "intt income",'indirect income', 'by interest', 'interest income', 'interest on sb a/c', 'interest on fd', 'dividend', 'bank interest', 'fdr interest recd.', 'discount recd.'], 
    
    "employee_cost": ["employee benefit","staff","salary","wages", "salaries and wages", "bonus", "employee benefits","employee expenses","employee costs", "employee benefits expense", "labour and related costs"],
    
    "finance_cost": ["financial costs", "interest", "intt", "bank charges & interest", "interest expenses","interest charges", "loan processing charges","bank charges & commission" ,"finance cost","net financing costs","finance charges", "finance expenses", "financial expenses", "finance overheads", "bank interest", "bank interest & charges", "financial charges", "Borrowing costs"],
    
    "cogs": ["opening stock", "closing stock", "opening wip", 'finished goods', "closing work in progress", "contract expenses","cost of operation", "opening work in progress","cost of materials consumed", "cost of goods sold", "direct material", "direct labour", "direct cost", "cost of sales", "cost of raw materials and packing materials consumed", "excise duty", 'consumption of material', 'raw material consumed','direct expenses', 'changes in inventories', 'stock in trade', 'purchases', 'purchase', 'construction meterials consumption', "cost of construction", "cost of stock sold", "material cost"],
    
    "revenue_header" : ['revenues', 'Revenue', 'income', 'continuing operations'],
    
    'expense_header': ['expenditure', 'expense', 'expenses'],

    'revenue_line_item': ['Revenue', 'sales', 'operating income', 'operations', 'fees', 'turnover', 'contract receipt'],

    'cost_line_item': ['cost', 'expenses', 'costs', 'expense'],

    'depreciation': ['depreciation', 'depn', 'amortization', "deprication"],

    'exclusion_operating_expenses': ['other expenses', 'interest and finance charges', 'non operating expenses', 'tax'],

    # 'KM_5_fallback': ['eps', 'earning per share', 'basic', 'diluted'],

    'total_exclusion': ['total'],

    'attribute_exclusion': ['before', 'excluding'],

    'inclusion_tax': ['tax', 'provision', 'mat'],

    "lineitem_remove": ['by gross profit', 'by gross profit Brought Down','by gross profit Transferred from Trading Account', 'to gross loss', 'by profit before tax', 'by net profit b d'],

    "finance_cost_fallback": ["finance", "interest", "bank", "loan", "processing", "financial"],

    "other_income_fallback": ['other', 'indirect', 'interest'],

    "other_income_exclusion": ['work in progress', 'closing work in progress', 'closing wip', 'closing stock'],

    "KM_4_fallback": ["tax expense"],

    "KM_5_fallback": ["profit", "loss", "continuing"],

    "revenue_exclusion": ['closing stock', 'finished goods', 'raw materials', 'work in progress'],

    "operating_expense_fallback": ["depreciation", "operating", "operational"],

    "cogs_exclusion": ['sales']
    }




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


def roman_number(lineitem : str) -> str:
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
    # roman=["","I","II","III","IV","V","VI","VII","VIII","IX","X"]
    # remove_items=[".","-","+","/","(",")","*"]
    # #str_ = "vii. profit before exceptional items and tax (v+vi)"
    # str_=lineitem
    # remove=[c for c in str_ if c in remove_items]
    # #
    # for each in remove:
    #     str_=str_.replace(each," ")
    # sentance=""  
    # for i in str_.split():
    #     if i.upper() in roman:
    #         pass
    #     else:
    #         sentance+=i+" "
    # # print(sentance,"sentance",remove)
    # return sentance
    return lineitem.lower()

def other_income(list_ : list) -> list:
    global type_
    if not isinstance(list_, list) :
        raise TypeError

    else:
        level=[]

        df = pd.DataFrame(list_)
        list_2 = df['particular'].to_list()

        signage_list = df['Label Signage'].to_list()
        corpus=income_statement_IS["other_income"]

        for idx, each in enumerate(list_2):
            # if not (max(df.iloc[idx].values[1], df.iloc[idx].values[2]) == 0.0 and min(df.iloc[idx].values[1], df.iloc[idx].values[2]) == 0.0):
            if not check_header(list_, idx):
                for c in corpus:
                    if fuzz.token_sort_ratio(each.lower(), c.lower()) >= 80 and all(fuzz.partial_token_set_ratio(each.lower(), c.lower()) <= 85 for c in income_statement_IS["total_exclusion"]) and not signage_list[idx] is 'H' and not each.lower().startswith('to '):
                        level.append(list_2.index(each))

        if not level:
            for each in list_2:
                    if each.lower().strip() == corpus[-1]:
                        level.append(list_2.index(each))

        if not level:
            print('-----------------other income not found...Executing fallback---------------------')
            corpus=income_statement_IS['other_income_fallback']

            global signage, exp_head

            if not signage is -1:
                end_index = signage
            elif exp_head:
                end_index = exp_head[0]
            else:
                end_index = len(list_2)

            print('end_index:------------------->', end_index)

            for idx, each in enumerate(list_2):
            
                if all(fuzz.partial_token_set_ratio(each.lower(), c.lower()) <= 85 for c in income_statement_IS["total_exclusion"]) and all(fuzz.partial_token_set_ratio(each.lower(), c.lower()) <= 85 for c in income_statement_IS["attribute_exclusion"]) and not signage_list[idx] is 'H' and idx < end_index:
                    break_lineitem = each.split(" ")
                    
                    for word in break_lineitem:
                        for c in corpus:
                            # print(fuzz.token_sort_ratio(word.lower(), c.lower()), fuzz.partial_token_set_ratio(each.lower(), 'comprehensive'), fuzz.partial_token_set_ratio(each.lower(), 'expense'))
                            if fuzz.token_sort_ratio(word.lower(), c.lower()) >= 85 and not fuzz.partial_token_set_ratio(each.lower(), 'comprehensive') >= 85 and not fuzz.partial_token_set_ratio(each.lower(), 'expense') >= 85:
                                # print(word.lower(), '-->', c.lower(), fuzz.token_sort_ratio(word.lower(), c.lower()))
                                # level.append(list_2.index(each))
                                print(df['Label Signage'].iloc[idx], '&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
                                if type_ in 'T-form_Tally' and df['Label Signage'].iloc[idx] is 'BY':
                                    level.append(list_2.index(each))
                                elif type_ in 'Schedule-III':
                                    level.append(list_2.index(each))
                                break
                        else:
                            continue  
                        break
                    else:
                        continue  
                    break

        level=list(set(level))
        level.sort()
        
        if type_ in 'T-form_Tally':
            if level and not signage is -1:
                for idx in range(level[0]+1,signage):
                    # if not (max(df.iloc[idx].values[1], df.iloc[idx].values[2]) == 0.0 and min(df.iloc[idx].values[1], df.iloc[idx].values[2]) == 0.0) and not df['particular'].iloc[idx] is '':
                    if not check_header(list_, idx) and not df['particular'].iloc[idx] is '':
                        if str(signage_list[idx]) in "BY":
                            level.append(idx)

        return level
    
def employee_cost(list_ : list) -> list:

    global signage, type_
    if not isinstance(list_, list) :
        raise TypeError

    else:
        level=[]
  
        df = pd.DataFrame(list_)
        list_2=df['particular'].to_list()

        signage_list = pd.DataFrame(list_)['Label Signage'].to_list()
        corpus=income_statement_IS["employee_cost"]

        for idx, each in enumerate(list_2):
            for c in corpus:
                # if not (max(df.iloc[idx].values[1], df.iloc[idx].values[2]) == 0.0 and min(df.iloc[idx].values[1], df.iloc[idx].values[2]) == 0.0):
                if not check_header(list_, idx):
                    if fuzz.token_sort_ratio(each.lower(), c.lower()) >= 85 and all(fuzz.partial_token_set_ratio(each.lower(), c.lower()) <= 85 for c in income_statement_IS["total_exclusion"]) and not signage_list[idx] is 'H':
                        # level.append(list_2.index(each))
                        if type_ in 'Schedule-III':
                            level.append(list_2.index(each))
                        else:
                            level.append(list_2.index(each)+signage)
                    
        level=list(set(level))
        level.sort()
        return level
    
def finance_cost(list_ : list) -> list:

    global signage, type_

    if not isinstance(list_, list) :
        raise TypeError

    else:
        level=[]

        df = pd.DataFrame(list_)
        list_2 = df['particular'].to_list()

        signage_list = df['Label Signage'].to_list()
        corpus=income_statement_IS["finance_cost"]

        print('Finance cost:::::::::::', type_)

        if type_ in 'Schedule-III':

            for idx, each in enumerate(list_2):
                for c in corpus:
                    # if not (max(df.iloc[idx].values[1], df.iloc[idx].values[2]) == 0.0 and min(df.iloc[idx].values[1], df.iloc[idx].values[2]) == 0.0):
                    if not check_header(list_, idx):
                        if fuzz.token_sort_ratio(roman_number(each.lower()), c.lower()) >= 85 and all(fuzz.partial_token_set_ratio(each.lower(), c.lower()) <= 85 for c in income_statement_IS["total_exclusion"]) and all(fuzz.partial_token_set_ratio(each.lower(), c.lower()) <= 85 for c in income_statement_IS["attribute_exclusion"]) and not signage_list[idx] is 'H' and not 'income' in each and not 'capital' in each:
                            level.append(list_2.index(each))

            if not level:

                level=[]
                corpus=income_statement_IS["finance_cost_fallback"] 
                print('------------------finance cost fallback-------------------------')
            
                for idx, each in enumerate(list_2):
                    # if not (max(df.iloc[idx].values[1], df.iloc[idx].values[2]) == 0.0 and min(df.iloc[idx].values[1], df.iloc[idx].values[2]) == 0.0):
                    if not check_header(list_, idx):
                        if all(fuzz.partial_token_set_ratio(each.lower(), c.lower()) <= 85 for c in income_statement_IS["total_exclusion"]) and all(fuzz.partial_token_set_ratio(each.lower(), c.lower()) <= 85 for c in income_statement_IS["attribute_exclusion"]) and not signage_list[idx] is 'H' and not 'income' in each and not 'capital' in each:
                            break_lineitem = each.split(" ")
            
                            for word in break_lineitem:
                                for c in corpus:
                                    if fuzz.token_sort_ratio(word.lower(), c.lower()) >= 85 or any(ind in break_lineitem for ind in ['od','cc','bd']):
                                        print(word.lower(), c.lower(), fuzz.token_sort_ratio(word.lower(), c.lower()))
                                        level.append(list_2.index(each))
                                    

        else:

            level=[]
            corpus=income_statement_IS["finance_cost_fallback"] 
            print('------------------finance cost fallback-------------------------')
        
            for idx, each in enumerate(list_2):
                # if not (max(df.iloc[idx].values[1], df.iloc[idx].values[2]) == 0.0 and min(df.iloc[idx].values[1], df.iloc[idx].values[2]) == 0.0):
                if not check_header(list_, idx):
                    if all(fuzz.partial_token_set_ratio(each.lower(), c.lower()) <= 85 for c in income_statement_IS["total_exclusion"]) and all(fuzz.partial_token_set_ratio(each.lower(), c.lower()) <= 85 for c in income_statement_IS["attribute_exclusion"]) and not signage_list[idx] is 'H' and not 'income' in each and not 'capital' in each and not 'internet' in each:
                        break_lineitem = each.split(" ")
                        # print(break_lineitem, 'break_lineitem #######')
                        for word in break_lineitem:
                            for c in corpus:
                                if fuzz.token_sort_ratio(word.lower(), c.lower()) >= 85 or any(ind in break_lineitem for ind in ['od','cc','bd']):
                                    print(word.lower(), c.lower(), fuzz.token_sort_ratio(word.lower(), c.lower()))
                                    if not signage is -1:
                                        level.append(list_2.index(each)+signage)
                                    else:
                                        level.append(list_2.index(each))
                    
        level=list(set(level))
        level.sort()

        return level
    
def cogs(list_ : list) -> list:

    global signage, type_,l3, exp_head

    if not isinstance(list_, list) :
        raise TypeError

    else:
        level=[]

        df = pd.DataFrame(list_)
        list_2 = df['particular'].to_list()

        signage_list = df['Label Signage'].to_list()
        corpus = income_statement_IS["cogs"]

        for idx, each in enumerate(list_2):
            for c in corpus:
                # if not (max(df.iloc[idx].values[1], df.iloc[idx].values[2]) == 0.0 and min(df.iloc[idx].values[1], df.iloc[idx].values[2]) == 0.0):
                if not check_header(list_, idx):
                    # print(each.lower(), c.lower(), '----->',fuzz.token_set_ratio(roman_number(each.lower()), c.lower()))
                    if fuzz.token_set_ratio(roman_number(each.lower()), c.lower()) >= 85 and all(fuzz.partial_token_set_ratio(each.lower(), c.lower()) <= 85 for c in income_statement_IS["total_exclusion"]) and not signage_list[idx] is 'H' and not 'indirect' in each:
                        # print(each.lower(), c.lower(), '----->',fuzz.token_set_ratio(roman_number(each.lower()), c.lower()), idx)
                        # level.append(list_2.index(each))
                        level.append(idx)

        if not level:
            for each in list_2:
                # if not (max(df.iloc[idx].values[1], df.iloc[idx].values[2]) == 0.0 and min(df.iloc[idx].values[1], df.iloc[idx].values[2]) == 0.0):
                if not check_header(list_, idx):
                    for c in corpus:
                        if fuzz.partial_token_set_ratio(roman_number(each.lower()), 'purchase') >= 85:
                            level.append(list_2.index(each))


        if not level:
            print(list_2)
            exp_header = process.extractOne("expenses", {v: k for v, k in enumerate(list_2)}, scorer=fuzz.token_set_ratio)
            emp_ben = employee_cost(list_)
            if exp_header[1] >= 85:
                start = exp_header[2]
                if emp_ben:
                    end = emp_ben[0]
                    for c in range(start, end):
                        level.append(c)
                   
        level=list(set(level))
        level.sort()

        if type_ in 'T-form_Tally' and signage and level:
            temp = [each for each in level if each >= signage] 
            level = temp

        if exp_head:
            level = [each for each in level if each > exp_head[0]]

        return level
    
def KM_1(list_ : list) -> list:

    if not isinstance(list_, list) :
        raise TypeError

    else:
        level=[]
        final_level=[]

        list_2=pd.DataFrame(list_)['particular'].to_list()
        signage_list = pd.DataFrame(list_)['Label Signage'].to_list()
        corpus=income_statement_IS["KM_1"]

        for idx, each in enumerate(list_2):
            for c in corpus:
                if fuzz.token_sort_ratio(roman_number(each.lower()), c.lower()) >= 85 and not signage_list[idx] is 'H':
                    level.append(list_2.index(each))

        level=list(set(level))
        level.sort()
        return level
    
def KM_2(list_ : list) -> list:

    if not isinstance(list_, list) :
        raise TypeError

    else:
        level=[]
        final_level=[]
        list_2=pd.DataFrame(list_)['particular'].to_list()
        signage_list = pd.DataFrame(list_)['Label Signage'].to_list()
        corpus=income_statement_IS["KM_2"]

        for idx, each in enumerate(list_2):
            for c in corpus:
                if fuzz.token_sort_ratio(roman_number(each.lower()), c.lower()) >= 85 and not signage_list[idx] is 'H':
                    level.append(list_2.index(each))

        level=list(set(level))
        level.sort()
        return level

def KM_3(list_ : list) -> list:

    if not isinstance(list_, list) :
        raise TypeError

    else:
        level=[]
        final_level=[]
        list_2=pd.DataFrame(list_)['particular'].to_list()
        signage_list = pd.DataFrame(list_)['Label Signage'].to_list()
        corpus=income_statement_IS["KM_3"]

        for idx, each in enumerate(list_2):
            for c in corpus:
                if fuzz.token_sort_ratio(roman_number(each.lower()), c.lower()) >= 85 and not signage_list[idx] is 'H':
                    level.append(list_2.index(each))
                    break
            else:
                continue  
            break

        level=list(set(level))
        level.sort()
        return level

def find_tax_expense(list_ : list) -> list:

    if not isinstance(list_, list) :
        raise TypeError

    else:
        level=[]
        final_level=[]
        list_2=pd.DataFrame(list_)['particular'].to_list()

        corpus=income_statement_IS["KM_4_fallback"]

        for idx, each in enumerate(list_2):
            for c in corpus:
                if fuzz.token_sort_ratio(roman_number(each.lower()), c.lower()) >= 85:
                    level.append(list_2.index(each))

        level=list(set(level))
        level.sort()
        return level
    
def KM_4(list_ : list) -> list:

    if not isinstance(list_, list) :
        raise TypeError

    else:
        level=[]
        final_level=[]
        list_2=pd.DataFrame(list_)['particular'].to_list()
        signage_list = pd.DataFrame(list_)['Label Signage'].to_list()
        corpus=income_statement_IS["KM_4"]

        for idx, each in enumerate(list_2):
            for c in corpus:
                # print(each, c, '---->', fuzz.token_sort_ratio(roman_number(each.lower()), c.lower()))
                if fuzz.token_sort_ratio(roman_number(each.lower()), c.lower()) >= 85 and not signage_list[idx] is 'H':
                    level.append(list_2.index(each))
                    break
            else:
                continue  
            break

        if not level:
            index = find_tax_expense(list_)
            if index:
                return [index[0]-1]

        level=list(set(level))
        level.sort()
        return level
    
def KM_5(list_ : list) -> list:

    if not isinstance(list_, list) :
        raise TypeError

    else:
        level=[]
    
        # limit = 0
        # if signage != -1:
        #     limit = -signage 

        # list_2=pd.DataFrame(list_[index:])['particular'].to_list()
        list_2=pd.DataFrame(list_)['particular'].to_list()
        # signage_list = pd.DataFrame(list_[index:])['Label Signage'].to_list()
        signage_list = pd.DataFrame(list_)['Label Signage'].to_list()
        corpus=income_statement_IS["KM_5"]

        for idx, each in enumerate(list_2):
            for c in corpus:
                if fuzz.token_sort_ratio(each.lower(), c.lower()) >= 85 and not signage_list[idx] is 'H' and not signage_list[idx] is 'BY':
                    # level.append(list_2.index(each)+index)
                    level.append(list_2.index(each))
                    break
            else:
                continue  
            break

        if not level:
            print('-----------------KM_5 not found...Executing fallback---------------------')
            corpus=income_statement_IS['KM_5_fallback']

            for idx, each in enumerate(list_2):
                if all(fuzz.partial_token_set_ratio(each.lower(), c.lower()) <= 85 for c in income_statement_IS["total_exclusion"]) and all(fuzz.partial_token_set_ratio(each.lower(), c.lower()) <= 85 for c in income_statement_IS["attribute_exclusion"]) and not signage_list[idx] is 'H' and not signage_list[idx] is 'BY':
                    break_lineitem = each.split(" ")
   
                    for word in break_lineitem:
                        for c in corpus:
                            if fuzz.token_sort_ratio(word.lower(), c.lower()) >= 85:
                                print(word.lower(), '-->', c.lower(), fuzz.token_sort_ratio(word.lower(), c.lower()))
                                # return [idx+index]
                                return [idx]

        level=list(set(level))
        level.sort()
        return level

def check_header(list_:list, idx:int)->bool:

    global year_count

    df_ = pd.DataFrame(list_)

    if year_count == 2 and [df_.iloc[idx].values[1], df_.iloc[idx].values[2]].count(0.0) == 2:
        return True
    elif year_count == 1 and [df_.iloc[idx].values[1]].count(0.0) == 1:
        return True
    elif year_count == 3 and [df_.iloc[idx].values[1], df_.iloc[idx].values[2], df_.iloc[idx].values[3]].count(0.0) == 3:
        return True

    return False

def find_revenue_header(list_ : list) -> list:

    if not isinstance(list_, list) :
        raise TypeError

    else:
        level=[]
        final_level=[]
        list_2=pd.DataFrame(list_)['particular'].to_list()
        corpus=income_statement_IS["revenue_header"]
        for idx,each in enumerate(list_2):
            for c in corpus:
                if fuzz.token_sort_ratio(roman_number(each.lower()), c.lower()) >= 85:
                    # if pd.DataFrame(list_).iloc[idx].values[1] == 0.0 and pd.DataFrame(list_).iloc[idx].values[2] == 0.0:
                    if check_header(list_, idx):
                        level.append(list_2.index(each))
                    
        level=list(set(level))
        level.sort()
        return level
    
def find_expense_header(list_ : list) -> list:

    if not isinstance(list_, list) :
        raise TypeError

    else:
        level=[]
        final_level=[]
        list_2=pd.DataFrame(list_)['particular'].to_list()
        corpus=income_statement_IS["expense_header"]
        for idx,each in enumerate(list_2):
            for c in corpus:
                if fuzz.token_sort_ratio(roman_number(each.lower()), c.lower()) >= 85:
                    # if pd.DataFrame(list_).iloc[idx].values[1] == 0.0 and pd.DataFrame(list_).iloc[idx].values[2] == 0.0:
                    if check_header(list_, idx):
                        level.append(list_2.index(each))


        if not level:
            for idx,each in enumerate(list_2):
                if fuzz.token_sort_ratio(roman_number(each.lower()), 'total revenue') >= 85:
                    level.append(list_2.index(each)+1)
                    break

        level=list(set(level))
        level.sort()
        return level

def check_revenue_line_item(item):
    corpus=income_statement_IS["revenue_line_item"]
    for c in corpus:
        if fuzz.partial_token_set_ratio(item.lower(), c.lower()) >= 85:
            return True
    return False

def check_cost_line_item(list_ : list) -> list:

    if not isinstance(list_, list) :
        raise TypeError

    else:
        level=[]
        final_level=[]
        list_2=pd.DataFrame(list_)['particular'].to_list()
        corpus=income_statement_IS["cost_line_item"]
        for idx,each in enumerate(list_2):
            for c in corpus:
                if fuzz.partial_token_set_ratio(roman_number(each.lower()), c.lower()) >= 85:
                    try:
                        # if not (max(pd.DataFrame(list_).iloc[idx].values[1], pd.DataFrame(list_).iloc[idx].values[2]) == 0.0 and min(pd.DataFrame(list_).iloc[idx].values[1], pd.DataFrame(list_).iloc[idx].values[2]) == 0.0):
                        if not check_header(list_, idx):
                            level.append(list_2.index(each))
                    except:
                        level.append(list_2.index(each))
                    
        level=list(set(level))
        level.sort()
        return level

def check_depreciation(list_ : list) -> list:

    if not isinstance(list_, list) :
        raise TypeError

    else:
        dep_index = []
        level=[]
        final_level=[]

        list_2=pd.DataFrame(list_)['particular'].to_list()
        signage_list = pd.DataFrame(list_)['Label Signage'].to_list()
        corpus=income_statement_IS["depreciation"]

        for idx, each in enumerate(list_2):
            for c in corpus:
                if fuzz.partial_token_set_ratio(each.lower(), c.lower()) >= 85 and all(fuzz.partial_token_set_ratio(each.lower(), c.lower()) <= 85 for c in income_statement_IS["total_exclusion"]) and not signage_list[idx] is 'H' and all(fuzz.partial_token_set_ratio(each.lower(), c.lower()) <= 85 for c in income_statement_IS["attribute_exclusion"]):
                    level.append(list_2.index(each))
                    dep_index.append(idx)

        level=list(set(level))
        level.sort()
        return level

def year_count_(dict_:dict)->int:
    ''' Return the number of year present in extraction json'''

    name = ' '.join(list(dict_.keys()))

    m = re.findall("(Year[0-9] Value)", name)
    return len(m)

def convert_income_statement(dict_:dict)-> list:
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
    global type_, year_count
    income_statement=[]
    

    for idx, Is in enumerate(dict_ ["Data"]["Financial Tables"][1]["Income Statement"]):

        income_statement.append({"particular":Is["Label Name"]})

        z = [income_statement[idx].update({Is["Year"+str(yc+1)]: normalize(Is["Year"+str(yc+1)+" Value"])}) for yc in range(year_count)]

        if type_ in 'Schedule-III':
            income_statement[idx].update( {"Label Signage": positive_negative_sign([Is["Year"+str(yc+1)+" Value"] for yc in range(year_count)] ) })
        else:
            income_statement[idx].update({"Label Signage": ToBy(Is["Label Name"])})

        income_statement[idx].update({"inner_outer": Is["meta_year1"]})
        income_statement[idx].update({"id": idx})

    return income_statement 



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


def ToBy(item: str):
    if item.lower().startswith("to"):
        return 'TO'
    elif item.lower().startswith("by"):
        return 'BY'
    else:
        return None


def find_first_signage(list_):

    df = pd.DataFrame(list_)

    if type_ in 'Schedule-III':

        df = df[df["Label Signage"] != "H"]
        df =  df[df["Label Signage"] != "E"]

        list__ = list(df.T.to_dict().values())

        for idx in range(0,len(list__)-1):
            if not list__[idx]["Label Signage"] is "H" and not list__[idx+1]["Label Signage"] is "H":
                if list__[idx]["Label Signage"] != list__[idx+1]["Label Signage"]:
                    return list_.index(list__[idx+1])
    else:
        # df.fillna(value="H", inplace=True)
        df["Label Signage"].fillna(value="H", inplace=True)
        # print(list_)
        df = df[df["Label Signage"] != "H"]
    
        # list__ = list(df.T.to_dict().values())
        list__ = list(df.where(df.notnull(), None).T.to_dict().values())

        for idx in range(0,len(list__)-1):
            if not list__[idx]["Label Signage"] is "H" and not list__[idx+1]["Label Signage"] is "H":
                if list__[idx]["Label Signage"] != list__[idx+1]["Label Signage"]:
                    return list_.index(list__[idx+1])
    
    return -1
   
def classify_revenue(list_ : list, graph_output:list) -> None:

    global l1,l2,l3,l4,exp_head,signage,cost,km1,km2,km3,km4,km5,classfi_format, global_df,type_, rev_idx, dep_index,operating_idx,nonoperating_idx

    if not isinstance(list_, list) :
        raise TypeError

    else:

        # if type_ in 'Schedule-III':

        key_metric = km1 + km2 + km3 + km4 + km5
        #Rule1
        if l1 and l2:

            print('----------Rule1---------------')
            if not signage is -1:
                signage_=[signage]
            else:
                signage_=[]

            lower_index= min(min(l1+l2), min(exp_head + cost + signage_ , default=1000000000000000))
            print('index--------->', lower_index)

            for idx in range(0,lower_index):
                try:
                    # if not (max(pd.DataFrame(list_).iloc[idx].values[1], pd.DataFrame(list_).iloc[idx].values[2]) == 0.0 and min(pd.DataFrame(list_).iloc[idx].values[1], pd.DataFrame(list_).iloc[idx].values[2]) == 0.0):
                    if not check_header(list_, idx):
                        if all(fuzz.partial_token_set_ratio(pd.DataFrame(list_)['particular'].iloc[idx].lower(), c.lower()) <= 85 for c in income_statement_IS["total_exclusion"]) and idx not in key_metric and pd.DataFrame(list_)['particular'].iloc[idx].strip() is not '':
                            classfi_format['Revenue'].append(list_[idx])
                            global_df['Class'].iloc[idx] = 'Revenue'
                            rev_idx.append(idx)
                except:
                    if all(fuzz.partial_token_set_ratio(pd.DataFrame(list_)['particular'].iloc[idx].lower(), c.lower()) <= 85 for c in income_statement_IS["total_exclusion"]) and idx not in key_metric and pd.DataFrame(list_)['particular'].iloc[idx].strip() is not '':
                        classfi_format['Revenue'].append(list_[idx])
                        global_df['Class'].iloc[idx] = 'Revenue'
                        rev_idx.append(idx)
        #Rule2
        elif l1 or l2:

            print('----------Rule2---------------')
            if not signage is -1:
                signage_=[signage]
            else:
                signage_=[]

            if l1:
                valid_index = min(min(l1), min(exp_head + cost + signage_  , default=1000000000000000))
            else:
                valid_index = min(min(l2), min(exp_head + cost + signage_ , default=1000000000000000))

            print('index--------->', valid_index)
            for idx in range(0,valid_index):
                try:
                    # if check_revenue_line_item(pd.DataFrame(list_)['particular'].iloc[idx]) and not (max(pd.DataFrame(list_).iloc[idx].values[1], pd.DataFrame(list_).iloc[idx].values[2]) == 0.0 and min(pd.DataFrame(list_).iloc[idx].values[1], pd.DataFrame(list_).iloc[idx].values[2]) == 0.0):
                    if check_revenue_line_item(pd.DataFrame(list_)['particular'].iloc[idx]) and not check_header(list_, idx):
                        if all(fuzz.partial_token_set_ratio(pd.DataFrame(list_)['particular'].iloc[idx].lower(), c.lower()) <= 85 for c in income_statement_IS["total_exclusion"]) and idx not in key_metric and pd.DataFrame(list_)['particular'].iloc[idx].strip() is not '':
                            classfi_format['Revenue'].append(list_[idx])

                            global_df['Class'].iloc[idx] = 'Revenue'
                            rev_idx.append(idx)
                except:
                    if all(fuzz.partial_token_set_ratio(pd.DataFrame(list_)['particular'].iloc[idx].lower(), c.lower()) <= 85 for c in income_statement_IS["total_exclusion"]) and idx not in key_metric and pd.DataFrame(list_)['particular'].iloc[idx].strip() is not '':
                        classfi_format['Revenue'].append(list_[idx])
                        global_df['Class'].iloc[idx] = 'Revenue'
                        rev_idx.append(idx)
        #Rule3
        elif not l1 and not l2 and exp_head:
            print('----------Rule3---------------')
            valid_index = exp_head[0]

            print('index--------->', valid_index)
            for idx in range(0,valid_index):
                try:
                    # if check_revenue_line_item(pd.DataFrame(list_)['particular'].iloc[idx]) and not (max(pd.DataFrame(list_).iloc[idx].values[1], pd.DataFrame(list_).iloc[idx].values[2]) == 0.0 and min(pd.DataFrame(list_).iloc[idx].values[1], pd.DataFrame(list_).iloc[idx].values[2]) == 0.0):
                    if check_revenue_line_item(pd.DataFrame(list_)['particular'].iloc[idx]) and not check_header(list_, idx):
                        if all(fuzz.partial_token_set_ratio(pd.DataFrame(list_)['particular'].iloc[idx].lower(), c.lower()) <= 85 for c in income_statement_IS["total_exclusion"]) and idx not in key_metric and pd.DataFrame(list_)['particular'].iloc[idx].strip() is not '':
                            classfi_format['Revenue'].append(list_[idx])
                            global_df['Class'].iloc[idx] = 'Revenue'
                            rev_idx.append(idx)
                except:
                    if all(fuzz.partial_token_set_ratio(pd.DataFrame(list_)['particular'].iloc[idx].lower(), c.lower()) <= 85 for c in income_statement_IS["total_exclusion"]) and idx not in key_metric and pd.DataFrame(list_)['particular'].iloc[idx].strip() is not '':
                        classfi_format['Revenue'].append(list_[idx])
                        global_df['Class'].iloc[idx] = 'Revenue'
                        rev_idx.append(idx)

        #Rule4
        elif not l1 and not l2 and not exp_head and signage == -1:
            print('----------Rule4---------------')
            if cost:
                valid_index = cost[0]
            else:
                valid_index = 0

            print('index--------->', valid_index)
            for idx in range(0,valid_index):
                try:
                    # if check_revenue_line_item(pd.DataFrame(list_)['particular'].iloc[idx]) and not (max(pd.DataFrame(list_).iloc[idx].values[1], pd.DataFrame(list_).iloc[idx].values[2]) == 0.0 and min(pd.DataFrame(list_).iloc[idx].values[1], pd.DataFrame(list_).iloc[idx].values[2]) == 0.0):
                    if check_revenue_line_item(pd.DataFrame(list_)['particular'].iloc[idx]) and not check_header(list_, idx):
                        if all(fuzz.partial_token_set_ratio(pd.DataFrame(list_)['particular'].iloc[idx].lower(), c.lower()) <= 85 for c in income_statement_IS["total_exclusion"]) and idx not in key_metric and pd.DataFrame(list_)['particular'].iloc[idx].strip() is not '':
                            classfi_format['Revenue'].append(list_[idx])
                            global_df['Class'].iloc[idx] = 'Revenue'
                            rev_idx.append(idx)
                except:
                    if all(fuzz.partial_token_set_ratio(pd.DataFrame(list_)['particular'].iloc[idx].lower(), c.lower()) <= 85 for c in income_statement_IS["total_exclusion"]) and idx not in key_metric and pd.DataFrame(list_)['particular'].iloc[idx].strip() is not '':
                        classfi_format['Revenue'].append(list_[idx])
                        global_df['Class'].iloc[idx] = 'Revenue'
                        rev_idx.append(idx)

        #Rule5
        elif not l1 and not l2 and not exp_head and signage > 0:
            print('----------Rule5---------------')
            valid_index = signage

            print('index--------->', valid_index)
            for idx in range(0,valid_index):
                try:
                    # if check_revenue_line_item(pd.DataFrame(list_)['particular'].iloc[idx]) and not (max(pd.DataFrame(list_).iloc[idx].values[1], pd.DataFrame(list_).iloc[idx].values[2]) == 0.0 and min(pd.DataFrame(list_).iloc[idx].values[1], pd.DataFrame(list_).iloc[idx].values[2]) == 0.0):
                    if check_revenue_line_item(pd.DataFrame(list_)['particular'].iloc[idx]) and not check_header(list_, idx):
                        if all(fuzz.partial_token_set_ratio(pd.DataFrame(list_)['particular'].iloc[idx].lower(), c.lower()) <= 85 for c in income_statement_IS["total_exclusion"]) and idx not in key_metric and pd.DataFrame(list_)['particular'].iloc[idx].strip() is not '':
                            classfi_format['Revenue'].append(list_[idx])
                            global_df['Class'].iloc[idx] = 'Revenue'
                            rev_idx.append(idx)
                except:
                    if all(fuzz.partial_token_set_ratio(pd.DataFrame(list_)['particular'].iloc[idx].lower(), c.lower()) <= 85 for c in income_statement_IS["total_exclusion"]) and idx not in key_metric and pd.DataFrame(list_)['particular'].iloc[idx].strip() is not '':
                        classfi_format['Revenue'].append(list_[idx])
                        global_df['Class'].iloc[idx] = 'Revenue'
                        rev_idx.append(idx)


        print('\n\nChecking by graph again.................!!!!!!!')

        rev_index = [each15[1] for each15 in graph_output if '.' in list(each15)[2][0] and int(list(each15)[2][0].replace(list(each15)[2][0][list(each15)[2][0].find('.'):],'').replace('Level','')) < 3 and int(list(each15)[2][0].replace(list(each15)[2][0][list(each15)[2][0].find('.'):],'').replace('Level','')) != 2]
        exclusion_index = l1+l2+l3+l4+dep_index+km1+km2+km3+km4+km5+operating_idx+nonoperating_idx+rev_idx
        print("rev_index:::", rev_index)
        print("exclusion_index:::", exclusion_index)

        if rev_index:
            for ri_ in rev_index:
                if not ri_ in exclusion_index:

                    print("ADDING:::", list_[ri_]['particular'])
                    classfi_format['Revenue'].append(list_[ri_])
                    global_df['Class'].iloc[ri_] = 'Revenue'
                    rev_idx.append(ri_)
        print('\n\n')

def classify_revenue_T(list_ : list) -> None:

    global l1,l2,l3,l4,exp_head,signage,cost,km1,km2,km3,km4,km5,classfi_format, global_df,type_, rev_idx, by_grosss_proft_index

    if not isinstance(list_, list) :
        raise TypeError

    else:


        print('----------Rule1---------------')
        print(by_grosss_proft_index, '&&&&&&&&&&&&&&&&&&')
        if by_grosss_proft_index:
            valid_index = by_grosss_proft_index[0]
        elif l1:
            valid_index = l1[0]
        elif not signage is -1:
            valid_index = signage
        elif km1:
            valid_index = km1[0]
        elif km5:
            valid_index = km5[0]
        else:
            valid_index = 0
            

        print('index--------->', valid_index)
        for idx in range(0,valid_index):

            try:
                # if not (max(pd.DataFrame(list_).iloc[idx].values[1], pd.DataFrame(list_).iloc[idx].values[2]) == 0.0 and min(pd.DataFrame(list_).iloc[idx].values[1], pd.DataFrame(list_).iloc[idx].values[2]) == 0.0):
                if not check_header(list_, idx):
                    if all(fuzz.partial_token_set_ratio(pd.DataFrame(list_)['particular'].iloc[idx].lower(), c.lower()) <= 85 for c in income_statement_IS["total_exclusion"]) and pd.DataFrame(list_)['particular'].iloc[idx].strip() is not '' and pd.DataFrame(list_)['Label Signage'].iloc[idx] is 'BY':
                        classfi_format['Revenue'].append(list_[idx])

                        global_df['Class'].iloc[idx] = 'Revenue'
                        rev_idx.append(idx)
            except:
                if all(fuzz.partial_token_set_ratio(pd.DataFrame(list_)['particular'].iloc[idx].lower(), c.lower()) <= 85 for c in income_statement_IS["total_exclusion"]) and pd.DataFrame(list_)['particular'].iloc[idx].strip() is not '' and pd.DataFrame(list_)['Label Signage'].iloc[idx] is 'BY':
                    classfi_format['Revenue'].append(list_[idx])
                    global_df['Class'].iloc[idx] = 'Revenue'
                    rev_idx.append(idx)


def classify_cogs(list_ : list, graph_output:list) -> None:

    global l1,l2,l3,l4,exp_head,signage,cost,km1,km2,km3,km4,km5,classfi_format,global_df, rev_idx, dep_index, operating_idx, nonoperating_idx

    if not isinstance(list_, list) :
        raise TypeError

    else:

        #Rule1
        l2_ = copy.deepcopy(l2)
        level1 = [each2[1] for each2 in graph_output if '.' in  list(each2)[2][0] and list(each2)[2][0].replace(list(each2)[2][0][list(each2)[2][0].find('.'):],'') == 'Level1']
        level3 = [each3[1] for each3 in graph_output if '.' in  list(each3)[2][0] and list(each3)[2][0].replace(list(each3)[2][0][list(each3)[2][0].find('.'):],'') == 'Level3']
        print("level1:::",level1, "level3:::",level3)
        if level1:
            level1 = [level1[-1]+1]
        if level3:
             level3 = [level3[-1]+1]

        if level1 or level3:
            l2_= max(l2, level1, level3)

        except_index = [each2_[1] for each2_ in graph_output if '.' in  list(each2_)[2][0] and (list(each2_)[2][0].replace(list(each2_)[2][0][list(each2_)[2][0].find('.'):],'').replace('Level','') >= str(6) or list(each2_)[2][0].replace(list(each2_)[2][0][list(each2_)[2][0].find('.'):],'').replace('Level','') == str(3))] 
        print("EXCEPT INDEX:::", except_index)

        km1__ = 10000000
        if km1:
            km1__ = km1[0]

        key_metric = km1 + km2 + km3 + km4 + km5
        if l1 and l2_ and l3:
            if l1[0] < l2_[0]:
                # if l3[0] > l2_[0]:
                try:
                    print('emp cost value: ',pd.DataFrame(list_).iloc[l3[0]].values[1] , 'cogs value: ',pd.DataFrame(list_).iloc[:,1][l2_[0]:l3[0]].max())
                    # if pd.DataFrame(list_).iloc[l3[0]].values[1] > pd.DataFrame(list_).iloc[l2_[0]].values[1]:
                    if pd.DataFrame(list_).iloc[l3[0]].values[1] > pd.DataFrame(list_).iloc[:,1][l2_[0]:l3[0]].max():
                        
                        # end_index = l3[0]
                        end_index = l3[0]+1
                        # l2_.append(end_index-2)

                    else:
                        # end_index = l3[0]-1
                        end_index = l3[0]
                        print('-----------------------else------------------------',l3)
                        # l2_.append(end_index-1)
                except:
                    print('Exception ocuured .... wrong extraction')
                    end_index = l3[0]
                
                start_index = l2_[0]

                print('----------------Rule1-----------------')
                print('start_index, end_index-->', start_index, end_index-1)
                for idx in range(start_index, end_index):
                    try:
                        # if not (max(pd.DataFrame(list_).iloc[idx].values[1], pd.DataFrame(list_).iloc[idx].values[2]) == 0.0 and min(pd.DataFrame(list_).iloc[idx].values[1], pd.DataFrame(list_).iloc[idx].values[2]) == 0.0):
                        if not check_header(list_, idx) and not idx in except_index:
                            if all(fuzz.partial_token_set_ratio(pd.DataFrame(list_)['particular'].iloc[idx].lower(), c.lower()) <= 85 for c in income_statement_IS["total_exclusion"]) and idx not in key_metric and pd.DataFrame(list_)['particular'].iloc[idx].strip() is not '':
                                classfi_format['Cost of goods sold / Cost of Sales'].append(list_[idx])
                                global_df['Class'].iloc[idx] = 'Cost of goods sold / Cost of Sales'
                                l2.append(idx)
                    except:
                        if all(fuzz.partial_token_set_ratio(pd.DataFrame(list_)['particular'].iloc[idx].lower(), c.lower()) <= 85 for c in income_statement_IS["total_exclusion"]) and idx not in key_metric and pd.DataFrame(list_)['particular'].iloc[idx].strip() is not '' and not idx in except_index:
                            classfi_format['Cost of goods sold / Cost of Sales'].append(list_[idx])
                            global_df['Class'].iloc[idx] = 'Cost of goods sold / Cost of Sales'
                            l2.append(idx)

            else:
                print('----------------Rule1-----------------')
                print('cogs_index-->', l2_)

                if l3:
                    if pd.DataFrame(list_).iloc[l3[0]].values[1] > pd.DataFrame(list_).iloc[:,1][l2_[0]:l3[0]].max():
                        classfi_format['Cost of goods sold / Cost of Sales'].append(list_[l3[0]])
                        global_df['Class'].iloc[l3[0]] = 'Cost of goods sold / Cost of Sales'

                for idx in l2_:
                    # if not (max(pd.DataFrame(list_).iloc[idx].values[1], pd.DataFrame(list_).iloc[idx].values[2]) == 0.0 and min(pd.DataFrame(list_).iloc[idx].values[1], pd.DataFrame(list_).iloc[idx].values[2]) == 0.0):
                    if all(fuzz.partial_token_set_ratio(pd.DataFrame(list_)['particular'].iloc[idx].lower(), c.lower()) <= 85 for c in income_statement_IS["total_exclusion"]) and pd.DataFrame(list_)['particular'].iloc[idx].strip() is not '' and idx < km1__ and not idx in except_index:
                        classfi_format['Cost of goods sold / Cost of Sales'].append(list_[idx])
                        global_df['Class'].iloc[idx] = 'Cost of goods sold / Cost of Sales'
                        

        #Rule2
        elif l2_:
            # end_index = l2_[0]
            print('----------------Rule2-----------------')
            print('cogs_index-->', l2_)

            if l3:
                if pd.DataFrame(list_).iloc[l3[0]].values[1] > pd.DataFrame(list_).iloc[:,1][l2_[0]:l3[0]].max():
                    classfi_format['Cost of goods sold / Cost of Sales'].append(list_[l3[0]])
                    global_df['Class'].iloc[l3[0]] = 'Cost of goods sold / Cost of Sales'

            for idx in l2_:
                if all(fuzz.partial_token_set_ratio(pd.DataFrame(list_)['particular'].iloc[idx].lower(), c.lower()) <= 85 for c in income_statement_IS["total_exclusion"]) and pd.DataFrame(list_)['particular'].iloc[idx].strip() is not '' and not 'indirect' in pd.DataFrame(list_)['particular'].iloc[idx].lower() and idx < km1__ and not idx in except_index:
                    classfi_format['Cost of goods sold / Cost of Sales'].append(list_[idx])
                    global_df['Class'].iloc[idx] = 'Cost of goods sold / Cost of Sales'
        
        #Rule3
        elif l1 and l3 and not l2_ and not type_ in 'T-form_Tally':

            if not signage is -1:
                signage_=[signage]
            else:
                signage_=[]

            print(exp_head, signage_)
            start_index = min(exp_head + signage_)
            end_index = l3[0]
            print('----------------Rule3-----------------')
            print('start_index, end_index-->', start_index, end_index-1)

            for idx in range(start_index, end_index):
                try:
                    # if not (max(pd.DataFrame(list_).iloc[idx].values[1], pd.DataFrame(list_).iloc[idx].values[2]) == 0.0 and min(pd.DataFrame(list_).iloc[idx].values[1], pd.DataFrame(list_).iloc[idx].values[2]) == 0.0):
                    if not check_header(list_, idx) and not idx in except_index:
                        if all(fuzz.partial_token_set_ratio(pd.DataFrame(list_)['particular'].iloc[idx].lower(), c.lower()) <= 85 for c in income_statement_IS["total_exclusion"]) and idx not in key_metric and pd.DataFrame(list_)['particular'].iloc[idx].strip() is not '':
                            classfi_format['Cost of goods sold / Cost of Sales'].append(list_[idx])
                            global_df['Class'].iloc[idx] = 'Cost of goods sold / Cost of Sales'
                            l2.append(idx)
                except:
                    if all(fuzz.partial_token_set_ratio(pd.DataFrame(list_)['particular'].iloc[idx].lower(), c.lower()) <= 85 for c in income_statement_IS["total_exclusion"]) and idx not in key_metric and pd.DataFrame(list_)['particular'].iloc[idx].strip() is not '' and not idx in except_index:
                        classfi_format['Cost of goods sold / Cost of Sales'].append(list_[idx])
                        global_df['Class'].iloc[idx] = 'Cost of goods sold / Cost of Sales'
                        l2.append(idx)



        #Rule4
        elif km2 and not l2_:
            if not signage is -1:
                signage_=[signage]
            else:
                signage_=[]

            start_index = min(exp_head + cost + signage_ )
            end_index = km2[0]
            print('----------------Rule4-----------------')
            print('start_index, end_index-->', start_index, end_index-1)

           
            for idx in range(start_index, end_index):
                try:
                    # if not (max(pd.DataFrame(list_).iloc[idx].values[1], pd.DataFrame(list_).iloc[idx].values[2]) == 0.0 and min(pd.DataFrame(list_).iloc[idx].values[1], pd.DataFrame(list_).iloc[idx].values[2]) == 0.0):
                    if not check_header(list_, idx) and not idx in except_index:
                        if fuzz.partial_token_set_ratio(pd.DataFrame(list_)['particular'].iloc[idx].lower(), 'purchases') >= 85 and all(fuzz.partial_token_set_ratio(pd.DataFrame(list_)['particular'].iloc[idx].lower(), c.lower()) <= 85 for c in income_statement_IS["total_exclusion"]) and idx not in key_metric and pd.DataFrame(list_)['particular'].iloc[idx].strip() is not '':
                            classfi_format['Cost of goods sold / Cost of Sales'].append(list_[idx])
                            global_df['Class'].iloc[idx] = 'Cost of goods sold / Cost of Sales'
                            l2.append(idx)
                except:
                    pass

        #Rule5
        elif km3 and not l2_:
            if not signage is -1:
                signage_=[signage]
            else:
                signage_=[]

            start_index = min(exp_head + cost + signage_ )
            end_index = km3[0]
            print('----------------Rule5-----------------')
            print('start_index, end_index-->', start_index, end_index-1)

           
            for idx in range(start_index, end_index):
                try:
                    # if not (max(pd.DataFrame(list_).iloc[idx].values[1], pd.DataFrame(list_).iloc[idx].values[2]) == 0.0 and min(pd.DataFrame(list_).iloc[idx].values[1], pd.DataFrame(list_).iloc[idx].values[2]) == 0.0):
                    if not check_header(list_, idx) and not idx in except_index:
                        if fuzz.partial_token_set_ratio(pd.DataFrame(list_)['particular'].iloc[idx].lower(), 'purchases') >= 85 and all(fuzz.partial_token_set_ratio(pd.DataFrame(list_)['particular'].iloc[idx].lower(), c.lower()) <= 85 for c in income_statement_IS["total_exclusion"]) and idx not in key_metric and pd.DataFrame(list_)['particular'].iloc[idx].strip() is not '':
                            classfi_format['Cost of goods sold / Cost of Sales'].append(list_[idx])
                            global_df['Class'].iloc[idx] = 'Cost of goods sold / Cost of Sales'
                            l2.append(idx)
                except:
                    pass

        #Rule6
        elif km4 and not l2_:
            if not signage is -1:
                signage_=[signage]
            else:
                signage_=[]

            start_index = min(exp_head + cost + signage_ )
            end_index = km4[0]
            print('----------------Rule6-----------------')
            print('start_index, end_index-->', start_index, end_index-1)


            for idx in range(start_index, end_index):
                try:
                    # if not (max(pd.DataFrame(list_).iloc[idx].values[1], pd.DataFrame(list_).iloc[idx].values[2]) == 0.0 and min(pd.DataFrame(list_).iloc[idx].values[1], pd.DataFrame(list_).iloc[idx].values[2]) == 0.0):
                    if not check_header(list_, idx) and not idx in except_index:
                        if fuzz.partial_token_set_ratio(pd.DataFrame(list_)['particular'].iloc[idx].lower(), 'purchases') >= 85 and all(fuzz.partial_token_set_ratio(pd.DataFrame(list_)['particular'].iloc[idx].lower(), c.lower()) <= 85 for c in income_statement_IS["total_exclusion"]) and idx not in key_metric and pd.DataFrame(list_)['particular'].iloc[idx].strip() is not '':
                            classfi_format['Cost of goods sold / Cost of Sales'].append(list_[idx])
                            global_df['Class'].iloc[idx] = 'Cost of goods sold / Cost of Sales'
                            l2.append(idx)
                except:
                    pass


        print('\n\nChecking by graph again.................!!!!!!!')

        levels = [list(each2)[2][0] for each2 in graph_output]
        levels = [each15.replace(each15[each15.find('.'):],'').replace('Level','') if '.' in each15 else each15.replace('Level','') for each15 in levels]
        # ending_index = max(max([graph_output[i][1]] if v == '4' else [0] for i, v in enumerate(levels)), km1)[0]
        if km1:
            ending_index = km1[0]
        else:
            ending_index = max([graph_output[i][1]] if v == '4' else [0] for i, v in enumerate(levels))[0]

            if '7' in levels:
                ending_index = min(ending_index, graph_output[levels.index('7')][1])

        print("ending_index:::", ending_index)

        cogs_index_graph = [each2[1] for each2 in graph_output if '.' in  list(each2)[2][0] and int(list(each2)[2][0].replace(list(each2)[2][0][list(each2)[2][0].find('.'):],'').replace('Level','')) > 3 and each2[1] < ending_index] 
        print("cogs_index_graph:::", cogs_index_graph)
        exclusion_index = l1+l2+l3+l4+dep_index+km1+km2+km3+km4+km5+operating_idx+nonoperating_idx+rev_idx
        print("exclusion_index:::", exclusion_index)

        if cogs_index_graph:

            for cg_ in cogs_index_graph:
                if not cg_ in exclusion_index:

                    print("ADDING:::", list_[cg_]['particular'])
                    classfi_format['Cost of goods sold / Cost of Sales'].append(list_[cg_])
                    global_df['Class'].iloc[cg_] = 'Cost of goods sold / Cost of Sales'
                    l2.append(cg_)

        print('\n\n')

def classify_operating_items(list_ : list, graph_output:list) -> None:

    global l1,l2,l3,l4,exp_head,signage,cost,km1,km2,km3,km4,km5,rev_idx,classfi_format,operating_items_end_index,dep,global_df, operating_idx, nonoperating_idx, dep_index

    if not isinstance(list_, list) :
        raise TypeError

    else:
        key_metric = km1 + km2 + km3 + km4 + km5
        #Rule1
        start_index = -1
        end_index = -1

        if l2:
            start_index = l2[-1]+1
        elif exp_head:
            start_index =exp_head[0]+1
        elif cost:
            start_index = cost[0]
        elif signage:
            start_index = signage[0]

        if l1:
            if l1[0] < start_index:
                classfi_format['Non-operating or Other Income / Expenses'].append(list_[l1[0]])
                global_df['Class'].iloc[l1[0]] = 'Non-operating or Other Income / Expenses'

        if km2:
            end_index = km2[-1]
        elif km3:
            end_index = km3[-1]
        elif l4:
            end_index = l4[0]
        elif km4:
            end_index = km4[-1]

        elif km5:
            end_index = km5[-1]

        print('classify_operating_items:::::: start_index, end_index:', start_index, end_index-1)
        if not start_index is -1 and not end_index is -1 and start_index < end_index:
            print('---------------------Rule1--------------------------------')
            print('start_index, end_index:', start_index, end_index-1)

            for idx in range(start_index, end_index):
                try:
                    # if not (max(pd.DataFrame(list_).iloc[idx].values[1], pd.DataFrame(list_).iloc[idx].values[2]) == 0.0 and min(pd.DataFrame(list_).iloc[idx].values[1], pd.DataFrame(list_).iloc[idx].values[2]) == 0.0):
                    if not check_header(list_, idx):

                        if all(fuzz.partial_token_set_ratio(pd.DataFrame(list_)['particular'].iloc[idx].lower(), c.lower()) <= 85 for c in income_statement_IS["total_exclusion"]) and idx not in key_metric and pd.DataFrame(list_)['particular'].iloc[idx].strip() is not '' and global_df['Class'].iloc[idx] is '':
                           
                            if operating_expense_exclusion(pd.DataFrame(list_)['particular'].iloc[idx], idx):
                                classfi_format['Non-operating or Other Income / Expenses'].append(list_[idx])
                                global_df['Class'].iloc[idx] = 'Non-operating or Other Income / Expenses'
                                nonoperating_idx.append(idx)
                            else:        
                                classfi_format['Operating expenses'].append(list_[idx])
                                global_df['Class'].iloc[idx] = 'Operating expenses'
                                operating_idx.append(idx)
                            
                except:
                    if all(fuzz.partial_token_set_ratio(pd.DataFrame(list_)['particular'].iloc[idx].lower(), c.lower()) <= 85 for c in income_statement_IS["total_exclusion"]) and idx not in key_metric and pd.DataFrame(list_)['particular'].iloc[idx].strip() is not '' and global_df['Class'].iloc[idx] is '':
                    
                        if operating_expense_exclusion(pd.DataFrame(list_)['particular'].iloc[idx], idx):
                            classfi_format['Non-operating or Other Income / Expenses'].append(list_[idx])
                            global_df['Class'].iloc[idx] = 'Non-operating or Other Income / Expenses'
                            nonoperating_idx.append(idx)
                        else:        
                            classfi_format['Operating expenses'].append(list_[idx])
                            global_df['Class'].iloc[idx] = 'Operating expenses'
                            operating_idx.append(idx)
                       
        else:
            print('---------------------NULL-------------------------------')
            if start_index <= end_index:
                if km4:
                    end_index = km4[0]
                    print('---------------Excuting Fallback------------------')
                    print('start_index, end_index:', start_index, end_index)
                    for idx in range(start_index, end_index):
                        try:
                            # if not (max(pd.DataFrame(list_).iloc[idx].values[1], pd.DataFrame(list_).iloc[idx].values[2]) == 0.0 and min(pd.DataFrame(list_).iloc[idx].values[1], pd.DataFrame(list_).iloc[idx].values[2]) == 0.0):
                            if not check_header(list_, idx):

                                if all(fuzz.partial_token_set_ratio(pd.DataFrame(list_)['particular'].iloc[idx].lower(), c.lower()) <= 85 for c in income_statement_IS["total_exclusion"]) and idx not in key_metric and pd.DataFrame(list_)['particular'].iloc[idx].strip() is not '' and global_df['Class'].iloc[idx] is '':
                                   
                                    if any(fuzz.partial_token_set_ratio(pd.DataFrame(list_)['particular'].iloc[idx].lower(), c.lower()) >= 85 for c in income_statement_IS["operating_expense_fallback"]):       
                                        classfi_format['Operating expenses'].append(list_[idx])
                                        global_df['Class'].iloc[idx] = 'Operating expenses'
                                        operating_idx.append(idx)
                                    
                        except:
                            if all(fuzz.partial_token_set_ratio(pd.DataFrame(list_)['particular'].iloc[idx].lower(), c.lower()) <= 85 for c in income_statement_IS["total_exclusion"]) and idx not in key_metric and pd.DataFrame(list_)['particular'].iloc[idx].strip() is not '' and global_df['Class'].iloc[idx] is '':
                            
                                if any(fuzz.partial_token_set_ratio(pd.DataFrame(list_)['particular'].iloc[idx].lower(), c.lower()) >= 85 for c in income_statement_IS["operating_expense_fallback"]):      
                                    classfi_format['Operating expenses'].append(list_[idx])
                                    global_df['Class'].iloc[idx] = 'Operating expenses'
                                    operating_idx.append(idx)                    


        operating_items_end_index = end_index

        print('\n\nChecking by graph again.................!!!!!!!')
        levels = [list(each2)[2][0] for each2 in graph_output]
        levels = [each15.replace(each15[each15.find('.'):],'').replace('Level','') if '.' in each15 else each15.replace('Level','') for each15 in levels]
        starting_index = max(max([graph_output[i][1]] if v == '4' else [0] for i, v in enumerate(levels)), km1)[0]

        if '7' in levels:
            starting_index = min(starting_index, graph_output[levels.index('7')][1])

        print("starting_index:::", starting_index)

        op_index_graph = [each2[1] for each2 in graph_output if '.' in  list(each2)[2][0] and int(list(each2)[2][0].replace(list(each2)[2][0][list(each2)[2][0].find('.'):],'').replace('Level','')) < 6 and each2[1] > starting_index] 
        print("op_index_graph:::", op_index_graph)
        exclusion_index = l1+l2+l3+l4+dep_index+km1+km2+km3+km4+km5+operating_idx+nonoperating_idx+rev_idx
        print("exclusion_index:::", exclusion_index)

        if op_index_graph:

            for op_ in op_index_graph:
                if not op_ in exclusion_index:

                    print("ADDING:::", list_[op_]['particular'])
                    classfi_format['Operating expenses'].append(list_[op_])
                    global_df['Class'].iloc[op_] = 'Operating expenses'
                    operating_idx.append(op_)
        print('\n\n')

def operating_expense_exclusion(lineitem : str, idx: int) -> bool:

    global l1,l2,l3,l4,exp_head,signage,cost,km1,km2,km3,km4,km5,classfi_format,operating_items_end_index,dep

    if not isinstance(lineitem, str) :
        raise TypeError

    else:
        if l4:
            if idx == l4[0]:
                return True

        if km3:
            if idx >= km3[-1]:
                return True

        if l1:
            if idx == l1[0]:
                return True

        corpus = income_statement_IS['exclusion_operating_expenses']
        for c in corpus[:2]:
            if fuzz.token_sort_ratio(lineitem.lower(), c.lower()) >= 85:
                    return True

        if fuzz.token_sort_ratio(lineitem.lower(), corpus[2].lower()) >= 85 and fuzz.partial_token_set_ratio(lineitem.lower(), 'non') >= 85 :
                return True

        if km4:
            if idx > km4[0]:
                if fuzz.partial_token_set_ratio(lineitem.lower(), corpus[-1]) >= 85:
                    return True

        if fuzz.partial_token_set_ratio(lineitem.lower(), 'income') >= 85 and not fuzz.partial_token_set_ratio(lineitem.lower(), 'tax') >= 85:
            l1.append(idx)
            return True

        if (fuzz.partial_token_set_ratio(lineitem.lower(), 'interest') >= 85 or fuzz.partial_token_set_ratio(lineitem.lower(), 'capital') >= 85) and not idx in l4:
            return True

        if fuzz.partial_token_set_ratio(lineitem.lower(), 'indirect') >= 85 :
            return True

        if process.extractOne(lineitem.lower(), ['partner', 'director'], scorer=fuzz.partial_token_set_ratio)[1] >= 85:
            print(lineitem.lower(), '@@@@@@TRUE@@@@@@@@')
            return True

        return False


def classify_non_operating_items(list_ : list, graph_output:list) -> None:

    global l1,l2,l3,l4,exp_head,signage,cost,km1,km2,km3,km4,km5,rev_idx,classfi_format,operating_items_end_index,dep,global_df,exclude_tax_index, operating_idx, nonoperating_idx, dep_index

    if not isinstance(list_, list) :
        raise TypeError
    else:
        key_metric = km1 + km2 + km3 + km4 + km5
        if not operating_items_end_index is -1:
            start_index = operating_items_end_index
        else:
            start_index = []

        if km5:
            end_index = km5[-1]
        else:
            end_index = []

        if start_index and end_index:
            print('---------------------Rule1--------------------------------')
            print('start_index, end_index:', start_index, end_index-1)

            for idx in range(start_index, end_index):
                try:
                    # if not (max(pd.DataFrame(list_).iloc[idx].values[1], pd.DataFrame(list_).iloc[idx].values[2]) == 0.0 and min(pd.DataFrame(list_).iloc[idx].values[1], pd.DataFrame(list_).iloc[idx].values[2]) == 0.0):
                    if not check_header(list_, idx):
                        if all(fuzz.partial_token_set_ratio(pd.DataFrame(list_)['particular'].iloc[idx].lower(), c.lower()) <= 85 for c in income_statement_IS["total_exclusion"]) and idx not in key_metric and pd.DataFrame(list_)['particular'].iloc[idx].strip() is not '': 

                            if not idx in exclude_tax_index: 

                                if non_operating_expense_exclusion(idx):
                                    classfi_format['Operating expenses'].append(list_[idx])
                                    global_df['Class'].iloc[idx] = 'Operating expenses'
                                    operating_idx.append(idx)
                                else:
                                    classfi_format['Non-operating or Other Income / Expenses'].append(list_[idx])
                                    global_df['Class'].iloc[idx] = global_df['Class'].iloc[idx] + 'Non-operating or Other Income / Expenses'
                                    nonoperating_idx.append(idx)
                except:
                    if all(fuzz.partial_token_set_ratio(pd.DataFrame(list_)['particular'].iloc[idx].lower(), c.lower()) <= 85 for c in income_statement_IS["total_exclusion"]) and idx not in key_metric and pd.DataFrame(list_)['particular'].iloc[idx].strip() is not '':
                        
                        if not idx in exclude_tax_index: 

                            if non_operating_expense_exclusion(idx):
                                classfi_format['Operating expenses'].append(list_[idx])
                                global_df['Class'].iloc[idx] = 'Operating expenses'
                                operating_idx.append(idx)
                            else:
                                classfi_format['Non-operating or Other Income / Expenses'].append(list_[idx])
                                global_df['Class'].iloc[idx] = global_df['Class'].iloc[idx] + 'Non-operating or Other Income / Expenses'
                                nonoperating_idx.append(idx)
        else:
            print('---------------------NULL-------------------------------')
            print('start_index, end_index:', start_index, end_index)


        print('\n\nChecking by graph again.................!!!!!!!')
        end_index = min(km4+km5)
        print("end_inde:::", end_index)
        nonop_index_graph = [each2[1] for each2 in graph_output if '.' in  list(each2)[2][0] and int(list(each2)[2][0].replace(list(each2)[2][0][list(each2)[2][0].find('.'):],'').replace('Level','')) > 6 and each2[1] < end_index] 
        print("nonop_index_graph:::", nonop_index_graph)
        exclusion_index = l1+l2+l3+l4+dep_index+km1+km2+km3+km4+km5+operating_idx+nonoperating_idx+rev_idx
        print("exclusion_index:::", exclusion_index)

        if nonop_index_graph:

            for nop_ in nonop_index_graph:
                if not nop_ in exclusion_index:

                    print("ADDING:::", list_[nop_]['particular'])
                    classfi_format['Non-operating or Other Income / Expenses'].append(list_[nop_])
                    global_df['Class'].iloc[nop_] = global_df['Class'].iloc[nop_] + 'Non-operating or Other Income / Expenses'
                    nonoperating_idx.append(nop_)
        print('\n\n')

def non_operating_expense_exclusion(idx: int) -> bool:

    global l1,l2,l3,l4,exp_head,signage,cost,km1,km2,km3,km4,km5,classfi_format,operating_items_end_index,dep

    if not isinstance(idx, int) :
        raise TypeError

    else:
        if dep:
            if idx == dep[0]:
                return True

        return False

def classify_tax(list_ : list) -> None:

    global l1,l2,l3,l4,exp_head,signage,cost,km1,km2,km3,km4,km5,classfi_format,operating_items_end_index,dep,global_df,exclude_tax_index, tax_index
    temp = True

    if not isinstance(list_, list) :
        raise TypeError

    else:
        #Rule1
        start_index = -1
        end_index = -1

        if km4:
            start_index = km4[0]+1
        if km5:
            end_index = km5[0]

        print('start_index, end_index:', start_index, end_index)
        lineitem = pd.DataFrame(list_)['particular']

        index = find_tax_expense(list_)

        if not start_index is -1 and not end_index is -1:
            for idx in range(start_index, end_index):
                try:

                    # if not (max(pd.DataFrame(list_).iloc[idx].values[1], pd.DataFrame(list_).iloc[idx].values[2]) == 0.0 and min(pd.DataFrame(list_).iloc[idx].values[1], pd.DataFrame(list_).iloc[idx].values[2]) == 0.0):
                    if not check_header(list_, idx):
                        if any(fuzz.partial_token_set_ratio(lineitem.iloc[idx].lower(), c.lower()) >= 0 for c in income_statement_IS["inclusion_tax"]) and all(fuzz.partial_token_set_ratio(lineitem.iloc[idx].lower(), c.lower()) <= 85 for c in income_statement_IS["total_exclusion"]) and lineitem.iloc[idx].strip() is not '':

                            if not (fuzz.token_set_ratio(lineitem.iloc[idx], 'income') > 85 and ((fuzz.token_set_ratio(lineitem.iloc[idx], 'prior') > 85 or fuzz.token_set_ratio(lineitem.iloc[idx], 'earlier') > 85) and fuzz.token_set_ratio(lineitem.iloc[idx], 'period') > 85) and fuzz.token_set_ratio(lineitem.iloc[idx], 'tax') < 85):
                                if temp:    
                                    classfi_format['Tax'].append(list_[idx])
                                    global_df['Class'].iloc[idx] = global_df['Class'].iloc[idx] + '(Tax)--->'
                                    tax_index.append(idx)
                                else:
                                    '''Avoid classification for non operating'''
                                    exclude_tax_index.append(idx)
                                
                                '''If Tax expense is classified as Tax then discard all for classification upto KM5'''
                                if index:
                                    if index[0] == idx:
                                        temp = False

                except:

                    if any(fuzz.partial_token_set_ratio(lineitem.iloc[idx], c.lower()) >= 0 for c in income_statement_IS["inclusion_tax"]) and all(fuzz.partial_token_set_ratio(lineitem.iloc[idx], c.lower()) <= 85 for c in income_statement_IS["total_exclusion"]) and lineitem.iloc[idx].strip() is not '':
                        if not (fuzz.token_set_ratio(lineitem.iloc[idx], 'income') > 85 and ((fuzz.token_set_ratio(lineitem.iloc[idx], 'prior') > 85 or fuzz.token_set_ratio(lineitem.iloc[idx], 'earlier') > 85) and fuzz.token_set_ratio(lineitem.iloc[idx], 'period') > 85) and fuzz.token_set_ratio(lineitem.iloc[idx], 'tax') < 85):
                            
                            classfi_format['Tax'].append(list_[idx])
                            global_df['Class'].iloc[idx] = global_df['Class'].iloc[idx] + '-->(Tax)'
                            tax_index.append(idx)
                

def classify_expenses(list_ : list) -> None:

    global l1,l2,l3,l4,exp_head,signage,cost,km1,km2,km3,km4,km5,classfi_format, global_df,type_, operating_idx

    if not isinstance(list_, list) :
        raise TypeError

    else:
        if km1:
            idx = [each for each in range(0,km1[-1]+1)]
        else:
            idx = km1

        new_df = global_df.iloc[:min(km4+km5)]
        new_df = new_df.drop(idx + km2 + km3 + l1 + l3 +l4)
        new_df = new_df[new_df['Label Signage']=='TO']
        new_df = new_df[new_df['particular']!='']
        new_df = new_df[~new_df.particular.str.contains("total", na=False, flags=re.IGNORECASE)]
        # print(new_df.iloc[:,1].to_list())
        print(new_df)

        median_ = median(new_df.iloc[:,1].to_list())
        print('median-------------------->', median_)
        key_metric = km1 + km2 + km3 + km4 + km5 + l1

        if km1:
            start_index = km1[-1]
        elif signage:
            start_index = signage
        else:
            start_index = 0

        if km5:
            end_index = min(km4+km5)
        else:
            end_index = len(list_)

        for idx in range(start_index, end_index):

            try:
                # if not (max(pd.DataFrame(list_).iloc[idx].values[1], pd.DataFrame(list_).iloc[idx].values[2]) == 0.0 and min(pd.DataFrame(list_).iloc[idx].values[1], pd.DataFrame(list_).iloc[idx].values[2]) == 0.0):
                if not check_header(list_, idx):
                
                    if abs(int(round(pd.DataFrame(list_).iloc[idx].values[1]))) >= abs(int(round(median_))) and pd.DataFrame(list_)['Label Signage'].iloc[idx] is 'TO' and not global_df['particular'].iloc[idx] is '' and idx not in key_metric and all(fuzz.partial_token_set_ratio(pd.DataFrame(list_)['particular'].iloc[idx].lower(), c.lower()) <= 85 for c in income_statement_IS["total_exclusion"]):
                        
                        if global_df['Class'].iloc[idx] is '' or global_df['Class'].iloc[idx] in '(Tax)--->':

                            if operating_expense_exclusion(pd.DataFrame(list_)['particular'].iloc[idx], idx):
                                classfi_format['Non-operating or Other Income / Expenses'].append(list_[idx])
                                global_df['Class'].iloc[idx] = global_df['Class'].iloc[idx] + 'Non-operating or Other Income / Expenses'
                            else:
                                classfi_format['Operating expenses'].append(list_[idx])
                                global_df['Class'].iloc[idx] = 'Operating expenses'
                                operating_idx.append(idx)

                    elif abs(int(round(pd.DataFrame(list_).iloc[idx].values[1]))) < abs(int(round(median_))) and pd.DataFrame(list_)['Label Signage'].iloc[idx] is 'TO' and not global_df['particular'].iloc[idx] is '' and idx not in key_metric and all(fuzz.partial_token_set_ratio(pd.DataFrame(list_)['particular'].iloc[idx].lower(), c.lower()) <= 85 for c in income_statement_IS["total_exclusion"]):

                        if global_df['Class'].iloc[idx] is '' or global_df['Class'].iloc[idx] in '(Tax)--->':

                            if non_operating_expense_exclusion(idx):
                                classfi_format['Operating expenses'].append(list_[idx])
                                global_df['Class'].iloc[idx] = 'Operating expenses'
                                operating_idx.append(idx)

                            else:
                                classfi_format['Non-operating or Other Income / Expenses'].append(list_[idx])
                                global_df['Class'].iloc[idx] = global_df['Class'].iloc[idx] + 'Non-operating or Other Income / Expenses'
                                
                                if fuzz.partial_token_set_ratio(global_df['particular'].iloc[idx].lower(), 'income') >= 85 and not global_df['particular'].iloc[idx].lower() in [d['particular'] for d in classfi_format['Tax']] and fuzz.token_set_ratio('tax', global_df['particular'].iloc[idx].lower()) <= 85:
                                    l1.append(idx)
            except:
                print('----------------------------Exception occured------------------------------')
                pass


def replace_unclassified_cells(list_: list)-> None:

    global l1,l2,l3,l4,exp_head,signage,cost,km1,km2,km3,km4,km5,classfi_format, global_df,type_,exclude_tax_index
    if type_ in 'Schedule-III':
        if km5:

            for idx in range(0, km5[0]):

                if not global_df['Label Signage'].iloc[idx] is 'H' and not global_df['Class'].iloc[idx] is '':

                    if global_df['Class'].iloc[idx] is 'km':
                        element = ''
                    elif global_df['Class'].iloc[idx] is 'attribute':
                        element = 'attribute'
                    else:
                        element= global_df['Class'].iloc[idx]

                if global_df['Class'].iloc[idx] is '' and not global_df['Label Signage'].iloc[idx] is 'H' and all(fuzz.partial_token_set_ratio(global_df['particular'].iloc[idx].lower(), c.lower()) <= 85 for c in income_statement_IS["total_exclusion"]):

                    try:
                        if not global_df['particular'].iloc[idx] is '' and not idx in exclude_tax_index:
                            global_df['Class'].iloc[idx] = element
                            classfi_format[element].append(list_[idx])
                    except:
                        pass
    else:
        if km5:

            for idx in range(0, km5[0]):
                if not global_df['Label Signage'].iloc[idx] is None and not global_df['Class'].iloc[idx] is '':
                    
                    if global_df['Class'].iloc[idx] is 'km':
                        element = ''
                    elif global_df['Class'].iloc[idx] is 'attribute':
                        element = 'attribute'
                    else:
                        element= global_df['Class'].iloc[idx]


                if global_df['Class'].iloc[idx] is '' and not global_df['Label Signage'].iloc[idx] is None and all(fuzz.partial_token_set_ratio(global_df['particular'].iloc[idx].lower(), c.lower()) <= 85 for c in income_statement_IS["total_exclusion"]):
                    # if not (max(pd.DataFrame(list_).iloc[idx].values[1], pd.DataFrame(list_).iloc[idx].values[2]) == 0.0 and min(pd.DataFrame(list_).iloc[idx].values[1], pd.DataFrame(list_).iloc[idx].values[2]) == 0.0):
                    if not check_header(list_, idx):
                        try:
                            if not global_df['particular'].iloc[idx] is '':
                                global_df['Class'].iloc[idx] = element
                                classfi_format[element].append(list_[idx])
                        except:
                            pass




def second_phase(list_: list)-> None:
    global l1,l2,l3,l4,exp_head,signage,cost,km1,km2,km3,km4,km5,classfi_format, global_df,type_

    attribute = l1+l2+l3+l4
    km = km1+km2+km3+km4+km5

    print('attribute:', attribute)
    print('km:', km)

    for idx in attribute:
        if global_df['Class'].iloc[idx] is '':
            global_df['Class'].iloc[idx] = 'attribute'

    for idx in km:
        if global_df['Class'].iloc[idx] is '':
            global_df['Class'].iloc[idx] = 'km'

    replace_unclassified_cells(list_)


def remove_lineitem(list_ : list) -> list:
    global remove_item, by_grosss_proft_index

    if not isinstance(list_, list) :
        raise TypeError

    else:
        level=[]
        final_level=[]
        list_2=pd.DataFrame(list_)['particular'].to_list()
        corpus=income_statement_IS["lineitem_remove"]

        # for idx, each in enumerate(list_2):
        #   for c in corpus:
        #       # print(roman_number(each.lower()), '==',c.lower(),'-->',fuzz.token_sort_ratio(roman_number(each.lower()), c.lower()))
        #       if fuzz.token_sort_ratio(roman_number(each.lower()), c.lower()) >= 85:
        #           list_.pop(idx)
        #           remove_item.append(idx)
        #           break
        #   else:
        #       continue  
        #   break

        for idx, each in enumerate(list_2):
            for c in corpus:
                # print(roman_number(each.lower()), '==',c.lower(),'-->',fuzz.token_sort_ratio(roman_number(each.lower()), c.lower()))
                if fuzz.token_sort_ratio(roman_number(each.lower()), c.lower()) >= 85:
                    remove_item.append(idx)


        for idx in remove_item[::-1]:

            if fuzz.token_sort_ratio(roman_number(list_2[idx].lower()), 'by gross profit') >= 85:
                    by_grosss_proft_index.append(idx)

            list_.pop(idx)


        return list_  

def other_income_exclusion(list_ : list) -> None:

    global l1,l2,l3,l4,exp_head,signage,cost,km1,km2,km3,km4,km5,classfi_format, global_df,type_

    if not isinstance(list_, list) :
        raise TypeError

    else:
        level=[]
        list_2=pd.DataFrame(list_)['particular'].to_list()
        corpus=income_statement_IS["other_income_exclusion"]
        remove = -1

        for idx in l1:
            for c in corpus:
                if fuzz.token_set_ratio(list_2[idx], c.lower()) >= 85:
                    # list_.pop(idx)
                    remove = idx
                    print('------------idx------------', idx)
                    classfi_format['Cost of goods sold / Cost of Sales'].append(list_[idx])
                    global_df['Class'].iloc[idx] = 'Cost of goods sold / Cost of Sales'
                    break
            else:
                continue  
            break

        if not remove is -1:
            l1.remove(remove)

def revenue_exclusion(list_ : list) -> None:

    global l1,l2,l3,l4,exp_head,signage,cost,km1,km2,km3,km4,km5,classfi_format, global_df,type_, rev_idx

    if not isinstance(list_, list) :
        raise TypeError

    else:
        level=[]
        list_2=pd.DataFrame(list_)['particular'].to_list()
        corpus=income_statement_IS["revenue_exclusion"]
        remove = []

        for idx in rev_idx:
            for c in corpus:
                if fuzz.partial_token_set_ratio(list_2[idx], c.lower()) >= 85 and not 'job' in list_2[idx] and not 'sale' in list_2[idx]:
                    # list_.pop(idx)
                    remove.append(idx)
                    print('------------idx------------', idx)
                    classfi_format['Cost of goods sold / Cost of Sales'].append(list_[idx])
                    global_df['Class'].iloc[idx] = 'Cost of goods sold / Cost of Sales'

                    for each2 in rev_idx[rev_idx.index(idx)+1:]:
                        remove.append(each2)
                        print('------------idx------------', each2)
                        classfi_format['Cost of goods sold / Cost of Sales'].append(list_[each2])
                        global_df['Class'].iloc[each2] = 'Cost of goods sold / Cost of Sales'
                    break
        print(classfi_format['Revenue'])
        remove = list(set(remove))
        if remove:
            print(rev_idx, remove , "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            # temp = 0
            # for idx in remove:
            #   idx = idx - temp
            #   temp = 1
            #   classfi_format['Revenue'].pop(rev_idx.index(idx))
            for idx in remove[::-1]:
                classfi_format['Revenue'].pop(rev_idx.index(idx))
                rev_idx.remove(idx)

        print(rev_idx)

def cogs_exclusion(list_ : list) -> None:

    global l1,l2,l3,l4,exp_head,signage,cost,km1,km2,km3,km4,km5,classfi_format, global_df,type_, rev_idx

    if not isinstance(list_, list) :
        raise TypeError

    else:
        level=[]
        list_2=pd.DataFrame(list_)['particular'].to_list()
        corpus=income_statement_IS["cogs_exclusion"]
        remove = []

        for idx in list(set(l2)):
            for c in corpus:
                if fuzz.partial_token_set_ratio(list_2[idx], c.lower()) >= 85 and fuzz.partial_token_set_ratio(list_2[idx], 'cost') <= 85 and fuzz.partial_token_set_ratio(list_2[idx], 'excise') <= 85 and fuzz.partial_token_set_ratio(list_2[idx], 'inventories') <= 85:
                    # list_.pop(idx)
                    remove.append(idx)
                    print('------------idx------------', idx)
                    classfi_format['Revenue'].append(list_[idx])
                    global_df['Class'].iloc[idx] = 'Revenue'
                    break
        # print(classfi_format['Cost of goods sold / Cost of Sales'])
        if remove:
            print(l2, remove , "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            temp = 0
            for idx in remove:
                idx = idx - temp
                temp = 1
                if l2.index(idx) < len(classfi_format['Cost of goods sold / Cost of Sales']):
                    classfi_format['Cost of goods sold / Cost of Sales'].pop(l2.index(idx))

def cogs_null(list_ : list) -> None:

 

    '''If cogs are not classified then all employee cost will be classified as cogs '''

 

    global l1,l2,l3,l4,exp_head,signage,cost,km1,km2,km3,km4,km5,classfi_format, global_df,type_, operating_idx

 

    if not isinstance(list_, list) :
        raise TypeError

 

    else:
        level=[]
        remove = []
        list_2=pd.DataFrame(list_)['particular'].to_list()

 
        print(l3,l2,"+++++++++")
        if not l2 and l3:
            for idx in l3: 
                classfi_format['Cost of goods sold / Cost of Sales'].append(list_[idx])
                global_df['Class'].iloc[idx] = 'Cost of goods sold / Cost of Sales'
                remove.append(idx)

 

        print(operating_idx)
        print(classfi_format['Operating expenses'])

 

        try:
            if remove:
                temp = 0
                for idx in remove:
                    idx = idx - temp
                    temp = 1
                    classfi_format['Operating expenses'].pop(operating_idx.index(idx))
        except Exception as e:
            print(traceback.print_exc())
            print(e)
            pass


def km5_tax(list_ : list) -> None:

    '''If any particular year value of KM4 is 0 and KM5 is not 0 then calculate year value of km4 as km5 year value + tax year values''' 
    global km4,km5,classfi_format, tax_index, year_count

    if not isinstance(list_, list) :
        raise TypeError

    else:

        df = pd.DataFrame(list_)

        flag = False
        print(km5, '@@@@@@@@@@@@@@@@@@@@@')
        if km5:
            if year_count >= 1:
                if df.iloc[km4[0]].values[1] == 0.0:
                    # print(df.iloc[km4[0]].values[1], df.iloc[km5[0]].values[1], "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
                    if df.iloc[km5[0]].values[1] != 0.0:
                        flag =True

            if year_count >= 2:
                if df.iloc[km4[0]].values[2] == 0.0:
                    # print(df.iloc[km4[0]].values[2], df.iloc[km5[0]].values[2]), "################################################")
                    if df.iloc[km5[0]].values[2] != 0.0:
                        flag =True

            if year_count == 3:
                if df.iloc[km4[0]].values[3] == 0.0:
                    # print(df.iloc[km4[0]].values[2], df.iloc[km5[0]].values[2]), "################################################")
                    if df.iloc[km5[0]].values[3] != 0.0:
                        flag =True

        if flag:
            if year_count >= 1:
                value1 = df.iloc[tax_index,1].sum() + df.iloc[km5[0]].values[1]
            if year_count >= 2:
                value2 = df.iloc[tax_index,2].sum() + df.iloc[km5[0]].values[2]
            if year_count == 3:
                value3 = df.iloc[tax_index,3].sum() + df.iloc[km5[0]].values[3]

            keys = list(list_[km4[0]].keys())

            if year_count >= 1:
                list_[km4[0]].update({keys[1]: value1})
            if year_count >= 2:
                list_[km4[0]].update({keys[1]: value1, keys[2]: value2})
            if year_count == 3:
                list_[km4[0]].update({keys[1]: value1, keys[2]: value2, keys[3]: value3})

            classfi_format['KM4'] = [list_[km4[0]]]
        else:
            classfi_format['KM4'] = [list_[km4[-1]]]


def find_total_header_after_income(list_ : list) -> int:

    '''For other vertical format if we unable to find the cogs indexs then find the first total/blank/header after other income/revenue''' 
    global rev_idx,l1

    if not isinstance(list_, list) :
        raise TypeError

    else:

        if l1:
            stp = l1[-1]
        elif rev_idx:
            stp = rev_idx[-1]
        else:
            stp = 0

        df = pd.DataFrame(list_)[stp:]

        for idx,line in enumerate(df['particular'].to_list()):
            if line is '' or fuzz.partial_token_set_ratio(line, 'total') >= 85 or df['Label Signage'].to_list()[idx] is 'H':
                return idx+stp+1

        return 0


def by_gross_profit_other_income(list_ : list):

    '''If By gross profit exist then all after that all line items should be classified as Other Income''' 
    global l1, by_grosss_proft_index, signage

    if not isinstance(list_, list) :
        raise TypeError

    else:
        list_2=pd.DataFrame(list_)['Label Signage'].to_list()

        for idx in range(by_grosss_proft_index[0], signage):
            
            # if not (max(pd.DataFrame(list_).iloc[idx].values[1], pd.DataFrame(list_).iloc[idx].values[2]) == 0.0 and min(pd.DataFrame(list_).iloc[idx].values[1], pd.DataFrame(list_).iloc[idx].values[2]) == 0.0):
            if not check_header(list_, idx):
                if all(fuzz.partial_token_set_ratio(pd.DataFrame(list_)['particular'].iloc[idx].lower(), c.lower()) <= 85 for c in income_statement_IS["total_exclusion"]) and pd.DataFrame(list_)['particular'].iloc[idx].strip() is not '': 
                    l1.append(idx)

        l1 = list( dict.fromkeys(l1) )
        l1.sort()


def signage_to_gross_profit_cogs(list_ : list):

    ''' From signage to gross profit all should be classified as cogs''' 
    global km1, signage, classfi_format

    if not isinstance(list_, list) :
        raise TypeError

    else:

        for idx in range(signage, km1[0]):

            # if not (max(pd.DataFrame(list_).iloc[idx].values[1], pd.DataFrame(list_).iloc[idx].values[2]) == 0.0 and min(pd.DataFrame(list_).iloc[idx].values[1], pd.DataFrame(list_).iloc[idx].values[2]) == 0.0):
            if not check_header(list_, idx):
                if all(fuzz.partial_token_set_ratio(pd.DataFrame(list_)['particular'].iloc[idx].lower(), c.lower()) <= 85 for c in income_statement_IS["total_exclusion"]) and pd.DataFrame(list_)['particular'].iloc[idx].strip() is not '' and global_df['Class'].iloc[idx] is '':
                    
                    classfi_format['Cost of goods sold / Cost of Sales'].append(list_[idx])
                    global_df['Class'].iloc[idx] = 'Cost of goods sold / Cost of Sales'



def default_class(classification_is):
    for subclass in classification_is:
        print("-------------",subclass,"------------")
        seen_finance_cost = [sub_element for sub_element in classification_is["Finance cost"]]
        seen_tax = [sub_element for sub_element in classification_is["Tax"]]
        seen_depreciation = [sub_element for sub_element in classification_is["Depreciation"]]
        seen_other_income = [sub_element for sub_element in classification_is["Other Income"]]

        #print(seen_depreciation,seen_finance_cost,seen_tax ,seen_other_income,"SEEN finance cost & depreciation & Tax & other income")
        sub_element_check_duplicate=[]
        for sub_element in classification_is[subclass]:

            if sub_element[list(sub_element.keys())[1]] < 0:
                    sub_element.update({'Label Signage':'N'})
            else:
                sub_element.update({'Label Signage':'P'})

            print(sub_element)
            print(seen_depreciation)
            if subclass== "Operating expenses" or subclass== "Non-operating or Other Income / Expenses":
                if sub_element not in seen_finance_cost and sub_element not in seen_depreciation and sub_element not in seen_tax  and sub_element not in seen_other_income:

                    sub_element_check_duplicate.append(sub_element)
                    
                    
            elif subclass == "Cost of goods sold / Cost of Sales":

                sub_element_check_duplicate.append(sub_element)

                if sub_element in seen_finance_cost:
                    classification_is["Finance cost"].remove(sub_element)

                elif sub_element in seen_depreciation:
                    classification_is["Depreciation"].remove(sub_element)

                elif sub_element in seen_tax:
                    classification_is["Tax"].remove(sub_element)

                elif sub_element in seen_other_income:
                    classification_is["Other Income"].remove(sub_element)


            else:
                sub_element_check_duplicate.append(sub_element)
        
        classification_is.update({subclass:sub_element_check_duplicate})

    return classification_is




def income_statement_lineitems(dict_: dict, typ: str, datasource : str):

    

    global l1,l2,l3,l4,exp_head,signage,cost,km1,km2,km3,km4,km5,classfi_format,operating_items_end_index,dep,global_df,type_,rev_idx,tax_index,operating_idx,remove_item, by_grosss_proft_index, year_count, nonoperating_idx
    
    FINAL_OUTPUT = {}
    l1,l2,l3,l4,exp_head,signage,cost,km1,km2,km3,km4,km5,operating_items_end_index,dep,global_df,type_,exclude_tax_index,rev_idx,tax_index,operating_idx, remove_item, by_grosss_proft_index, nonoperating_idx, dep_index = [],[],[],[],[],-1,[],[],[],[],[],[],-1,[],[],'',[],[],[],[],[],[],[],[]
    #uncomment to switch OFF print statement
    #blockPrint()


    print('-----------------TYPE---------------')
    type_ = typ

    year_count = year_count_(dict_["Data"]["Financial Tables"][1]["Income Statement"][0])
    print('year_count:::::', year_count)
    each = convert_income_statement(dict_)
    print("------------------------pdf------------------------")
    # print(jsn.split('/')[-1])
    # each = preprocessing_IS_input(each)
    if typ in 'T-form_Tally':
        each = remove_lineitem(each)
        
    print(each)

    global_df = pd.DataFrame(each)

    print(global_df['particular'].to_list())
    graph_output=start_graph_process({"query_type" : "classification","branch_name" : "IS", "lineitem_list": global_df['particular'].to_list()})
    graph_output = sorted(graph_output, key=lambda x: float(x[1]), reverse=False)

    levels = [list(each21)[2][0] for each21 in graph_output]
    levels = [each22.replace(each22[each22.find('.'):],'').replace('Level','') if '.' in each22 else each22.replace('Level','') for each22 in levels]

    if '18' in levels:
        graph_output = graph_output[0:levels.index('18')]

    print("\nINDEXED MAPPED STATEMENTS\n", graph_output)

    if not isinstance(graph_output,list):
        graph_output = []

    END_POINT = [list(e3)[1] for e3 in graph_output if 'EndPoint' in list(e3)[2]]
    END_POINT_INDEX = 10000
    if END_POINT:
        END_POINT.sort()
        END_POINT_INDEX = END_POINT[0]

    print("END_POINT_INDEX::::", END_POINT_INDEX)

    global_df['Class'] = ''
    print(pd.DataFrame(global_df))
    df =pd.DataFrame(each)
    

    # classfi_format = {'Revenue':[], 'expenses': {'Cost of goods sold / Cost of Sales': [], 'Operating expenses': [], 'non_operating_items': []}}
    classfi_format = {'Revenue':[], 'Cost of goods sold / Cost of Sales': [], 'Operating expenses': [], 'Non-operating or Other Income / Expenses': [], 'Depreciation': [], 'KM4': [], 'Tax': [],'Finance cost':[],'Other Income':[], 'signage_index':[]}
    print('-------------------------------------header search-------------------------------------')
    header_index = 0
    rev_head = find_revenue_header(each)
    if rev_head:
        print("revenue_head--->", [each1 for each1 in rev_head])
        header_index=header_index+rev_head[0]+1
    else:
        print("revenue_head--->", rev_head)
    print("last header index: ", header_index)
    
    exp_head = find_expense_header(each[header_index:])
    if exp_head:
        exp_head = [header_index+each2 for each2 in exp_head]
        print("expense_head--->", exp_head)
        header_index=header_index+exp_head[0]+1

        if datasource in 'Other vertical format':
            type_ = 'T-form_Tally'

            df= pd.DataFrame(each)
            df['Label Signage'][0:exp_head[0]].loc[df['Label Signage'] == 'P'] = 'BY'
            df['Label Signage'][0:exp_head[0]].loc[df['Label Signage'] == 'N'] = 'BY'
            df['Label Signage'][0:exp_head[0]].loc[df['Label Signage'] == 'H'] = None

            df['Label Signage'][exp_head[0]:].loc[df['Label Signage'] == 'P'] = 'TO'
            df['Label Signage'][exp_head[0]:].loc[df['Label Signage'] == 'N'] = 'TO'
            df['Label Signage'][exp_head[0]:].loc[df['Label Signage'] == 'H'] = None

            each = list(df.T.to_dict().values())

            print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ Converted to T-form @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')

            global_df = pd.DataFrame(each)
            global_df['Class'] = ''
            print(global_df)

    else:
        print("expense_head--->", exp_head)
    print("last header index: ", header_index)

    #if type_ in 'Schedule-III':
    print('----------------------------------Signage-----------------------------------------------')
    signage = find_first_signage(each)
    print('signage-------->', signage)

    print('----------------------------------cost line item----------------------------------------')
    cost = check_cost_line_item(each)
    print('cost----------->', cost)
    
    print('--------------------------------Key metric and attribute search-------------------------')
    attribute_index = 0
    
    l1_ = other_income(each)
    if l1_:
        l1 = [attribute_index+each3 for each3 in l1_]
        print("other_income--->", l1)
        ######

        
        attribute_index=attribute_index+l1_[0]+1
    else:
        print("other_income--->", l1_)
    print("last attribute_index: ", attribute_index)
    
    l2 = cogs(each)
    if l2:
        print("cogs----------->", l2)
        if attribute_index < l2[0]+1: 
            attribute_index = l2[0]+1
    else:
        print("cogs----------->", l2)
    print("last attribute_index: ", attribute_index)

    if type_ in 'Schedule-III':

        l3_ = employee_cost(each[attribute_index:])
        if l3_:
            l3 = [attribute_index+each4 for each4 in l3_]
            print("employee_cost----------->", l3)
            attribute_index=attribute_index+l3_[0]+1
        else:
            print("employee_cost----------->", l3_)
        print("last attribute_index: ", attribute_index)

        l4_ = finance_cost(each[attribute_index:])
        if l4_:
            l4 = [attribute_index+each5 for each5 in l4_]
            print("finance_cost----------->", l4)
            #####
            
            attribute_index=attribute_index+l4_[0]+1
        else:
            print("finance_cost----------->", l4_)
        print("last attribute_index: ", attribute_index)

    else:
        #l3 = employee_cost(each)
        if not signage is -1:
            l3 = employee_cost(each[signage:])
        else:
            l3 = employee_cost(each[0:])
        if l3:
            print("employee_cost----------->", l3)
        else:
            print("employee_cost----------->", l3)

        if not signage is -1:
            l4 = finance_cost(each[signage:])
        else:
            l4 = finance_cost(each[0:])
        if l4:
            print("finance_cost----------->", l4)
        else:
            print("finance_cost----------->", l4)


    
    index = 0

    km1_, km2_, km3_, km4_, km5_ = [], [], [], [], []

    if dict_["Source"]["annualReportType"] in ['Schedule-III', 'Other vertical format']:
        km1 = [list(e1)[1] for e1 in graph_output if 'KM1' in list(e1)[2] and list(e1)[1]<END_POINT_INDEX]
        km1.sort()
        if km1:
            km1 = [km1[0]]
    else:
        km1_ = KM_1(each)


    if km1_:
        km1 = [index+each6 for each6 in km1_]
        # print("KM_1------->", km1)
        index=index+km1_[-1]+1



    if dict_["Source"]["annualReportType"] in ['Schedule-III', 'Other vertical format']:
        # km2_ = KM_2(each[index:15])
        km2 = [list(e2)[1] for e2 in graph_output if 'KM2' in list(e2)[2] and list(e2)[1]<END_POINT_INDEX]
        km2.sort()
        if km2:
            km2 = [km2[0]]        
    else:
        km2_ = KM_2(each)

    if km2_:
        km2 = [index+each7 for each7 in km2_]
        print("KM_2------->", km2)
        index=index+km2_[-1]+1

    # print("KM_2------->", km2)

    if dict_["Source"]["annualReportType"] in ['Schedule-III', 'Other vertical format']:
        km3 = [list(e3)[1] for e3 in graph_output if 'KM3' in list(e3)[2] and list(e3)[1]<END_POINT_INDEX]
        km3.sort()
        if km3:
            km3 = [km3[-1]]
    else:
        km3_ = KM_3(each[index:])

    if km3_:
        km3 = [index+each8 for each8 in km3_]
        print("KM_3------->", km3)
        index=index+km3_[-1]+1
    
    # print("KM_3------->", km3)

    if dict_["Source"]["annualReportType"] in ['Schedule-III', 'Other vertical format']:
        km4 = [list(e4)[1] for e4 in graph_output if 'KM4' in list(e4)[2] and list(e4)[1]<END_POINT_INDEX]
        km4.sort()
        if km4:
            km4 = [km4[0]]
        else:
            tax_exp = [list(e4)[1] for e4 in graph_output if 'Level16.0' in list(e4)[2]]
            print("Tax expenses:::", tax_exp, km3)
            if tax_exp and km3:
                if km3[0] == tax_exp[0] - 1:
                    km4.append(km3[0])
                    km3 = []

            elif not km4:

                if tax_exp:
                    df1 = pd.DataFrame(each)
                    list_3=df1['particular'].to_list()

                    if list_3[tax_exp[0]-1] == '':
                        km4.append(tax_exp[0]-1)

    else:
        km4_ = KM_4(each[index:])

    if km4_:
        km4 = [index+each9 for each9 in km4_]
        print("KM_4------->", km4)
        index=index+km4_[-1]+1

    # print("KM_4------->", km4)

    if dict_["Source"]["annualReportType"] in ['Schedule-III', 'Other vertical format']:
        km5 = [list(e5)[1] for e5 in graph_output if 'KM5' in list(e5)[2] and list(e5)[1]<END_POINT_INDEX]
        km5.sort()
        if km5:
            km5 = [km5[0]]
    else:
        km5_ = KM_5(each[index:])

    if km5_:
        km5 = [index+each10 for each10 in km5_]
        index=index+km5_[-1]+1

    print("KM_1------->", km1)
    print("KM_2------->", km2)
    print("KM_3------->", km3)
    print("KM_4------->", km4)
    print("KM_5------->", km5)

    if km4:
        km5_tax(each)
    if km5:
        if l1:
            temp = [each11 for each11 in l1 if each11 < km5[0]]
            l1= temp


        if l3:
            temp = [each12 for each12 in l3 if each12 < km5[0]]
            l3= temp
    
    if l4:
        if km5:
            temp = [each13 for each13 in l4 if each13 < km5[0]]
            l4= temp
        classfi_format['Finance cost'] = [ each[i] for i in l4 ]

    dep = check_depreciation(each)
    print('---------dep------------->>',dep)
    if dep:
        classfi_format['Depreciation'] = [each[d] for d in dep]
    else:
        classfi_format['Depreciation'] = []


    print('-------------------Revenue Classification-----------------------')
    #classify_revenue(each)

    if type_ in 'Schedule-III':
        classify_revenue(each, copy.deepcopy(graph_output))
    else:
        classify_revenue_T(each)
        print('rev_idx @@@@@@@@@@',rev_idx)
    # print(global_df)

    print('-------------------Cogs Classification-----------------------')
    classify_cogs(each, copy.deepcopy(graph_output))
    # print(global_df)
    if not exp_head and datasource in 'Other vertical format':

        if l2:
            stop = l2
        else:
            stop = [find_total_header_after_income(each)]
            print('l2 not been found ..........excuted total_header_after_income: ', stop)

        type_ = 'T-form_Tally'

        df= pd.DataFrame(each)
        df['Label Signage'][0:stop[0]].loc[df['Label Signage'] == 'P'] = 'BY'
        df['Label Signage'][0:stop[0]].loc[df['Label Signage'] == 'N'] = 'BY'
        df['Label Signage'][0:stop[0]].loc[df['Label Signage'] == 'H'] = None

        df['Label Signage'][stop[0]:].loc[df['Label Signage'] == 'P'] = 'TO'
        df['Label Signage'][stop[0]:].loc[df['Label Signage'] == 'N'] = 'TO'
        df['Label Signage'][stop[0]:].loc[df['Label Signage'] == 'H'] = None

        each = list(df.T.to_dict().values())

        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ Converted to T-form @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
 
        global_df['Label Signage'] = list(pd.DataFrame(each)['Label Signage'])
        print(global_df)

        print('----------------------------------Calculating Signage again-----------------------------------------------')
        signage = find_first_signage(each)
        print('signage-------->', signage)



    if datasource in 'Other vertical format' and km4:
        print('--------------------tax------------------------')
        classify_tax(each)

    if type_ in 'Schedule-III':
        print('-------------------Operating items Classification-----------------------')
        classify_operating_items(each, copy.deepcopy(graph_output))
        print('--------------------tax------------------------')
        classify_tax(each)
        print('-------------------Non Operating items Classification-----------------------')
        classify_non_operating_items(each, copy.deepcopy(graph_output))

    if type_ in 'T-form_Tally':
        print('--------------------classifyExpenses------------------------')
        classify_expenses(each)
        if km5 and not km4:
            classfi_format['KM4'] = [each[km5[-1]]]

    if type_ in 'T-form_Tally' and by_grosss_proft_index:
        by_gross_profit_other_income(each)

    if type_ in 'T-form_Tally' and km1 and signage:
        print('-----------------signage_to_gross_profit_cogs -------------------')
        signage_to_gross_profit_cogs(each)

    # print(global_df)
    second_phase(each)
    # print(global_df)

    if type_ in 'T-form_Tally' and l1:
        print('--------------------other_income_exclusion------------------------')
        other_income_exclusion(each)
        print('-------------other income-------------->', l1)

    if type_ in 'T-form_Tally' and rev_idx:
        print('--------------------revenue_exclusion------------------------')
        #print(global_df)
        revenue_exclusion(each)

    cogs_exclusion(each)
    cogs_null(each)

    if l1:
        classfi_format['Other Income'] =  [ each[i] for i in l1 ]

    
    # km_index_ = km1+km2+km3+km4+km5
    km_index_ = []

    if km1:
        km_index_.append(km1[-1])
    else:
        km_index_.append(-1)

    if km2:
        km_index_.append(km2[-1])
    else:
        km_index_.append(-1)

    if km3:
        km_index_.append(km3[-1])
    else:
        km_index_.append(-1)

    if km4:
        km_index_.append(km4[-1])
    else:
        km_index_.append(-1)

    if km5:
        km_index_.append(km5[-1])
    else:
        km_index_.append(-1)


    l4__ = l4
    signage_ = [signage]

    if remove_item:
        # temp = [each14+1 if remove_item[0] <= each14 else each14 for each14 in km_index_]
        temp = [each14+len(remove_item) if remove_item[-1] <= each14 else each14 for each14 in km_index_]
        km_index_ = temp

        # temp = [each15+1 for each15 in l4__ if remove_item[0] <= each15]
        temp = [each15+len(remove_item) for each15 in l4__ if remove_item[-1] <= each15]
        l4__= temp

        if not signage_[0] is -1:
            # temp = [signage_[0]+1 if remove_item[0] <= signage_[0] else signage_[0]]
            temp = [signage_[0]+len(remove_item) if remove_item[-1] <= signage_[0] else signage_[0]]
            if temp:
                signage_= temp

    print(global_df)
    # print(global_df.T.to_dict().values())graph_output = sorted(graph_output, key=lambda x: float(x[1]), reverse=False)
    # global_df.to_csv('save.csv',index=False)
    for each_key in classfi_format:
        if each_key in ['Revenue', 'Cost of goods sold / Cost of Sales']:
            classfi_format[each_key] = list(global_df[global_df['Class'] == each_key].drop(labels='Class', axis=1).T.to_dict().values())

    all_km_graph = [list(e3)[1] for e3 in graph_output if 'KM' in list(e3)[2][1]]
    classified_index = [in_ for in_ in global_df.loc[global_df["Class"]!=''].index.to_list() if not in_ in all_km_graph]
    classified_items_ = [global_df['particular'].iloc[in1_] for in1_ in global_df.loc[global_df["Class"]!=''].index.to_list() if not in1_ in all_km_graph]
    #l1,l2,l3,l4,exp_head,signage,cost,km1,km2,km3,km4,km5,classfi_format,operating_items_end_index,dep,global_df,type_,exclude_tax_index,rev_idx = [],[],[],[],[],-1,[],[],[],[],[],[],{},-1,[],[],'',[],[]
    l1,l2,l3,l4,exp_head,signage,cost,km1,km2,km3,km4,km5,operating_items_end_index,dep,global_df,type_,exclude_tax_index,rev_idx,tax_index,operating_idx, remove_item, by_grosss_proft_index, nonoperating_idx, dep_index = [],[],[],[],[],-1,[],[],[],[],[],[],-1,[],[],'',[],[],[],[],[],[], [], []
    # print(global_df)
    for each in classfi_format:
        classfi_format[each] = list(unique_everseen(classfi_format[each]))

    pprint.pprint(classfi_format) 
    classfi_format= default_class(classfi_format)

    classfi_format['km_index'] = km_index_
    classfi_format['km_index'].append({"classified_index":classified_index})
    classfi_format['km_index'].append({"classified_items_":classified_items_})
    classfi_format['finance_cost_index'] = l4__
    classfi_format['signage_index'] = signage_
    classfi_format['graph_output'] = graph_output

    print("----------------after default class-------------------")
    pprint.pprint(classfi_format)
    return classfi_format



