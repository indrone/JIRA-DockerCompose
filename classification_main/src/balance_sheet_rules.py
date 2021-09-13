from fuzzywuzzy import fuzz
from nltk.corpus import wordnet
import nltk,re
import difflib
import yaml

net_current_asset_pos = -100
asset_pos = -100
equity_liabilities_pos = -100
liability_pos = -100
equity_pos = -100
non_current_liabilities_pos = -100
current_liabilities_pos = -100
application_asset = False
total_asset_pos = -100
total_current_asset_pos = -100
total_non_current_asset_pos = -100
total_equity_liabilities_pos = -100
total_liabilities_pos = -100
total_equity_pos = -100
total_current_liabilities_pos = -100
total_non_current_liabilities_pos = -100

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
            return(corpus)
        except yaml.YAMLError as exc:
            print(exc)
            return(exc)
            raise

corpus=yaml_parse()

class_corpus = corpus["balance_sheet_BS"]["class_corpus"]
current_assets_corpus =corpus["balance_sheet_BS"]["current_assets_corpus"]
non_current_assets_corpus =corpus["balance_sheet_BS"]["non_current_assets_corpus"]
current_liabilities_corpus=corpus["balance_sheet_BS"]["current_liabilities_corpus"]
non_current_liabilities_corpus=corpus["balance_sheet_BS"]["non_current_liabilities_corpus"]
bank_corpus = corpus["balance_sheet_BS"]["bank_corpus"]
equity_corpus=corpus["balance_sheet_BS"]["equity_corpus"]
avoid_calculated_field=corpus["balance_sheet_BS"]["calculated_field_bs"]

def check_name(name:str)->list: 

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

def find_amount_list(list_: list) -> list:
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
    list_amount=[]
    try:
        for each in list_:
            list_amount.append(list(each.values())[0])
            
    except:
        pass

    return list_amount


def difflib_matcher(extracted_string: str, query_string: str)-> int:
    """
    Sequence matching to check if a word is present in sentence or not

    Parameters
    ----------
    extracted_string: str
        Sentence
    query_string: str
        word

    Returns
    -------
    int
        Match probability
    """
    s = difflib.SequenceMatcher(None, extracted_string, query_string)
    return sum(n for i,j,n in s.get_matching_blocks()) / float(len(query_string))


def asset_level1_start_pos(list_:list)-> dict:
    """
    Find and return start_pos and linematched_with of asset from extracted BS table

    Parameters
    ----------
    list_ : list
        List of index of lineitems 

    Returns
    --------
    asset_dict: dict
        Dictionary containing lineitem name and index position of asset
    """

    asset_dict= {"class_id":1,"hiererchy":"main","level":"class","item_name":"asset","matched_with":"","start_pos":-100,"end_position":-100}
    list_2=find_list(list_)
    item_found=0
    global asset_pos, application_asset


    for item in list_2:
        if fuzz.token_sort_ratio(item.lower(),"asset")>85 and not "current" in item.lower() and not "total" in item.lower() and item_found==0:
            asset_dict["start_pos"]= list_2.index(item)
            asset_dict["matched_with"]= item
            asset_pos = list_2.index(item)
            item_found=1
        else:
            pass

    if asset_dict["start_pos"] == -100 and item_found==0:
        for item in list_2:
            if fuzz.partial_ratio(item.lower(),"application")>85 and not "current" in item.lower() and not "share" in item.lower() and not "tax" in item.lower() and not "deducted" in item.lower() and item_found==0:
                asset_dict["start_pos"]= list_2.index(item)
                asset_dict["matched_with"]= item
                asset_pos = list_2.index(item)
                application_asset = True
                item_found=1

    return asset_dict

def total_asset_level1_start_pos(list_:list)-> dict:
    """
    Find and return start_pos and linematched_with of total asset from extracted BS table

    Parameters
    ----------
    list_ : list
        List of index of lineitems 

    Returns
    --------
    total_asset_dict: dict
        Dictionary containing lineitem name and index position of total asset
    """

    total_asset_dict = {"class_id":1,"hiererchy":"main","level":"total","item_name":"total_asset","matched_with":"","start_pos":-100}
    list_2 = find_list(list_)
    item_found = 0
    global total_asset_pos

    for item in list_2:
        if fuzz.token_sort_ratio(item.lower(),"total assets") > 80 and not "current" in item.lower() and difflib_matcher(item.lower(),"total")>= 0.8 and item_found == 0:
            total_asset_dict["start_pos"] = list_2.index(item)
            total_asset_dict["matched_with"] = item
            total_asset_pos = list_2.index(item)
            item_found = 1
        else:
            pass

    return total_asset_dict


def net_asset_level1_start_pos(list_:list)-> dict:
    """
    Find and return start_pos and linematched_with of net asset from extracted BS table

    Parameters
    ----------
    list_ : list
        List of index of lineitems 

    Returns
    --------
    total_asset_dict: dict
        Dictionary containing lineitem name and index position of net asset
    """

    net_asset_dict= {"class_id":0,"hiererchy":"main","level":"total","item_name":"net_asset","matched_with":"","start_pos":-100}
    list_2=find_list(list_)
    item_found = 0

    for item in list_2:
        if fuzz.token_sort_ratio(item.lower(),"net assets")>85 and not "current" in item.lower() and not "total" in item.lower() and "net" in item.lower() and item_found == 0:
            net_asset_dict["start_pos"]= list_2.index(item)
            net_asset_dict["matched_with"]= item
            item_found = 1
        else:
            pass

    return net_asset_dict

def current_asset_level2_start_pos(list_:list)-> dict:
    """
    Find and return start_pos and linematched_with of current_asset from extracted BS table

    Parameters
    ----------
    list_ : list
        List of index of lineitems 

    Returns
    --------
    current_asset_dict: dict
        Dictionary containing lineitem name and index position of current_asset
    """
    
    current_asset_dict= {"class_id":1,"sub_class_id":1,"hiererchy":"sub","level":"class","item_name":"current_asset","matched_with":"","start_pos":-100,"end_position":-100}
    list_2=find_list(list_)
    item_found = 0
    current_asset_direct_search = False
    current_asset_corpus_search = False
    item_before_ca = 0 # For tracking lineitems(denoting current asset) before current asset
    item_closing_stock = 0
    global asset_pos

    for item in list_2:
        if fuzz.token_sort_ratio(item.lower(),"current assets")>85 and not "non" in item.lower() and not "total" in item.lower() and not "other" in item.lower() and item_found == 0:
            if len(item.lower().strip().split(" "))>2:
                if len(item.lower().strip().split(" ")[:-2])<1:
                    current_asset_dict["start_pos"]= list_2.index(item)
                    current_asset_dict["matched_with"]= item
                    current_asset_direct_search = True
                    item_found = 1
            elif len(item.lower().strip().split(" "))<=2:
                    current_asset_dict["start_pos"]= list_2.index(item)
                    current_asset_dict["matched_with"]= item
                    current_asset_direct_search = True
                    item_found = 1
        else:
            pass

    if current_asset_dict["start_pos"]== -100:
        for item in list_2:
            for word in current_assets_corpus:
                if fuzz.token_sort_ratio(item.lower(),word)>85 and item_found==0:
                    current_asset_dict["start_pos"]= list_2.index(item)
                    current_asset_dict["matched_with"]= item
                    current_asset_corpus_search = True
                    item_found=1

    if current_asset_dict["start_pos"]== -100 and item_found == 0:
        for item in list_2:
            if fuzz.partial_ratio(item.lower(),"current")>85 and fuzz.partial_ratio(item.lower(),"assets")>85 and not "non" in item.lower() and not "total" in item.lower() and not "other" in item.lower() and item_found==0:
                    current_asset_dict["start_pos"]= list_2.index(item)
                    current_asset_dict["matched_with"]= item
                    current_asset_direct_search = True
                    item_found=1

    # Check current asset position based on corpus search but corpus word must match with 3 requested words 
    
    if current_asset_dict["start_pos"]== -100:          
        for item in list_2:         
            for word in current_assets_corpus:
                count = 0
                for i_word in word.split(" "):
                    if fuzz.partial_ratio(item.lower(),i_word)>85 and item_found==0:
                        count+=1
                        if count == 3:
                            current_asset_dict["start_pos"]= list_2.index(item)
                            current_asset_dict["matched_with"]= item
                            current_asset_corpus_search = True
                            item_found=1
                            break   

    # If Any lineitem (denoting current asset) is placed between asset and current asset (direct search) position,
    # then change the start position

    if item_found == 1 and current_asset_direct_search == True and asset_pos != -100:
        for item in list_2[asset_pos:current_asset_dict["start_pos"]]:
            for word in current_assets_corpus:
                if fuzz.token_sort_ratio(item.lower(),word)>85 and "current" in item.lower() and "non" not in item.lower() and item_before_ca == 0:
                    current_asset_dict["start_pos"]= list_2.index(item)
                    current_asset_dict["matched_with"]= item
                    item_before_ca = 1

    # if Closing stock is present between first lineitem and corpus search position 
    # then shift the position of current asset

    #liability/equity should be included later

    if item_found == 1 and current_asset_corpus_search == True:
        for item in list_2[:current_asset_dict["start_pos"]]:
            if (fuzz.token_set_ratio(item.lower(),"closing stock")>85 or fuzz.token_set_ratio(item.lower(),"closing stocks")>85) and item_closing_stock == 0:
                current_asset_dict["start_pos"]= list_2.index(item)
                current_asset_dict["matched_with"]= item
                item_closing_stock = 1

    return current_asset_dict

