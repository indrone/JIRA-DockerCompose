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
import traceback
import ast
from utils import *

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
from src import *
import pytest
from src.mapping import *
import input_




def test_calculated_field_bs():

    with pytest.raises(TypeError):
        calculated_field_bs('current asset',[1,2,3])
        calculated_field_bs((1, 2, 3),'1')
        calculated_field_bs([1, 2, 3],1)

    calculated_field_bs_input1_Credit_Financials = input_.calculated_field_bs_input1_Credit_Financials25_T_Format
    calculated_field_bs_input2_Credit_Financials = input_.calculated_field_bs_input2_Credit_Financials25_T_Format
    calculated_field_bs_output_Credit_Financials = input_.calculated_field_bs_output_Credit_Financials25_T_Format
    calculated_field_bs_input1_Credit = input_.calculated_field_bs_input1_Credit_Financials38
    calculated_field_bs_input2_Credit = input_.calculated_field_bs_input2_Credit_Financials38
    calculated_field_bs_output_Credit = input_.calculated_field_bs_output_Credit_Financials38
    calculated_field_bs_input1_Decon = input_.calculated_field_bs_input1_Decon
    calculated_field_bs_input2_Decon = input_.calculated_field_bs_input2_Decon
    calculated_field_bs_output_Decon= input_.calculated_field_bs_output_Decon
    calculated_field_bs_input1_DHO = input_.calculated_field_bs_input1_DHO
    calculated_field_bs_input2_DHO = input_.calculated_field_bs_input2_DHO
    calculated_field_bs_output_DHO = input_.calculated_field_bs_output_DHO
    calculated_field_bs_input1_Intex_ITR_AY=input_.calculated_field_bs_input1_Intex_ITR_AY
    calculated_field_bs_input2_Intex_ITR_AY=input_.calculated_field_bs_input2_Intex_ITR_AY
    calculated_field_bs_output_Intex_ITR_AY=input_.calculated_field_bs_output_Intex_ITR_AY
    calculated_field_bs_input1_MDMOTOR_ITR=input_.calculated_field_bs_input1_MDMOTOR_ITR
    calculated_field_bs_input2_MDMOTOR_ITR=input_.calculated_field_bs_input2_MDMOTOR_ITR
    calculated_field_bs_output_MDMOTOR_ITR =input_.calculated_field_bs_output_MDMOTOR_ITR
    calculated_field_bs_input1_Shruthi_Engg=input_.calculated_field_bs_input1_Shruthi_Engg
    calculated_field_bs_input2_Shruthi_Engg=input_.calculated_field_bs_input2_Shruthi_Engg
    calculated_field_bs_output_Shruthi_Engg=input_.calculated_field_bs_output_Shruthi_Engg


    assert calculated_field_bs(calculated_field_bs_input1_Credit_Financials,calculated_field_bs_input2_Credit_Financials)==calculated_field_bs_output_Credit_Financials
    assert calculated_field_bs(calculated_field_bs_input1_Credit,calculated_field_bs_input2_Credit)==calculated_field_bs_output_Credit
    assert calculated_field_bs(calculated_field_bs_input1_Decon,calculated_field_bs_input2_Decon)==calculated_field_bs_output_Decon
    assert calculated_field_bs(calculated_field_bs_input1_DHO,calculated_field_bs_input2_DHO)==calculated_field_bs_output_DHO
    assert calculated_field_bs(calculated_field_bs_input1_Intex_ITR_AY,calculated_field_bs_input2_Intex_ITR_AY)==calculated_field_bs_output_Intex_ITR_AY
    assert calculated_field_bs(calculated_field_bs_input1_MDMOTOR_ITR,calculated_field_bs_input2_MDMOTOR_ITR)==calculated_field_bs_output_MDMOTOR_ITR
    assert calculated_field_bs(calculated_field_bs_input1_Shruthi_Engg,calculated_field_bs_input2_Shruthi_Engg)==calculated_field_bs_output_Shruthi_Engg
    

def test_profit_loss_account_check():

    # with pytest.raises(AttributeError):
    #     profit_loss_account_check({'a':1})
    #     profit_loss_account_check(1.0)
    #     profit_loss_account_check([1,2])

    profit_loss_account_check_input_Credit_Financials25_T_Format=input_.profit_loss_account_check_input_Credit_Financials25_T_Format
    profit_loss_account_check_output_Credit_Financials25_T_Format=input_.profit_loss_account_check_output_Credit_Financials25_T_Format
    profit_loss_account_check_input_Shruthi_Engg=input_.profit_loss_account_check_input_Shruthi_Engg
    profit_loss_account_check_output_Shruthi_Engg=input_.profit_loss_account_check_output_Shruthi_Engg
    df= pd.DataFrame(profit_loss_account_check_input_Credit_Financials25_T_Format)
    df1= pd.DataFrame(profit_loss_account_check_input_Shruthi_Engg)
    assert profit_loss_account_check(df) == profit_loss_account_check_output_Credit_Financials25_T_Format
    assert profit_loss_account_check(df1)== profit_loss_account_check_output_Shruthi_Engg

def test_machinary_pos():

    # with pytest.raises(TypeError):
    #     machinary_pos('current asset','asasss')
    #     machinary_pos((1, 2, 3),'1')
    #     machinary_pos([1, 2, 3],1)

    machinary_pos_input1_Credit_Financials25_T_Format=input_.machinary_pos_input1_Credit_Financials25_T_Format
    machinary_pos_input2_Credit_Financials25_T_Format=input_.machinary_pos_input2_Credit_Financials25_T_Format
    machinary_pos_output1_Credit_Financials25_T_Format=input_.machinary_pos_output1_Credit_Financials25_T_Format
    machinary_pos_output2_Credit_Financials25_T_Format=input_.machinary_pos_output2_Credit_Financials25_T_Format
    machinary_pos_output3_Credit_Financials25_T_Format=input_.machinary_pos_output3_Credit_Financials25_T_Format

    machinary_pos_input1_Credit_Financials38=input_.machinary_pos_input1_Credit_Financials38
    machinary_pos_input2_Credit_Financials38=input_.machinary_pos_input2_Credit_Financials38
    machinary_pos_output1_Credit_Financials38=input_.machinary_pos_output1_Credit_Financials38
    machinary_pos_output2_Credit_Financials38=input_.machinary_pos_output2_Credit_Financials38
    machinary_pos_output3_Credit_Financials38=input_.machinary_pos_output3_Credit_Financials38

    machinary_pos_input1_Decon=input_.machinary_pos_input1_Decon
    machinary_pos_input2_Decon=input_.machinary_pos_input2_Decon
    machinary_pos_output1_Decon=input_.machinary_pos_output1_Decon
    machinary_pos_output2_Decon=input_.machinary_pos_output2_Decon
    machinary_pos_output3_Decon=input_.machinary_pos_output3_Decon

    machinary_pos_input1_DHO=input_.machinary_pos_input1_DHO
    machinary_pos_input2_DHO=input_.machinary_pos_input2_DHO
    machinary_pos_output1_DHO=input_.machinary_pos_output1_DHO
    machinary_pos_output2_DHO=input_.machinary_pos_output2_DHO
    machinary_pos_output3_DHO=input_.machinary_pos_output3_DHO

    machinary_pos_input1_Intex_ITR_AY=input_.machinary_pos_input1_Intex_ITR_AY
    machinary_pos_input2_Intex_ITR_AY=input_.machinary_pos_input2_Intex_ITR_AY
    machinary_pos_output1_Intex_ITR_AY=input_.machinary_pos_output1_Intex_ITR_AY
    machinary_pos_output2_Intex_ITR_AY=input_.machinary_pos_output2_Intex_ITR_AY
    machinary_pos_output3_Intex_ITR_AY=input_.machinary_pos_output3_Intex_ITR_AY

    machinary_pos_input1_MDMOTOR_ITR=input_.machinary_pos_input1_MDMOTOR_ITR
    machinary_pos_input2_MDMOTOR_ITR=input_.machinary_pos_input2_MDMOTOR_ITR
    machinary_pos_output1_MDMOTOR_ITR=input_.machinary_pos_output1_MDMOTOR_ITR
    machinary_pos_output2_MDMOTOR_ITR=input_.machinary_pos_output2_MDMOTOR_ITR
    machinary_pos_output3_MDMOTOR_ITR=input_.machinary_pos_output3_MDMOTOR_ITR

    machinary_pos_input1_Shruthi_Engg=input_.machinary_pos_input1_Shruthi_Engg
    machinary_pos_input2_Shruthi_Engg=input_.machinary_pos_input2_Shruthi_Engg
    machinary_pos_output1_Shruthi_Engg=input_.machinary_pos_output1_Shruthi_Engg
    machinary_pos_output2_Shruthi_Engg=input_.machinary_pos_output2_Shruthi_Engg
    machinary_pos_output3_Shruthi_Engg=input_.machinary_pos_output3_Shruthi_Engg
    df= pd.DataFrame(machinary_pos_input1_Credit_Financials25_T_Format)
    df1=pd.DataFrame(machinary_pos_input1_Credit_Financials38)
    df2=pd.DataFrame(machinary_pos_input1_Decon)
    df3=pd.DataFrame(machinary_pos_input1_DHO)
    df4=pd.DataFrame(machinary_pos_input1_Intex_ITR_AY)
    df5=pd.DataFrame(machinary_pos_input1_MDMOTOR_ITR)
    df6=pd.DataFrame(machinary_pos_input1_Shruthi_Engg)

    assert machinary_pos(df,machinary_pos_input2_Credit_Financials25_T_Format)==(machinary_pos_output1_Credit_Financials25_T_Format,machinary_pos_output2_Credit_Financials25_T_Format,machinary_pos_output3_Credit_Financials25_T_Format)
    assert machinary_pos(df1,machinary_pos_input2_Credit_Financials38)==(machinary_pos_output1_Credit_Financials38,machinary_pos_output2_Credit_Financials38,machinary_pos_output3_Credit_Financials38)
    assert machinary_pos(df2,machinary_pos_input2_Decon)==(machinary_pos_output1_Decon,machinary_pos_output2_Decon,machinary_pos_output3_Decon)
    assert machinary_pos(df3,machinary_pos_input2_DHO)== (machinary_pos_output1_DHO,machinary_pos_output2_DHO,machinary_pos_output3_DHO)
    assert machinary_pos(df4,machinary_pos_input2_Intex_ITR_AY)==(machinary_pos_output1_Intex_ITR_AY,machinary_pos_output2_Intex_ITR_AY,machinary_pos_output3_Intex_ITR_AY)
    assert machinary_pos(df5,machinary_pos_input2_MDMOTOR_ITR)==(machinary_pos_output1_MDMOTOR_ITR,machinary_pos_output2_MDMOTOR_ITR,machinary_pos_output3_MDMOTOR_ITR)
    assert machinary_pos(df6,machinary_pos_input2_Shruthi_Engg)==(machinary_pos_output1_Shruthi_Engg,machinary_pos_output2_Shruthi_Engg,machinary_pos_output3_Shruthi_Engg)

