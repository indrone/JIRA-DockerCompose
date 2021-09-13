import json
import re
from fuzzywuzzy import fuzz

bs_share_capital_corpus = ['Share Capital', 'Called up share capital', 'Equity Share Capital', 'Issued Capital', 'Contributed Equity', 'Capital Account']
revenue_corpus = ['Revenue', 'sales', 'operating income', 'operations', 'fees', 'turnover', 'contract receipt']

def find_sign_count(class_data):
    pos_counter, neg_counter = 0, 0
    for item in class_data:
        for header, value in item.items():
            try:
                year_val, amt_val = int(header), float(value)
                if amt_val >= 0:
                    pos_counter += 1
                else:
                    neg_counter += 1
            except Exception:
                pass
    return pos_counter, neg_counter


def check_single_item_class(is_data):
    for class_, class_data in is_data.items():
        if len(class_data) != 1:
            return False
    return True


def change_neg_signage(class_, class_data, item=None, all_class=True):
    if not all_class:
        negative_amount = False
        for header, value in item.items():
            try:
                year_val, amt_val = int(header), float(value)
                if amt_val < 0 and class_ != "Tax":
                    negative_amount = True
            except Exception:
                pass
        if not negative_amount:
            item['Label Signage'] = '-'
        else:
            item['Label Signage'] = '+'
        return item

    for item in class_data:
        item['Label Signage'] = '-'
    return class_data


def bs_equity_signage(class_data):
    share_capital_data = []
    for item in class_data:
        item_val = item['particular']
        for words in bs_share_capital_corpus:
            fuzz_score = fuzz.token_set_ratio(item_val, words)
            if fuzz_score > 88:
                share_capital_data.append(item)
    pos_counter, neg_counter = find_sign_count(share_capital_data)
    if neg_counter > pos_counter:
        for item in class_data:
            if neg_counter > pos_counter and item['Label Signage'] != 'H':
                item['Label Signage'] = '-'
            elif pos_counter >= neg_counter and item['Label Signage'] != 'H':
                item['Label Signage'] = '+'
    return class_data


def assert_label_signage(class_data, pos_counter, neg_counter, only_assert=False):
    if only_assert:
        for item in class_data:
            signage_val = str(item['Label Signage'])
            if signage_val == 'N':
                item['Label Signage'] = '-'
            if signage_val == 'P':
                item['Label Signage'] = '+'
            if len(signage_val) == 0 or signage_val.casefold() == 'null' or signage_val.casefold() == 'none':
                item['Label Signage'] = '+'
        return class_data

 

    for item in class_data:
        if neg_counter > pos_counter and item['Label Signage'] != 'H':
            item['Label Signage'] = '-'
        elif pos_counter >= neg_counter and item['Label Signage'] != 'H':
            item['Label Signage'] = '+'
    return class_data


def is_signage(is_data):
    if check_single_item_class(is_data):
        pos_counter, neg_counter = find_sign_count(is_data['Cost of goods sold / Cost of Sales'])
        if neg_counter > pos_counter:
            for class_, class_data in is_data.items():
                class_data = change_neg_signage(class_, class_data)
        elif pos_counter >= neg_counter:
            for class_, class_data in is_data.items():
                class_data = assert_label_signage(class_data, pos_counter, neg_counter)
        return is_data
    for class_, class_data in is_data.items():
        if "index" in class_:
            continue
        pos_counter, neg_counter = find_sign_count(is_data[class_])
        if class_ in ["Revenue", "Other Income"]:
            class_data = assert_label_signage(class_data, pos_counter, neg_counter)
        elif class_ in ["Cost of goods sold / Cost of Sales", "Operating expenses", "Finance cost", "Depreciation"]:
            if neg_counter > pos_counter:
                class_data = change_neg_signage(class_, class_data)
            else:
                class_data = assert_label_signage(class_data, pos_counter, neg_counter)
        else:
            class_data = assert_label_signage(class_data, pos_counter, neg_counter, only_assert=True)

    # Less transfer logic
    # less_expr = ""
    for class_, class_data in is_data.items():
        for item in class_data:
            try:
                lineitem_val = item["particular"]
                lineitem_val = lineitem_val.replace(":"," ").replace(",","").replace("-"," ")
                if " " in lineitem_val:
                    split_lineitem = lineitem_val.split(' ')
                else:
                    split_lineitem = [lineitem_val] + [" "]
                word1, word2 = split_lineitem[:2]
                word1, word2 = word1.strip(), word2.strip()
                # if class_ == "Revenue":
                #     print("WORD1 ::: ", word1)
                #     print("WORD2 ::: ", word2)
                if len(word2) == 0:
                    if word1.lower().find("less") >= 0 and word1.lower().find("less") <= 2:
                        item = change_neg_signage(class_, class_data, item, all_class=False)
                if (re.search("(?:LES)", word1, re.IGNORECASE) and len(word1) < 5) or (re.search("(?:LES)", word2, re.IGNORECASE) and len(word2) < 5):
                    item = change_neg_signage(class_, class_data, item, all_class=False)
                elif (re.search("(?:LES)", word1[:4], re.IGNORECASE) and len(word1) > 5) or (re.search("(?:LES)", word2[:4], re.IGNORECASE) and len(word2) > 5):
                    item = change_neg_signage(class_, class_data, item, all_class=False)
            except Exception:
                pass
        # if class_ == "Tax":
        #     tax_signage = None
        #     for item in class_data:
        #         try:
        #             lineitem_val = item["particular"]
        #             if lineitem_val.lower().find("current tax") >= 0:
        #                 tax_signage = item["Label Signage"]
        #                 break
        #         except:
        #             pass
        #     if tax_signage is not None:
        #         for item in class_data:
        #             item["Label Signage"] = tax_signage

    return is_data


