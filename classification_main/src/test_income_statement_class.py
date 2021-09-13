from income_statement_class import *
import pandas as pd
import pytest
import income_statement_class
import input_
from input_ import *






def test_convert_income_statement():
    # raise TypeError if input is not dictionary.
    with pytest.raises(TypeError):
        convert_income_statement(0)
        convert_income_statement(4.0)
        convert_income_statement([1, 2])
        convert_income_statement('xyz')

    convert_income_statement_input_MDMOTOR = input_.convert_income_statement_input_MDMOTOR_ITR_2017_18
    convert_income_statement_output_MDMOTOR = input_.convert_income_statement_output_MDMOTOR_ITR_2017_18
    convert_income_statement_input_Credit_Financials25 = input_.convert_income_statement_input_Credit_Financials25_T_Format_Poor_Quality
    convert_income_statement_output_Credit_Financials25 = input_.convert_income_statement_output_Credit_Financials25_T_Format_Poor_Quality
    convert_income_statement_input_Intex_ITR = input_.convert_income_statement_input_Intex_ITR_AY_19_20
    convert_income_statement_output_Intex_ITR = input_.convert_income_statement_output_Intex_ITR_AY_19_20
    convert_income_statement_input_DHO = input_.convert_income_statement_input_DHO
    convert_income_statement_output_DHO = input_.convert_income_statement_output_DHO
    convert_income_statement_input_Shruthi = input_.convert_income_statement_input_Shruthi_Engg_19_20
    convert_income_statement_output_Shruthi = input_.convert_income_statement_output_Shruthi_Engg_19_20
    convert_income_statement_input_Credit_Financial38 = input_.convert_income_statement_input_Credit_Financials38 
    convert_income_statement_output_Credit_Financial38 = input_.convert_income_statement_output_Credit_Financials38
    convert_income_statement_input_Decon = input_.convert_income_statement_input_Decon
    convert_income_statement_output_Decon = input_.convert_income_statement_output_Decon
    convert_income_statement_input_iyantram = input_.convert_income_statement_input_iyantram19
    convert_income_statement_output_iyantram = input_.convert_income_statement_output_iyantram19

    assert convert_income_statement(convert_income_statement_input_MDMOTOR) == convert_income_statement_output_MDMOTOR
    assert convert_income_statement(convert_income_statement_input_Credit_Financials25) == convert_income_statement_output_Credit_Financials25
    assert convert_income_statement(convert_income_statement_input_Intex_ITR) == convert_income_statement_output_Intex_ITR
    assert convert_income_statement(convert_income_statement_input_DHO) == convert_income_statement_output_DHO
    assert convert_income_statement(convert_income_statement_input_Shruthi) == convert_income_statement_output_Shruthi
    assert convert_income_statement(convert_income_statement_input_Credit_Financial38) == convert_income_statement_output_Credit_Financial38
    assert convert_income_statement(convert_income_statement_input_Decon) == convert_income_statement_output_Decon
    assert convert_income_statement(convert_income_statement_input_iyantram) == convert_income_statement_output_iyantram