def test_secured_loan_pos():

    # with pytest.raises(TypeError):
    #     secured_loan_pos('current asset','asasss')
    #     secured_loan_pos((1, 2, 3),'1')
    #     secured_loan_pos([1, 2, 3],1)

    secured_loan_pos_input1_Credit_Financials25_T_Format=input_.secured_loan_pos_input1_Credit_Financials25_T_Format
    secured_loan_pos_input2_Credit_Financials25_T_Format=input_.secured_loan_pos_input2_Credit_Financials25_T_Format
    secured_loan_pos_output1_Credit_Financials25_T_Format=input_.secured_loan_pos_output1_Credit_Financials25_T_Format
    secured_loan_pos_output2_Credit_Financials25_T_Format=input_.secured_loan_pos_output2_Credit_Financials25_T_Format
    secured_loan_pos_output3_Credit_Financials25_T_Format=input_.secured_loan_pos_output3_Credit_Financials25_T_Format
    secured_loan_pos_input1_Credit_Financials38=input_.secured_loan_pos_input1_Credit_Financials38
    secured_loan_pos_input2_Credit_Financials38=input_.secured_loan_pos_input2_Credit_Financials38
    secured_loan_pos_output1_Credit_Financials38=input_.secured_loan_pos_output1_Credit_Financials38
    secured_loan_pos_output2_Credit_Financials38=input_.secured_loan_pos_output2_Credit_Financials38
    secured_loan_pos_output3_Credit_Financials38=input_.secured_loan_pos_output3_Credit_Financials38
    secured_loan_pos_input1_Decon=input_.secured_loan_pos_input1_Decon
    secured_loan_pos_input2_Decon=input_.secured_loan_pos_input2_Decon
    secured_loan_pos_output1_Decon=input_.secured_loan_pos_output1_Decon
    secured_loan_pos_output2_Decon=input_.secured_loan_pos_output2_Decon
    secured_loan_pos_output3_Decon=input_.secured_loan_pos_output3_Decon
    secured_loan_pos_input1_DHO=input_.secured_loan_pos_input1_DHO
    secured_loan_pos_input2_DHO=input_.secured_loan_pos_input2_DHO
    secured_loan_pos_output1_DHO=input_.secured_loan_pos_output1_DHO
    secured_loan_pos_output2_DHO=input_.secured_loan_pos_output2_DHO
    secured_loan_pos_output3_DHO=input_.secured_loan_pos_output3_DHO
    secured_loan_pos_input1_Intex_ITR_AY=input_.secured_loan_pos_input1_Intex_ITR_AY
    secured_loan_pos_input2_Intex_ITR_AY=input_.secured_loan_pos_input2_Intex_ITR_AY
    secured_loan_pos_output1_Intex_ITR_AY=input_.secured_loan_pos_output1_Intex_ITR_AY
    secured_loan_pos_output2_Intex_ITR_AY=input_.secured_loan_pos_output2_Intex_ITR_AY
    secured_loan_pos_output3_Intex_ITR_AY=input_.secured_loan_pos_output3_Intex_ITR_AY
    secured_loan_pos_input1_MDMOTOR_ITR=input_.secured_loan_pos_input1_MDMOTOR_ITR
    secured_loan_pos_input2_MDMOTOR_ITR=input_.secured_loan_pos_input2_MDMOTOR_ITR
    secured_loan_pos_output1_MDMOTOR_ITR=input_.secured_loan_pos_output1_MDMOTOR_ITR
    secured_loan_pos_output2_MDMOTOR_ITR=input_.secured_loan_pos_output2_MDMOTOR_ITR
    secured_loan_pos_output3_MDMOTOR_ITR=input_.secured_loan_pos_output3_MDMOTOR_ITR
    secured_loan_pos_input1_Shruthi_Engg=input_.secured_loan_pos_input1_Shruthi_Engg
    secured_loan_pos_input2_Shruthi_Engg=input_.secured_loan_pos_input2_Shruthi_Engg
    secured_loan_pos_output1_Shruthi_Engg=input_.secured_loan_pos_output1_Shruthi_Engg
    secured_loan_pos_output2_Shruthi_Engg=input_.secured_loan_pos_output2_Shruthi_Engg
    secured_loan_pos_output3_Shruthi_Engg=input_.secured_loan_pos_output3_Shruthi_Engg

    df=pd.DataFrame(secured_loan_pos_input1_Credit_Financials25_T_Format)
    df1=pd.DataFrame(secured_loan_pos_input1_Credit_Financials38)
    df2=pd.DataFrame(secured_loan_pos_input1_Decon)
    df3=pd.DataFrame(secured_loan_pos_input1_DHO)
    df4=pd.DataFrame(secured_loan_pos_input1_Intex_ITR_AY)
    df5=pd.DataFrame(secured_loan_pos_input1_MDMOTOR_ITR)
    df6=pd.DataFrame(secured_loan_pos_input1_Shruthi_Engg)
    assert secured_loan_pos((df),secured_loan_pos_input2_Credit_Financials25_T_Format)==(secured_loan_pos_output1_Credit_Financials25_T_Format,secured_loan_pos_output2_Credit_Financials25_T_Format,secured_loan_pos_output3_Credit_Financials25_T_Format)
    assert secured_loan_pos((df1),secured_loan_pos_input2_Credit_Financials38)==(secured_loan_pos_output1_Credit_Financials38,secured_loan_pos_output2_Credit_Financials38,secured_loan_pos_output3_Credit_Financials38)
    assert secured_loan_pos((df2),secured_loan_pos_input2_Decon)==(secured_loan_pos_output1_Decon,secured_loan_pos_output2_Decon,secured_loan_pos_output3_Decon)
    assert secured_loan_pos((df3),secured_loan_pos_input2_DHO)==(secured_loan_pos_output1_DHO,secured_loan_pos_output2_DHO,secured_loan_pos_output3_DHO)
    assert secured_loan_pos((df4),secured_loan_pos_input2_Intex_ITR_AY)==(secured_loan_pos_output1_Intex_ITR_AY,secured_loan_pos_output2_Intex_ITR_AY,secured_loan_pos_output3_Intex_ITR_AY)
    assert secured_loan_pos((df5),secured_loan_pos_input2_MDMOTOR_ITR)==(secured_loan_pos_output1_MDMOTOR_ITR,secured_loan_pos_output2_MDMOTOR_ITR,secured_loan_pos_output3_MDMOTOR_ITR)
    assert secured_loan_pos((df6),secured_loan_pos_input2_Shruthi_Engg)==(secured_loan_pos_output1_Shruthi_Engg,secured_loan_pos_output2_Shruthi_Engg,secured_loan_pos_output3_Shruthi_Engg)


def test_find_first_header():

    # with pytest.raises(AttributeError):
    #     find_first_header(1)
    #     find_first_header(1.0)
    #     find_first_header([1,2])

    find_first_header_input_Credit_Financials25_T_Format=input_.find_first_header_input_Credit_Financials25_T_Format
    find_first_header_output_Credit_Financials25_T_Format=input_.find_first_header_output_Credit_Financials25_T_Format
    find_first_header_input_Credit_Financials38=input_.find_first_header_input_Credit_Financials38
    find_first_header_output_Credit_Financials38=input_.find_first_header_output_Credit_Financials38
    find_first_header_input_Decon=input_.find_first_header_input_Decon
    find_first_header_output_Decon=input_.find_first_header_output_Decon
    find_first_header_input_DHO=input_.find_first_header_input_DHO
    find_first_header_output_DHO=input_.find_first_header_output_DHO
    find_first_header_input_Intex_ITR_AY=input_.find_first_header_input_Intex_ITR_AY
    find_first_header_output_Intex_ITR_AY=input_.find_first_header_output_Intex_ITR_AY
    find_first_header_input_MDMOTOR_ITR=input_.find_first_header_input_MDMOTOR_ITR
    find_first_header_output_MDMOTOR_ITR=input_.find_first_header_output_MDMOTOR_ITR
    find_first_header_input_Shruthi_Engg=input_.find_first_header_input_Shruthi_Engg
    find_first_header_output_Shruthi_Engg=input_.find_first_header_output_Shruthi_Engg

    df=pd.DataFrame(find_first_header_input_Credit_Financials25_T_Format)
    df1=pd.DataFrame(find_first_header_input_Credit_Financials38)
    df2=pd.DataFrame(find_first_header_input_Decon)
    df3=pd.DataFrame(find_first_header_input_DHO)
    df4=pd.DataFrame(find_first_header_input_Intex_ITR_AY)
    df5=pd.DataFrame(find_first_header_input_MDMOTOR_ITR)
    df6=pd.DataFrame(find_first_header_input_Shruthi_Engg)


    assert find_first_header(df) ==find_first_header_output_Credit_Financials25_T_Format
    assert find_first_header(df1)==find_first_header_output_Credit_Financials38
    assert find_first_header(df2)==find_first_header_output_Decon
    assert find_first_header(df3)==find_first_header_output_DHO
    assert find_first_header(df4)==find_first_header_output_Intex_ITR_AY
    assert find_first_header(df5)==find_first_header_output_MDMOTOR_ITR
    assert find_first_header(df6)==find_first_header_output_Shruthi_Engg




