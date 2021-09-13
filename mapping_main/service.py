from src.mapping import *
from fuzzywuzzy import fuzz 
from fuzzywuzzy import process 

from datetime import datetime
import os,re

import traceback
import sys

import re


def junkremover(num:str)->str:
    ''' 
    minus sign between 2nd and 3rd place - convert to decimal
    minus sign at extreme left - retain
    all other minus sign - remove
    '''
    try:
        junk_pos = [True if not n is '-' else False for n in num][::-1]
        second_pos = nth_index(junk_pos, True, 2)
        third_pos = nth_index(junk_pos, True, 3)

        if second_pos is None:
            second_pos = 1000
        if third_pos is None:
            third_pos = 2000
        if third_pos - second_pos == 2:
            # print(1)
            num = num[::-1]
            num = list(num)
            num[second_pos+1] = '.'
            num = ''.join(num)
            num = num[::-1]
            if num.startswith('-'):
                return num[0]+re.sub("[^\d\.]","",num[1:])
        elif num.startswith('-'):
            #print(2)
            return num[0]+re.sub("[^\d\.]","",num[1:])
        # print(3)
        return re.sub("[^\d\.]","",num)
    except Exception as e:
        print(e)
        print('---------------------------------------------')
        print(traceback.print_exc())
        return 0.0



def balance_sheet_service(DATA : dict,balance_sheet_cls: dict,dynamic_data:dict, logger:object) -> dict:
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

    try:
        DATA = calculated_field_bs(DATA, balance_sheet_cls)

        df_temp = template_api_to_dataframe(dynamic_data)

        df_temp.to_csv("mapping_output/Final_Output/"+DATA['Source']['documentid']+'/'+DATA['Source']['filename'].replace('.pdf','')+"_template.csv",index=False)

        balance_sheet = BS_mapping(DATA, df_temp, balance_sheet_cls)
        

    except Exception as e:
        print(e)
        print(traceback.print_exc())
        # sys.exit(0)
        logger.error(e, extra={'props': {"documentid": DATA['Source']['documentid']}})
        balance_sheet=[]

    

    #print (balance_sheet,"ENNNNNNNNNNNNNNNNNNNNNNNNN BS")
    return balance_sheet

def income_statement_service(DATA:dict,income_statement_cls : dict,dynamic_data: dict, logger:object)-> dict:
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



    try:
        DATA = calculated_field_is(DATA, income_statement_cls)

        df_temp = template_api_to_dataframe(dynamic_data)

        income_statement = IS_mapping(DATA, df_temp, income_statement_cls)

    except Exception as e:
        print(e)
        print(traceback.print_exc())
        income_statement=[]
        logger.error(e, extra={'props': {"documentid": DATA['Source']['documentid']}})

    return income_statement
