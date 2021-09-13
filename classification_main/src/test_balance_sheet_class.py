import pytest
from balance_sheet_class import *
import input_

def test_yaml_parse():
    with pytest.raises(TypeError):
        yaml_parse('')
        yaml_parse(6)
 

def test_asset_level1_start_pos():
    # raise TypeError if input is not list.
    with pytest.raises(TypeError):
        net_asset_level1_start_pos((4, 5))
        net_asset_level1_start_pos('abcd')
        net_asset_level1_start_pos(1)
        net_asset_level1_start_pos(1.0)
        net_asset_level1_start_pos({1: 'a'})

    # Decon
    input_Decon = input_.input_Decon
    output_Decon = {'class_id':0,'hiererchy':'main','level':'total','item_name':'net_asset','matched_with':'','start_pos':-100}
    assert net_asset_level1_start_pos(input_Decon) == output_Decon

    # _Credit_Financials
    input_Credit_Fin = input_.input_Credit_Fin
    output_Credit_Fin = {'class_id':0,'hiererchy':'main','level':'total','item_name':'net_asset','matched_with':'','start_pos':-100}
    assert net_asset_level1_start_pos(input_Credit_Fin) == output_Credit_Fin

    # _Shruthi_engg
    input_Shruthi_engg = input_.input_Shruthi_engg
    output_Shruthi_engg = {'class_id':0,'hiererchy':'main','level':'total','item_name':'net_asset','matched_with':'','start_pos':-100}
    assert net_asset_level1_start_pos(input_Shruthi_engg) == output_Shruthi_engg

    # _MD_Motors
    input_MD_motors = input_.input_MD_motors
    output_MD_motors = {'class_id':0,'hiererchy':'main','level':'total','item_name':'net_asset','matched_with':'','start_pos':-100}
    assert net_asset_level1_start_pos(input_MD_motors) == output_MD_motors

    # DHO
    input_Dho = input_.input_Dho
    output_Dho = {'class_id':0,'hiererchy':'main','level':'total','item_name':'net_asset','matched_with':'','start_pos':-100}
    assert net_asset_level1_start_pos(input_Dho) == output_Dho

    # _Credit_Financials_Poor_Quality
    input_Cre_Fin_PQ = input_.input_Cre_Fin_PQ
    output_Cre_Fin_PQ = {'class_id':0,'hiererchy':'main','level':'total','item_name':'net_asset','matched_with':'','start_pos':-100}
    assert net_asset_level1_start_pos(input_Cre_Fin_PQ) == output_Cre_Fin_PQ

    # _iyantram
    input_Iyantram = input_.input_Iyantram
    output_Iyantram = {'class_id':0,'hiererchy':'main','level':'total','item_name':'net_asset','matched_with':'','start_pos':-100}
    assert net_asset_level1_start_pos(input_Iyantram) == output_Iyantram

    # _Intex
    input_Intex = input_.input_Intex
    output_Intex = {'class_id':0,'hiererchy':'main','level':'total','item_name':'net_asset','matched_with':'','start_pos':-100}
    assert net_asset_level1_start_pos(input_Intex) == output_Intex


def test_current_asset_level2_start_pos():
    with pytest.raises(TypeError):
        current_asset_level2_start_pos({1,1,1})
        current_asset_level2_start_pos({'a':1 , 'b':2})
        current_asset_level2_start_pos('')
    
    # Decon
    input_Decon = input_.input_Decon
    output_Decon = {'class_id':1,'sub_class_id': 1,'hiererchy':'sub','level':'class','item_name':'current_asset','matched_with':'inventory ','start_pos':8}
    assert current_asset_level2_start_pos(input_Decon) == output_Decon

    # _Credit_Financials
    input_Credit_Fin = input_.input_Credit_Fin
    output_Credit_Fin = {'class_id':1,'sub_class_id':1,'hiererchy':'sub','level':'class','item_name':'current_asset','matched_with':'current assets loans ','start_pos':7}
    assert current_asset_level2_start_pos(input_Credit_Fin) == output_Credit_Fin

    # _Shruthi_engg
    input_Shruthi_engg = input_.input_Shruthi_engg
    output_Shruthi_engg = {'class_id':1,'sub_class_id':1,'hiererchy':'sub','level':'class','item_name':'current_asset','matched_with':'current assets ','start_pos':2}
    assert current_asset_level2_start_pos(input_Shruthi_engg) == output_Shruthi_engg

    # _MD_Motors
    input_MD_motors = input_.input_MD_motors
    output_MD_motors = {'class_id':1,'sub_class_id':1,'hiererchy':'sub','level':'class','item_name':'current_asset','matched_with':'current assets ','start_pos':28}
    assert current_asset_level2_start_pos(input_MD_motors) == output_MD_motors

    # DHO
    input_Dho = input_.input_Dho
    output_Dho = {'class_id':1,'sub_class_id':1,'hiererchy':'sub','level':'class','item_name':'current_asset','matched_with':'closing stocks ','start_pos': 4}
    assert current_asset_level2_start_pos(input_Dho) == output_Dho

    # _Credit_Financials_Poor_Quality
    input_Cre_Fin_PQ = input_.input_Cre_Fin_PQ
    output_Cre_Fin_PQ = {'class_id':1,'sub_class_id':1,'hiererchy':'sub','level':'class','item_name':'current_asset','matched_with':'loans & advances ','start_pos':5}
    assert current_asset_level2_start_pos(input_Cre_Fin_PQ) == output_Cre_Fin_PQ

    # _iyantram
    input_Iyantram = input_.input_Iyantram
    output_Iyantram = {'class_id':1,'sub_class_id':1,'hiererchy':'sub','level':'class','item_name':'current_asset','matched_with':'inventory ','start_pos':8}
    assert current_asset_level2_start_pos(input_Iyantram) == output_Iyantram

    # _Intex
    input_Intex = input_.input_Intex
    output_Intex = {'class_id':1,'sub_class_id':1,'hiererchy':'sub','level':'class','item_name':'current_asset','matched_with':'current assets ','start_pos':3}
    assert current_asset_level2_start_pos(input_Intex) == output_Intex


def test_non_current_asset_level2_start_pos():
    with pytest.raises(TypeError):
        non_current_asset_level2_start_pos('')
        non_current_asset_level2_start_pos({1,'A'})
        non_current_asset_level2_start_pos('0')
    
    # _Decon
    input_Decon = input_.input_Decon
    output_Decon = {'class_id':1,'sub_class_id':2,'hiererchy':'sub','level':'class','item_name':'non_current_asset','matched_with':'capital ','start_pos':1}
    assert non_current_asset_level2_start_pos(input_Decon) == output_Decon

    # _Credit_Financials
    input_Credit_Fin = input_.input_Credit_Fin
    output_Credit_Fin = {'class_id':1,'sub_class_id':2,'hiererchy':'sub','level':'class','item_name':'non_current_asset','matched_with':'','start_pos':-100}
    assert non_current_asset_level2_start_pos(input_Credit_Fin) == output_Credit_Fin

    # _Shruthi_engg
    input_Shruthi_engg = input_.input_Shruthi_engg
    output_Shruthi_engg = {'class_id':1,'sub_class_id':2,'hiererchy':'sub','level':'class','item_name':'non_current_asset','matched_with':'assets ','start_pos': 0}
    assert non_current_asset_level2_start_pos(input_Shruthi_engg) == output_Shruthi_engg

    # _MD_Motors
    input_MD_motors = input_.input_MD_motors
    output_MD_motors = {'class_id':1,'sub_class_id':2,'hiererchy':'sub','level':'class','item_name':'non_current_asset','matched_with':'capital ','start_pos':39}
    assert non_current_asset_level2_start_pos(input_MD_motors) == output_MD_motors

    # DHO
    input_Dho = input_.input_Dho
    output_Dho = {'class_id':1,'sub_class_id':2,'hiererchy':'sub','level':'class','item_name':'non_current_asset','matched_with':'assets ','start_pos': 0}
    assert non_current_asset_level2_start_pos(input_Dho) == output_Dho

    # _Credit_Financials_Poor_Quality
    input_Cre_Fin_PQ = input_.input_Cre_Fin_PQ
    output_Cre_Fin_PQ = {'class_id':1,'sub_class_id':2,'hiererchy':'sub','level':'class','item_name':'non_current_asset','matched_with':'assets ','start_pos': 0}
    assert non_current_asset_level2_start_pos(input_Cre_Fin_PQ) == output_Cre_Fin_PQ

    # _iyantram
    input_Iyantram = input_.input_Iyantram
    output_Iyantram = {'class_id':1,'sub_class_id':2,'hiererchy':'sub','level':'class','item_name':'non_current_asset','matched_with':'capital ','start_pos':1}
    assert non_current_asset_level2_start_pos(input_Iyantram) == output_Iyantram

    # _Intex
    input_Intex = input_.input_Intex
    output_Intex = {'class_id':1,'sub_class_id':2,'hiererchy':'sub','level':'class','item_name':'non_current_asset','matched_with': 'assets ','start_pos': 0}
    assert non_current_asset_level2_start_pos(input_Intex) == output_Intex