def test_partner_salary_pos():
    #Decon
    input_dict_psp_Decon = input_.input_dict_psp_Decon
    df_psp_Decon = pd.DataFrame(input_dict_psp_Decon)
    classes_psp_Decon =  input_.input_classes_psp_Decon
    assert partner_salary_pos(df_psp_Decon,classes_psp_Decon) == ('Salary / Remuneration to Partners (Partnership)', 'SALARYTOPARTNER')

    #Shruthi_engg

    input_dict_psp_Shruthi_engg = input_.input_dict_psp_Shruthi_engg
    df_psp_Shruthi_engg = pd.DataFrame(input_dict_psp_Shruthi_engg)
    classes_psp_Shruthi_engg =  input_.input_classes_psp_Shruthi_engg
    assert partner_salary_pos(df_psp_Shruthi_engg,classes_psp_Shruthi_engg) == ('Salary / Remuneration to Partners (Partnership)', 'SALARYTOPARTNER')
    #MD_motors
    input_dict_psp_MD_motors = input_.input_dict_psp_MD_motors
    df_psp_MD_motors = pd.DataFrame(input_dict_psp_MD_motors)
    classes_psp_MD_motors =  input_.input_classes_psp_MD_motors
    assert partner_salary_pos(df_psp_MD_motors,classes_psp_MD_motors) == ('Salary / Remuneration to Partners (Partnership)', 'SALARYTOPARTNER')
    #Credit_Financials38
    input_dict_psp_Cre_Fin38 = input_.input_dict_psp_Cre_Fin38
    df_psp_Cre_Fin38 = pd.DataFrame(input_dict_psp_Cre_Fin38)
    classes_psp_Cre_Fin38 =  input_.input_classes_psp_Cre_Fin38
    assert partner_salary_pos(df_psp_Cre_Fin38,classes_psp_Cre_Fin38) == ('Salary / Remuneration to Partners (Partnership)', 'SALARYTOPARTNER')

    #Intex
    input_dict_psp_Intex = input_.input_dict_psp_Intex
    df_psp_Intex = pd.DataFrame(input_dict_psp_Intex)
    classes_psp_Intex =  input_.input_classes_psp_Intex
    assert partner_salary_pos(df_psp_Intex,classes_psp_Intex) == ('Salary / Remuneration to Partners (Partnership)', 'SALARYTOPARTNER')
    #iyantram
    input_dict_psp_iyantram = input_.input_dict_psp_iyantram
    df_psp_iyantram = pd.DataFrame(input_dict_psp_iyantram)
    classes_psp_iyantram =  input_.input_classes_psp_iyantram
    assert partner_salary_pos(df_psp_iyantram,classes_psp_iyantram) == ('Salary / Remuneration to Partners (Partnership)', 'SALARYTOPARTNER')
    #Credit_Financials25
    input_dict_psp_Cre_Fin25 =input_.input_dict_psp_Cre_Fin25
    df_psp_Cre_Fin25 = pd.DataFrame(input_dict_psp_Cre_Fin25)
    classes_psp_Cre_Fin25 =  input_.input_classes_psp_Cre_Fin25
    assert partner_salary_pos(df_psp_Cre_Fin25,classes_psp_Cre_Fin25) == ('Salary / Remuneration to Partners (Partnership)', 'SALARYTOPARTNER')
    #Dho
    input_dict_psp_Dho = input_.input_dict_psp_Dho
    df_psp_Dho = pd.DataFrame(input_dict_psp_Dho)
    classes_psp_Dho =  input_.input_classes_psp_Dho
    assert partner_salary_pos(df_psp_Dho,classes_psp_Dho) == ('Salary / Remuneration to Partners (Partnership)', 'SALARYTOPARTNER')



def test_partner_capital_pos():
    #Decon
    input_dict_pcp_Decon = input_.input_dict_pcp_Decon
    df_pcp_Decon = pd.DataFrame(input_dict_pcp_Decon)
    classes_pcp_Decon =  input_.input_classes_pcp_Decon
    assert partner_capital_pos(df_pcp_Decon,classes_pcp_Decon) == ('Interest on Capital + Interest Paid on UnSecured Loans', 'INTONCAPITAL')
    #Shruthi_engg

    input_dict_pcp_Shruthi_engg = input_.input_dict_pcp_Shruthi_engg
    df_pcp_Shruthi_engg = pd.DataFrame(input_dict_pcp_Shruthi_engg)
    classes_pcp_Shruthi_engg =  input_.input_classes_pcp_Shruthi_engg
    assert partner_capital_pos(df_pcp_Shruthi_engg,classes_pcp_Shruthi_engg) == ('Interest on Capital + Interest Paid on UnSecured Loans', 'INTONCAPITAL')

    #MD_motors
    input_dict_pcp_MD_motors = input_.input_dict_pcp_MD_motors
    df_pcp_MD_motors = pd.DataFrame(input_dict_pcp_MD_motors)
    classes_pcp_MD_motors =  input_.input_classes_pcp_MD_motors
    assert partner_capital_pos(df_pcp_MD_motors,classes_pcp_MD_motors) == ('Interest on Capital + Interest Paid on UnSecured Loans', 'INTONCAPITAL')
    #Credit_Financials38
    input_dict_pcp_Cre_Fin38 = input_.input_dict_pcp_Cre_Fin38
    df_pcp_Cre_Fin38 = pd.DataFrame(input_dict_pcp_Cre_Fin38)
    classes_pcp_Cre_Fin38 =  input_.input_classes_pcp_Cre_Fin38
    assert partner_capital_pos(df_pcp_Cre_Fin38,classes_pcp_Cre_Fin38) == ('Interest on Capital + Interest Paid on UnSecured Loans', 'INTONCAPITAL')
    #Intex
    input_dict_pcp_Intex = input_.input_dict_pcp_Intex
    df_pcp_Intex = pd.DataFrame(input_dict_pcp_Intex)
    classes_pcp_Intex =  input_.input_classes_pcp_Intex
    assert partner_capital_pos(df_pcp_Intex,classes_pcp_Intex) ==  ('Interest on Capital + Interest Paid on UnSecured Loans', 'INTONCAPITAL')
    #iyantram
    input_dict_pcp_iyantram = input_.input_dict_pcp_iyantram
    df_pcp_iyantram = pd.DataFrame(input_dict_pcp_iyantram)
    classes_pcp_iyantram =  input_.input_classes_pcp_iyantram
    assert partner_capital_pos(df_pcp_iyantram,classes_pcp_iyantram) == ('Interest on Capital + Interest Paid on UnSecured Loans', 'INTONCAPITAL')
    #Credit_Financials25
    input_dict_pcp_Cre_Fin25 = input_.input_dict_pcp_Cre_Fin25
    df_pcp_Cre_Fin25 = pd.DataFrame(input_dict_pcp_Cre_Fin25)
    classes_pcp_Cre_Fin25 =  input_.input_classes_pcp_Cre_Fin25
    assert partner_capital_pos(df_pcp_Cre_Fin25,classes_pcp_Cre_Fin25) == ('Interest on Capital + Interest Paid on UnSecured Loans', 'INTONCAPITAL')
    #Dho
    input_dict_pcp_Dho = input_.input_dict_pcp_Dho
    df_pcp_Dho = pd.DataFrame(input_dict_pcp_Dho)
    classes_pcp_Dho =  input_.input_classes_pcp_Dho
    assert partner_capital_pos(df_pcp_Dho,classes_pcp_Dho) == ('Interest on Capital + Interest Paid on UnSecured Loans', 'INTONCAPITAL')