def total_current_asset_level2_start_pos(list_:list)-> dict:
    """
    Find and return start_pos and linematched_with of total current asset from extracted BS table

    Parameters
    ----------
    list_ : list
        List of index of lineitems 

    Returns
    --------
    total_current_asset_dict: dict
        Dictionary containing lineitem name and index position of total current asset
    """

    total_current_asset_dict = {"class_id":1,"sub_class_id":1,"hiererchy":"sub","level":"total","item_name":"total_current_asset","matched_with":"","start_pos":-100}
    list_2 = find_list(list_)
    item_found = 0
    global total_current_asset_pos 

    for item in list_2:
        if fuzz.token_sort_ratio(item.lower(),"total current assets") > 85 and difflib_matcher(item.lower(),"total") >= 0.8 and not "non" in item.lower() and item_found == 0:
            total_current_asset_dict["start_pos"] = list_2.index(item)
            total_current_asset_dict["matched_with"] = item
            total_current_asset_pos = list_2.index(item)
            item_found = 1
        else:
            pass

    return total_current_asset_dict

def net_current_asset_level2_start_pos(list_:list)-> dict:
    """
    Find and return start_pos and linematched_with of net asset from extracted BS table

    Parameters
    ----------
    list_ : list
        List of index of lineitems 

    Returns
    --------
    total_asset_dict: dict
        Dictionary containing lineitem name and index position of net asset
    """
    global net_current_asset_pos
    net_current_asset_dict= {"class_id":1,"hiererchy":"main","level":"total","item_name":"net_current_asset","matched_with":"","start_pos":-100}
    list_2=find_list(list_)
    item_found = 0

    for item in list_2:
        if fuzz.token_sort_ratio(item.lower(),"net current assets")>85 and not "non" in item.lower() and not "total" in item.lower() and "net" in item.lower() and item_found == 0:
            net_current_asset_dict["start_pos"]= list_2.index(item)
            net_current_asset_dict["matched_with"]= item
            net_current_asset_pos = 1
            item_found = 1
        else:
            pass

    return net_current_asset_dict

def non_current_asset_level2_start_pos(list_:list)-> dict:
    """
    Find and return start_pos and linematched_with of non_current_asset from extracted BS table

    Parameters
    ----------
    list_ : list
        List of index of lineitems 

    Returns
    --------
    non_current_asset_dict: dict
        Dictionary containing lineitem name and index position of non_current_asset
    """
    
    non_current_asset_dict= {"class_id":1,"sub_class_id":2,"hiererchy":"sub","level":"class","item_name":"non_current_asset","matched_with":"","start_pos":-100,"end_position":-100}
    list_2=find_list(list_)
    global asset_pos, application_asset
    non_current_asset_corpus_search = False
    item_found=0
    item_before_nca = 0

    if asset_pos != -100:
        for item in list_2[asset_pos+1:len(list_2)]:
            if fuzz.partial_ratio(item.lower(),"non current assets")>85 and "non" in item.lower() and "asset" in item.lower() and not "total" in item.lower() and not "other" in item.lower() and item_found == 0:
                non_current_asset_dict["start_pos"]= list_2.index(item)
                non_current_asset_dict["matched_with"]= item
                item_found =1
            else:
                pass
    else:
        for item in list_2:
            if fuzz.partial_ratio(item.lower(),"non current assets")>85 and "non" in item.lower() and "asset" in item.lower() and not "total" in item.lower() and not "other" in item.lower() and item_found == 0:
                non_current_asset_dict["start_pos"]= list_2.index(item)
                non_current_asset_dict["matched_with"]= item
                item_found =1
            else:
                pass


    if non_current_asset_dict["start_pos"]== -100:
        if asset_pos != -100:
            for item in list_2[asset_pos+1:len(list_2)]:
                for word in non_current_assets_corpus:
                    if fuzz.token_set_ratio(item.lower(),word)>86 and "deposit" not in item.lower() and "current" not in item.lower() and item_found==0:
                        non_current_asset_dict["start_pos"]= list_2.index(item)
                        non_current_asset_dict["matched_with"]= item
                        non_current_asset_corpus_search = True
                        item_found=1
        else:
            for item in list_2:
                for word in non_current_assets_corpus:
                    if fuzz.token_set_ratio(item.lower(),word)>86 and "deposit" not in item.lower() and "current" not in item.lower() and item_found==0:
                        non_current_asset_dict["start_pos"]= list_2.index(item)
                        non_current_asset_dict["matched_with"]= item
                        non_current_asset_corpus_search = True
                        item_found=1

    # If there is a gap between application_asset and non_current_asset, then change the start position
    # of non_current_asset just after application_asset, provided next position of application_asset
    # contains string with length greater than atleast 3

    if item_found == 1 and non_current_asset_corpus_search == True and application_asset == True:
        for item in list_2[asset_pos+1:non_current_asset_dict["start_pos"]]:
            if isinstance(item, str) and len(item) > 3 and item_before_nca == 0:
                non_current_asset_dict["start_pos"]= list_2.index(item)
                non_current_asset_dict["matched_with"]= item
                item_before_nca = 1

    return non_current_asset_dict

def total_non_current_asset_level2_start_pos(list_:list)-> dict:
    """
    Find and return start_pos and linematched_with of total non current asset from extracted BS table

    Parameters
    ----------
    list_ : list
        List of index of lineitems 

    Returns
    --------
    total_non_current_asset_dict: dict
        Dictionary containing lineitem name and index position of total non current asset
    """

    total_non_current_asset_dict= {"class_id":1,"sub_class_id":2,"hiererchy":"sub","level":"total","item_name":"total_non_current_asset","matched_with":"","start_pos":-100}
    list_2=find_list(list_)
    item_found = 0
    global total_non_current_asset_pos

    for item in list_2:
        if fuzz.token_sort_ratio(item.lower(),"total non current asset")>85 and difflib_matcher(item.lower(),"total")>= 0.8 and "non" in item.lower() and item_found == 0:
            total_non_current_asset_dict["start_pos"]= list_2.index(item)
            total_non_current_asset_dict["matched_with"]= item
            total_non_current_asset_pos = list_2.index(item)
            item_found = 1
        else:
            pass

    return total_non_current_asset_dict


def equity_liabilities_level1_start_pos(list_:list)-> dict:
    """
    Find and return start_pos and linematched_with of equity and liabilities from extracted BS table

    Parameters
    ----------
    list_ : list
        List of index of lineitems 

    Returns
    --------
    equity_liabilities_dict: dict
        Dictionary containing lineitem name and index position of equity and liabilities
    """

    equity_liabilities_dict= {"class_id":2,"hiererchy":"main","level":"class","item_name":"equity_liabilities","matched_with":"","start_pos":-100,"end_position":-100} 
    list_2=find_list(list_)
    item_found=0
    global equity_liabilities_pos

    for item in list_2:
        if (fuzz.token_sort_ratio(item.lower(),"equity and liabilities")>85 or fuzz.token_sort_ratio(item.lower(),"liabilities & capital")>85 or fuzz.token_sort_ratio(item.lower(),"liabilities and equity")>85 or fuzz.token_sort_ratio(item.lower(),"liabilities and shareholder's equity")>85) and not "total" in item.lower() and item_found==0:
            equity_liabilities_dict["start_pos"]= list_2.index(item)
            equity_liabilities_dict["matched_with"]= item
            item_found=1
        else:
            pass

    if equity_liabilities_dict["start_pos"] == -100 and item_found==0:
        for item in list_2:
            if (fuzz.partial_ratio(item.lower(),"sources")>85 or fuzz.partial_ratio(item.lower(),"source")>85) and not "current" in item.lower() and not "share" in item.lower() and not "tax" in item.lower() and not "deducted" in item.lower() and item_found==0:
                equity_liabilities_dict["start_pos"]= list_2.index(item)
                equity_liabilities_dict["matched_with"]= item
                item_found=1

    equity_liabilities_pos = equity_liabilities_dict["start_pos"]

    return equity_liabilities_dict