def test_equity_liabilities_level1_start_pos():
    with pytest.raises(TypeError):
        equity_liabilities_level1_start_pos('1,2,3')
        equity_liabilities_level1_start_pos('')
        equity_liabilities_level1_start_pos([0])
    
    #_Decon
    input_Decon = input_.input_Decon
    output_Decon = {'class_id':2,'hiererchy':'main','level':'class','item_name':'equity_liabilities','matched_with':'sources of funds ','start_pos':0}
    assert equity_liabilities_level1_start_pos(input_Decon ) == output_Decon

    # _Credit_Financials
    input_Credit_Fin = input_.input_Credit_Fin
    output_Credit_Fin = {'class_id':2,'hiererchy':'main','level':'class','item_name':'equity_liabilities','matched_with':'','start_pos':-100}
    assert equity_liabilities_level1_start_pos(input_Credit_Fin) == output_Credit_Fin

    # _Shruthi_engg
    input_Shruthi_engg = input_.input_Shruthi_engg
    output_Shruthi_engg = {'class_id':2,'hiererchy':'main','level':'class','item_name':'equity_liabilities','matched_with':'','start_pos':-100}
    assert equity_liabilities_level1_start_pos(input_Shruthi_engg) == output_Shruthi_engg

    # _MD_Motors
    input_MD_motors = input_.input_MD_motors
    output_MD_motors = {'class_id':2,'hiererchy':'main','level':'class','item_name':'equity_liabilities','matched_with':'','start_pos':-100}
    assert equity_liabilities_level1_start_pos(input_MD_motors) == output_MD_motors

    # DHO
    input_Dho = input_.input_Dho
    output_Dho = {'class_id':2,'hiererchy':'main','level':'class','item_name':'equity_liabilities','matched_with':'','start_pos':-100}
    assert equity_liabilities_level1_start_pos(input_Dho) == output_Dho

    # _Credit_Financials_Poor_Quality
    input_Cre_Fin_PQ = input_.input_Cre_Fin_PQ
    output_Cre_Fin_PQ = {'class_id':2,'hiererchy':'main','level':'class','item_name':'equity_liabilities','matched_with':'','start_pos':-100}
    assert equity_liabilities_level1_start_pos(input_Cre_Fin_PQ) == output_Cre_Fin_PQ

    # _iyantram
    input_Iyantram = input_.input_Iyantram
    output_Iyantram = {'class_id':2,'hiererchy':'main','level':'class','item_name':'equity_liabilities','matched_with':'sources of funds ','start_pos':0}
    assert equity_liabilities_level1_start_pos(input_Iyantram) == output_Iyantram

    # _Intex
    input_Intex = input_.input_Intex
    output_Intex = {'class_id':2,'hiererchy':'main','level':'class','item_name':'equity_liabilities','matched_with':'','start_pos':-100}
    assert equity_liabilities_level1_start_pos(input_Intex) == output_Intex




def test_liabilities_level2_start_pos():
    with pytest.raises(TypeError):
        liabilities_level2_start_pos('')
        liabilities_level2_start_pos({'a':'12'})
        liabilities_level2_start_pos(['k,l,m'])
    
    # _Decon
    input_Decon = input_.input_Decon
    output_Decon = {'class_id':2,'hiererchy':'main','level':'class','item_name':'liabilities','matched_with':'','start_pos':-100}
    assert liabilities_level2_start_pos(input_Decon) == output_Decon

    # _Credit_Financials
    input_Credit_Fin = input_.input_Credit_Fin
    output_Credit_Fin = {'class_id':2,'hiererchy':'main','level':'class','item_name':'liabilities','matched_with':'','start_pos':-100}
    assert liabilities_level2_start_pos(input_Credit_Fin) == output_Credit_Fin

    # _Shruthi_engg
    input_Shruthi_engg = input_.input_Shruthi_engg
    output_Shruthi_engg = {'class_id':2,'hiererchy':'main','level':'class','item_name':'liabilities','matched_with':'liabilities ','start_pos':9}
    assert liabilities_level2_start_pos(input_Shruthi_engg) == output_Shruthi_engg

    # _MD_Motors
    input_MD_motors = input_.input_MD_motors
    output_MD_motors = {'class_id':2,'hiererchy':'main','level':'class','item_name':'liabilities','matched_with':'','start_pos':-100}
    assert liabilities_level2_start_pos(input_MD_motors) == output_MD_motors

    # DHO
    input_Dho = input_.input_Dho
    output_Dho = {'class_id':2,'hiererchy':'main','level':'class','item_name':'liabilities','matched_with':'','start_pos':-100}
    assert liabilities_level2_start_pos(input_Dho) == output_Dho

    # _Credit_Financials_Poor_Quality
    input_Cre_Fin_PQ = input_.input_Cre_Fin_PQ
    output_Cre_Fin_PQ = {'class_id':2,'hiererchy':'main','level':'class','item_name':'liabilities','matched_with':'liabilities ','start_pos':12}
    assert liabilities_level2_start_pos(input_Cre_Fin_PQ) == output_Cre_Fin_PQ

    # _iyantram
    input_Iyantram = input_.input_Iyantram
    output_Iyantram = {'class_id':2,'hiererchy':'main','level':'class','item_name':'liabilities','matched_with':'','start_pos':-100}
    assert liabilities_level2_start_pos(input_Iyantram) == output_Iyantram

    # _Intex
    input_Intex = input_.input_Intex
    output_Intex = {'class_id':2,'hiererchy':'main','level':'class','item_name':'liabilities','matched_with':'liabilities ','start_pos':10}
    assert liabilities_level2_start_pos(input_Intex) == output_Intex