def bs_signage(bs_data):
    for class_, class_data in bs_data.items():
        pos_counter, neg_counter = find_sign_count(bs_data[class_])
        if class_ in ['Current Assets', 'Non-current Assets', 'Non-Current Liabilities', 'Current Liabilities']:
            class_data = assert_label_signage(class_data, pos_counter, neg_counter)
        elif class_ == 'Equity':
            if neg_counter > pos_counter:
                class_data = bs_equity_signage(class_data)
            else:
                class_data = assert_label_signage(class_data, pos_counter, neg_counter)
        else:
            class_data = assert_label_signage(class_data, pos_counter, neg_counter, only_assert=True)

    # Less transfer logic
    # less_expr = ""
    for class_, class_data in bs_data.items():
        for item in class_data:
            # if class_ == "Equity":
            #     print(item)
            try:
                lineitem_val = item["particular"]
                lineitem_val = lineitem_val.replace(":"," ").replace(",","").replace("-"," ")
                if len(lineitem_val) == 0:
                    continue
                # if class_ == "Equity":
                # print("LINE ITEM IS ::::: ", lineitem_val)
                if " " in lineitem_val:
                    split_lineitem = lineitem_val.split(' ')
                else:
                    split_lineitem = [lineitem_val] + [" "]
                # print("AFTER SPLITTING :::: ", split_lineitem, "...")
                word1, word2 = split_lineitem[:2]
                # print("AFTER SPLITTING :::: ", word1, word2)
                word1, word2 = word1.strip(), word2.strip()
                # if class_ == "Equity":
                #     print("WORD1 ::: ", word1)
                #     print("WORD2 ::: ", word2)                
                if len(word2) == 0:
                    if word1.lower().find("less") >= 0 and word1.lower().find("less") <= 2:
                        item = change_neg_signage(class_, class_data, item, all_class=False)
                if (re.search("(?:LES)", word1, re.IGNORECASE) and len(word1) < 5) or (re.search("(?:LES)", word2, re.IGNORECASE) and len(word2) < 5):
                    item = change_neg_signage(class_, class_data, item, all_class=False)
                elif (re.search("(?:LES)", word1[:4], re.IGNORECASE) and len(word1) > 5) or (re.search("(?:LES)", word2[:4], re.IGNORECASE) and len(word2) > 5):
                    item = change_neg_signage(class_, class_data, item, all_class=False)
            except Exception:
                pass

    return bs_data

def year_count_(dict_:dict)->int:
    ''' Return the number of year present in extraction json'''

    name = ' '.join(list(dict_.keys()))

    m = re.findall("(Year[0-9] Value)", name)
    return len(m)