def total_equity_liabilities_level1_start_pos(list_:list)-> dict:
    """
    Find and return start_pos and linematched_with of total equity and liabilities from extracted BS table

    Parameters
    ----------
    list_ : list
        List of index of lineitems 

    Returns
    --------
    total_equity_liabilities_dict: dict
        Dictionary containing lineitem name and index position of total equity and liabilities
    """

    total_equity_liabilities_dict= {"class_id":2,"hiererchy":"main","level":"total","item_name":"total_equity_liabilities","matched_with":"","start_pos":-100}
    list_2=find_list(list_)
    item_found = 0
    global total_equity_liabilities_pos

    for item in list_2:
        if (fuzz.token_sort_ratio(item.lower(),"total equity and liabilities")>=85 or fuzz.token_sort_ratio(item.lower(),"total equity & liabilities")>=85) and difflib_matcher(item.lower(),"total")>= 0.8 and item_found == 0:
            total_equity_liabilities_dict["start_pos"]= list_2.index(item)
            total_equity_liabilities_dict["matched_with"]= item
            total_equity_liabilities_pos = list_2.index(item)
            item_found = 1
        else:
            pass

    return total_equity_liabilities_dict



def equity_level2_start_pos(list_:list)-> dict:
    """
    Find and return start_pos and linematched_with of equity from extracted BS table

    Parameters
    ----------
    list_ : list
        List of index of lineitems 

    Returns
    --------
    equity_dict: dict
        Dictionary containing lineitem name and index position of equity and liabilities
    """

    equity_dict= {"class_id":2,"sub_class_id":1,"hiererchy":"sub","level":"class","item_name":"equity","matched_with":"","start_pos":-100,"secondary_start_pos":-100,"secondary_matched_with":"","end_position":-100}
    list_2=find_list(list_)
    amount_list = find_amount_list(list_)
    global liability_pos
    global equity_pos
    item_found= 0
    item_found_borrowing_match = 0
    item_found_corpus = 0
    item_found_pl= 0

    for item in list_2:
        if fuzz.token_sort_ratio(item.lower(),"equity")>85 and not "total" in item.lower():
            equity_dict["start_pos"]= list_2.index(item)
            equity_dict["matched_with"]= item
            item_found = 1
        else:
            pass

    if equity_dict["start_pos"] == -100:
        for item in list_2:
            for word in equity_corpus:
                if fuzz.token_sort_ratio(item.lower(),word)>80 and item_found==0:
                    equity_dict["start_pos"]= list_2.index(item)
                    equity_dict["matched_with"]= item
                    item_found=1
                    item_found_corpus = 1

    if equity_dict["start_pos"] == -100 and item_found==0 and liability_pos!= -100:
        for item in list_2[liability_pos:]:
            for char in item.split(" "):
                for word in equity_corpus:
                    if fuzz.token_sort_ratio(char.lower(),word)>85 and item_found==0:
                        equity_dict["start_pos"]= list_2.index(item)
                        equity_dict["matched_with"]= item
                        item_found=1

    if item_found == 0 and liability_pos != -100:
        for item in list_2[liability_pos:]:
            for char in item.split(" "):
                if fuzz.token_sort_ratio(char.lower(),"drawings")>85 or fuzz.token_set_ratio(char.lower(),"net profit")>85 and item_found==0:
                        equity_dict["start_pos"]= list_2.index(item)
                        equity_dict["matched_with"]= item
                        item_found=1
                        item_found_borrowing_match = 1


    # India Specific rule. Equity should be after liability

    if item_found_borrowing_match == 1:
        if abs(liability_pos - equity_dict["start_pos"]) < 6:
                equity_dict["start_pos"]= list_2.index(list_2[liability_pos+1])
                equity_dict["matched_with"]= list_2[liability_pos+1]
        else:
            pass

    # If Equity Search matched with corpus
    # Logic: If corpus match is successful, check the associated amount. If amount is 0 or 0.0 then check previous item.
    # If previous item amount has value and previous item is a "name" then mark it as equity start position

    if item_found_corpus == 1:
        if int(amount_list[equity_dict["start_pos"]]) == 0:
            if check_name(list_2[equity_dict["start_pos"]-1]) and int(amount_list[equity_dict["start_pos"]-1]) != 0:
                equity_dict["start_pos"]= list_2.index(list_2[equity_dict["start_pos"]-1])
                equity_dict["matched_with"]= list_2[equity_dict["start_pos"]]

    # Secondary search on profit and loss

    if item_found == 1 or item_found_borrowing_match == 1 and item_found_pl == 0:
        for item in list_2[equity_dict["start_pos"]:]:
            if (fuzz.token_sort_ratio(item.lower(),"profit & loss a")>85 or fuzz.token_set_ratio(item.lower(),"profit and loss a")>85) and item_found_pl==0:
                equity_dict["secondary_start_pos"]= list_2.index(item)
                equity_dict["secondary_matched_with"]= item
                item_found_pl = 1

    equity_pos = equity_dict["start_pos"]

    return equity_dict


def total_equity_level2_start_pos(list_:list)-> dict:
    """
    Find and return start_pos and linematched_with of total equity from extracted BS table

    Parameters
    ----------
    list_ : list
        List of index of lineitems 

    Returns
    --------
    total_equity_dict: dict
        Dictionary containing lineitem name and index position of total equity
    """

    total_equity_dict= {"class_id":2,"sub_class_id":1,"hiererchy":"sub","level":"total","item_name":"total_equity","matched_with":"","start_pos":-100}
    list_2=find_list(list_)
    item_found=0
    global total_equity_pos

    for item in list_2:
        if fuzz.token_sort_ratio(item.lower(),"total equity")>85 and difflib_matcher(item.lower(),"total")>= 0.8 and difflib_matcher(item.lower(),"liabilities")<0.8:
            total_equity_dict["start_pos"]= list_2.index(item)
            total_equity_dict["matched_with"]= item
            total_equity_pos = list_2.index(item)
        else:
            pass

    if total_equity_dict["start_pos"]==-100:
        for item in list_2:
            if "total" in item.lower() and "equity" in item.lower() and not "liabilities" in item.lower() and item_found==0:
                total_equity_dict["start_pos"]= list_2.index(item)
                total_equity_dict["matched_with"]= item
                total_equity_pos = list_2.index(item)
                item_found=1
            else:
                pass

    return total_equity_dict

def liabilities_level2_start_pos(list_:list)-> dict:
    """
    Find and return start_pos and linematched_with of liabilities from extracted BS table

    Parameters
    ----------
    list_ : list
        List of index of lineitems 

    Returns
    --------
    liabilities_dict: dict
        Dictionary containing lineitem name and index position of liabilities
    """

    liabilities_dict= {"class_id":2,"hiererchy":"main","level":"class","item_name":"liabilities","matched_with":"","start_pos":-100,"end_position":-100}
    list_2=find_list(list_)
    item_found = 0
    global liability_pos, equity_liabilities_pos

    for item in list_2:
        if (fuzz.token_sort_ratio(item.lower(),"liabilities")>85) and not "total" in item.lower() and not "equity" in item.lower() and not "capital" in item.lower() and not "current" in item.lower() and item_found == 0:
            liabilities_dict["start_pos"]= list_2.index(item)
            liabilities_dict["matched_with"]= item
            liability_pos = list_2.index(item)
            item_found = 1

    # If liability not found but equity_liability position is present then just update liability
    # position to equity_liability_position, for ease of liability subclass search.
    # No need to update liabilities_dict

    if item_found == 0 and equity_liabilities_pos != -100:
        liability_pos = equity_liabilities_pos

    return liabilities_dict