def test_interest_expense_pos():
     #Decon   

    input_dict_iep_Decon = input_.input_dict_iep_Decon
    df_iep_Decon = pd.DataFrame(input_dict_iep_Decon)
    classes_iep_Decon =  input_.input_classes_iep_Decon
    assert interest_expense_pos(df_iep_Decon,classes_iep_Decon) == ('Interest Expense', 'INTEXPSUB')
    #Shruthi_engg

    input_dict_iep_Shruthi_engg = input_.input_dict_iep_Shruthi_engg
    df_iep_Shruthi_engg = pd.DataFrame(input_dict_iep_Shruthi_engg)
    classes_iep_Shruthi_engg =  input_.input_classes_iep_Shruthi_engg
    assert interest_expense_pos(df_iep_Shruthi_engg,classes_iep_Shruthi_engg) == ('Interest Expense', 'INTEXPSUB')

    #MD_motors
    input_dict_iep_MD_motors = input_.input_dict_iep_MD_motors
    df_iep_MD_motors = pd.DataFrame(input_dict_iep_MD_motors)
    classes_iep_MD_motors =  input_.input_classes_iep_MD_motors
    assert interest_expense_pos(df_iep_MD_motors,classes_iep_MD_motors) == ('Interest Expense', 'INTEXPSUB')
    #Credit_Financials38
    input_dict_iep_Cre_Fin38 = input_.input_dict_iep_Cre_Fin38
    df_iep_Cre_Fin38 = pd.DataFrame(input_dict_iep_Cre_Fin38)
    classes_iep_Cre_Fin38 =  input_.input_classes_iep_Cre_Fin38
    assert interest_expense_pos(df_iep_Cre_Fin38,classes_iep_Cre_Fin38) == ('Interest Expense', 'INTEXPSUB')
    #Intex
    input_dict_iep_Intex = input_.input_dict_iep_Intex
    df_iep_Intex = pd.DataFrame(input_dict_iep_Intex)
    classes_iep_Intex =  input_.input_classes_iep_Intex
    assert interest_expense_pos(df_iep_Intex,classes_iep_Intex) == ('Interest Expense', 'INTEXPSUB')
    #iyantram
    input_dict_iep_iyantram = input_.input_dict_iep_iyantram
    df_iep_iyantram = pd.DataFrame(input_dict_iep_iyantram)
    classes_iep_iyantram =  input_.input_classes_iep_iyantram
    assert interest_expense_pos(df_iep_iyantram,classes_iep_iyantram) == ('Interest Expense', 'INTEXPSUB')
    #Credit_Financials25
    input_dict_iep_Cre_Fin25 = input_.input_dict_iep_Cre_Fin25
    df_iep_Cre_Fin25 = pd.DataFrame(input_dict_iep_Cre_Fin25)
    classes_iep_Cre_Fin25 =  input_.input_classes_iep_Cre_Fin25
    assert interest_expense_pos(df_iep_Cre_Fin25,classes_iep_Cre_Fin25) ==  ('Interest Expense', 'INTEXPSUB')
    #Dho
    input_dict_iep_Dho = input_.input_dict_iep_Dho
    df_iep_Dho = pd.DataFrame(input_dict_iep_Dho)
    classes_iep_Dho =  input_.input_classes_iep_Dho
    assert interest_expense_pos(df_iep_Dho,classes_iep_Dho) == ('Interest Expense', 'INTEXPSUB')



def test_overdraft_pos():
    #Decon

    input_dict_op_Decon = input_.input_dict_op_Decon
    df_op_Decon = pd.DataFrame(input_dict_op_Decon)
    classes_op_Decon =  input_.input_classes_op_Decon
    assert overdraft_pos(df_op_Decon,classes_op_Decon) == ('CC / OD / BD / Packing-Credit / Factoring - Non Current', 'ZZCCSUB2', 'CC / OD / BD / Packing-Credit / Factoring - Current', 'ZZCCSUB1')
    #Shruthi_engg

    input_dict_op_Shruthi_engg = input_.input_dict_op_Shruthi_engg
    df_op_Shruthi_engg = pd.DataFrame(input_dict_op_Shruthi_engg)
    classes_op_Shruthi_engg =  input_.input_classes_op_Shruthi_engg
    assert overdraft_pos(df_op_Shruthi_engg,classes_op_Shruthi_engg) == ('CC / OD / BD / Packing-Credit / Factoring - Non Current', 'ZZCCSUB2', 'CC / OD / BD / Packing-Credit / Factoring - Current', 'ZZCCSUB1')

    #MD_motors
    input_dict_op_MD_motors = input_.input_dict_op_MD_motors
    df_op_MD_motors = pd.DataFrame(input_dict_op_MD_motors)
    classes_op_MD_motors =  input_.input_classes_op_MD_motors
    assert overdraft_pos(df_op_MD_motors,classes_op_MD_motors) == ('CC / OD / BD / Packing-Credit / Factoring - Non Current', 'ZZCCSUB2', 'CC / OD / BD / Packing-Credit / Factoring - Current', 'ZZCCSUB1')
    #Credit_Financials38
    input_dict_op_Cre_Fin38 = input_.input_dict_op_Cre_Fin38
    df_op_Cre_Fin38 = pd.DataFrame(input_dict_op_Cre_Fin38)
    classes_op_Cre_Fin38 =  input_.input_classes_op_Cre_Fin38
    assert overdraft_pos(df_op_Cre_Fin38,classes_op_Cre_Fin38) == ('CC / OD / BD / Packing-Credit / Factoring - Non Current', 'ZZCCSUB2', 'CC / OD / BD / Packing-Credit / Factoring - Current', 'ZZCCSUB1')
    #Intex
    input_dict_op_Intex = input_.input_dict_op_Intex
    df_op_Intex = pd.DataFrame(input_dict_op_Intex)
    classes_op_Intex =  input_.input_classes_op_Intex
    assert overdraft_pos(df_op_Intex,classes_op_Intex) == ('CC / OD / BD / Packing-Credit / Factoring - Non Current', 'ZZCCSUB2', 'CC / OD / BD / Packing-Credit / Factoring - Current', 'ZZCCSUB1')
    #iyantram
    input_dict_op_iyantram = input_.input_dict_op_iyantram
    df_op_iyantram = pd.DataFrame(input_dict_op_iyantram)
    classes_op_iyantram =  input_.input_classes_op_iyantram
    assert overdraft_pos(df_op_iyantram,classes_op_iyantram) == ('CC / OD / BD / Packing-Credit / Factoring - Non Current', 'ZZCCSUB2', 'CC / OD / BD / Packing-Credit / Factoring - Current', 'ZZCCSUB1')
    #Credit_Financials25
    input_dict_op_Cre_Fin25 = input_.input_dict_op_Cre_Fin25
    df_op_Cre_Fin25 = pd.DataFrame(input_dict_op_Cre_Fin25)
    classes_op_Cre_Fin25 =  input_.input_classes_op_Cre_Fin25
    assert overdraft_pos(df_op_Cre_Fin25,classes_op_Cre_Fin25) == ('CC / OD / BD / Packing-Credit / Factoring - Non Current', 'ZZCCSUB2', 'CC / OD / BD / Packing-Credit / Factoring - Current', 'ZZCCSUB1')
    #Dho
    input_dict_op_Dho = input_.input_dict_op_Dho
    df_op_Dho = pd.DataFrame(input_dict_op_Dho)
    classes_op_Dho =  input_.input_classes_op_Dho
    assert overdraft_pos(df_op_Dho,classes_op_Dho) == ('CC / OD / BD / Packing-Credit / Factoring - Non Current', 'ZZCCSUB2', 'CC / OD / BD / Packing-Credit / Factoring - Current', 'ZZCCSUB1')



def test_check_unsecured_loan_previous_immediate_header():
    #Decon
    input_dict_check_unsecured_Decon = input_.input_dict_check_unsecured_Decon
    df_check_unsecured_Decon = pd.DataFrame(input_dict_check_unsecured_Decon)
    assert check_unsecured_loan_previous_immediate_header(df_check_unsecured_Decon,0) == None

    #Shruthi_engg
    input_dict_check_unsecured_Shruthi_engg = input_.input_dict_check_unsecured_Shruthi_engg
    df_check_unsecured_Shruthi_engg = pd.DataFrame(input_dict_check_unsecured_Shruthi_engg)
    assert check_unsecured_loan_previous_immediate_header(df_check_unsecured_Shruthi_engg,1) == None
    #Intex
    input_dict_check_unsecured_Intex = input_.input_dict_check_unsecured_Intex
    df_check_unsecured_Intex = pd.DataFrame(input_dict_check_unsecured_Intex)
    assert check_unsecured_loan_previous_immediate_header(df_check_unsecured_Intex,0) == True
    #iyantram
    input_dict_check_unsecured_iyantram = input_.input_dict_check_unsecured_iyantram
    df_check_unsecured_iyantram = pd.DataFrame(input_dict_check_unsecured_iyantram)
    assert check_unsecured_loan_previous_immediate_header(df_check_unsecured_iyantram,0) == None
    #Credit_Financials25
    input_dict_check_unsecured_Cre_Fin25 = input_.input_dict_check_unsecured_Cre_Fin25
    df_check_unsecured_Cre_Fin25 = pd.DataFrame(input_dict_check_unsecured_Cre_Fin25)
    assert check_unsecured_loan_previous_immediate_header(df_check_unsecured_Cre_Fin25,0) == None
    #Dho
    input_dict_check_unsecured_Dho = input_.input_dict_check_unsecured_Dho
    df_check_unsecured_Dho = pd.DataFrame(input_dict_check_unsecured_Dho)
    assert check_unsecured_loan_previous_immediate_header(df_check_unsecured_Dho,0) == True



def test_BS_mapping_override():
    # # raise TypeError if input is not string
    # with pytest.raises(TypeError):
    #Decon
    assert BS_mapping_override('loan liabilities') == True
    #Shruthi_engg
    assert BS_mapping_override('sundry creditors') == False
    #MD_motors
    assert BS_mapping_override('audit expenses') == False
    #Intex
    assert BS_mapping_override('provisions') == False
    #iyantram
    assert BS_mapping_override('current liabilities') == False
    #Credit_Financials25
    assert BS_mapping_override('total') == False
    #Dho
    assert BS_mapping_override('income tax') == False