def test_preprocessing_IS_input():

    # with pytest.raises(TypeError):
        # preprocessing_IS_input('current asset')
        # preprocessing_IS_input((1, 2, 3))
        # preprocessing_IS_input(('a'))
    income_statement_class.type_ = "T-form_Tally"
    preprocessing_IS_input_input_MDMOTOR= input_.preprocessing_IS_input_input_MDMOTOR_ITR_2017_18
    preprocessing_IS_input_output_MDMOTOR= input_.preprocessing_IS_input_output_MDMOTOR_ITR_2017_18
    preprocessing_IS_input_input_Credit_Financial25 = input_.preprocessing_IS_input_input_Credit_Financials25_T_Format_Poor_Quality
    preprocessing_IS_input_output_Credit_Financials25 = input_.preprocessing_IS_input_outut_Credit_Financials25_T_Format_Poor_Quality
    preprocessing_IS_input_input_Intex_ITR = input_.preprocessing_IS_input_input_Intex_ITR_AY_19_20
    preprocessing_IS_input_output_Intex_ITR = input_.preprocessing_IS_input_output_Intex_ITR_AY_19_20 
    preprocessing_IS_input_input_DHO = input_.preprocessing_IS_input_input_DHO
    preprocessing_IS_input_output_DHO = input_.preprocessing_IS_input_output_DHO
    preprocessing_IS_input_input_Shruthi = input_.preprocessing_IS_input_input_Shruthi_Engg_19_20 
    preprocessing_IS_input_output_Shruthi = input_.preprocessing_IS_input_output_Shruthi_Engg_19_20
    assert preprocessing_IS_input(preprocessing_IS_input_input_MDMOTOR)==preprocessing_IS_input_output_MDMOTOR
    assert preprocessing_IS_input(preprocessing_IS_input_input_Credit_Financial25)==preprocessing_IS_input_output_Credit_Financials25
    assert preprocessing_IS_input(preprocessing_IS_input_input_Intex_ITR)==preprocessing_IS_input_output_Intex_ITR
    assert preprocessing_IS_input(preprocessing_IS_input_input_DHO)==preprocessing_IS_input_output_DHO
    assert preprocessing_IS_input(preprocessing_IS_input_input_Shruthi)==preprocessing_IS_input_output_Shruthi

    income_statement_class.type_ = "Schedule-III"
    preprocessing_IS_input_input_Credit_Financial38 = input_.preprocessing_IS_input_input_Credit_Financials38
    preprocessing_IS_input_output_Credit_Financial38 = input_.preprocessing_IS_input_output_Credit_Financials38
    preprocessing_IS_input_input_Decon = input_.preprocessing_IS_input_input_Decon
    preprocessing_IS_input_output_Decon = input_.preprocessing_IS_input_output_Decon
    preprocessing_IS_input_input_iyantram = input_.preprocessing_IS_input_input_iyantram19
    preprocessing_IS_input_output_iyantram = input_.preprocessing_IS_input_output_iyantram19    
    assert preprocessing_IS_input(preprocessing_IS_input_input_Credit_Financial38)==preprocessing_IS_input_output_Credit_Financial38
    assert preprocessing_IS_input(preprocessing_IS_input_input_Decon)==preprocessing_IS_input_output_Decon
    assert preprocessing_IS_input(preprocessing_IS_input_input_iyantram)==preprocessing_IS_input_output_iyantram

def test_find_revenue_header():

    with pytest.raises(TypeError):
        find_revenue_header('current asset')
        find_revenue_header((1, 2, 3))
        find_revenue_header(('a'))

    find_revenue_header_input_MDMOTOR = input_.find_revenue_header_input_MDMOTOR_ITR_2017_18
    find_revenue_header_output_MDMOTOR=[]
    find_revenue_header_input_Credit_Financials25 = input_.find_revenue_header_input_Credit_Financials25_T_Format_Poor_Quality
    find_revenue_header_output_Credit_Financials25=[]
    find_revenue_header_input_Intex_ITR = input_.find_revenue_header_input_Intex_ITR_AY_19_20
    find_revenue_header_output_Intex_ITR=[]
    find_revenue_header_input_DHO = input_.find_revenue_header_input_DHO
    find_revenue_header_output_DHO = []
    find_revenue_header_input_Shruthi = input_.find_revenue_header_input_Shruthi_Engg_19_20
    find_revenue_header_output_Shruthi = []
    find_revenue_header_input_Credit_Financial38 = input_.find_revenue_header_input_Credit_Financials38
    find_revenue_header_output_Credit_Financial38 = []
    find_revenue_header_input_Decon = input_.find_revenue_header_input_Decon
    find_revenue_header_output_Decon = []
    find_revenue_header_input_iyantram = input_.find_revenue_header_input_iyantram19
    find_revenue_header_output_iyantram = []
    assert find_revenue_header(find_revenue_header_input_MDMOTOR)==find_revenue_header_output_MDMOTOR
    assert find_revenue_header(find_revenue_header_input_Credit_Financials25)==find_revenue_header_output_Credit_Financials25
    assert find_revenue_header(find_revenue_header_input_Intex_ITR)==find_revenue_header_output_Intex_ITR
    assert find_revenue_header(find_revenue_header_input_DHO)==find_revenue_header_output_DHO
    assert find_revenue_header(find_revenue_header_input_Shruthi)==find_revenue_header_output_Shruthi
    assert find_revenue_header(find_revenue_header_input_Credit_Financial38)==find_revenue_header_output_Credit_Financial38
    assert find_revenue_header(find_revenue_header_input_Decon)==find_revenue_header_output_Decon
    assert find_revenue_header(find_revenue_header_input_iyantram)==find_revenue_header_output_iyantram