def total_liabilities_level2_start_pos(list_:list)-> dict:
    """
    Find and return start_pos and linematched_with of total liabilities from extracted BS table

    Parameters
    ----------
    list_ : list
        List of index of lineitems 

    Returns
    --------
    total_liabilities_dict: dict
        Dictionary containing lineitem name and index position of total liabilities
    """

    total_liabilities_dict= {"class_id":2,"hiererchy":"main","level":"total","item_name":"total_liabilities","matched_with":"","start_pos":-100}
    list_2=find_list(list_)
    item_found = 0
    global total_liabilities_pos

    for item in list_2:
        if fuzz.token_sort_ratio(item.lower(),"total liabilities")>=85 and difflib_matcher(item.lower(),"total")>= 0.8 and not "current" in item.lower() and item_found == 0:
            total_liabilities_dict["start_pos"]= list_2.index(item)
            total_liabilities_dict["matched_with"]= item
            total_liabilities_pos = list_2.index(item)
            item_found = 1
        else:
            pass

    return total_liabilities_dict

def net_liabilities_level1_start_pos(list_:list)-> dict:
    """
    Find and return start_pos and linematched_with of net liability from extracted BS table

    Parameters
    ----------
    list_ : list
        List of index of lineitems 

    Returns
    --------
    net_liabilities_dict: dict
        Dictionary containing lineitem name and index position of net liabilities
    """

    net_liabilities_dict= {"class_id":0,"hiererchy":"main","level":"total","item_name":"net_liabilities","matched_with":"","start_pos":-100}
    list_2=find_list(list_)
    item_found = 0

    for item in list_2:
        if fuzz.token_sort_ratio(item.lower(),"net liabilities")>85 and not "current" in item.lower() and not "total" in item.lower() and "net" in item.lower() and item_found == 0:
            net_liabilities_dict["start_pos"]= list_2.index(item)
            net_liabilities_dict["matched_with"]= item
            item_found = 1
        else:
            pass

    return net_liabilities_dict

def current_liabilities_level2_start_pos(list_:list)-> dict:
    """
    Find and return start_pos and linematched_with of current_liabilities from extracted BS table

    Parameters
    ----------
    list_ : list
        List of index of lineitems 

    Returns
    --------
    current_liabilities_dict: dict
        Dictionary containing lineitem name and index position of current_liabilities
    """

    current_liabilities_dict= {"class_id":2,"sub_class_id":2,"hiererchy":"sub","level":"class","item_name":"current_liabilities","matched_with":"","start_pos":-100,"end_position":-100}
    list_2=find_list(list_)
    item_found=0
    global equity_pos, liability_pos, current_liabilities_pos

    for item in list_2:
        if fuzz.token_sort_ratio(item.lower(),"current liabilities")>85 and not "total" in item.lower() and not "non" in item.lower() and "current" in item.lower() and item_found==0:
            if len(item.lower().strip().split(" "))>2:
                if len(item.lower().strip().split(" ")[:-2])<1:
                    current_liabilities_dict["start_pos"]= list_2.index(item)
                    current_liabilities_dict["matched_with"]= item
                    item_found = 1

            elif len(item.lower().strip().split(" "))<=2:
                current_liabilities_dict["start_pos"]= list_2.index(item)
                current_liabilities_dict["matched_with"]= item
                item_found = 1

        elif (fuzz.token_sort_ratio(item.lower(),"current liabilities")+fuzz.token_set_ratio(item.lower(),"current liabilities"))/2 > 85 and not "total" in item.lower() and not "non" in item.lower() and "current" in item.lower() and item_found==0:
            if len(item.lower().strip().split(" "))>2:
                if len(item.lower().strip().split(" ")[:-2])<1:
                    current_liabilities_dict["start_pos"]= list_2.index(item)
                    current_liabilities_dict["matched_with"]= item
                    item_found = 1

            elif len(item.lower().strip().split(" "))<=2:
                current_liabilities_dict["start_pos"]= list_2.index(item)
                current_liabilities_dict["matched_with"]= item
                item_found = 1
        else:
            pass

    if current_liabilities_dict["start_pos"]== -100:
        for item in list_2:
            for word in current_liabilities_corpus:
                if fuzz.token_sort_ratio(item.lower(),word)>85 and item_found==0:
                    current_liabilities_dict["start_pos"]= list_2.index(item)
                    current_liabilities_dict["matched_with"]= item
                    item_found=1


    # Borrowing with short term

    if current_liabilities_dict["start_pos"]== -100:
        for item in list_2:
            if (fuzz.token_sort_ratio(item.lower(),"borrowing")>85 or fuzz.token_sort_ratio(item.lower(),"borrowings")>85 or fuzz.token_sort_ratio(item.lower(),"short term borrowings")>85) and "short" in item.lower() and "term" in item.lower()  and item_found==0:
                current_liabilities_dict["start_pos"]= list_2.index(item)
                current_liabilities_dict["matched_with"]= item
                item_found=1

    # Domain Search

    if current_liabilities_dict["start_pos"]== -100 or item_found == 0:
        if liability_pos == -100:
            for item in list_2:
                for word in current_liabilities_corpus:
                    for w in word.split(" "):
                        if fuzz.token_set_ratio(item.lower(),w)>85 and item_found==0 and not "financial" in item.lower():
                            current_liabilities_dict["start_pos"]= list_2.index(item)
                            current_liabilities_dict["matched_with"]= item
                            item_found=1
        else:
            for item in list_2[liability_pos+1:]:
                for word in current_liabilities_corpus:
                    for w in word.split(" "):
                        if fuzz.token_set_ratio(item.lower(),w)>85 and item_found==0 and not "financial" in item.lower():
                            current_liabilities_dict["start_pos"]= list_2.index(item)
                            current_liabilities_dict["matched_with"]= item
                            item_found=1

    current_liabilities_pos = current_liabilities_dict["start_pos"]

    return current_liabilities_dict

def total_current_liabilities_level2_start_pos(list_:list)-> dict:
    """
    Find and return start_pos and linematched_with of total current liabilities from extracted BS table

    Parameters
    ----------
    list_ : list
        List of index of lineitems 

    Returns
    --------
    total_current_liabilities_dict: dict
        Dictionary containing lineitem name and index position of total current liabilities
    """

    total_current_liabilities_dict= {"class_id":2,"sub_class_id":2,"hiererchy":"sub","level":"total","item_name":"total_current_liabilities","matched_with":"","start_pos":-100}
    list_2=find_list(list_)
    item_found = 0
    global total_current_liabilities_pos

    for item in list_2:
        if fuzz.token_sort_ratio(item.lower(),"total current liabilities")>=85 and difflib_matcher(item.lower(),"total")>= 0.8 and not "non" in item.lower() and not "net" in item.lower() and not "other" in item.lower() and "total" in item.lower() and item_found == 0:
            total_current_liabilities_dict["start_pos"]= list_2.index(item)
            total_current_liabilities_dict["matched_with"]= item
            total_current_liabilities_pos = list_2.index(item)
            item_found = 1
        else:
            pass

    return total_current_liabilities_dict