def test_BS_mapping():
    #Decon
    data_bs_Decon =  input_.input_data_bs_Decon
    input_dict_balance_sheet_Decon = input_.input_dict_balance_sheet_Decon
    df_balance_sheet_Decon = pd.DataFrame(input_dict_balance_sheet_Decon)
    class_bs_Decon =  input_.input_class_bs_Decon
    assert BS_mapping(data_bs_Decon,df_balance_sheet_Decon,class_bs_Decon) == input_.output_dict_balance_sheet_Decon

    #Shruthi_engg
    data_bs_Shruthi_engg =  input_.input_data_bs_Shruthi_engg
    input_dict_balance_sheet_Shruthi_engg = input_.input_dict_balance_sheet_Shruthi_engg
    df_balance_sheet_Shruthi_engg = pd.DataFrame(input_dict_balance_sheet_Shruthi_engg)
    class_bs_Shruthi_engg =  input_.input_class_bs_Shruthi_engg
    assert BS_mapping(data_bs_Shruthi_engg,df_balance_sheet_Shruthi_engg,class_bs_Shruthi_engg) == input_.output_dict_balance_sheet_Shruthi_engg

    #MD_motors
    data_bs_MD_motors =  input_.input_data_bs_MD_motors
    input_dict_balance_sheet_MD_motors = input_.input_dict_balance_sheet_MD_motors
    df_balance_sheet_MD_motors = pd.DataFrame(input_dict_balance_sheet_MD_motors)
    class_bs_MD_motors =  input_.input_class_bs_MD_motors
    assert BS_mapping(data_bs_MD_motors,df_balance_sheet_MD_motors,class_bs_MD_motors) == input_.output_dict_balance_sheet_MD_motors

    #Intex
    data_bs_Intex =  input_.input_data_bs_Intex
    input_dict_balance_sheet_Intex = input_.input_dict_balance_sheet_Intex
    df_balance_sheet_Intex = pd.DataFrame(input_dict_balance_sheet_Intex)
    class_bs_Intex =  input_.input_class_bs_Intex
    assert BS_mapping(data_bs_Intex,df_balance_sheet_Intex,class_bs_Intex) == input_.output_dict_balance_sheet_Intex

    #Credit_Financials38
    data_bs_Cre_Fin38 =  input_.input_data_bs_Cre_Fin38
    input_dict_balance_sheet_Cre_Fin38 = input_.input_dict_balance_sheet_Cre_Fin38
    df_balance_sheet_Cre_Fin38 = pd.DataFrame(input_dict_balance_sheet_Cre_Fin38)
    class_bs_Cre_Fin38 =  input_.input_class_bs_Cre_Fin38
    assert BS_mapping(data_bs_Cre_Fin38,df_balance_sheet_Cre_Fin38,class_bs_Cre_Fin38) == input_.output_dict_balance_sheet_Cre_Fin38

    #iyantram
    data_bs_iyantram =  input_.input_data_bs_iyantram
    input_dict_balance_sheet_iyantram = input_.input_dict_balance_sheet_iyantram
    df_balance_sheet_iyantram = pd.DataFrame(input_dict_balance_sheet_iyantram)
    class_bs_iyantram =  input_.input_class_bs_iyantram
    assert BS_mapping(data_bs_iyantram,df_balance_sheet_iyantram,class_bs_iyantram) == input_.output_dict_balance_sheet_iyantram

   #Credit_Financials25
    data_bs_Cre_Fin25 =  input_.input_data_bs_Cre_Fin25
    input_dict_balance_sheet_Cre_Fin25 = input_.input_dict_balance_sheet_Cre_Fin25
    df_balance_sheet_Cre_Fin25 = pd.DataFrame(input_dict_balance_sheet_Cre_Fin25)
    class_bs_Cre_Fin25 =  input_.input_class_bs_Cre_Fin25
    assert BS_mapping(data_bs_Cre_Fin25,df_balance_sheet_Cre_Fin25,class_bs_Cre_Fin25) == input_.output_dict_balance_sheet_Cre_Fin25

    #Dho
    data_bs_Dho =  input_.input_data_bs_Dho
    input_dict_balance_sheet_Dho = input_.input_dict_balance_sheet_Dho
    df_balance_sheet_Dho = pd.DataFrame(input_dict_balance_sheet_Dho)
    class_bs_Dho =  input_.input_class_bs_Dho
    assert BS_mapping(data_bs_Dho,df_balance_sheet_Dho,class_bs_Dho) == input_.output_dict_balance_sheet_Dho

        


def test_check_person():
    # raise TypeError if input is not string

    #Decon
    assert check_person('loan liabilities') == False
    #Shruthi_engg
    assert check_person('sundry creditors') == False
    #MD_motors
    assert check_person('audit expenses') == False
    #Intex
    assert check_person('provisions') == False
    #iyantram
    assert check_person('current liabilities') == False
    #Credit_Financials25
    assert check_person('total') == False
    #Dho
    assert check_person('income tax') == False



nan = float("nan")

def test_unsecured_loan_pos():
    input_dict_Credit_Financials25 = input_.input_dict_Credit_Financials25
    df_Credit_Financials25 = pd.DataFrame(input_dict_Credit_Financials25)
    classes_Credit_Financials25 = input_.input_classes_Credit_Financials25

    input_dict_Credit_Financials38 = input_.input_dict_Credit_Financials38
    df_Credit_Financials38 = pd.DataFrame(input_dict_Credit_Financials38)
    classes_Credit_Financials38 = input_.input_classes_Credit_Financials38

    input_dict_Decon = input_.input_dict_Decon
    df_Decon = pd.DataFrame(input_dict_Decon)
    classes_Decon = input_.input_classes_Decon

    input_dict_DHO = input_.input_dict_DHO
    df_DHO = pd.DataFrame(input_dict_DHO)
    classes_DHO = input_.input_classes_DHO

    input_dict_Intex = input_.input_dict_Intex
    df_Intex = pd.DataFrame(input_dict_Intex)
    classes_Intex = input_.input_classes_Intex

    input_dict_iyantram = input_.input_dict_iyantram
    df_iyantram = pd.DataFrame(input_dict_iyantram)
    classes_iyantram = input_.input_classes_iyantram

    input_dict_MDMotor = input_.input_dict_MDMotor
    df_MDMotor = pd.DataFrame(input_dict_MDMotor)
    classes_MDMotor = input_.input_classes_MDMotor

    input_dict_Shruthi = input_.input_dict_Shruthi
    df_Shruthi = pd.DataFrame(input_dict_Shruthi)
    classes_Shruthi = input_.input_classes_Shruthi
    assert unsecured_loan_pos(df_Credit_Financials25,classes_Credit_Financials25) == ('Borrowings Refundable with / without Interest', 'BORROWREFUND')
    assert unsecured_loan_pos(df_Credit_Financials38,classes_Credit_Financials38) == ('Borrowings Refundable with / without Interest', 'BORROWREFUND')
    assert unsecured_loan_pos(df_Decon,classes_Decon) == ('Borrowings Refundable with / without Interest', 'BORROWREFUND')
    assert unsecured_loan_pos(df_DHO,classes_DHO) == ('Borrowings Refundable with / without Interest', 'BORROWREFUND')
    assert unsecured_loan_pos(df_Intex,classes_Intex) == ('Borrowings Refundable with / without Interest', 'BORROWREFUND')
    assert unsecured_loan_pos(df_iyantram,classes_iyantram) == ('Borrowings Refundable with / without Interest', 'BORROWREFUND')
    assert unsecured_loan_pos(df_MDMotor,classes_MDMotor) == ('Borrowings Refundable with / without Interest', 'BORROWREFUND')
    assert unsecured_loan_pos(df_Shruthi,classes_Shruthi) == ('Borrowings Refundable with / without Interest', 'BORROWREFUND')



def test_other_fixed_asset_pos():
    input_dict_Credit_Financials25 = input_.input_dict_Credit_Financials25
    df_Credit_Financials25 = pd.DataFrame(input_dict_Credit_Financials25)
    classes_Credit_Financials25 = input_.input_classes_Credit_Financials25

    input_dict_Credit_Financials38 = input_.input_dict_Credit_Financials38
    df_Credit_Financials38 = pd.DataFrame(input_dict_Credit_Financials38)
    classes_Credit_Financials38 = input_.input_classes_Credit_Financials38

    input_dict_Decon = input_.input_dict_Decon
    df_Decon = pd.DataFrame(input_dict_Decon)
    classes_Decon = input_.input_classes_Decon

    input_dict_DHO = input_.input_dict_DHO
    df_DHO = pd.DataFrame(input_dict_DHO)
    classes_DHO = input_.input_classes_DHO

    input_dict_Intex = input_.input_dict_Intex
    df_Intex = pd.DataFrame(input_dict_Intex)
    classes_Intex = input_.input_classes_Intex

    input_dict_iyantram = input_.input_dict_iyantram
    df_iyantram = pd.DataFrame(input_dict_iyantram)
    classes_iyantram = input_.input_classes_iyantram

    input_dict_MDMotor = input_.input_dict_MDMotor
    df_MDMotor = pd.DataFrame(input_dict_MDMotor)
    classes_MDMotor = input_.input_classes_MDMotor

    input_dict_Shruthi = input_.input_dict_Shruthi
    df_Shruthi = pd.DataFrame(input_dict_Shruthi)
    classes_Shruthi = input_.input_classes_Shruthi
    assert other_fixed_asset_pos(df_Credit_Financials25,classes_Credit_Financials25) == ('Other Fixed Assets (Net Block)', 'OTHRFA')
    assert other_fixed_asset_pos(df_Credit_Financials38,classes_Credit_Financials38) == ('Other Fixed Assets (Net Block)', 'OTHRFA')
    assert other_fixed_asset_pos(df_Decon,classes_Decon) == ('Other Fixed Assets (Net Block)', 'OTHRFA')
    assert other_fixed_asset_pos(df_DHO,classes_DHO) == ('Other Fixed Assets (Net Block)', 'OTHRFA')
    assert other_fixed_asset_pos(df_Intex,classes_Intex) == ('Other Fixed Assets (Net Block)', 'OTHRFA')
    assert other_fixed_asset_pos(df_iyantram,classes_iyantram) == ('Other Fixed Assets (Net Block)', 'OTHRFA')
    assert other_fixed_asset_pos(df_MDMotor,classes_MDMotor) == ('Other Fixed Assets (Net Block)', 'OTHRFA')
    assert other_fixed_asset_pos(df_Shruthi,classes_Shruthi) == ('Other Fixed Assets (Net Block)', 'OTHRFA')