def test_find_expense_header():

    with pytest.raises(TypeError):
        find_expense_header('current asset')
        find_expense_header((1, 2, 3))
        find_expense_header(('a'))

    find_expense_header_input_MDMOTOR = input_.find_expense_header_input_MDMOTOR_ITR_2017_18
    find_expense_header_output_MDMOTOR=[]
    find_expense_header_input_Credit_Financials25 = input_.find_expense_header_input_Credit_Financials25_T_Format_Poor_Quality
    find_expense_header_output_Credit_Financials25=[]
    find_expense_header_input_Intex_ITR = input_.find_expense_header_input_Intex_ITR_AY_19_20
    find_expense_header_output_Intex_ITR=[]
    find_expense_header_input_DHO = input_.find_expense_header_input_DHO
    find_expense_header_output_DHO =[]
    find_expense_header_input_Shruthi = input_.find_expense_header_input_Shruthi_Engg_19_20
    find_expense_header_output_Shruthi =[]
    find_expense_header_input_Credit_Financial38 = input_.find_expense_header_input_Credit_Financials38
    find_expense_header_output_Credit_Financial38 =[]
    find_expense_header_input_Decon = input_.find_expense_header_input_Decon
    find_expense_header_output_Decon =[]
    find_expense_header_input_iyantram = input_.find_expense_header_input_iyantram19
    find_expense_header_output_iyantram =[]
    assert find_expense_header(find_expense_header_input_MDMOTOR)==find_expense_header_output_MDMOTOR
    assert find_expense_header(find_expense_header_input_Credit_Financials25)==find_expense_header_output_Credit_Financials25
    assert find_expense_header(find_expense_header_input_Intex_ITR)==find_expense_header_output_Intex_ITR
    assert find_expense_header(find_expense_header_input_DHO)==find_expense_header_output_DHO
    assert find_expense_header(find_expense_header_input_Shruthi)==find_expense_header_output_Shruthi
    assert find_expense_header(find_expense_header_input_Credit_Financial38)==find_expense_header_output_Credit_Financial38
    assert find_expense_header(find_expense_header_input_Decon)==find_expense_header_output_Decon
    assert find_expense_header(find_expense_header_input_iyantram)==find_expense_header_output_iyantram


def test_find_first_signage():

    with pytest.raises(TypeError):
        find_first_signage()
        find_first_signage('sss')
        find_first_signage(25)
        find_first_signage(6.8)
        find_first_signage({5: 'z'})

    find_first_signage_input_MDMOTOR = input_.find_first_signage_input_MDMOTOR_ITR_2017_18
    find_first_signage_output_MDMOTOR= 6
    find_first_signage_input_Credit_Financials25 = input_.find_first_signage_input_Credit_Financials25_T_Format_Poor_Quality
    find_first_signage_output_Credit_Financials25= 2
    find_first_signage_input_Intex_ITR = input_.find_first_signage_input_Intex_ITR_AY_19_20
    find_first_signage_output_Intex_ITR= 5
    find_first_signage_input_DHO = input_.find_first_signage_input_DHO
    find_first_signage_output_DHO = 8
    find_first_signage_input_Shruthi = input_.find_first_signage_input_Shruthi_Engg_19_20
    find_first_signage_output_Shruthi = 2
    find_first_signage_input_Credit_Financial38 = input_.find_first_signage_input_Credit_Financials38
    find_first_signage_output_Credit_Financial38 = 1
    find_first_signage_input_Decon = input_.find_first_signage_input_Decon
    find_first_signage_output_Decon = -1
    find_first_signage_input_iyantram = input_.find_first_signage_input_iyantram19
    find_first_signage_output_iyantram = -1
    assert find_first_signage(find_first_signage_input_MDMOTOR)==find_first_signage_output_MDMOTOR
    assert find_first_signage(find_first_signage_input_Credit_Financials25)==find_first_signage_output_Credit_Financials25
    assert find_first_signage(find_first_signage_input_Intex_ITR)==find_first_signage_output_Intex_ITR
    assert find_first_signage(find_first_signage_input_DHO)==find_first_signage_output_DHO
    assert find_first_signage(find_first_signage_input_Shruthi)==find_first_signage_output_Shruthi
    assert find_first_signage(find_first_signage_input_Credit_Financial38)==find_first_signage_output_Credit_Financial38
    assert find_first_signage(find_first_signage_input_Decon)==find_first_signage_output_Decon
    assert find_first_signage(find_first_signage_input_iyantram)==find_first_signage_output_iyantram