def non_current_liabilities_level2_start_pos(list_:list)-> dict:
    """
    Find and return start_pos and linematched_with of non_current_liabilities from extracted BS table

    Parameters
    ----------
    list_ : list
        List of index of lineitems 

    Returns
    --------
    non_current_liabilities_dict: dict
        Dictionary containing lineitem name and index position of non_current_liabilities
    """

    non_current_liabilities_dict= {"class_id":2,"sub_class_id":3,"hiererchy":"sub","level":"class","item_name":"non_current_liabilities","matched_with":"","start_pos":-100,"end_position":-100}
    list_2 = find_list(list_)
    item_found = 0
    item_found_bank = 0
    item_found_cc_od = 0
    item_before_ncl = 0
    global liability_pos, equity_pos, non_current_liabilities_pos, current_liabilities_pos
    non_current_liabilities_direct_search = False
    non_current_liabilities_corpus_search = False

    for item in list_2:
        if fuzz.token_sort_ratio(item.lower(),"non current liabilities")>85 and not "total" in item.lower() and "non" in item.lower() and item_found==0:
            non_current_liabilities_dict["start_pos"]= list_2.index(item)
            non_current_liabilities_dict["matched_with"]= item
            non_current_liabilities_direct_search = True
            item_found = 1
        else:
            pass

    if non_current_liabilities_dict["start_pos"] == -100: 
        #if equity_pos == -100 and liability_pos == -100:
        if equity_pos != -100 and current_liabilities_pos != -100 and equity_pos < current_liabilities_pos:
            # Current liability rule added for TSX-MGA-2018
            for item in list_2[equity_pos+1:]:      
                for word in non_current_liabilities_corpus:
                    if fuzz.token_set_ratio(item.lower(),word) > 85 and "asset" not in item.lower() and "financial" not in item.lower() and "property" not in item.lower() and "plant" not in item.lower() and "short" not in item.lower() and "interest" not in item.lower() and "advances" not in item.lower() and item_found == 0:
                        non_current_liabilities_dict["start_pos"] = list_2.index(item)
                        non_current_liabilities_dict["matched_with"] = item
                        non_current_liabilities_corpus_search = True
                        item_found = 1
        elif liability_pos != -100:
            for item in list_2[liability_pos+1:]:       
                for word in non_current_liabilities_corpus:
                    if fuzz.token_set_ratio(item.lower(),word) > 85 and "asset" not in item.lower() and "financial" not in item.lower() and "property" not in item.lower() and "plant" not in item.lower() and "short" not in item.lower() and "interest" not in item.lower() and "advances" not in item.lower() and item_found == 0:
                        non_current_liabilities_dict["start_pos"] = list_2.index(item)
                        non_current_liabilities_dict["matched_with"] = item
                        non_current_liabilities_corpus_search = True
                        item_found = 1
        else:
            for item in list_2: 
                for word in non_current_liabilities_corpus:
                    if fuzz.token_set_ratio(item.lower(),word) > 85 and "asset" not in item.lower() and "financial" not in item.lower() and "property" not in item.lower() and "plant" not in item.lower() and "short" not in item.lower() and "interest" not in item.lower() and "advances" not in item.lower() and item_found == 0:
                        non_current_liabilities_dict["start_pos"] = list_2.index(item)
                        non_current_liabilities_dict["matched_with"] = item
                        non_current_liabilities_corpus_search = True
                        item_found = 1

    # Domain Search
    if non_current_liabilities_dict["start_pos"]== -100 or item_found == 0:
        if liability_pos == -100:
            for item in list_2:
                for word in non_current_liabilities_corpus:
                    for w in word.split(" "):
                        if fuzz.token_set_ratio(item.lower(),w)>85 and "non" in item.lower() and item_found==0:
                            non_current_liabilities_dict["start_pos"]= list_2.index(item)
                            non_current_liabilities_dict["matched_with"]= item
                            item_found=1
        else:
            for item in list_2[liability_pos+1:]:
                for word in non_current_liabilities_corpus:
                    for w in word.split(" "):
                        if fuzz.token_set_ratio(item.lower(),w)>85 and "non" in item.lower() and item_found==0:
                            non_current_liabilities_dict["start_pos"]= list_2.index(item)
                            non_current_liabilities_dict["matched_with"]= item
                            item_found=1

    # india specific/ search bank
    if item_found == 0:
        if equity_pos == -100 and liability_pos == -100:
            for item in list_2:     
                for word in bank_corpus:
                    if fuzz.token_set_ratio(item.lower(),word) > 85 and item_found == 0:
                        non_current_liabilities_dict["start_pos"] = list_2.index(item)
                        non_current_liabilities_dict["matched_with"] = item
                        item_found = 1
                        item_found_bank = 1

        elif equity_pos != -100:
            for item in list_2[equity_pos+1:]:      
                for word in bank_corpus:
                    if fuzz.token_set_ratio(item.lower(),word) > 85 and  item_found == 0:
                        non_current_liabilities_dict["start_pos"] = list_2.index(item)
                        non_current_liabilities_dict["matched_with"] = item
                        item_found = 1
                        item_found_bank = 1

        elif liability_pos != -100:
            for item in list_2[liability_pos+1:]:       
                for word in bank_corpus:
                    if fuzz.token_set_ratio(item.lower(),word) > 85 and  item_found == 0:
                        non_current_liabilities_dict["start_pos"] = list_2.index(item)
                        non_current_liabilities_dict["matched_with"] = item
                        item_found = 1
                        item_found_bank = 1

    if item_found == 1 and item_found_bank == 0:
        if equity_pos == -100 and liability_pos == -100:
            for item in list_2:     
                for word in bank_corpus:
                    if fuzz.token_set_ratio(item.lower(),word) > 85 and item_found_bank == 0:
                        non_current_liabilities_dict["start_pos"] = list_2.index(item)
                        non_current_liabilities_dict["matched_with"] = item
                        item_found_bank = 1
        elif equity_pos != -100:
            for item in list_2[equity_pos+1:non_current_liabilities_dict["start_pos"]]:     
                for word in bank_corpus:
                    if fuzz.token_set_ratio(item.lower(),word) > 85 and  item_found_bank == 0:
                        non_current_liabilities_dict["start_pos"] = list_2.index(item)
                        non_current_liabilities_dict["matched_with"] = item
                        item_found_bank = 1

        elif liability_pos != -100:
            for item in list_2[liability_pos+1:non_current_liabilities_dict["start_pos"]]:      
                for word in bank_corpus:
                    if fuzz.token_set_ratio(item.lower(),word) > 85 and  item_found_bank == 0:
                        non_current_liabilities_dict["start_pos"] = list_2.index(item)
                        non_current_liabilities_dict["matched_with"] = item
                        item_found_bank = 1

    # Search based on word bank (after liability position)
    if (item_found == 0 or non_current_liabilities_dict["start_pos"] == -100) and liability_pos != -100:
        for item in list_2[liability_pos+1:]:
            if fuzz.token_set_ratio(item.lower(),"bank") > 85 and  item_found == 0:
                non_current_liabilities_dict["start_pos"] = list_2.index(item)
                non_current_liabilities_dict["matched_with"] = item
                item_found = 1

    # CC/OD Search (secondary search) from liability/equity position (Purpose is to exclude non current liability from equity)

    if item_found == 1 and item_found_cc_od == 0:
        if liability_pos != -100:
            for item in list_2[liability_pos+1:non_current_liabilities_dict["start_pos"]]:  
                for char in item.split(" "):
                    if len(char) == 2 and (fuzz.token_set_ratio(char.lower(),"cc")>85 or fuzz.token_set_ratio(char.lower(),"od")>85) and item_found_cc_od == 0:
                        non_current_liabilities_dict["start_pos"]= list_2.index(item)
                        non_current_liabilities_dict["matched_with"]= item
                        item_found_cc_od = 1
        elif equity_pos != -100:
            for item in list_2[equity_pos+1:non_current_liabilities_dict["start_pos"]]: 
                for char in item.split(" "):
                    if len(char) == 2 and (fuzz.token_set_ratio(char.lower(),"cc")>85 or fuzz.token_set_ratio(char.lower(),"od")>85) and item_found_cc_od == 0:
                        non_current_liabilities_dict["start_pos"]= list_2.index(item)
                        non_current_liabilities_dict["matched_with"]= item
                        item_found_cc_od = 1

    # If lineitem named dues to is placed between liability/equity and non current liability (corpus search) position,
    # then change the start position

    if item_found == 1 and non_current_liabilities_corpus_search == True and liability_pos != -100:
        for item in list_2[liability_pos:non_current_liabilities_dict["start_pos"]]:
            if (fuzz.token_set_ratio(item.lower(),"dues") > 85 or fuzz.token_set_ratio(item.lower(),"due") > 85) and not "msme" in item.lower() and not "small" in item.lower() and not "micro" in item.lower() and not "payable" in item.lower() and not "financial" in item.lower() and not "other" in item.lower() and item_before_ncl == 0:
                non_current_liabilities_dict["start_pos"] = list_2.index(item)
                non_current_liabilities_dict["matched_with"] = item
                item_before_ncl = 1

    elif item_found == 1 and non_current_liabilities_corpus_search == True and equity_pos != -100:
        for item in list_2[equity_pos:non_current_liabilities_dict["start_pos"]]:
            if (fuzz.token_set_ratio(item.lower(),"dues") > 85 or fuzz.token_set_ratio(item.lower(),"due") > 85) and not "msme" in item.lower() and not "small" in item.lower() and not "micro" in item.lower() and not "payable" in item.lower() and not "financial" in item.lower() and not "other" in item.lower() and item_before_ncl == 0:
                non_current_liabilities_dict["start_pos"] = list_2.index(item)
                non_current_liabilities_dict["matched_with"] = item
                item_before_ncl = 1

    non_current_liabilities_pos = non_current_liabilities_dict["start_pos"]
    return non_current_liabilities_dict