def test_current_liabilities_level2_start_pos():
    with pytest.raises(TypeError):
        current_liabilities_level2_start_pos('1')
        current_liabilities_level2_start_pos({'z':'10'})
        current_liabilities_level2_start_pos(['0'])
    
    # _Decon
    input_Decon = input_.input_Decon
    output_Decon = {'class_id':2,'sub_class_id':2,'hiererchy':'sub','level':'class','item_name':'current_liabilities','matched_with':'current liabilities ','start_pos':3}
    assert current_liabilities_level2_start_pos(input_Decon) == output_Decon

    # _Credit_Financials
    input_Credit_Fin = input_.input_Credit_Fin
    output_Credit_Fin = {'class_id':2,'sub_class_id':2,'hiererchy':'sub','level':'class','item_name':'current_liabilities','matched_with':'','start_pos':-100}
    assert current_liabilities_level2_start_pos(input_Credit_Fin) == output_Credit_Fin

    # _Shruthi_engg
    input_Shruthi_engg = input_.input_Shruthi_engg
    output_Shruthi_engg = {'class_id':2,'sub_class_id':2,'hiererchy':'sub','level':'class','item_name':'current_liabilities','matched_with':'sundry creditors ','start_pos':24}
    assert current_liabilities_level2_start_pos(input_Shruthi_engg) == output_Shruthi_engg

    # _MD_Motors
    input_MD_motors = input_.input_MD_motors
    output_MD_motors = {'class_id':2,'sub_class_id':2,'hiererchy':'sub','level':'class','item_name':'current_liabilities','matched_with':'sundry creditors ','start_pos':45}
    assert current_liabilities_level2_start_pos(input_MD_motors) == output_MD_motors

    # DHO
    input_Dho = input_.input_Dho
    output_Dho = {'class_id':2,'sub_class_id':2,'hiererchy':'sub','level':'class','item_name':'current_liabilities','matched_with':'current liablities ','start_pos':41}
    assert current_liabilities_level2_start_pos(input_Dho) == output_Dho

    # _Credit_Financials_Poor_Quality
    input_Cre_Fin_PQ = input_.input_Cre_Fin_PQ
    output_Cre_Fin_PQ = {'class_id':2,'sub_class_id':2,'hiererchy':'sub','level':'class','item_name':'current_liabilities','matched_with':'','start_pos':-100}
    assert current_liabilities_level2_start_pos(input_Cre_Fin_PQ) == output_Cre_Fin_PQ

    # _iyantram
    input_Iyantram = input_.input_Iyantram
    output_Iyantram = {'class_id':2,'sub_class_id':2,'hiererchy':'sub','level':'class','item_name':'current_liabilities','matched_with':'current liabilities ','start_pos':3}
    assert current_liabilities_level2_start_pos(input_Iyantram) == output_Iyantram

    # _Intex
    input_Intex = input_.input_Intex
    output_Intex = {'class_id':2,'sub_class_id':2,'hiererchy':'sub','level':'class','item_name':'current_liabilities','matched_with':'current liabilities ','start_pos':20}
    assert current_liabilities_level2_start_pos(input_Intex) == output_Intex



def test_non_current_liabilities_level2_start_pos():
    # raise TypeError if input is not list.
    with pytest.raises(TypeError):
        non_current_liabilities_level2_start_pos((1, 2, 3))
        non_current_liabilities_level2_start_pos('abcd')
        non_current_liabilities_level2_start_pos(1)
        non_current_liabilities_level2_start_pos(1.0)
        non_current_liabilities_level2_start_pos({1: 'a'})
    
    # _Decon
    input_Decon = input_.input_Decon
    output_Decon = {'class_id':2,'sub_class_id':3,'hiererchy':'sub','level':'class','item_name':'non_current_liabilities','matched_with':'','start_pos':-100}
    assert non_current_liabilities_level2_start_pos(input_Decon) == output_Decon

    # _Credit_Financials
    input_Credit_Fin = input_.input_Credit_Fin
    output_Credit_Fin = {'class_id':2,'sub_class_id':3,'hiererchy':'sub','level':'class','item_name':'non_current_liabilities','matched_with':'','start_pos':-100}
    assert non_current_liabilities_level2_start_pos(input_Credit_Fin) == output_Credit_Fin

    # _Shruthi_engg
    input_Shruthi_engg = input_.input_Shruthi_engg
    output_Shruthi_engg = {'class_id': 2,'sub_class_id': 3,'hiererchy':'sub','level':'class','item_name':'non_current_liabilities','matched_with':'electronica finance ','start_pos': 17}
    assert non_current_liabilities_level2_start_pos(input_Shruthi_engg) == output_Shruthi_engg

    # _MD_Motors
    input_MD_motors = input_.input_MD_motors
    output_MD_motors = {'class_id':2,'sub_class_id':3,'hiererchy':'sub','level':'class','item_name':'non_current_liabilities','matched_with':'','start_pos':-100}
    assert non_current_liabilities_level2_start_pos(input_MD_motors) == output_MD_motors

    # DHO
    input_Dho = input_.input_Dho
    output_Dho = {'class_id':2,'sub_class_id':3,'hiererchy':'sub','level':'class','item_name':'non_current_liabilities','matched_with':'loans and advances ','start_pos':18}
    assert non_current_liabilities_level2_start_pos(input_Dho) == output_Dho

    # _Credit_Financials_Poor_Quality
    input_Cre_Fin_PQ = input_.input_Cre_Fin_PQ
    output_Cre_Fin_PQ = {'class_id':2,'sub_class_id':3,'hiererchy':'sub','level':'class','item_name':'non_current_liabilities','matched_with': 'liabilities ','start_pos': 12}
    assert non_current_liabilities_level2_start_pos(input_Cre_Fin_PQ) == output_Cre_Fin_PQ

    # _iyantram
    input_Iyantram = input_.input_Iyantram
    output_Iyantram = {'class_id':2,'sub_class_id':3,'hiererchy':'sub','level':'class','item_name':'non_current_liabilities','matched_with': '','start_pos': -100}
    assert non_current_liabilities_level2_start_pos(input_Iyantram) == output_Iyantram

    # _Intex
    input_Intex = input_.input_Intex
    output_Intex = {'class_id':2,'sub_class_id':3,'hiererchy':'sub','level':'class','item_name':'non_current_liabilities','matched_with': 'loans liability ','start_pos': 16}
    assert non_current_liabilities_level2_start_pos(input_Intex) == output_Intex