def test_check_cost_line_item():
    # raise TypeError if input is not list.
    with pytest.raises(TypeError):
        check_cost_line_item((8, 1, 2))
        check_cost_line_item('sss')
        check_cost_line_item(25)
        check_cost_line_item(6.8)
        check_cost_line_item({5: 'z'})

    check_cost_line_item_input_MDMOTOR = input_.check_cost_line_item_input_MDMOTOR_ITR_2017_18 
    check_cost_line_item_output_MDMOTOR=[17, 25, 27]
    check_cost_line_item_input_Credit_Financials25 = input_.check_cost_line_item_input_Credit_Financials25_T_Format_Poor_Quality
    check_cost_line_item_output_Credit_Financials25=[14, 15]
    check_cost_line_item_input_Intex_ITR = input_.check_cost_line_item_input_Intex_ITR_AY_19_20
    check_cost_line_item_output_Intex_ITR=[14, 16, 21, 23, 27, 28, 29]
    check_cost_line_item_input_DHO = input_.check_cost_line_item_input_DHO
    check_cost_line_item_output_DHO=[4, 12, 13, 20, 38, 39, 40, 45, 51, 56, 64]
    check_cost_line_item_input_Shruthi = input_.check_cost_line_item_input_Shruthi_Engg_19_20
    check_cost_line_item_output_Shruthi= [7, 15]
    check_cost_line_item_input_Credit_Financial38 = input_.check_cost_line_item_input_Credit_Financials38
    check_cost_line_item_output_Credit_Financial38 = []
    check_cost_line_item_input_Decon = input_.check_cost_line_item_input_Decon
    check_cost_line_item_output_Decon = [3, 6, 10]
    check_cost_line_item_input_iyantram = input_.check_cost_line_item_input_iyantram19
    check_cost_line_item_output_iyantram = [3, 6, 10]


    assert check_cost_line_item(check_cost_line_item_input_MDMOTOR)==check_cost_line_item_output_MDMOTOR
    assert check_cost_line_item(check_cost_line_item_input_Credit_Financials25)==check_cost_line_item_output_Credit_Financials25
    assert check_cost_line_item(check_cost_line_item_input_Intex_ITR)==check_cost_line_item_output_Intex_ITR
    assert check_cost_line_item(check_cost_line_item_input_DHO)==check_cost_line_item_output_DHO
    assert check_cost_line_item(check_cost_line_item_input_Shruthi)==check_cost_line_item_output_Shruthi
    assert check_cost_line_item(check_cost_line_item_input_Credit_Financial38)==check_cost_line_item_output_Credit_Financial38
    assert check_cost_line_item(check_cost_line_item_input_Decon)==check_cost_line_item_output_Decon
    assert check_cost_line_item(check_cost_line_item_input_iyantram)==check_cost_line_item_output_iyantram

def test_other_income():

    with pytest.raises(TypeError):
        other_income((8, 1, 2))
        other_income('sss')
        other_income(25)
        other_income(6.8)
        other_income({5: 'z'})

    other_income_input_MDMOTOR = input_.other_income_input_MDMOTOR_ITR_2017_18
    other_income_output_MDMOTOR=[]
    other_income_input_Credit_Financials25 = input_.other_income_input_Credit_Financials25_T_Format_Poor_Quality
    other_income_output_Credit_Financials25=[6]
    other_income_input_Intex_ITR = input_.other_income_input_Intex_ITR_AY_19_20
    other_income_output_Intex_ITR=[]
    other_income_input_DHO = input_.other_income_input_DHO
    other_income_output_DHO=[1]
    other_income_input_Shruthi = input_.other_income_input_Shruthi_Engg_19_20
    other_income_output_Shruthi=[11]
    other_income_input_Credit_Financial38 = input_.other_income_input_Credit_Financials38
    other_income_output_Credit_Financial38 = [3]
    other_income_input_Decon = input_.other_income_input_Decon
    other_income_output_Decon=[8]
    other_income_input_iyantram = input_.other_income_input_iyantram19
    other_income_output_iyantram=[8]

    assert other_income(other_income_input_MDMOTOR)==other_income_output_MDMOTOR
    assert other_income(other_income_input_Credit_Financials25)==other_income_output_Credit_Financials25
    assert other_income(other_income_input_Intex_ITR)==other_income_output_Intex_ITR
    assert other_income(other_income_input_DHO)==other_income_output_DHO
    assert other_income(other_income_input_Shruthi)==other_income_output_Shruthi
    assert other_income(other_income_input_Credit_Financial38)==other_income_output_Credit_Financial38
    assert other_income(other_income_input_Decon)==other_income_output_Decon
    assert other_income(other_income_input_iyantram)==other_income_output_iyantram