def total_non_current_liabilities_level2_start_pos(list_:list)-> dict:
    """
    Find and return start_pos and linematched_with of total non current liabilities from extracted BS table

    Parameters
    ----------
    list_ : list
        List of index of lineitems 

    Returns
    --------
    total_non_current_liabilities_dict: dict
        Dictionary containing lineitem name and index position of total non current liabilities
    """

    total_non_current_liabilities_dict= {"class_id":2,"sub_class_id":3,"hiererchy":"sub","level":"total","item_name":"total_non_current_liabilities","matched_with":"","start_pos":-100}
    list_2=find_list(list_)
    item_found = 0

    global total_non_current_liabilities_pos

    for item in list_2:
        if fuzz.token_sort_ratio(item.lower(),"total non current liabilities")>=80 and difflib_matcher(item.lower(),"total")>= 0.8 and "non" in item.lower() and not "other" in item.lower() and "total" in item.lower() and item_found == 0:
            total_non_current_liabilities_dict["start_pos"]= list_2.index(item)
            total_non_current_liabilities_dict["matched_with"]= item
            total_non_current_liabilities_pos = list_2.index(item)
            item_found = 1
        else:
            pass

    return total_non_current_liabilities_dict


def total_any_level(list_:list)-> list:
    """
    Find and return start_pos and linematched_with of all totals from extracted BS table

    Parameters
    ----------
    list_ : list
        List of index of lineitems 

    Returns
    --------
    total_list: list
        List containing dictionaries of all total positions 
    """

    total_list=[]
    list_2=find_list(list_)

    global total_asset_pos,total_current_asset_pos,total_non_current_asset_pos,total_equity_liabilities_pos,total_equity_pos,total_liabilities_pos,total_current_liabilities_pos,total_non_current_liabilities_pos

    all_found_totals = [total_asset_pos,total_current_asset_pos,total_non_current_asset_pos,total_equity_liabilities_pos,total_equity_pos,total_liabilities_pos,total_current_liabilities_pos,total_non_current_liabilities_pos]

    all_found_totals_fixed = [x for x in all_found_totals if x != -100]

    list_2_search = [el for i,el in enumerate(list_2) if i not in all_found_totals_fixed]

    for idx,item in enumerate(list_2_search):
        total_dict= {"class_id":0,"hiererchy":"Null","level":"total","item_name":"total","matched_with":"","start_pos":-100}
        if fuzz.token_sort_ratio(item.lower(),"total")>=80:
            total_dict["start_pos"]= idx
            total_dict["matched_with"]= item+str(idx)
            total_list.append(total_dict)
        # elif fuzz.token_set_ratio(item.lower(),"total")>=80:
        #   total_dict["start_pos"]= idx
        #   total_dict["matched_with"]= item+str(idx)
        #   total_list.append(total_dict)
        else:
            pass

    return total_list

def blank_any_level(list_:list)-> list:
    """
    Find and return start_pos and linematched_with of all blanks from extracted BS table

    Parameters
    ----------
    list_ : list
        List of index of lineitems 

    Returns
    --------
    blank_list: list
        List containing dictionaries of all blank positions 
    """

    list_2=find_list(list_)
    blank_list=[]
    list_without_particular=[]
    keys={"particular"}
    
    for i in list_:
        list_without_particular.append({k:v for k,v in i.items() if k not in keys})

    for idx,item in enumerate(list_2):
        blank_dict= {"class_id":0,"hiererchy":"Null","level":"total","item_name":"blank","matched_with":"","start_pos":-100}
        if len(item)==0:
            k= list(list_without_particular[idx].values())
            for i in range(len(k)-1):
                if not isinstance(k[i],str) and not isinstance(k[i+1],str):
                    if (k[i]>0 or k[i+1]>0) or (k[i]<0 or k[i+1]<0):
                        blank_dict["start_pos"]= idx
                        blank_dict["matched_with"]= "blank"+str(idx)
                        blank_list.append(blank_dict)
        else:
            pass

    return blank_list

def fix_missing_class(list1:list,list2:list)-> list:
    """
    Fix class which improperly got placed due to wrong fuzzy match

    Logic
    -----
        If the difference between positions of two adjacent class or between total and class is 2 then shift position of second class by -1

    Parameters
    ----------
    list1: list
        List of index of lineitems
    list2: list
        Ordered list of dictionaries containing required items with its position

    Returns
    -------
    list2: list
        List with classes modified
    """

    list1=find_list(list1)

    for i in range(len(list2)-1):
        if list2[i]["level"] == "class" and list2[i+1]["level"] == "class":
            if abs(list2[i]["start_pos"]-list2[i+1]["start_pos"])==2:
                list2[i+1]["start_pos"]= list2[i+1]["start_pos"]-1
                list2[i+1]["matched_with"]= list1[list2[i+1]["start_pos"]]
        if list2[i]["level"] == "total" and list2[i+1]["level"]=="class":
            if abs(list2[i]["start_pos"]-list2[i+1]["start_pos"])==2:
                list2[i+1]["start_pos"]= list2[i+1]["start_pos"]-1
                list2[i+1]["matched_with"]= list1[list2[i+1]["start_pos"]]

    return list2

def fix_redundant_class1_total(list2:list)-> list:
    """
    Fix multiple totals between two sub class for class_id 1

    Logic
    -----
        1. If there are more than 1 total/blank between two sub class of same id then keep the total immediately before the second subclass and remove rest
        2. 2. Remove total not followed by class (hiererchy = Null)
    Parameters
    ----------
    list2: list
        Ordered list of dictionaries containing required items with its position

    Returns
    -------
    list2: list
        List with classes modified
    """

    #filter and create bucket of all class1
    class_1_bucket=[]
    class_1_total_bucket = []
    keep_total = []
    delete_total = []

    for i in range(len(list2)-1):
        if list2[i]["level"]=="class" and list2[i]["hiererchy"]=="sub" and list2[i]["class_id"]==1:
            class_1_bucket.append(i)

    class_1_bucket.sort()

    for t,val in enumerate(list2[class_1_bucket[0]:class_1_bucket[-1]]):
        if val["hiererchy"] == "Null" and val["level"]=="total":
            class_1_total_bucket.append(class_1_bucket[0]+t)

    class_1_total_bucket.sort() 

    # remove redundant total in between two subclass
    for j in range(len(class_1_bucket)-1):
        while class_1_bucket[j]<class_1_bucket[j+1]:
            if (list2[class_1_bucket[j]]["item_name"]=="total" or list2[class_1_bucket[j]]["item_name"]=="blank") and not list2[class_1_bucket[j]+1]["level"]=="class":
                list2.pop(class_1_bucket[j])

            class_1_bucket[j]=class_1_bucket[j]+1


    # Remove total not followed by a lineitem subclass
    for m in class_1_bucket[1:]:
        for n in class_1_total_bucket:
            if list2[n]["start_pos"]-list2[m]["start_pos"] != -1:
                delete_total.append(n)
            else:
                keep_total.append(n)

    total_to_be_deleted = list(set(delete_total).difference(set(keep_total)))
    
    for val in total_to_be_deleted:
        list2.pop(val)

    return list2

def fix_redundant_class2_total(list2:list)-> list:
    """
    Fix multiple totals between two sub class for class_id 2

    Logic
    -----
        1. If there are more than 1 total/blank between two sub class of same id then keep the total immediately before the second subclass and remove rest
        2. Remove total not followed by class (hiererchy = Null)
    Parameters
    ----------
    list2: list
        Ordered list of dictionaries containing required items with its position

    Returns
    -------
    list2: list
        List with classes modified
    """

    
    class_2_bucket=[]
    class_2_total_bucket = []
    keep_total = []
    delete_total = []

    # filter and create bucket of all class2
    for i in range(len(list2)-1):
        if list2[i]["level"]=="class" and list2[i]["hiererchy"]=="sub" and list2[i]["class_id"]==2:
            class_2_bucket.append(i)

    class_2_bucket.sort()

    for t,val in enumerate(list2[class_2_bucket[0]:class_2_bucket[-1]]):
        if val["hiererchy"] == "Null" and val["level"]=="total":
            class_2_total_bucket.append(class_2_bucket[0]+t)

    class_2_total_bucket.sort()  


    # remove redundant total in between two subclass
    for j in range(len(class_2_bucket)-1):
        while class_2_bucket[j]<class_2_bucket[j+1]:
            if (list2[class_2_bucket[j]]["level"]=="total" or list2[class_2_bucket[j]]["item_name"]=="blank")  and not list2[class_2_bucket[j]+1]["level"]=="class":
                list2.pop(class_2_bucket[j])    

            class_2_bucket[j]=class_2_bucket[j]+1


    # Remove total not followed by a lineitem subclass
    for m in class_2_bucket[1:]:
        for n in class_2_total_bucket:
            if list2[n]["start_pos"]-list2[m]["start_pos"] != -1:
                delete_total.append(n)
            else:
                keep_total.append(n)

    total_to_be_deleted = list(set(delete_total).difference(set(keep_total)))
    
    for val in total_to_be_deleted:
        list2.pop(val)


    return list2