def test_cash_bank_pos():
    input_dict_Credit_Financials25 = input_.input_dict_Credit_Financials25
    df_Credit_Financials25 = pd.DataFrame(input_dict_Credit_Financials25)
    classes_Credit_Financials25 = input_.input_classes_Credit_Financials25

    input_dict_Credit_Financials38 = input_.input_dict_Credit_Financials38
    df_Credit_Financials38 = pd.DataFrame(input_dict_Credit_Financials38)
    classes_Credit_Financials38 = input_.input_classes_Credit_Financials38

    input_dict_Decon = input_.input_dict_Decon
    df_Decon = pd.DataFrame(input_dict_Decon)
    classes_Decon = input_.input_classes_Decon

    input_dict_DHO = input_.input_dict_DHO
    df_DHO = pd.DataFrame(input_dict_DHO)
    classes_DHO = input_.input_classes_DHO

    input_dict_Intex = input_.input_dict_Intex
    df_Intex = pd.DataFrame(input_dict_Intex)
    classes_Intex = input_.input_classes_Intex

    input_dict_iyantram = input_.input_dict_iyantram
    df_iyantram = pd.DataFrame(input_dict_iyantram)
    classes_iyantram = input_.input_classes_iyantram

    input_dict_MDMotor = input_.input_dict_MDMotor
    df_MDMotor = pd.DataFrame(input_dict_MDMotor)
    classes_MDMotor = input_.input_classes_MDMotor

    input_dict_Shruthi = input_.input_dict_Shruthi
    df_Shruthi = pd.DataFrame(input_dict_Shruthi)
    classes_Shruthi = input_.input_classes_Shruthi
    assert cash_bank_pos(df_Credit_Financials25,classes_Credit_Financials25) == ('Cash & Bank Balance', 'CASH')
    assert cash_bank_pos(df_Credit_Financials38,classes_Credit_Financials38) == ('Cash & Bank Balance', 'CASH')
    assert cash_bank_pos(df_Decon,classes_Decon) == ('Cash & Bank Balance', 'CASH')
    assert cash_bank_pos(df_DHO,classes_DHO) == ('Cash & Bank Balance', 'CASH')
    assert cash_bank_pos(df_Intex,classes_Intex) == ('Cash & Bank Balance', 'CASH')
    assert cash_bank_pos(df_iyantram,classes_iyantram) == ('Cash & Bank Balance', 'CASH')
    assert cash_bank_pos(df_MDMotor,classes_MDMotor) == ('Cash & Bank Balance', 'CASH')
    assert cash_bank_pos(df_Shruthi,classes_Shruthi) == ('Cash & Bank Balance', 'CASH')

def test_ownmoney_pos():
    input_dict_Credit_Financials25 = input_.input_dict_Credit_Financials25
    df_Credit_Financials25 = pd.DataFrame(input_dict_Credit_Financials25)
    classes_Credit_Financials25 = input_.input_classes_Credit_Financials25

    input_dict_Credit_Financials38 = input_.input_dict_Credit_Financials38
    df_Credit_Financials38 = pd.DataFrame(input_dict_Credit_Financials38)
    classes_Credit_Financials38 = input_.input_classes_Credit_Financials38

    input_dict_Decon = input_.input_dict_Decon
    df_Decon = pd.DataFrame(input_dict_Decon)
    classes_Decon = input_.input_classes_Decon

    input_dict_DHO = input_.input_dict_DHO
    df_DHO = pd.DataFrame(input_dict_DHO)
    classes_DHO = input_.input_classes_DHO

    input_dict_Intex = input_.input_dict_Intex
    df_Intex = pd.DataFrame(input_dict_Intex)
    classes_Intex = input_.input_classes_Intex

    input_dict_iyantram = input_.input_dict_iyantram
    df_iyantram = pd.DataFrame(input_dict_iyantram)
    classes_iyantram = input_.input_classes_iyantram

    input_dict_MDMotor = input_.input_dict_MDMotor
    df_MDMotor = pd.DataFrame(input_dict_MDMotor)
    classes_MDMotor = input_.input_classes_MDMotor

    input_dict_Shruthi = input_.input_dict_Shruthi
    df_Shruthi = pd.DataFrame(input_dict_Shruthi)
    classes_Shruthi = input_.input_classes_Shruthi
    assert ownmoney_pos(df_Credit_Financials25,classes_Credit_Financials25) == ('Own Money ', 'OWNMONEY')
    assert ownmoney_pos(df_Credit_Financials38,classes_Credit_Financials38) == ('Own Money ', 'OWNMONEY')
    assert ownmoney_pos(df_Decon,classes_Decon) == ('Own Money ', 'OWNMONEY')
    assert ownmoney_pos(df_DHO,classes_DHO) == ('Own Money ', 'OWNMONEY')
    assert ownmoney_pos(df_Intex,classes_Intex) == ('Own Money ', 'OWNMONEY')
    assert ownmoney_pos(df_iyantram,classes_iyantram) == ('Own Money ', 'OWNMONEY')
    assert ownmoney_pos(df_MDMotor,classes_MDMotor) == ('Own Money ', 'OWNMONEY')
    assert ownmoney_pos(df_Shruthi,classes_Shruthi) == ('Own Money ', 'OWNMONEY')

def test_land_pos():
    input_dict_Credit_Financials25 = input_.input_dict_Credit_Financials25
    df_Credit_Financials25 = pd.DataFrame(input_dict_Credit_Financials25)
    classes_Credit_Financials25 = input_.input_classes_Credit_Financials25

    input_dict_Credit_Financials38 = input_.input_dict_Credit_Financials38
    df_Credit_Financials38 = pd.DataFrame(input_dict_Credit_Financials38)
    classes_Credit_Financials38 = input_.input_classes_Credit_Financials38

    input_dict_Decon = input_.input_dict_Decon
    df_Decon = pd.DataFrame(input_dict_Decon)
    classes_Decon = input_.input_classes_Decon

    input_dict_DHO = input_.input_dict_DHO
    df_DHO = pd.DataFrame(input_dict_DHO)
    classes_DHO = input_.input_classes_DHO

    input_dict_Intex = input_.input_dict_Intex
    df_Intex = pd.DataFrame(input_dict_Intex)
    classes_Intex = input_.input_classes_Intex

    input_dict_iyantram = input_.input_dict_iyantram
    df_iyantram = pd.DataFrame(input_dict_iyantram)
    classes_iyantram = input_.input_classes_iyantram

    input_dict_MDMotor = input_.input_dict_MDMotor
    df_MDMotor = pd.DataFrame(input_dict_MDMotor)
    classes_MDMotor = input_.input_classes_MDMotor

    input_dict_Shruthi = input_.input_dict_Shruthi
    df_Shruthi = pd.DataFrame(input_dict_Shruthi)
    classes_Shruthi = input_.input_classes_Shruthi
    assert land_pos(df_Credit_Financials25,classes_Credit_Financials25) == ('Land and Building / Property', 'LANDSUB')
    assert land_pos(df_Credit_Financials38,classes_Credit_Financials38) == ('Land and Building / Property', 'LANDSUB')
    assert land_pos(df_Decon,classes_Decon) == ('Land and Building / Property', 'LANDSUB')
    assert land_pos(df_DHO,classes_DHO) == ('Land and Building / Property', 'LANDSUB')
    assert land_pos(df_Intex,classes_Intex) == ('Land and Building / Property', 'LANDSUB')
    assert land_pos(df_iyantram,classes_iyantram) == ('Land and Building / Property', 'LANDSUB')
    assert land_pos(df_MDMotor,classes_MDMotor) == ('Land and Building / Property', 'LANDSUB')
    assert land_pos(df_Shruthi,classes_Shruthi) == ('Land and Building / Property', 'LANDSUB')

def test_capitalacc_pos():
    input_dict_Credit_Financials25 = input_.input_dict_Credit_Financials25
    df_Credit_Financials25 = pd.DataFrame(input_dict_Credit_Financials25)
    classes_Credit_Financials25 = input_.input_classes_Credit_Financials25

    input_dict_Credit_Financials38 = input_.input_dict_Credit_Financials38
    df_Credit_Financials38 = pd.DataFrame(input_dict_Credit_Financials38)
    classes_Credit_Financials38 = input_.input_classes_Credit_Financials38

    input_dict_Decon = input_.input_dict_Decon
    df_Decon = pd.DataFrame(input_dict_Decon)
    classes_Decon = input_.input_classes_Decon

    input_dict_DHO = input_.input_dict_DHO
    df_DHO = pd.DataFrame(input_dict_DHO)
    classes_DHO = input_.input_classes_DHO

    input_dict_Intex = input_.input_dict_Intex
    df_Intex = pd.DataFrame(input_dict_Intex)
    classes_Intex = input_.input_classes_Intex

    input_dict_iyantram = input_.input_dict_iyantram
    df_iyantram = pd.DataFrame(input_dict_iyantram)
    classes_iyantram = input_.input_classes_iyantram

    input_dict_MDMotor = input_.input_dict_MDMotor
    df_MDMotor = pd.DataFrame(input_dict_MDMotor)
    classes_MDMotor = input_.input_classes_MDMotor

    input_dict_Shruthi = input_.input_dict_Shruthi
    df_Shruthi = pd.DataFrame(input_dict_Shruthi)
    classes_Shruthi = input_.input_classes_Shruthi
    assert capitalacc_pos(df_Credit_Financials25,classes_Credit_Financials25) == ('Capital Account (Prop/Partnership/Company)', 'CAPAC')
    assert capitalacc_pos(df_Credit_Financials38,classes_Credit_Financials38) == ('Capital Account (Prop/Partnership/Company)', 'CAPAC')
    assert capitalacc_pos(df_Decon,classes_Decon) == ('Capital Account (Prop/Partnership/Company)', 'CAPAC')
    assert capitalacc_pos(df_DHO,classes_DHO) == ('Capital Account (Prop/Partnership/Company)', 'CAPAC')
    assert capitalacc_pos(df_Intex,classes_Intex) == ('Capital Account (Prop/Partnership/Company)', 'CAPAC')
    assert capitalacc_pos(df_iyantram,classes_iyantram) == ('Capital Account (Prop/Partnership/Company)', 'CAPAC')
    assert capitalacc_pos(df_MDMotor,classes_MDMotor) == ('Capital Account (Prop/Partnership/Company)', 'CAPAC')
    assert capitalacc_pos(df_Shruthi,classes_Shruthi) == ('Capital Account (Prop/Partnership/Company)', 'CAPAC')