def test_cogs():
    # raise TypeError if input is not list.
    with pytest.raises(TypeError):
        cogs((8, 1, 2))
        cogs('sss')
        cogs(5)
        cogs(6.8)
        cogs({5: 'z'})

    cogs_input_MDMOTOR = input_.cogs_input_MDMOTOR_ITR_2017_18 
    cogs_output_MDMOTOR=[5, 8, 9]
    cogs_input_Credit_Financials25 = input_.cogs_input_Credit_Financials25_T_Format_Poor_Quality
    cogs_output_Credit_Financials25=[1, 8, 9]
    cogs_input_Intex_ITR = input_.cogs_input_Intex_ITR_AY_19_20
    cogs_output_Intex_ITR=[3, 8, 14]
    cogs_input_DHO = input_.cogs_input_DHO
    cogs_output_DHO = [14, 69]
    cogs_input_Shruthi = input_.cogs_input_Shruthi_Engg_19_20
    cogs_output_Shruthi = [1, 3, 4]
    cogs_input_Credit_Financial38 = input_.cogs_input_Credit_Financials38
    cogs_output_Credit_Financial38 = [2]
    cogs_input_Decon = input_.cogs_input_Decon
    cogs_output_Decon = [0, 1, 2, 3, 5, 6]
    cogs_input_iyantram = input_.cogs_input_iyantram19
    cogs_output_iyantram = [0, 1, 2, 3, 5, 6]

    assert cogs(cogs_input_MDMOTOR)==cogs_output_MDMOTOR
    assert cogs(cogs_input_Credit_Financials25)==cogs_output_Credit_Financials25
    assert cogs(cogs_input_Intex_ITR)==cogs_output_Intex_ITR
    assert cogs(cogs_input_DHO)==cogs_output_DHO
    assert cogs(cogs_input_Shruthi)==cogs_output_Shruthi
    assert cogs(cogs_input_Credit_Financial38)==cogs_output_Credit_Financial38
    assert cogs(cogs_input_Decon)==cogs_output_Decon
    assert cogs(cogs_input_iyantram)==cogs_output_iyantram

def test_employee_cost():

    with pytest.raises(TypeError):
        employee_cost((2, 7, 9))
        employee_cost('efgb')
        employee_cost(1)
        employee_cost(3.0)
        employee_cost({4: 's'})
    employee_cost_input_MDMOTOR = input_.employee_cost_input_MDMOTOR_ITR_2017_18
    employee_cost_output_MDMOTOR=[]
    employee_cost_input_Credit_Financials25 = input_.employee_cost_input_Credit_Financials25_T_Format_Poor_Quality
    employee_cost_output_Credit_Financials25=[]
    employee_cost_input_Intex_ITR = input_.employee_cost_input_Intex_ITR_AY_19_20
    employee_cost_output_Intex_ITR=[]
    employee_cost_input_DHO = input_.employee_cost_input_DHO
    employee_cost_output_DHO=[]
    employee_cost_input_Shruthi = input_.employee_cost_input_Shruthi_Engg_19_20
    employee_cost_output_Shruthi=[]
    employee_cost_input_Credit_Financial38 = input_.employee_cost_input_Credit_Financials38
    employee_cost_output_Credit_Financial38 = []
    employee_cost_input_Decon = input_.employee_cost_input_Decon
    employee_cost_output_Decon=[]
    employee_cost_input_iyantram = input_.employee_cost_input_iyantram19
    employee_cost_output_iyantram=[]
    assert employee_cost(employee_cost_input_MDMOTOR)==employee_cost_output_MDMOTOR
    assert employee_cost(employee_cost_input_Credit_Financials25)==employee_cost_output_Credit_Financials25
    assert employee_cost(employee_cost_input_Intex_ITR)==employee_cost_output_Intex_ITR
    assert employee_cost(employee_cost_input_DHO)==employee_cost_output_DHO
    assert employee_cost(employee_cost_input_Shruthi)==employee_cost_output_Shruthi
    assert employee_cost(employee_cost_input_Credit_Financial38)==employee_cost_output_Credit_Financial38
    assert employee_cost(employee_cost_input_Decon)==employee_cost_output_Decon
    assert employee_cost(employee_cost_input_iyantram)==employee_cost_output_iyantram