def test_equity_level2_start_pos():
    # raise TypeError if input is not list.
    with pytest.raises(TypeError):
        equity_level2_start_pos((1, 2, 3))
        equity_level2_start_pos('abcd')
        equity_level2_start_pos(1)
        equity_level2_start_pos(1.0)
        equity_level2_start_pos({1: 'a'})
        
    # _Decon
    input_Decon = input_.input_Decon
    output_Decon = {'class_id':2,'sub_class_id':1,'hiererchy':'sub','level':'class','item_name':'equity','secondary_matched_with': '','secondary_start_pos': -100,'matched_with':'capital ','start_pos':1}
    assert equity_level2_start_pos(input_Decon) == output_Decon

    # _Credit_Financials
    input_Credit_Fin = input_.input_Credit_Fin
    output_Credit_Fin = {'class_id':2,'sub_class_id':1,'hiererchy':'sub','level':'class','item_name':'equity','matched_with':'capial account ','secondary_matched_with': '','secondary_start_pos': -100,'start_pos':18}
    assert equity_level2_start_pos(input_Credit_Fin) == output_Credit_Fin

    # _Shruthi_engg
    input_Shruthi_engg = input_.input_Shruthi_engg
    output_Shruthi_engg = {'class_id':2,'sub_class_id':1,'hiererchy':'sub','level':'class','item_name':'equity','matched_with':"proprietor's capital a ",'secondary_matched_with': '','secondary_start_pos': -100,'start_pos':10}
    assert equity_level2_start_pos(input_Shruthi_engg) == output_Shruthi_engg

    # _MD_Motors
    input_MD_motors = input_.input_MD_motors
    output_MD_motors = {'class_id':2,'sub_class_id':1,'hiererchy':'sub','level':'class','item_name':'equity','matched_with':'capital ','secondary_matched_with': '','secondary_start_pos': -100,'start_pos':39}
    assert equity_level2_start_pos(input_MD_motors) == output_MD_motors

    # DHO
    input_Dho = input_.input_Dho
    output_Dho = {'class_id':2,'sub_class_id':1,'hiererchy':'sub','level':'class','item_name':'equity','matched_with':'pariners capital ','secondary_matched_with': '','secondary_start_pos': -100,'start_pos': 36}
    assert equity_level2_start_pos(input_Dho) == output_Dho

    # _Credit_Financials_Poor_Quality
    input_Cre_Fin_PQ = input_.input_Cre_Fin_PQ
    output_Cre_Fin_PQ = {'class_id':2,'sub_class_id':1,'hiererchy':'sub','level':'class','item_name':'equity','matched_with':'capital account ','secondary_matched_with': '','secondary_start_pos': -100,'start_pos':13}
    assert equity_level2_start_pos(input_Cre_Fin_PQ) == output_Cre_Fin_PQ

    # _iyantram
    input_Iyantram = input_.input_Iyantram
    output_Iyantram = {'class_id':2,'sub_class_id':1,'hiererchy':'sub','level':'class','item_name':'equity','matched_with':'capital ','secondary_matched_with': '','secondary_start_pos': -100,'start_pos':1}
    assert equity_level2_start_pos(input_Iyantram) == output_Iyantram

    # _Intex
    input_Intex = input_.input_Intex
    output_Intex = {'class_id':2,'sub_class_id':1,'hiererchy':'sub','level':'class','item_name':'equity','matched_with':'capital account ','secondary_matched_with': 'profit & loss a ','secondary_start_pos': 25,'start_pos':11}
    assert equity_level2_start_pos(input_Intex) == output_Intex



def test_total_asset_level1_start_pos():
    # raise TypeError if input is not list.
    with pytest.raises(TypeError):
        total_asset_level1_start_pos((1, 2, 3))
        total_asset_level1_start_pos('abcd')
        total_asset_level1_start_pos(1)
        total_asset_level1_start_pos(1.0)
        total_asset_level1_start_pos({1: 'a'})
        
    # _Decon
    input_Decon = input_.input_Decon
    output_Decon = {'class_id':1,'hiererchy':'main','level':'total','item_name':'total_asset','matched_with':'','start_pos':-100}
    assert total_asset_level1_start_pos(input_Decon) == output_Decon

    # _Credit_Financials
    input_Credit_Fin = input_.input_Credit_Fin
    output_Credit_Fin = {'class_id':1,'hiererchy':'main','level':'total','item_name':'total_asset','matched_with':'','start_pos':-100}
    assert total_asset_level1_start_pos(input_Credit_Fin) == output_Credit_Fin

    # _Shruthi_engg
    input_Shruthi_engg = input_.input_Shruthi_engg
    output_Shruthi_engg = {'class_id':1,'hiererchy':'main','level':'total','item_name':'total_asset','matched_with':'','start_pos':-100}
    assert total_asset_level1_start_pos(input_Shruthi_engg) == output_Shruthi_engg

    # _MD_Motors
    input_MD_motors = input_.input_MD_motors
    output_MD_motors = {'class_id':1,'hiererchy':'main','level':'total','item_name':'total_asset','matched_with':'','start_pos':-100}
    assert total_asset_level1_start_pos(input_MD_motors) == output_MD_motors

    # DHO
    input_Dho = input_.input_Dho
    output_Dho = {'class_id':1,'hiererchy':'main','level':'total','item_name':'total_asset','matched_with':'','start_pos':-100}
    assert total_asset_level1_start_pos(input_Dho) == output_Dho

    # _Credit_Financials_Poor_Quality
    input_Cre_Fin_PQ = input_.input_Cre_Fin_PQ
    output_Cre_Fin_PQ = {'class_id':1,'hiererchy':'main','level':'total','item_name':'total_asset','matched_with':'','start_pos':-100}
    assert total_asset_level1_start_pos(input_Cre_Fin_PQ) == output_Cre_Fin_PQ

    # _iyantram
    input_Iyantram = input_.input_Iyantram
    output_Iyantram = {'class_id':1,'hiererchy':'main','level':'total','item_name':'total_asset','matched_with':'','start_pos':-100}
    assert total_asset_level1_start_pos(input_Iyantram) == output_Iyantram

    # _Intex
    input_Intex = input_.input_Intex
    output_Intex = {'class_id':1,'hiererchy':'main','level':'total','item_name':'total_asset','matched_with':'','start_pos':-100}
    assert total_asset_level1_start_pos(input_Intex) == output_Intex



def test_net_asset_level1_start_pos():
    # raise TypeError if input is not list.
    with pytest.raises(TypeError):
        net_asset_level1_start_pos((1, 2, 3))
        net_asset_level1_start_pos('abcd')
        net_asset_level1_start_pos(1)
        net_asset_level1_start_pos(1.0)
        net_asset_level1_start_pos({1: 'a'})
        
    # _Decon
    input_Decon = input_.input_Decon
    output_Decon = {'class_id':0,'hiererchy':'main','level':'total','item_name':'net_asset','matched_with':'','start_pos':-100}
    assert net_asset_level1_start_pos(input_Decon) == output_Decon

    # _Credit_Financials
    input_Credit_Fin = input_.input_Credit_Fin
    output_Credit_Fin = {'class_id':0,'hiererchy':'main','level':'total','item_name':'net_asset','matched_with':'','start_pos':-100}
    assert net_asset_level1_start_pos(input_Credit_Fin) == output_Credit_Fin

    # _Shruthi_engg
    input_Shruthi_engg = input_.input_Shruthi_engg
    output_Shruthi_engg = {'class_id':0,'hiererchy':'main','level':'total','item_name':'net_asset','matched_with':'','start_pos':-100}
    assert net_asset_level1_start_pos(input_Shruthi_engg) == output_Shruthi_engg

    # _MD_Motors
    input_MD_motors = input_.input_MD_motors
    output_MD_motors = {'class_id':0,'hiererchy':'main','level':'total','item_name':'net_asset','matched_with':'','start_pos':-100}
    assert net_asset_level1_start_pos(input_MD_motors) == output_MD_motors

    # DHO
    input_Dho = input_.input_Dho
    output_Dho = {'class_id':0,'hiererchy':'main','level':'total','item_name':'net_asset','matched_with':'','start_pos':-100}
    assert net_asset_level1_start_pos(input_Dho) == output_Dho

    # _Credit_Financials_Poor_Quality
    input_Cre_Fin_PQ = input_.input_Cre_Fin_PQ
    output_Cre_Fin_PQ = {'class_id':0,'hiererchy':'main','level':'total','item_name':'net_asset','matched_with':'','start_pos':-100}
    assert net_asset_level1_start_pos(input_Cre_Fin_PQ) == output_Cre_Fin_PQ

    # _iyantram
    input_Iyantram = input_.input_Iyantram
    output_Iyantram = {'class_id':0,'hiererchy':'main','level':'total','item_name':'net_asset','matched_with':'','start_pos':-100}
    assert net_asset_level1_start_pos(input_Iyantram) == output_Iyantram

    # _Intex
    input_Intex = input_.input_Intex
    output_Intex = {'class_id':0,'hiererchy':'main','level':'total','item_name':'net_asset','matched_with':'','start_pos':-100}
    assert net_asset_level1_start_pos(input_Intex) == output_Intex