def group_classes(list2:list)-> dict:
    """
    Group balance sheet items based on class_id
    
    Parameters
    ----------
    list2: list
        Ordered list of dictionaries containing required items with its position

    Returns
    -------
    grouped_dict: dict
        Dictionary containing BS classes grouped
    """
    grouped_dict= {"Asset":[],"Equity_Liability":[]}


    #get first position of class_id 1 from list2
    class_id_1_pos= -100
    for item in list2:
        if item["class_id"]==1:
            class_id_1_pos= list2.index(item)
            break

    #get first position of class_id 2 from list2
    class_id_2_pos= -100
    for item in list2:
        if item["class_id"]==2:
            class_id_2_pos= list2.index(item)
            break


    if class_id_1_pos > class_id_2_pos:
        grouped_dict["Equity_Liability"].extend(list2[class_id_2_pos:class_id_1_pos])
        grouped_dict["Asset"].extend(list2[class_id_1_pos:len(list2)])
    else:
        grouped_dict["Asset"].extend(list2[class_id_1_pos:class_id_2_pos])
        grouped_dict["Equity_Liability"].extend(list2[class_id_2_pos:len(list2)])

    return grouped_dict


def class_id_mismatch_check(d:dict)-> dict:
    """
    Fix class_id not getting populated in respective classes

    Logic
    -----
        Enforcing class_id 1 to be present only within Asset section and class_id 2 to be present in Equity_Liability section
        if net_current_asset is found then move and delete items from one class to another class.

    Parameters
    ----------
    d: dict
        Grouped dictionary based on class_id

    Returns
    -------
    d_temp: dict
        Dictionary containing fixed class_id mapping
    """

    # Filter all asset items in equity list      
    temp_asset_from_equity_list = list(filter(lambda x: x["class_id"]==1, d["Equity_Liability"]))
    # Filter  only asset items in asset list  
    temp_asset_list = list(filter(lambda x: x["class_id"]==1, d["Asset"]))    

    # Filter all equity items in asset list  
    temp_equity_from_asset_list = list(filter(lambda x: x["class_id"]==2, d["Asset"]))
    # Filter  only equity items in equity list 
    temp_equity_list = list(filter(lambda x: x["class_id"]==2, d["Equity_Liability"]))
    
    asset_list = temp_asset_list+temp_asset_from_equity_list
    equity_list = temp_equity_list + temp_equity_from_asset_list

    d_temp = {"Asset":asset_list,"Equity_Liability":equity_list}
    
    return d_temp

def check_section_hierechy(d):

    # Check if asset section is < liability section (asset present on top or not)
    output_dict = {"Asset":-100,"Equity_Liability":-100}
    if d["Asset"] and d["Equity_Liability"]:
        asset_start = d["Asset"][0]["start_pos"]
        asset_end = d["Asset"][-1]["start_pos"]
        equity_liability_start = d["Equity_Liability"][0]["start_pos"]
        equity_liability_end = d["Equity_Liability"][-1]["start_pos"]

        if asset_end < equity_liability_start:
            output_dict = {"Asset":0,"Equity_Liability":1}
        else:
            output_dict = {"Asset":1,"Equity_Liability":0}

    return output_dict

def fix_india_specific_classes(d:dict, list_:list)-> dict:

    
    list_2=find_list(list_)
    asset_list = d["Asset"]

    global asset_pos, liability_pos, equity_pos, non_current_liabilities_pos,current_liabilities_pos, total_current_asset_pos,total_asset_pos, total_current_liabilities_pos, total_non_current_liabilities_pos

    # Fix non_current_asset position
    current_asset_pos = -100
    non_current_asset_pos = -100

    for each in asset_list:
        if each["item_name"] == "current_asset":
            current_asset_pos = each["start_pos"]
        elif each["item_name"] == "non_current_asset":
            non_current_asset_pos = each["start_pos"]

    if current_asset_pos != -100 and non_current_asset_pos != -100:
        if non_current_asset_pos > current_asset_pos and (non_current_asset_pos < total_current_asset_pos):
            for each2 in d["Asset"]:
                if each2["item_name"] == "non_current_asset":
                    d["Asset"].remove(each2)
            if asset_pos == -100:
                d["Asset"].insert(0,{"class_id":1,"sub_class_id":2,"hiererchy":"sub","level":"class","item_name":"non_current_asset","matched_with":list_2[0],"start_pos": 0})
                non_current_asset_pos = 0
            else:
                if list_2[asset_pos+1] != "":
                    d["Asset"].insert(1,{"class_id":1,"sub_class_id":2,"hiererchy":"sub","level":"class","item_name":"non_current_asset","matched_with":list_2[asset_pos+1],"start_pos": asset_pos+1})
                    non_current_asset_pos =  asset_pos+1
                else:
                    d["Asset"].insert(1,{"class_id":1,"sub_class_id":2,"hiererchy":"sub","level":"class","item_name":"non_current_asset","matched_with":list_2[0],"start_pos": 0})
                    non_current_asset_pos = 0

        if current_asset_pos < liability_pos and non_current_asset_pos > liability_pos:
            for each2 in d["Asset"]:
                if each2["item_name"] == "non_current_asset":
                    d["Asset"].remove(each2)

    # Check if asset section is < liability section (asset present on top or not)

    section_dict = check_section_hierechy(d)

    # Non current asset present inside liability section
    if non_current_asset_pos != -100:

        if section_dict["Asset"] == 0:

            if liability_pos != -100:
                if non_current_asset_pos > liability_pos:
                    for each2 in d["Asset"]:
                        if each2["item_name"] == "non_current_asset":
                            d["Asset"].remove(each2)
                    if asset_pos == -100:
                        d["Asset"].insert(0,{"class_id":1,"sub_class_id":2,"hiererchy":"sub","level":"class","item_name":"non_current_asset","matched_with":list_2[0],"start_pos": 0})
                    else:
                        if list_2[asset_pos+1] != "":
                            d["Asset"].insert(1,{"class_id":1,"sub_class_id":2,"hiererchy":"sub","level":"class","item_name":"non_current_asset","matched_with":list_2[asset_pos+1],"start_pos": asset_pos+1})
                        else:
                            d["Asset"].insert(1,{"class_id":1,"sub_class_id":2,"hiererchy":"sub","level":"class","item_name":"non_current_asset","matched_with":list_2[0],"start_pos": 0})

        
            elif equity_pos != -100:
                if non_current_asset_pos > equity_pos:
                    for each2 in d["Asset"]:
                        if each2["item_name"] == "non_current_asset":
                            d["Asset"].remove(each2)
                    if asset_pos == -100:
                        d["Asset"].insert(0,{"class_id":1,"sub_class_id":2,"hiererchy":"sub","level":"class","item_name":"non_current_asset","matched_with":list_2[0],"start_pos": 0})
                    else:
                        if list_2[asset_pos+1] != "":
                            d["Asset"].insert(1,{"class_id":1,"sub_class_id":2,"hiererchy":"sub","level":"class","item_name":"non_current_asset","matched_with":list_2[asset_pos+1],"start_pos": asset_pos+1})
                        else:
                            d["Asset"].insert(1,{"class_id":1,"sub_class_id":2,"hiererchy":"sub","level":"class","item_name":"non_current_asset","matched_with":list_2[0],"start_pos": 0})

    #Extra changes if non_current_asset is not detected
    elif current_asset_pos != -100 and non_current_asset_pos == -100 and asset_pos != -100:
        d["Asset"].insert(1,{"class_id":1,"sub_class_id":2,"hiererchy":"sub","level":"class","item_name":"non_current_asset","matched_with":list_2[asset_pos+1],"start_pos": asset_pos+1})
        non_current_asset_pos = asset_pos+1
    elif current_asset_pos != -100 and non_current_asset_pos == -100 and asset_pos == -100:
        d["Asset"].insert(0,{"class_id":1,"sub_class_id":2,"hiererchy":"sub","level":"class","item_name":"non_current_asset","matched_with":list_2[0],"start_pos": 0})
        non_current_asset_pos = 0


    # Check if current asset and non current asset position is same after above operation. If same delete non current asset position.

    if not abs(non_current_asset_pos - current_asset_pos) >= 1:
        for each2 in d["Asset"]:
            if each2["item_name"] == "non_current_asset":
                d["Asset"].remove(each2)

    # Fix non current liability present in between current and non-current asset

    if current_asset_pos > non_current_asset_pos:
        if non_current_liabilities_pos in range(non_current_asset_pos,current_asset_pos):
            for each2 in d["Equity_Liability"]:
                if each2["item_name"] == "non_current_liabilities":
                    d["Equity_Liability"].remove(each2)
    elif current_asset_pos < non_current_asset_pos:
        if non_current_liabilities_pos in range(current_asset_pos,non_current_asset_pos):
            for each2 in d["Equity_Liability"]:
                if each2["item_name"] == "non_current_liabilities":
                    d["Equity_Liability"].remove(each2)

    # Fix non current liability present in between current and total current liability
    # If a subclass T is present between start and end position of another subclass U
    # and  T.endpos > U.endpos then shift T.start_pos just after U.endpos
    if (non_current_liabilities_pos > current_liabilities_pos) and (non_current_liabilities_pos < total_current_liabilities_pos) and (total_non_current_liabilities_pos > total_current_liabilities_pos):
        for each2 in d["Equity_Liability"]:
            if each2["item_name"] == "non_current_liabilities":
                d["Equity_Liability"].remove(each2)
        d["Equity_Liability"].append({"class_id":2,"sub_class_id":3,"hiererchy":"sub","level":"class","item_name":"non_current_liabilities","matched_with":list_2[total_current_liabilities_pos+1],"start_pos":total_current_liabilities_pos+1,"end_position":-100})


    # Fix equity position
    if equity_pos == -100 and non_current_liabilities_pos != -100 and liability_pos != -100:
        if abs(liability_pos - non_current_liabilities_pos) > 1:
            d["Equity_Liability"].insert(1,{"class_id":2,"sub_class_id":1,"hiererchy":"sub","level":"class","item_name":"equity","matched_with": list_2[liability_pos+1],"start_pos": liability_pos+1})

    return d