def test_finance_cost():
    # raise TypeError if input is not list.
    with pytest.raises(TypeError):
        finance_cost((6, 1, 3))
        finance_cost('vbnm')
        finance_cost(7)
        finance_cost(9.6)
        finance_cost({2: 'c'})
    finance_cost_input_MDMOTOR = input_.finance_cost_input_MDMOTOR_ITR_2017_18
    finance_cost_output_MDMOTOR=[]
    finance_cost_input_Credit_Financials25 = input_.finance_cost_input_Credit_Financials25_T_Format_Poor_Quality 
    finance_cost_output_Credit_Financials25=[]
    finance_cost_input_Intex_ITR = input_.finance_cost_input_Intex_ITR_AY_19_20
    finance_cost_output_Intex_ITR=[11]
    finance_cost_input_DHO = input_.finance_cost_input_DHO 
    finance_cost_output_DHO=[1, 9, 14, 26]
    finance_cost_input_Shruthi = input_.finance_cost_input_Shruthi_Engg_19_20
    finance_cost_output_Shruthi=[8]
    finance_cost_input_Credit_Financial38 = input_.finance_cost_input_Credit_Financials38
    finance_cost_output_Credit_Financial38=[3]
    finance_cost_input_Decon = input_.finance_cost_input_Decon
    finance_cost_output_Decon=[]
    finance_cost_input_iyantram = input_.finance_cost_input_iyantram19
    finance_cost_output_iyantram=[]

    assert finance_cost(finance_cost_input_MDMOTOR)==finance_cost_output_MDMOTOR
    assert finance_cost(finance_cost_input_Credit_Financials25)==finance_cost_output_Credit_Financials25
    assert finance_cost(finance_cost_input_Intex_ITR)==finance_cost_output_Intex_ITR
    assert finance_cost(finance_cost_input_DHO)==finance_cost_output_DHO
    assert finance_cost(finance_cost_input_Shruthi)==finance_cost_output_Shruthi
    assert finance_cost(finance_cost_input_Credit_Financial38)==finance_cost_output_Credit_Financial38
    assert finance_cost(finance_cost_input_Decon)==finance_cost_output_Decon
    assert finance_cost(finance_cost_input_iyantram)==finance_cost_output_iyantram



def test_KM_1():
    # raise TypeError if input is not list.
    with pytest.raises(TypeError):
        KM_1((8, 1, 2))
        KM_1('sss')
        KM_1(5)
        KM_1(6.8)
        KM_1({5: 'z'})
    KM_1_input_MDMOTOR = input_.KM_1_input_MDMOTOR_ITR_2017_18
    KM_1_output_MDMOTOR = [12]
    KM_1_input_Credit_Financials25 = input_.KM_1_input_Credit_Financials25_T_Format_Poor_Quality
    KM_1_output_Credit_Financials25=[10]
    KM_1_input_Intex_ITR = input_.KM_1_input_Intex_ITR_AY_19_20
    KM_1_output_Intex_ITR=[]
    KM_1_input_DHO = input_.KM_1_input_DHO
    KM_1_output_DHO=[]
    KM_1_input_Shruthi = input_.KM_1_input_Shruthi_Engg_19_20
    KM_1_output_Shruthi=[]
    KM_1_input_Credit_Financial38 = input_.KM_1_input_Credit_Financials38
    KM_1_output_Credit_Financial38=[]
    KM_1_input_Decon = input_.KM_1_input_Decon
    KM_1_output_Decon=[7]
    KM_1_input_iyantram = input_.KM_1_input_iyantram19
    KM_1_output_iyantram=[7]

    assert KM_1(KM_1_input_MDMOTOR)==KM_1_output_MDMOTOR
    assert KM_1(KM_1_input_Credit_Financials25)==KM_1_output_Credit_Financials25
    assert KM_1(KM_1_input_Intex_ITR)==KM_1_output_Intex_ITR
    assert KM_1(KM_1_input_DHO)==KM_1_output_DHO
    assert KM_1(KM_1_input_Shruthi)==KM_1_output_Shruthi
    assert KM_1(KM_1_input_Credit_Financial38)==KM_1_output_Credit_Financial38
    assert KM_1(KM_1_input_Decon)==KM_1_output_Decon
    assert KM_1(KM_1_input_iyantram)==KM_1_output_iyantram

def test_KM_2():
    # raise TypeError if input is not list.
    with pytest.raises(TypeError):
        KM_2((8, 1, 2))
        KM_2('sss')
        KM_2(5)
        KM_2(6.8)
        KM_2({5: 'z'})
    KM_2_input_MDMOTOR = input_.KM_2_input_MDMOTOR_ITR_2017_18
    KM_2_output_MDMOTOR=[]
    KM_2_input_Credit_Financials25 = input_.KM_2_input_Credit_Financials25_T_Format_Poor_Quality
    KM_2_output_Credit_Financials25=[]
    KM_2_input_Intex_ITR = input_.KM_2_input_Intex_ITR_AY_19_20
    KM_2_output_Intex_ITR=[]
    KM_2_input_DHO = input_.KM_2_input_DHO
    KM_2_output_DHO=[]
    KM_2_input_Shruthi = input_.KM_2_input_Shruthi_Engg_19_20
    KM_2_output_Shruthi=[]
    KM_2_input_Credit_Financial38 = input_.KM_2_input_Credit_Financials38
    KM_2_output_Credit_Financial38=[]
    KM_2_input_Decon = input_.KM_2_input_Decon
    KM_2_output_Decon=[]
    KM_2_input_iyantram = input_.KM_2_input_iyantram19
    KM_2_output_iyantram=[]
    assert KM_2(KM_2_input_MDMOTOR)==KM_2_output_MDMOTOR
    assert KM_2(KM_2_input_Credit_Financials25)==KM_2_output_Credit_Financials25
    assert KM_2(KM_2_input_Intex_ITR)==KM_2_output_Intex_ITR
    assert KM_2(KM_2_input_DHO)==KM_2_output_DHO
    assert KM_2(KM_2_input_Shruthi)==KM_2_output_Shruthi
    assert KM_2(KM_2_input_Credit_Financial38)==KM_2_output_Credit_Financial38
    assert KM_2(KM_2_input_Decon)==KM_2_output_Decon
    assert KM_2(KM_2_input_iyantram)==KM_2_output_iyantram