def test_check_calculatedf_scenario():
    input_dict_check_calculatedf_scenario_Credit_Financials38 = input_.input_check_calculatedf_scenario_data_Credit_Financials38
    data_Credit_Financials38 = pd.DataFrame(input_dict_check_calculatedf_scenario_Credit_Financials38)
    assert check_calculatedf_scenario(data_Credit_Financials38) == 0
    input_dict_check_calculatedf_scenario_Credit_Financials25 = input_.input_check_calculatedf_scenario_data_Credit_Financials25
    data_Credit_Financials25 = pd.DataFrame(input_dict_check_calculatedf_scenario_Credit_Financials25)
    assert check_calculatedf_scenario(data_Credit_Financials25) == 0
    input_dict_check_calculatedf_scenario_Decon = input_.input_check_calculatedf_scenario_data_Decon
    data_Decon = pd.DataFrame(input_dict_check_calculatedf_scenario_Decon)
    assert check_calculatedf_scenario(data_Decon) == 2
    input_dict_check_calculatedf_scenario_DHO = input_.input_check_calculatedf_scenario_data_DHO
    data_DHO = pd.DataFrame(input_dict_check_calculatedf_scenario_DHO)
    assert check_calculatedf_scenario(data_DHO) == 0
    input_dict_check_calculatedf_scenario_Intex = input_.input_check_calculatedf_scenario_data_Intex
    data_Intex = pd.DataFrame(input_dict_check_calculatedf_scenario_Intex)
    assert check_calculatedf_scenario(data_Intex) == 1
    input_dict_check_calculatedf_scenario_Iyantram = input_.input_check_calculatedf_scenario_data_iyantram
    data_Iyantram = pd.DataFrame(input_dict_check_calculatedf_scenario_Iyantram)
    assert check_calculatedf_scenario(data_Iyantram) == 2
    input_dict_check_calculatedf_scenario_MDMotor = input_.input_check_calculatedf_scenario_data_MDMotor
    data_MDMotor = pd.DataFrame(input_dict_check_calculatedf_scenario_MDMotor)
    assert check_calculatedf_scenario(data_MDMotor) == 0    
    input_dict_check_calculatedf_scenario_Shruthi = input_.input_check_calculatedf_scenario_data_Shruthi
    data_Shruthi = pd.DataFrame(input_dict_check_calculatedf_scenario_Shruthi)
    assert check_calculatedf_scenario(data_Shruthi) == 0


def test_calculated_field_is():
    input_calculated_field_is_DATA_Credit_Financials38 = input_.input_calculated_field_is_DATA_Credit_Financials38
    input_calculated_field_is_income_statement_cls_Credit_Financials38 = input_.input_calculated_field_is_income_statement_cls_Credit_Financials38
    output_calculated_field_is_Credit_Financials38 = input_.output_calculated_field_is_Credit_Financials38
    assert calculated_field_is(input_calculated_field_is_DATA_Credit_Financials38,input_calculated_field_is_income_statement_cls_Credit_Financials38) == output_calculated_field_is_Credit_Financials38
    
    input_calculated_field_is_DATA_Credit_Financials25 = input_.input_calculated_field_is_DATA_Credit_Financials25
    input_calculated_field_is_income_statement_cls_Credit_Financials25 = input_.input_calculated_field_is_income_statement_cls_Credit_Financials25
    output_calculated_field_is_Credit_Financials25 = input_.output_calculated_field_is_Credit_Financials25
    assert calculated_field_is(input_calculated_field_is_DATA_Credit_Financials25,input_calculated_field_is_income_statement_cls_Credit_Financials25) == output_calculated_field_is_Credit_Financials25
    
    input_calculated_field_is_DATA_Decon = input_.input_calculated_field_is_DATA_Decon
    input_calculated_field_is_income_statement_cls_Decon = input_.input_calculated_field_is_income_statement_cls_Decon
    output_calculated_field_is_Decon = input_.output_calculated_field_is_Decon
    assert calculated_field_is(input_calculated_field_is_DATA_Decon,input_calculated_field_is_income_statement_cls_Decon) == output_calculated_field_is_Decon
    
    input_calculated_field_is_DATA_DHO = input_.input_calculated_field_is_DATA_DHO
    input_calculated_field_is_income_statement_cls_DHO = input_.input_calculated_field_is_income_statement_cls_DHO
    output_calculated_field_is_DHO = input_.output_calculated_field_is_DHO
    assert calculated_field_is(input_calculated_field_is_DATA_DHO,input_calculated_field_is_income_statement_cls_DHO) == output_calculated_field_is_DHO
    
    input_calculated_field_is_DATA_Intex = input_.input_calculated_field_is_DATA_Intex
    input_calculated_field_is_income_statement_cls_Intex = input_.input_calculated_field_is_income_statement_cls_Intex
    output_calculated_field_is_Intex = input_.output_calculated_field_is_Intex
    assert calculated_field_is(input_calculated_field_is_DATA_Intex,input_calculated_field_is_income_statement_cls_Intex) == output_calculated_field_is_Intex

    input_calculated_field_is_DATA_Iyantram = input_.input_calculated_field_is_DATA_iyantram
    input_calculated_field_is_income_statement_cls_Iyantram = input_.input_calculated_field_is_income_statement_cls_iyantram
    output_calculated_field_is_Iyantram = input_.output_calculated_field_is_iyantram
    assert calculated_field_is(input_calculated_field_is_DATA_Iyantram,input_calculated_field_is_income_statement_cls_Iyantram) == output_calculated_field_is_Iyantram

    input_calculated_field_is_DATA_MDMotor = input_.input_calculated_field_is_DATA_MDMotor
    input_calculated_field_is_income_statement_cls_MDMotor = input_.input_calculated_field_is_income_statement_cls_MDMotor
    output_calculated_field_is_MDMotor = input_.output_calculated_field_is_MDMotor
    assert calculated_field_is(input_calculated_field_is_DATA_MDMotor,input_calculated_field_is_income_statement_cls_MDMotor) == output_calculated_field_is_MDMotor
    
    input_calculated_field_is_DATA_Shruthi = input_.input_calculated_field_is_DATA_Shruthi
    input_calculated_field_is_income_statement_cls_Shruthi = input_.input_calculated_field_is_income_statement_cls_Shruthi
    output_calculated_field_is_Shruthi = input_.output_calculated_field_is_Shruthi
    assert calculated_field_is(input_calculated_field_is_DATA_Shruthi,input_calculated_field_is_income_statement_cls_Shruthi) == output_calculated_field_is_Shruthi
    
def test_salary_wages_mapping():
    input_salary_wages_mapping_template_code_Credit_Financials38 = 'T_SC_EFL_SME'
    input_salary_wages_mapping_new_Credit_Financials38 = 'p'
    assert salary_wages_mapping(input_salary_wages_mapping_template_code_Credit_Financials38,input_salary_wages_mapping_new_Credit_Financials38) == True
    input_salary_wages_mapping_template_code_Credit_Financials25 = 'T_SC_EFL_SME'
    input_salary_wages_mapping_new_Credit_Financials25 = 'to purchase'
    assert salary_wages_mapping(input_salary_wages_mapping_template_code_Credit_Financials25,input_salary_wages_mapping_new_Credit_Financials25) == True
    input_salary_wages_mapping_template_code_Decon = 'T_SC_EFL_SME'
    input_salary_wages_mapping_new_Decon = 'less: closing stock'
    assert salary_wages_mapping(input_salary_wages_mapping_template_code_Decon,input_salary_wages_mapping_new_Decon) == True
    input_salary_wages_mapping_template_code_DHO = 'T_SC_EFL_SME'
    input_salary_wages_mapping_new_DHO = 'by share profit from partnership fim'
    assert salary_wages_mapping(input_salary_wages_mapping_template_code_DHO,input_salary_wages_mapping_new_DHO) == True
    input_salary_wages_mapping_template_code_Intex = 'T_SC_EFL_SME'
    input_salary_wages_mapping_new_Intex = 'to bank charges'
    assert salary_wages_mapping(input_salary_wages_mapping_template_code_Intex,input_salary_wages_mapping_new_Intex) == True
    input_salary_wages_mapping_template_code_Iyantram = 'T_SC_EFL_SME'
    input_salary_wages_mapping_new_Iyantram = 'add: indirect incomes'
    assert salary_wages_mapping(input_salary_wages_mapping_template_code_Iyantram,input_salary_wages_mapping_new_Iyantram) == True
    input_salary_wages_mapping_template_code_MDMotor = 'T_SC_EFL_SME'
    input_salary_wages_mapping_new_MDMotor = 'to depreciations'
    assert salary_wages_mapping(input_salary_wages_mapping_template_code_MDMotor,input_salary_wages_mapping_new_MDMotor) == True
    input_salary_wages_mapping_template_code_Shruthi = 'T_SC_EFL_SME'
    input_salary_wages_mapping_new_Shruthi = 'to interest & charges'
    assert salary_wages_mapping(input_salary_wages_mapping_template_code_Shruthi,input_salary_wages_mapping_new_Shruthi) == True