def test_total_current_asset_level2_start_pos():
    # raise TypeError if input is not list.
    with pytest.raises(TypeError):
        total_current_asset_level2_start_pos((1, 2, 3))
        total_current_asset_level2_start_pos('abcd')
        total_current_asset_level2_start_pos(1)
        total_current_asset_level2_start_pos(1.0)
        total_current_asset_level2_start_pos({1: 'a'})
        
    # _Decon
    input_Decon = input_.input_Decon
    output_Decon = {'class_id':1,'sub_class_id':1,'hiererchy':'sub','level':'total','item_name':'total_current_asset','matched_with':'','start_pos':-100}
    assert total_current_asset_level2_start_pos(input_Decon) == output_Decon

    # _Credit_Financials
    input_Credit_Fin = input_.input_Credit_Fin
    output_Credit_Fin = {'class_id':1,'sub_class_id':1,'hiererchy':'sub','level':'total','item_name':'total_current_asset','matched_with':'','start_pos':-100}
    assert total_current_asset_level2_start_pos(input_Credit_Fin) == output_Credit_Fin

    # _Shruthi_engg
    input_Shruthi_engg = input_.input_Shruthi_engg
    output_Shruthi_engg = {'class_id':1,'sub_class_id':1,'hiererchy':'sub','level':'total','item_name':'total_current_asset','matched_with':'','start_pos':-100}
    assert total_current_asset_level2_start_pos(input_Shruthi_engg) == output_Shruthi_engg

    # _MD_Motors
    input_MD_motors = input_.input_MD_motors
    output_MD_motors = {'class_id':1,'sub_class_id':1,'hiererchy':'sub','level':'total','item_name':'total_current_asset','matched_with':'','start_pos':-100}
    assert total_current_asset_level2_start_pos(input_MD_motors) == output_MD_motors

    # DHO
    input_Dho = input_.input_Dho
    output_Dho = {'class_id':1,'sub_class_id':1,'hiererchy':'sub','level':'total','item_name':'total_current_asset','matched_with':'','start_pos':-100}
    assert total_current_asset_level2_start_pos(input_Dho) == output_Dho

    # _Credit_Financials_Poor_Quality
    input_Cre_Fin_PQ = input_.input_Cre_Fin_PQ
    output_Cre_Fin_PQ = {'class_id':1,'sub_class_id':1,'hiererchy':'sub','level':'total','item_name':'total_current_asset','matched_with':'','start_pos':-100}
    assert total_current_asset_level2_start_pos(input_Cre_Fin_PQ) == output_Cre_Fin_PQ

    # _iyantram
    input_Iyantram = input_.input_Iyantram
    output_Iyantram = {'class_id':1,'sub_class_id':1,'hiererchy':'sub','level':'total','item_name':'total_current_asset','matched_with':'','start_pos':-100}
    assert total_current_asset_level2_start_pos(input_Iyantram) == output_Iyantram

    # _Intex
    input_Intex = input_.input_Intex
    output_Intex = {'class_id':1,'sub_class_id':1,'hiererchy':'sub','level':'total','item_name':'total_current_asset','matched_with':'','start_pos':-100}
    assert total_current_asset_level2_start_pos(input_Intex) == output_Intex



def test_net_current_asset_level2_start_pos():
    # raise TypeError if input is not list.
    with pytest.raises(TypeError):
        net_current_asset_level2_start_pos((1, 2, 3))
        net_current_asset_level2_start_pos('abcd')
        net_current_asset_level2_start_pos(1)
        net_current_asset_level2_start_pos(1.0)
        net_current_asset_level2_start_pos({1: 'a'})
        
    # _Decon
    input_Decon = input_.input_Decon
    output_Decon = {'class_id':0,'hiererchy':'main','level':'total','item_name':'net_current_asset','matched_with':'','start_pos':-100}
    assert net_current_asset_level2_start_pos(input_Decon) == output_Decon

    # _Credit_Financials
    input_Credit_Fin = input_.input_Credit_Fin
    output_Credit_Fin = {'class_id':0,'hiererchy':'main','level':'total','item_name':'net_current_asset','matched_with':'','start_pos':-100}
    assert net_current_asset_level2_start_pos(input_Credit_Fin) == output_Credit_Fin

    # _Shruthi_engg
    input_Shruthi_engg = input_.input_Shruthi_engg
    output_Shruthi_engg = {'class_id':0,'hiererchy':'main','level':'total','item_name':'net_current_asset','matched_with':'','start_pos':-100}
    assert net_current_asset_level2_start_pos(input_Shruthi_engg) == output_Shruthi_engg

    # _MD_Motors
    input_MD_motors = input_.input_MD_motors
    output_MD_motors = {'class_id':0,'hiererchy':'main','level':'total','item_name':'net_current_asset','matched_with':'','start_pos':-100}
    assert net_current_asset_level2_start_pos(input_MD_motors) == output_MD_motors

    # DHO
    input_Dho = input_.input_Dho
    output_Dho = {'class_id':0,'hiererchy':'main','level':'total','item_name':'net_current_asset','matched_with':'','start_pos':-100}
    assert net_current_asset_level2_start_pos(input_Dho) == output_Dho

    # _Credit_Financials_Poor_Quality
    input_Cre_Fin_PQ = input_.input_Cre_Fin_PQ
    output_Cre_Fin_PQ = {'class_id':0,'hiererchy':'main','level':'total','item_name':'net_current_asset','matched_with':'','start_pos':-100}
    assert net_current_asset_level2_start_pos(input_Cre_Fin_PQ) == output_Cre_Fin_PQ

    # _iyantram
    input_Iyantram = input_.input_Iyantram
    output_Iyantram = {'class_id':0,'hiererchy':'main','level':'total','item_name':'net_current_asset','matched_with':'','start_pos':-100}
    assert net_current_asset_level2_start_pos(input_Iyantram) == output_Iyantram

    # _Intex
    input_Intex = input_.input_Intex
    output_Intex = {'class_id':0,'hiererchy':'main','level':'total','item_name':'net_current_asset','matched_with':'','start_pos':-100}
    assert net_current_asset_level2_start_pos(input_Intex) == output_Intex



def test_total_non_current_asset_level2_start_pos():
    # raise TypeError if input is not list.
    with pytest.raises(TypeError):
        total_non_current_asset_level2_start_pos((1, 2, 3))
        total_non_current_asset_level2_start_pos('abcd')
        total_non_current_asset_level2_start_pos(1)
        total_non_current_asset_level2_start_pos(1.0)
        total_non_current_asset_level2_start_pos({1: 'a'})
        
    # _Decon
    input_Decon = input_.input_Decon
    output_Decon = {'class_id':1,'sub_class_id':2,'hiererchy':'sub','level':'total','item_name':'total_non_current_asset','matched_with':'','start_pos':-100}
    assert total_non_current_asset_level2_start_pos(input_Decon) == output_Decon

    # _Credit_Financials
    input_Credit_Fin = input_.input_Credit_Fin
    output_Credit_Fin = {'class_id':1,'sub_class_id':2,'hiererchy':'sub','level':'total','item_name':'total_non_current_asset','matched_with':'','start_pos':-100}
    assert total_non_current_asset_level2_start_pos(input_Credit_Fin) == output_Credit_Fin

    # _Shruthi_engg
    input_Shruthi_engg = input_.input_Shruthi_engg
    output_Shruthi_engg = {'class_id':1,'sub_class_id':2,'hiererchy':'sub','level':'total','item_name':'total_non_current_asset','matched_with':'','start_pos':-100}
    assert total_non_current_asset_level2_start_pos(input_Shruthi_engg) == output_Shruthi_engg

    # _MD_Motors
    input_MD_motors = input_.input_MD_motors
    output_MD_motors = {'class_id':1,'sub_class_id':2,'hiererchy':'sub','level':'total','item_name':'total_non_current_asset','matched_with':'','start_pos':-100}
    assert total_non_current_asset_level2_start_pos(input_MD_motors) == output_MD_motors

    # DHO
    input_Dho = input_.input_Dho
    output_Dho = {'class_id':1,'sub_class_id':2,'hiererchy':'sub','level':'total','item_name':'total_non_current_asset','matched_with':'','start_pos':-100}
    assert total_non_current_asset_level2_start_pos(input_Dho) == output_Dho

    # _Credit_Financials_Poor_Quality
    input_Cre_Fin_PQ = input_.input_Cre_Fin_PQ
    output_Cre_Fin_PQ = {'class_id':1,'sub_class_id':2,'hiererchy':'sub','level':'total','item_name':'total_non_current_asset','matched_with':'','start_pos':-100}
    assert total_non_current_asset_level2_start_pos(input_Cre_Fin_PQ) == output_Cre_Fin_PQ

    # _iyantram
    input_Iyantram = input_.input_Iyantram
    output_Iyantram = {'class_id':1,'sub_class_id':2,'hiererchy':'sub','level':'total','item_name':'total_non_current_asset','matched_with':'','start_pos':-100}
    assert total_non_current_asset_level2_start_pos(input_Iyantram) == output_Iyantram

    # _Intex
    input_Intex = input_.input_Intex
    output_Intex = {'class_id':1,'sub_class_id':2,'hiererchy':'sub','level':'total','item_name':'total_non_current_asset','matched_with':'','start_pos':-100}
    assert total_non_current_asset_level2_start_pos(input_Intex) == output_Intex