def test_KM_3():
    # raise TypeError if input is not list.
    with pytest.raises(TypeError):
        KM_3((8, 1, 2))
        KM_3('sss')
        KM_3(25)
        KM_3(6.8)
        KM_3({5: 'z'})
    KM_3_input_MDMOTOR = input_.KM_3_input_MDMOTOR_ITR_2017_18
    KM_3_output_MDMOTOR=[]
    KM_3_input_Credit_Financials25 = input_.KM_3_input_Credit_Financials25_T_Format_Poor_Quality
    KM_3_output_Credit_Financials25=[]
    KM_3_input_Intex_ITR = input_.KM_3_input_Intex_ITR_AY_19_20
    KM_3_output_Intex_ITR=[]
    KM_3_input_DHO = input_.KM_3_input_DHO
    KM_3_output_DHO=[]
    KM_3_input_Shruthi = input_.KM_3_input_Shruthi_Engg_19_20 
    KM_3_output_Shruthi=[]
    KM_3_input_Credit_Financial38 = input_.KM_3_input_Credit_Financials38
    KM_3_output_Credit_Financial38=[]
    KM_3_input_Decon = input_.KM_3_input_Decon
    KM_3_output_Decon=[3]
    KM_3_input_iyantram = input_.KM_3_input_iyantram19
    KM_3_output_iyantram=[3]

    assert KM_3(KM_3_input_MDMOTOR)==KM_3_output_MDMOTOR
    assert KM_3(KM_3_input_Credit_Financials25)==KM_3_output_Credit_Financials25
    assert KM_3(KM_3_input_Intex_ITR)==KM_3_output_Intex_ITR
    assert KM_3(KM_3_input_DHO)==KM_3_output_DHO
    assert KM_3(KM_3_input_Shruthi)==KM_3_output_Shruthi
    assert KM_3(KM_3_input_Credit_Financial38)==KM_3_output_Credit_Financial38
    assert KM_3(KM_3_input_Decon)==KM_3_output_Decon
    assert KM_3(KM_3_input_iyantram)==KM_3_output_iyantram

def test_KM_4():
    # raise TypeError if input is not list.

    with pytest.raises(TypeError):
        KM_4((8, 1, 2))
        KM_4('sss')
        KM_4(25)
        KM_4(6.8)
    KM_4_input_MDMOTOR = input_.KM_4_input_MDMOTOR_ITR_2017_18 
    KM_4_output_MDMOTOR=[]
    KM_4_input_Credit_Financials25 = input_.KM_4_input_Credit_Financials25_T_Format_Poor_Quality
    KM_4_output_Credit_Financials25=[]
    KM_4_input_Intex_ITR = input_.KM_4_input_Intex_ITR_AY_19_20
    KM_4_output_Intex_ITR=[]
    KM_4_input_DHO = input_.KM_4_input_DHO
    KM_4_output_DHO=[]
    KM_4_input_Shruthi = input_.KM_4_input_Shruthi_Engg_19_20
    KM_4_output_Shruthi=[]
    KM_4_input_Credit_Financial38 = input_.KM_4_input_Credit_Financials38
    KM_4_output_Credit_Financial38=[]
    KM_4_input_Decon = input_.KM_4_input_Decon
    KM_4_output_Decon=[1]
    KM_4_input_iyantram = input_.KM_4_input_iyantram19
    KM_4_output_iyantram=[1]
    assert KM_4(KM_4_input_MDMOTOR)==KM_4_output_MDMOTOR
    assert KM_4(KM_4_input_Credit_Financials25)==KM_4_output_Credit_Financials25
    assert KM_4(KM_4_input_Intex_ITR)==KM_4_output_Intex_ITR
    assert KM_4(KM_4_input_DHO)==KM_4_output_DHO
    assert KM_4(KM_4_input_Shruthi)==KM_4_output_Shruthi
    assert KM_4(KM_4_input_Credit_Financial38)==KM_4_output_Credit_Financial38
    assert KM_4(KM_4_input_Decon)==KM_4_output_Decon
    assert KM_4(KM_4_input_iyantram)==KM_4_output_iyantram