def test_signage_inner_outer():
    input_signage_inner_outer_new_df_Credit_Financials38 = 'inner'
    input_signage_inner_outer_match_Credit_Financials38 = 2
    input_signage_inner_outer_is_data_Credit_Financials38 = 1
    assert signage_inner_outer(input_signage_inner_outer_new_df_Credit_Financials38,input_signage_inner_outer_match_Credit_Financials38,input_signage_inner_outer_is_data_Credit_Financials38) == True
    input_signage_inner_outer_new_df_Credit_Financials25 = 'inner'
    input_signage_inner_outer_match_Credit_Financials25 = 10
    input_signage_inner_outer_is_data_Credit_Financials25 = 17
    assert signage_inner_outer(input_signage_inner_outer_new_df_Credit_Financials25,input_signage_inner_outer_match_Credit_Financials25,input_signage_inner_outer_is_data_Credit_Financials25) == True
    input_signage_inner_outer_new_df_Decon = 'inner'
    input_signage_inner_outer_match_Decon = 5
    input_signage_inner_outer_is_data_Decon = 14
    assert signage_inner_outer(input_signage_inner_outer_new_df_Decon,input_signage_inner_outer_match_Decon,input_signage_inner_outer_is_data_Decon) == True
    input_signage_inner_outer_new_df_DHO = 'inner'
    input_signage_inner_outer_match_DHO = 7
    input_signage_inner_outer_is_data_DHO = 70
    assert signage_inner_outer(input_signage_inner_outer_new_df_DHO,input_signage_inner_outer_match_DHO,input_signage_inner_outer_is_data_DHO) == True
    input_signage_inner_outer_new_df_Intex = 'outer'
    input_signage_inner_outer_match_Intex = 8
    input_signage_inner_outer_is_data_Intex = 30
    assert signage_inner_outer(input_signage_inner_outer_new_df_Intex,input_signage_inner_outer_match_Intex,input_signage_inner_outer_is_data_Intex) == False
    input_signage_inner_outer_new_df_Iyantram = 'outer'
    input_signage_inner_outer_match_Iyantram = 0
    input_signage_inner_outer_is_data_Iyantram = 14
    assert signage_inner_outer(input_signage_inner_outer_new_df_Iyantram,input_signage_inner_outer_match_Iyantram,input_signage_inner_outer_is_data_Iyantram) == False
    input_signage_inner_outer_new_df_MDMotor = 'inner'
    input_signage_inner_outer_match_MDMotor = 30
    input_signage_inner_outer_is_data_MDMotor = 41
    assert signage_inner_outer(input_signage_inner_outer_new_df_MDMotor,input_signage_inner_outer_match_MDMotor,input_signage_inner_outer_is_data_MDMotor) == True
    input_signage_inner_outer_new_df_Shruthi = 'inner'
    input_signage_inner_outer_match_Shruthi = 8
    input_signage_inner_outer_is_data_Shruthi = 17
    assert signage_inner_outer(input_signage_inner_outer_new_df_Shruthi,input_signage_inner_outer_match_Shruthi,input_signage_inner_outer_is_data_Shruthi) == True

def test_check_person_2():
    input_check_person_2_Credit_Financials38 = 'p'
    assert check_person_2(input_check_person_2_Credit_Financials38) == []
    input_check_person_2_Credit_Financials25 = 'by constructiorn'
    assert check_person_2(input_check_person_2_Credit_Financials25) == ['constructiorn']
    input_check_person_2_Decon = 'net profit loss carried to balance sheet'
    assert check_person_2(input_check_person_2_Decon) == []
    input_check_person_2_DHO = 'to rounding off'
    assert check_person_2(input_check_person_2_DHO) == []
    input_check_person_2_Intex = 'to salary bharat khawale'
    assert check_person_2(input_check_person_2_Intex) == ['khawale']
    input_check_person_2_Iyantram = 'net profit loss carried to balance sheet'
    assert check_person_2(input_check_person_2_Iyantram) == []
    input_check_person_2_MDMotor = 'to a machine'
    assert check_person_2(input_check_person_2_MDMotor) == []
    input_check_person_2_Shruthi = 'to television set'
    assert check_person_2(input_check_person_2_Shruthi) == []
    
# def test_IS_mapping():
#     input_IS_mapping_DATA_Credit_Financials25 = input_.input_IS_mapping_DATA_Credit_Financials25
#     input_df_temp_dict_Credit_Financials25 = input_.input_df_temp_dict_Credit_Financials25
#     df_temp = pd.DataFrame(input_df_temp_dict_Credit_Financials25)
#     input_IS_mapping_income_statement_cls_Credit_Financials25 = input_.input_IS_mapping_income_statement_cls_Credit_Financials25
#     assert IS_mapping(input_IS_mapping_DATA_Credit_Financials25,df_temp,input_IS_mapping_income_statement_cls_Credit_Financials25) == input_.output_IS_mapping_Credit_Financials25
    
#     input_IS_mapping_DATA_Credit_Financials38 = input_.input_IS_mapping_DATA_Credit_Financials38
#     input_df_temp_dict_Credit_Financials38 = input_.input_df_temp_dict_Credit_Financials38
#     df_temp = pd.DataFrame(input_df_temp_dict_Credit_Financials38)
#     input_IS_mapping_income_statement_cls_Credit_Financials38 = input_.input_IS_mapping_income_statement_cls_Credit_Financials38
#     assert IS_mapping(input_IS_mapping_DATA_Credit_Financials38,df_temp,input_IS_mapping_income_statement_cls_Credit_Financials38) == input_.output_IS_mapping_Credit_Financials38
    
#     input_IS_mapping_DATA_Decon = input_.input_IS_mapping_DATA_Decon
#     input_df_temp_dict_Decon = input_.input_df_temp_dict_Decon
#     df_temp = pd.DataFrame(input_df_temp_dict_Decon)
#     input_IS_mapping_income_statement_cls_Decon = input_.input_IS_mapping_income_statement_cls_Decon
#     assert IS_mapping(input_IS_mapping_DATA_Decon,df_temp,input_IS_mapping_income_statement_cls_Decon) == input_.output_IS_mapping_Decon
    
#     input_IS_mapping_DATA_DHO = input_.input_IS_mapping_DATA_DHO
#     input_df_temp_dict_DHO = input_.input_df_temp_dict_DHO
#     df_temp = pd.DataFrame(input_df_temp_dict_DHO)
#     input_IS_mapping_income_statement_cls_DHO = input_.input_IS_mapping_income_statement_cls_DHO
#     assert IS_mapping(input_IS_mapping_DATA_DHO,df_temp,input_IS_mapping_income_statement_cls_DHO) == input_.output_IS_mapping_DHO

#     input_IS_mapping_DATA_Intex = input_.input_IS_mapping_DATA_Intex
#     input_df_temp_dict_Intex = input_.input_df_temp_dict_Intex
#     df_temp = pd.DataFrame(input_df_temp_dict_Intex)
#     input_IS_mapping_income_statement_cls_Intex = input_.input_IS_mapping_income_statement_cls_Intex
#     assert IS_mapping(input_IS_mapping_DATA_Intex,df_temp,input_IS_mapping_income_statement_cls_Intex) == input_.output_IS_mapping_Intex

#     input_IS_mapping_DATA_Iyantram = input_.input_IS_mapping_DATA_Iyantram
#     input_df_temp_dict_Iyantram = input_.input_df_temp_dict_Iyantram
#     df_temp = pd.DataFrame(input_df_temp_dict_Iyantram)
#     input_IS_mapping_income_statement_cls_Iyantram = input_.input_IS_mapping_income_statement_cls_Iyantram
#     assert IS_mapping(input_IS_mapping_DATA_Iyantram,df_temp,input_IS_mapping_income_statement_cls_Iyantram) == input_.output_IS_mapping_Iyantram

#     input_IS_mapping_DATA_MDMotor = input_.input_IS_mapping_DATA_MDMotor
#     input_df_temp_dict_MDMotor = input_.input_df_temp_dict_MDMotor
#     df_temp = pd.DataFrame(input_df_temp_dict_MDMotor)
#     input_IS_mapping_income_statement_cls_MDMotor = input_.input_IS_mapping_income_statement_cls_MDMotor
#     assert IS_mapping(input_IS_mapping_DATA_MDMotor,df_temp,input_IS_mapping_income_statement_cls_MDMotor) == input_.output_IS_mapping_MDMotor

#     input_IS_mapping_DATA_Shruthi = input_.input_IS_mapping_DATA_Shruthi
#     input_df_temp_dict_Shruthi = input_.input_df_temp_dict_Shruthi
#     df_temp = pd.DataFrame(input_df_temp_dict_Shruthi)
#     input_IS_mapping_income_statement_cls_Shruthi = input_.input_IS_mapping_income_statement_cls_Shruthi
#     assert IS_mapping(input_IS_mapping_DATA_Shruthi,df_temp,input_IS_mapping_income_statement_cls_Shruthi) == input_.output_IS_mapping_Shruthi