def test_total_equity_liabilities_level1_start_pos():
    # raise TypeError if input is not list.
    with pytest.raises(TypeError):
        total_equity_liabilities_level1_start_pos((1, 2, 3))
        total_equity_liabilities_level1_start_pos('abcd')
        total_equity_liabilities_level1_start_pos(1)
        total_equity_liabilities_level1_start_pos(1.0)
        total_equity_liabilities_level1_start_pos({1: 'a'})
        
    # _Decon
    input_Decon= input_.input_Decon
    output_Decon = {'class_id':2,'hiererchy':'main','level':'total','item_name':'total_equity_liabilities','matched_with':'','start_pos':-100}
    assert total_equity_liabilities_level1_start_pos(input_Decon) == output_Decon

    # _Credit_Financials
    input_Credit_Fin = input_.input_Credit_Fin
    output_Credit_Fin = {'class_id':2,'hiererchy':'main','level':'total','item_name':'total_equity_liabilities','matched_with':'','start_pos':-100}
    assert total_equity_liabilities_level1_start_pos(input_Credit_Fin) == output_Credit_Fin

    # _Shruthi_engg
    input_Shruthi_engg = input_.input_Shruthi_engg
    output_Shruthi_engg = {'class_id':2,'hiererchy':'main','level':'total','item_name':'total_equity_liabilities','matched_with':'','start_pos':-100}
    assert total_equity_liabilities_level1_start_pos(input_Shruthi_engg) == output_Shruthi_engg

    # _MD_Motors
    input_MD_motors = input_.input_MD_motors
    output_MD_motors = {'class_id':2,'hiererchy':'main','level':'total','item_name':'total_equity_liabilities','matched_with':'','start_pos':-100}
    assert total_equity_liabilities_level1_start_pos(input_MD_motors) == output_MD_motors

    # DHO
    input_Dho = input_.input_Dho
    output_Dho = {'class_id':2,'hiererchy':'main','level':'total','item_name':'total_equity_liabilities','matched_with':'','start_pos':-100}
    assert total_equity_liabilities_level1_start_pos(input_Dho) == output_Dho

    # _Credit_Financials_Poor_Quality
    input_Cre_Fin_PQ = input_.input_Cre_Fin_PQ
    output_Cre_Fin_PQ = {'class_id':2,'hiererchy':'main','level':'total','item_name':'total_equity_liabilities','matched_with':'','start_pos':-100}
    assert total_equity_liabilities_level1_start_pos(input_Cre_Fin_PQ) == output_Cre_Fin_PQ

    # _iyantram
    input_Iyantram = input_.input_Iyantram
    output_Iyantram = {'class_id':2,'hiererchy':'main','level':'total','item_name':'total_equity_liabilities','matched_with':'','start_pos':-100}
    assert total_equity_liabilities_level1_start_pos(input_Iyantram) == output_Iyantram

    # _Intex
    input_Intex = input_.input_Intex
    output_Intex = {'class_id':2,'hiererchy':'main','level':'total','item_name':'total_equity_liabilities','matched_with':'','start_pos':-100}
    assert total_equity_liabilities_level1_start_pos(input_Intex) == output_Intex



def test_total_equity_level2_start_pos():
    # raise TypeError if input is not list.
    with pytest.raises(TypeError):
        total_equity_level2_start_pos((1, 2, 3))
        total_equity_level2_start_pos('abcd')
        total_equity_level2_start_pos(1)
        total_equity_level2_start_pos(1.0)
        total_equity_level2_start_pos({1: 'a'})
        
    # _Decon
    input_Decon = input_.input_Decon
    output_Decon = {'class_id':2,'sub_class_id':1,'hiererchy':'sub','level':'total','item_name':'total_equity','matched_with':'','start_pos':-100}
    assert total_equity_level2_start_pos(input_Decon) == output_Decon

    # _Credit_Financials
    input_Credit_Fin = input_.input_Credit_Fin
    output_Credit_Fin = {'class_id':2,'sub_class_id':1,'hiererchy':'sub','level':'total','item_name':'total_equity','matched_with':'','start_pos':-100}
    assert total_equity_level2_start_pos(input_Credit_Fin) == output_Credit_Fin

    # _Shruthi_engg
    input_Shruthi_engg = input_.input_Shruthi_engg
    output_Shruthi_engg = {'class_id':2,'sub_class_id':1,'hiererchy':'sub','level':'total','item_name':'total_equity','matched_with':'','start_pos':-100}
    assert total_equity_level2_start_pos(input_Shruthi_engg) == output_Shruthi_engg

    # _MD_Motors
    input_MD_motors = input_.input_MD_motors
    output_MD_motors = {'class_id':2,'sub_class_id':1,'hiererchy':'sub','level':'total','item_name':'total_equity','matched_with':'','start_pos':-100}
    assert total_equity_level2_start_pos(input_MD_motors) == output_MD_motors

    # DHO
    input_Dho = input_.input_Dho
    output_Dho = {'class_id':2,'sub_class_id':1,'hiererchy':'sub','level':'total','item_name':'total_equity','matched_with':'','start_pos':-100}
    assert total_equity_level2_start_pos(input_Dho) == output_Dho

    # _Credit_Financials_Poor_Quality
    input_Cre_Fin_PQ = input_.input_Cre_Fin_PQ
    output_Cre_Fin_PQ = {'class_id':2,'sub_class_id':1,'hiererchy':'sub','level':'total','item_name':'total_equity','matched_with':'','start_pos':-100}
    assert total_equity_level2_start_pos(input_Cre_Fin_PQ) == output_Cre_Fin_PQ

    # _iyantram
    input_Iyantram = input_.input_Iyantram
    output_Iyantram = {'class_id':2,'sub_class_id':1,'hiererchy':'sub','level':'total','item_name':'total_equity','matched_with':'','start_pos':-100}
    assert total_equity_level2_start_pos(input_Iyantram) == output_Iyantram

    # _Intex
    input_Intex = input_.input_Intex
    output_Intex = {'class_id':2,'sub_class_id':1,'hiererchy':'sub','level':'total','item_name':'total_equity','matched_with':'','start_pos':-100}
    assert total_equity_level2_start_pos(input_Intex) == output_Intex