def test_KM_5():
    # raise TypeError if input is not list.
    with pytest.raises(TypeError):
        KM_5((8, 1, 2))
        KM_5('sss')
        KM_5(25)
        KM_5(6.8)
        KM_5({5: 'z'})
    KM_5_input_MDMOTOR = input_.KM_5_input_MDMOTOR_ITR_2017_18
    KM_5_output_MDMOTOR=[27]
    KM_5_input_Credit_Financials25 = input_.KM_5_input_Credit_Financials25_T_Format_Poor_Quality
    KM_5_output_Credit_Financials25=[5]
    KM_5_input_Intex_ITR = input_.KM_5_input_Intex_ITR_AY_19_20
    KM_5_output_Intex_ITR=[30]
    KM_5_input_DHO = input_.KM_5_input_DHO
    KM_5_output_DHO=[70]
    KM_5_input_Shruthi = input_.KM_5_input_Shruthi_Engg_19_20
    KM_5_output_Shruthi=[17]
    KM_5_input_Credit_Financial38 = input_.KM_5_input_Credit_Financials38
    KM_5_output_Credit_Financial38=[1]
    KM_5_input_Decon = input_.KM_5_input_Decon
    KM_5_output_Decon=[0]
    KM_5_input_iyantram = input_.KM_5_input_iyantram19
    KM_5_output_iyantram=[0]
    assert KM_5(KM_5_input_MDMOTOR)==KM_5_output_MDMOTOR
    assert KM_5(KM_5_input_Credit_Financials25)==KM_5_output_Credit_Financials25
    assert KM_5(KM_5_input_Intex_ITR)==KM_5_output_Intex_ITR
    assert KM_5(KM_5_input_DHO)==KM_5_output_DHO
    assert KM_5(KM_5_input_Shruthi)==KM_5_output_Shruthi
    assert KM_5(KM_5_input_Credit_Financial38)==KM_5_output_Credit_Financial38
    assert KM_5(KM_5_input_Decon)==KM_5_output_Decon
    assert KM_5(KM_5_input_iyantram)==KM_5_output_iyantram

def test_check_depreciation():
    # raise TypeError if input is not list.
    with pytest.raises(TypeError):
        check_depreciation((8, 1, 2))
        check_depreciation('sss')
        check_depreciation(25)
        check_depreciation(6.8)
        check_depreciation({5: 'z'})

    check_depreciation_input_MDMOTOR = input_.check_depreciation_input_MDMOTOR_ITR_2017_18
    check_depreciation_output_MDMOTOR=[29]
    check_depreciation_input_Credit_Financials25 = input_.check_depreciation_input_Credit_Financials25_T_Format_Poor_Quality 
    check_depreciation_output_Credit_Financials25=[]
    check_depreciation_input_Intex_ITR = input_.check_depreciation_input_Intex_ITR_AY_19_20 
    check_depreciation_output_Intex_ITR=[20]
    check_depreciation_input_DHO = input_.check_depreciation_input_DHO
    check_depreciation_output_DHO = [42]
    check_depreciation_input_Shruthi = input_.check_depreciation_input_Shruthi_Engg_19_20
    check_depreciation_output_Shruthi = [16]
    check_depreciation_input_Credit_Financial38 = input_.check_depreciation_input_Credit_Financials38
    check_depreciation_output_Credit_Financial38 = [42]
    check_depreciation_input_Decon = input_.check_depreciation_input_Decon
    check_depreciation_output_Decon = [42]
    check_depreciation_input_iyantram = input_.check_depreciation_input_iyantram19
    check_depreciation_output_iyantram = [42]

    check_depreciation(check_depreciation_input_MDMOTOR)==check_depreciation_output_MDMOTOR
    check_depreciation(check_depreciation_input_Credit_Financials25)==check_depreciation_output_Credit_Financials25
    check_depreciation(check_depreciation_input_Intex_ITR)==check_depreciation_output_Intex_ITR
    check_depreciation(check_depreciation_input_DHO)==check_depreciation_output_DHO
    check_depreciation(check_depreciation_input_Shruthi)==check_depreciation_output_Shruthi
    check_depreciation(check_depreciation_input_Credit_Financial38)==check_depreciation_output_Credit_Financial38
    check_depreciation(check_depreciation_input_Decon)==check_depreciation_output_Decon
    check_depreciation(check_depreciation_input_iyantram)==check_depreciation_output_iyantram