def less_signage(data):

    '''
        Input: list of dictionaries
        Output: the label_signage field, for less label will be updated
    '''

    # check if less label there
    if data:
        year_len = year_count_(data[0])
    else:
        year_len = 1

    less_flag = any(fuzz.token_set_ratio("less", data[idx]["Label Name"].lower())>88 for idx in range(len(data)))
    # print(less_flag)

    out_data = []

    if less_flag:
        # check which index is less label
        less_idx = [idx for idx in range(len(data)) if fuzz.token_set_ratio("less", data[idx]["Label Name"].lower())>88]
        # print(less_idx)
        
        for idx in less_idx:
            # check if it's value is 0.0
            # print(data[idx])
            # if data[idx]["Year1 Value"] == "0.0" and data[idx]["Year2 Value"] == "0.0":
            if all(data[idx]["Year"+str(each+1)+" Value"] == "0.0" for each in range(year_len)):
                start_point = idx
                end_point = idx+3
            else:
                continue
            
            # if last label blank, all are negative signage
            if data[end_point]["Label Name"] == "":
                data[start_point+1]["Label Signage"] = "-"
                data[start_point+2]["Label Signage"] = "-" 
                out_data.append(data[start_point+1])
                out_data.append(data[start_point+2])
            else: 
                # if net/total as well as domain check in last label, then all negative
                str1 = data[end_point]["Label Name"].strip().lower()
                str2 = data[start_point-1]["Label Name"].strip().lower()
                str1_List = str1.split(" ")
                str2_List = str2.split(" ")
                # print(str1_List, str2_List)
                common_word_list = list(set(str1_List)&set(str2_List))
                if len(common_word_list)>0:
                    domain_check = any(fuzz.token_set_ratio(revenue_word.lower(), common_word_list[0])>88 for revenue_word in revenue_corpus)
                    if ("net" in data[end_point]["Label Name"].lower() or \
                        "total" in data[end_point]["Label Name"].lower()) or \
                            (len(common_word_list)>0 and domain_check):
                        # print(common_word_list, domain_check,"\n")    
                        data[start_point+1]["Label Signage"] = "-"
                        data[start_point+2]["Label Signage"] = "-"

            # print(data[start_point+1])
            # print(data[start_point+2])

                        out_data.append(data[start_point+1])
                        out_data.append(data[start_point+2])

    return out_data   # list of dictionaries



# file_name = '/home/user/workspace/xlrt_vol2/cnn_identification/mapping_sprint4/classification/classification_main/classification_output/processing_Gobinda_Construction_balancesheet_FY_2018_TFormat.json'
# out_file_name = file_name.replace('.json', '_result.json')
# json_file = open(file_name).read()

# json_ob = json.loads(json_file)

def start_signage(json_ob: dict)->dict:
    bs_data = json_ob['Balance Sheet_BS']
    is_data = json_ob['Profit and Loss_IS']
    cf_data = json_ob['Cash_Flow_CF']

    # # print(bs_data)
    if isinstance(is_data, dict):
        json_ob['Profit and Loss_IS'] = is_signage(is_data)
    else:
        json_ob['Profit and Loss_IS'] = []

    if isinstance(bs_data, dict):
        json_ob['Balance Sheet_BS'] = bs_signage(bs_data)
    else:
        json_ob['Balance Sheet_BS'] = []
        

    bs_data = json_ob["Extraction"][0]["Balance Sheet"]
    is_data = json_ob["Extraction"][1]["Income Statement"]   # list of dictionaries
    cf_data = json_ob["Extraction"][2]["Cash Flow"]

    # for less signage perform on extraction json and return only updated ones
    ext_data = {}
    ext_data["Balance Sheet_BS"] = less_signage(bs_data)
    ext_data["Profit and Loss_IS"] = less_signage(is_data)  # returns with the label_signage updated
    ext_data["Cash_Flow_CF"] = less_signage(cf_data)

    for ext_class, ext_values in ext_data.items():
        if len(ext_values)==0 or isinstance(json_ob[ext_class], list):
            continue
        else:
            for label in ext_values:
                line_item1 = label["Label Name"]
                label_value1 = label["Year1 Value"]
                for _, class_data in json_ob[ext_class].items():
                    # print("\n",class_data)
                    if len(class_data)>0:
                        if isinstance(class_data[0], dict):
                            for item in class_data:
                                line_item2 = item["particular"]
                                item_value1 = item[label["Year1"]]
                                if line_item1.lower() == line_item2 and \
                                    round(float(label_value1)) == round(item_value1):
                                    item["Label Signage"] = label["Label Signage"]


    # with open(out_file_name, 'w') as out_json:
    #   json.dump(json_ob, out_json)

    return json_ob