def test_total_liabilities_level2_start_pos():
    # raise TypeError if input is not list.
    with pytest.raises(TypeError):
        total_liabilities_level2_start_pos((1, 2, 3))
        total_liabilities_level2_start_pos('abcd')
        total_liabilities_level2_start_pos(1)
        total_liabilities_level2_start_pos(1.0)
        total_liabilities_level2_start_pos({1: 'a'})
        
    # _Decon
    input_Decon = input_.input_Decon
    output_Decon = {'class_id':2,'hiererchy':'main','level':'total','item_name':'total_liabilities','matched_with':'','start_pos':-100}
    assert total_liabilities_level2_start_pos(input_Decon) == output_Decon

    # _Credit_Financials
    input_Credit_Fin = input_.input_Credit_Fin
    output_Credit_Fin = {'class_id':2,'hiererchy':'main','level':'total','item_name':'total_liabilities','matched_with':'','start_pos':-100}
    assert total_liabilities_level2_start_pos(input_Credit_Fin) == output_Credit_Fin

    # _Shruthi_engg
    input_Shruthi_engg = input_.input_Shruthi_engg
    output_Shruthi_engg = {'class_id':2,'hiererchy':'main','level':'total','item_name':'total_liabilities','matched_with':'','start_pos':-100}
    assert total_liabilities_level2_start_pos(input_Shruthi_engg) == output_Shruthi_engg

    # _MD_Motors
    input_MD_motors = input_.input_MD_motors
    output_MD_motors = {'class_id':2,'hiererchy':'main','level':'total','item_name':'total_liabilities','matched_with':'','start_pos':-100}
    assert total_liabilities_level2_start_pos(input_MD_motors) == output_MD_motors

    # DHO
    input_Dho = input_.input_Dho
    output_Dho = {'class_id':2,'hiererchy':'main','level':'total','item_name':'total_liabilities','matched_with':'','start_pos':-100}
    assert total_liabilities_level2_start_pos(input_Dho) == output_Dho

    # _Credit_Financials_Poor_Quality
    input_Cre_Fin_PQ = input_.input_Cre_Fin_PQ
    output_Cre_Fin_PQ = {'class_id':2,'hiererchy':'main','level':'total','item_name':'total_liabilities','matched_with':'','start_pos':-100}
    assert total_liabilities_level2_start_pos(input_Cre_Fin_PQ) == output_Cre_Fin_PQ

    # _iyantram
    input_Iyantram = input_.input_Iyantram
    output_Iyantram = {'class_id':2,'hiererchy':'main','level':'total','item_name':'total_liabilities','matched_with':'','start_pos':-100}
    assert total_liabilities_level2_start_pos(input_Iyantram) == output_Iyantram

    # _Intex
    input_Intex = input_.input_Intex
    output_Intex = {'class_id':2,'hiererchy':'main','level':'total','item_name':'total_liabilities','matched_with':'','start_pos':-100}
    assert total_liabilities_level2_start_pos(input_Intex) == output_Intex




def test_net_liabilities_level1_start_pos():
    # raise TypeError if input is not list.
    with pytest.raises(TypeError):
        net_liabilities_level1_start_pos((1, 2, 3))
        net_liabilities_level1_start_pos('abcd')
        net_liabilities_level1_start_pos(1)
        net_liabilities_level1_start_pos(1.0)
        net_liabilities_level1_start_pos({1: 'a'})
        
    # _Decon
    input_Decon = input_.input_Decon
    output_Decon = {'class_id':0,'hiererchy':'main','level':'total','item_name':'net_liabilities','matched_with':'','start_pos':-100}
    assert net_liabilities_level1_start_pos(input_Decon) == output_Decon

    # _Credit_Financials
    input_Credit_Fin = input_.input_Credit_Fin
    output_Credit_Fin = {'class_id':0,'hiererchy':'main','level':'total','item_name':'net_liabilities','matched_with':'','start_pos':-100}
    assert net_liabilities_level1_start_pos(input_Credit_Fin) == output_Credit_Fin

    # _Shruthi_engg
    input_Shruthi_engg = input_.input_Shruthi_engg
    output_Shruthi_engg = {'class_id':0,'hiererchy':'main','level':'total','item_name':'net_liabilities','matched_with':'','start_pos':-100}
    assert net_liabilities_level1_start_pos(input_Shruthi_engg) == output_Shruthi_engg

    # _MD_Motors
    input_MD_motors = input_.input_MD_motors
    output_MD_motors = {'class_id':0,'hiererchy':'main','level':'total','item_name':'net_liabilities','matched_with':'','start_pos':-100}
    assert net_liabilities_level1_start_pos(input_MD_motors) == output_MD_motors

    # DHO
    input_Dho = input_.input_Dho
    output_Dho = {'class_id':0,'hiererchy':'main','level':'total','item_name':'net_liabilities','matched_with':'','start_pos':-100}
    assert net_liabilities_level1_start_pos(input_Dho) == output_Dho

    # _Credit_Financials_Poor_Quality
    input_Cre_Fin_PQ = input_.input_Cre_Fin_PQ
    output_Cre_Fin_PQ = {'class_id':0,'hiererchy':'main','level':'total','item_name':'net_liabilities','matched_with':'','start_pos':-100}
    assert net_liabilities_level1_start_pos(input_Cre_Fin_PQ) == output_Cre_Fin_PQ

    # _iyantram
    input_Iyantram = input_.input_Iyantram
    output_Iyantram = {'class_id':0,'hiererchy':'main','level':'total','item_name':'net_liabilities','matched_with':'','start_pos':-100}
    assert net_liabilities_level1_start_pos(input_Iyantram) == output_Iyantram

    # _Intex
    input_Intex = input_.input_Intex
    output_Intex = {'class_id':0,'hiererchy':'main','level':'total','item_name':'net_liabilities','matched_with':'','start_pos':-100}
    assert net_liabilities_level1_start_pos(input_Intex) == output_Intex



def test_total_current_liabilities_level2_start_pos():
    # raise TypeError if input is not list.
    with pytest.raises(TypeError):
        total_current_liabilities_level2_start_pos((1, 2, 3))
        total_current_liabilities_level2_start_pos('abcd')
        total_current_liabilities_level2_start_pos(1)
        total_current_liabilities_level2_start_pos(1.0)
        total_current_liabilities_level2_start_pos({1: 'a'})
        
    # _Decon
    input_Decon= input_.input_Decon
    output_Decon = {'class_id':2,'sub_class_id':2,'hiererchy':'sub','level':'total','item_name':'total_current_liabilities','matched_with':'','start_pos':-100}
    assert total_current_liabilities_level2_start_pos(input_Decon) == output_Decon

    # _Credit_Financials
    input_Credit_Fin = input_.input_Credit_Fin
    output_Credit_Fin = {'class_id':2,'sub_class_id':2,'hiererchy':'sub','level':'total','item_name':'total_current_liabilities','matched_with':'','start_pos':-100}
    assert total_current_liabilities_level2_start_pos(input_Credit_Fin) == output_Credit_Fin

    # _Shruthi_engg
    input_Shruthi_engg = input_.input_Shruthi_engg
    output_Shruthi_engg = {'class_id':2,'sub_class_id':2,'hiererchy':'sub','level':'total','item_name':'total_current_liabilities','matched_with':'','start_pos':-100}
    assert total_current_liabilities_level2_start_pos(input_Shruthi_engg) == output_Shruthi_engg

    # _MD_Motors
    input_MD_motors = input_.input_MD_motors
    output_MD_motors = {'class_id':2,'sub_class_id':2,'hiererchy':'sub','level':'total','item_name':'total_current_liabilities','matched_with':'','start_pos':-100}
    assert total_current_liabilities_level2_start_pos(input_MD_motors) == output_MD_motors

    # DHO
    input_Dho = input_.input_Dho
    output_Dho = {'class_id':2,'sub_class_id':2,'hiererchy':'sub','level':'total','item_name':'total_current_liabilities','matched_with':'','start_pos':-100}
    assert total_current_liabilities_level2_start_pos(input_Dho) == output_Dho

    # _Credit_Financials_Poor_Quality
    input_Cre_Fin_PQ = input_.input_Cre_Fin_PQ
    output_Cre_Fin_PQ = {'class_id':2,'sub_class_id':2,'hiererchy':'sub','level':'total','item_name':'total_current_liabilities','matched_with':'','start_pos':-100}
    assert total_current_liabilities_level2_start_pos(input_Cre_Fin_PQ) == output_Cre_Fin_PQ

    # _iyantram
    input_Iyantram = input_.input_Iyantram
    output_Iyantram = {'class_id':2,'sub_class_id':2,'hiererchy':'sub','level':'total','item_name':'total_current_liabilities','matched_with':'','start_pos':-100}
    assert total_current_liabilities_level2_start_pos(input_Iyantram) == output_Iyantram

    # _Intex
    input_Intex = input_.input_Intex
    output_Intex = {'class_id':2,'sub_class_id':2,'hiererchy':'sub','level':'total','item_name':'total_current_liabilities','matched_with':'','start_pos':-100}
    assert total_current_liabilities_level2_start_pos(input_Intex) == output_Intex