def update_end_positions(item,total):
    """
    Update end position of level1/level2 items based on its corresponding total,
    If total["start_pos"] not equals to -100 then assign total["start_pos"] to item["end_position"] else
    item["end_position"] == -100
    """

    item["end_position"] = total["start_pos"]
    return item

def get_pos_rule(rule_dict):
    """
    return initial position of subclass from graph
    """
    current_asset_pos = -100
    non_current_asset_pos = -100
    current_liability_pos = -100
    non_current_liability_pos = -100
    equity_pos = -100

    for each in rule_dict["Asset"]:
        if each["item_name"] == "current_asset" and current_asset_pos == -100:
            current_asset_pos = each["start_pos"]
        if each["item_name"] == "non_current_asset" and non_current_asset_pos == -100:
            non_current_asset_pos = each["start_pos"]

    for each in rule_dict["Equity_Liability"]:
        if each["item_name"] == "current_liabilities" and current_liability_pos == -100:
            current_liability_pos = each["start_pos"]
        if each["item_name"] == "non_current_liabilities" and non_current_liability_pos == -100:
            non_current_liability_pos = each["start_pos"]
        if each["item_name"] == "equity" and equity_pos == -100:
            equity_pos = each["start_pos"]

    return (("cap",current_asset_pos), ("ncap",non_current_asset_pos), ("clp",current_liability_pos), ("nclp",non_current_liability_pos), ("ep",equity_pos))


def start_bs_rule_processing(input_list:list) -> dict:

    global net_current_asset_pos, asset_pos, liability_pos, application_asset,total_asset_pos,total_current_asset_pos,total_non_current_asset_pos,total_equity_liabilities_pos,total_liabilities_pos,total_equity_pos,total_current_liabilities_pos,total_non_current_liabilities_pos
    asset_dict = asset_level1_start_pos(input_list)
    current_asset_dict = current_asset_level2_start_pos(input_list)
    non_current_asset_dict = non_current_asset_level2_start_pos(input_list)
    equity_liabilities_dict = equity_liabilities_level1_start_pos(input_list)
    liabilities_dict = liabilities_level2_start_pos(input_list)
    current_liabilities_dict = current_liabilities_level2_start_pos(input_list)
    equity_dict = equity_level2_start_pos(input_list)
    non_current_liabilities_dict = non_current_liabilities_level2_start_pos(input_list)

    total_asset_dict = total_asset_level1_start_pos(input_list)
    asset_dict = update_end_positions(asset_dict,total_asset_dict)
    net_asset_dict = net_asset_level1_start_pos(input_list)
    total_current_asset_dict = total_current_asset_level2_start_pos(input_list)
    current_asset_dict = update_end_positions(current_asset_dict,total_current_asset_dict)
    #net_current_asset_dict = net_current_asset_level2_start_pos(input_list)
    total_non_current_asset_dict = total_non_current_asset_level2_start_pos(input_list)
    non_current_asset_dict =  update_end_positions(non_current_asset_dict,total_non_current_asset_dict)
    total_equity_liabilities_dict = total_equity_liabilities_level1_start_pos(input_list)
    equity_liabilities_dict = update_end_positions(equity_liabilities_dict,total_equity_liabilities_dict)
    total_equity_dict = total_equity_level2_start_pos(input_list)
    equity_dict = update_end_positions(equity_dict,total_equity_dict)
    total_liabilities_dict = total_liabilities_level2_start_pos(input_list)
    liabilities_dict = update_end_positions(liabilities_dict,total_liabilities_dict)
    net_liabilities_dict = net_liabilities_level1_start_pos(input_list)
    total_current_liabilities_dict = total_current_liabilities_level2_start_pos(input_list)
    current_liabilities_dict = update_end_positions(current_liabilities_dict,total_current_liabilities_dict)
    total_non_current_liabilities_dict = total_non_current_liabilities_level2_start_pos(input_list)
    non_current_liabilities_dict = update_end_positions(non_current_liabilities_dict,total_non_current_liabilities_dict)
    total_list = total_any_level(input_list)

    class_start_list_temp= [asset_dict,current_asset_dict,non_current_asset_dict,equity_liabilities_dict,equity_dict,liabilities_dict,current_liabilities_dict,non_current_liabilities_dict]
    #total_class_start_list_temp= [total_asset_dict,net_asset_dict,total_current_asset_dict,net_current_asset_dict,total_non_current_asset_dict,total_equity_liabilities_dict,total_equity_dict,total_liabilities_dict,net_liabilities_dict,total_current_liabilities_dict,total_non_current_liabilities_dict]
    total_class_start_list_temp= [total_asset_dict,net_asset_dict,total_current_asset_dict,total_non_current_asset_dict,total_equity_liabilities_dict,total_equity_dict,total_liabilities_dict,net_liabilities_dict,total_current_liabilities_dict,total_non_current_liabilities_dict]
    total_blank_class_start_list_temp= total_list#+blank_list
    class_bucket_temp= class_start_list_temp+total_class_start_list_temp+total_blank_class_start_list_temp
    class_bucket_unsorted= [x for x in class_bucket_temp if not (-100 == x.get('start_pos'))]
    class_bucket_sorted = sorted(class_bucket_unsorted, key=lambda k: k['start_pos']) 

    grouped_dictionary= group_classes(class_bucket_sorted)
    class_id_mismatch_check_dict = class_id_mismatch_check(grouped_dictionary)
    india_specific_dict = fix_india_specific_classes(class_id_mismatch_check_dict,input_list)

    net_current_asset_pos = -100
    asset_pos = -100
    equity_liabilities_pos = -100
    liability_pos = -100
    equity_pos = -100
    non_current_liabilities_pos = -100
    current_liabilities_pos = -100
    application_asset = False
    total_asset_pos = -100
    total_current_asset_pos = -100
    total_non_current_asset_pos = -100
    total_equity_liabilities_pos = -100
    total_liabilities_pos = -100
    total_equity_pos = -100
    total_current_liabilities_pos = -100
    total_non_current_liabilities_pos = -100

    return india_specific_dict