def test_total_non_current_liabilities_level2_start_pos():
    # raise TypeError if input is not list.
    with pytest.raises(TypeError):
        total_non_current_liabilities_level2_start_pos((1, 2, 3))
        total_non_current_liabilities_level2_start_pos('abcd')
        total_non_current_liabilities_level2_start_pos(1)
        total_non_current_liabilities_level2_start_pos(1.0)
        total_non_current_liabilities_level2_start_pos({1: 'a'})
        
    # _Decon
    input_Decon = input_.input_Decon
    output_Decon = {'class_id':2,'sub_class_id':3,'hiererchy':'sub','level':'total','item_name':'total_non_current_liabilities','matched_with':'','start_pos':-100}
    assert total_non_current_liabilities_level2_start_pos(input_Decon) == output_Decon

    # _Credit_Financials
    input_Credit_Fin = input_.input_Credit_Fin
    output_Credit_Fin = {'class_id':2,'sub_class_id':3,'hiererchy':'sub','level':'total','item_name':'total_non_current_liabilities','matched_with':'','start_pos':-100}
    assert total_non_current_liabilities_level2_start_pos(input_Credit_Fin) == output_Credit_Fin

    # _Shruthi_engg
    input_Shruthi_engg = input_.input_Shruthi_engg
    output_Shruthi_engg = {'class_id':2,'sub_class_id':3,'hiererchy':'sub','level':'total','item_name':'total_non_current_liabilities','matched_with':'','start_pos':-100}
    assert total_non_current_liabilities_level2_start_pos(input_Shruthi_engg) == output_Shruthi_engg

    # _MD_Motors
    input_MD_motors = input_.input_MD_motors
    output_MD_motors = {'class_id':2,'sub_class_id':3,'hiererchy':'sub','level':'total','item_name':'total_non_current_liabilities','matched_with':'','start_pos':-100}
    assert total_non_current_liabilities_level2_start_pos(input_MD_motors) == output_MD_motors

    # DHO
    input_Dho = input_.input_Dho
    output_Dho = {'class_id':2,'sub_class_id':3,'hiererchy':'sub','level':'total','item_name':'total_non_current_liabilities','matched_with':'','start_pos':-100}
    assert total_non_current_liabilities_level2_start_pos(input_Dho) == output_Dho

    # _Credit_Financials_Poor_Quality
    input_Cre_Fin_PQ = input_.input_Cre_Fin_PQ
    output_Cre_Fin_PQ = {'class_id':2,'sub_class_id':3,'hiererchy':'sub','level':'total','item_name':'total_non_current_liabilities','matched_with':'','start_pos':-100}
    assert total_non_current_liabilities_level2_start_pos(input_Cre_Fin_PQ) == output_Cre_Fin_PQ

    # _iyantram
    input_Iyantram = input_.input_Iyantram
    output_Iyantram = {'class_id':2,'sub_class_id':3,'hiererchy':'sub','level':'total','item_name':'total_non_current_liabilities','matched_with':'','start_pos':-100}
    assert total_non_current_liabilities_level2_start_pos(input_Iyantram) == output_Iyantram

    # _Intex
    input_Intex = input_.input_Intex
    output_Intex = {'class_id':2,'sub_class_id':3,'hiererchy':'sub','level':'total','item_name':'total_non_current_liabilities','matched_with':'','start_pos':-100}
    assert total_non_current_liabilities_level2_start_pos(input_Intex) == output_Intex




def test_total_any_level():
    # raise TypeError if input is not list.
    with pytest.raises(TypeError):
        total_any_level((1, 2, 3))
        total_any_level('abcd')
        total_any_level(1)
        total_any_level(1.0)
        total_any_level({1: 'a'})
        
    # _Decon
    input_Decon = input_.input_Decon
    output_Decon = [{'class_id':0,'hiererchy':'Null','level':'total','item_name':'total','matched_with':'total 5','start_pos':5},{'class_id':0,'hiererchy':'Null','level':'total','item_name':'total','matched_with':'total 12','start_pos':12}]
    assert total_any_level(input_Decon) == output_Decon

    # _Credit_Financials
    input_Credit_Fin = input_.input_Credit_Fin
    output_Credit_Fin = []
    assert total_any_level(input_Credit_Fin) == output_Credit_Fin

    # _Shruthi_engg
    input_Shruthi_engg = input_.input_Shruthi_engg
    output_Shruthi_engg = []
    assert total_any_level(input_Shruthi_engg) == output_Shruthi_engg

    # _MD_Motors
    input_MD_motors = input_.input_MD_motors
    output_MD_motors = []
    assert total_any_level(input_MD_motors) == output_MD_motors

    # DHO
    input_Dho = input_.input_Dho
    output_Dho = []
    assert total_any_level(input_Dho) == output_Dho

    # _Credit_Financials_Poor_Quality
    input_Cre_Fin_PQ = input_.input_Cre_Fin_PQ
    output_Cre_Fin_PQ = [{'class_id':0,'hiererchy':'Null','level':'total','item_name':'total','matched_with':'total 11','start_pos':11},{'class_id':0,'hiererchy':'Null','level':'total','item_name':'total','matched_with':'total 17','start_pos':17}]
    assert total_any_level(input_Cre_Fin_PQ) == output_Cre_Fin_PQ

    # _iyantram
    input_Iyantram = input_.input_Iyantram
    output_Iyantram = [{'class_id':0,'hiererchy':'Null','level':'total','item_name':'total','matched_with':'total 5','start_pos':5},{'class_id':0,'hiererchy':'Null','level':'total','item_name':'total','matched_with':'total 12','start_pos':12}]
    assert total_any_level(input_Iyantram) == output_Iyantram

    # _Intex
    input_Intex = input_.input_Intex
    output_Intex = [{'class_id':0,'hiererchy':'Null','level':'total','item_name':'total','matched_with':'total 9','start_pos':9},{'class_id':0,'hiererchy':'Null','level':'total','item_name':'total','matched_with':'total 29','start_pos':29}]
    assert total_any_level(input_Intex) == output_Intex










    
    
    