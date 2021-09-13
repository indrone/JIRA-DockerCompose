import json
import copy
import re
#import pprint

year_count_bs = 2
year_count_is = 2

def json_renderer(input_json: dict,meta_format: dict) -> dict:
    """
    This module creates the periods list with period indexes and source values list for each lineitem.
    Parameters
    ----------
    input_json:dict
        Data generated after classification and mapping.
    
    meta_format:dict
        The years present in the annual report with periodidx,periodkey initialized. 

    Returns
    -------
    data:dict
        Reformatted json

    """
    

    
    
    if not isinstance(input_json, dict) and not isinstance(meta_format,dict) :
        raise TypeError


    else:
        global year_count_bs

        res = {"extracteddata":[]}  
        input_json = input_json['data']
        for k,v in input_json.items():

            if v:

                doc_type = {"Balance Sheet_BS":"Balance Sheet","Profit and Loss_IS":"Income Statement",'Cash Flow': 'Cash Flow'}
                for i in input_json[k]:
                    temp ={}
                    temp['id'] = i['id']
                    # i["particular"] to i["Label Name"] for integreting non mapped line items
                    try:
                        temp["sourcelabel"]=i["particular"]
                    except KeyError:
                        temp["sourcelabel"]=i["Label Name"]
                    temp['sourcevalue']=[]
                    for year in meta_format['periods']:
                        year_ = copy.deepcopy(year)
                        # print("Year::", year_)
                        index = meta_format['periods'].index(year)
                        year_['index'] = index
                        # print("Index:::", index)
                        # print("i:::", i)
                        
                        year_['value']  = i[str(meta_format["periods"][index]["year value"])]

                        del year_['year']
                        del year_['periodtype']
                        del year_['year value']
                        del year_['periodidx']
                        del year_['yearidx']
                        if 'startdate' in list(year_.keys()):
                            del year_['startdate']
                            del year_['enddate']

                        temp["sourcevalue"].append(year_)
                    
                    temp["children"]=[]

                    try:
                        for idx, each in enumerate(i['children']):

                            # temp["children"].append({"sourcelabel":i["children"][idx]['Label Name'].lower(), "sourcevalue": copy.deepcopy(temp["sourcevalue"]), "isaggregated": False , "calculatedfield": False, "extrainfo": {"report_type":doc_type[k]}, "suggestion": i["suggestion"], "lineitemType": "Mapped"}) 
                            if "id" in list(i["children"][idx].keys()):
                                temp["children"].append({"sourcelabel":i["children"][idx]['Label Name'].lower(), "id":i["children"][idx]["id"], "sourcevalue": copy.deepcopy(temp["sourcevalue"]), "isaggregated": False , "calculatedfield": False, "extrainfo": {"report_type":doc_type[k]}, "suggestion": i["suggestion"], "lineitemType": "Mapped"}) 
                            else:
                                temp["children"].append({"sourcelabel":i["children"][idx]['Label Name'].lower(), "sourcevalue": copy.deepcopy(temp["sourcevalue"]), "isaggregated": False , "calculatedfield": False, "extrainfo": {"report_type":doc_type[k]}, "suggestion": i["suggestion"], "lineitemType": "Mapped"}) 
                            
                            if year_count_bs >= 1:
                                temp["children"][idx]["sourcevalue"][0]["value"] = i["children"][idx]["Year1 Value"]
                            if year_count_bs >= 2:
                                temp["children"][idx]["sourcevalue"][1]["value"] = i["children"][idx]["Year2 Value"]
                            if year_count_bs == 3:
                                temp["children"][idx]["sourcevalue"][2]["value"] = i["children"][idx]["Year3 Value"]
                        # print(i)
                    except Exception as e:
                        # print(e)
                        pass
                        
                    temp["isaggregated"]=False
                    temp["calculatedfield"]=i["Calculated Field"]
                    temp["extrainfo"]={"report_type":doc_type[k]}
                    try:
                        temp['suggestion'] = copy.deepcopy(i['suggestion'])
                    except KeyError:
                        temp['suggestion'] = {}

                    
                    if not temp['suggestion'] == {}:
                        if i['Label Signage']=="H" :
                            temp["lineitemType"]="Header"
                        else :
                            temp["lineitemType"]="Mapped"
                        temp['suggestion']['name'] = i['suggestion']['label']#[obj['name'] for obj in json_object['body'] if obj['label']==i['suggestion']['label']][0] if len([obj['name'] for obj in json_object['body'] if obj['label']==i['suggestion']['label']])!=0 else None #[0]['name']
                        del temp['suggestion']['label']
                        
                        temp['suggestion']['label'] = temp['suggestion'].pop('lineitem')
                        del temp['suggestion']['labelitem']
                        temp['suggestion']['classname'] =temp['suggestion'].pop('class')
                        temp['suggestion']['subclassname']=temp['suggestion'].pop('subclass')
                    else:
                        temp["lineitemType"]="Unmapped"

                        


                    res['extracteddata'].append(temp)
                
        d = {'data':[]}
        d['data'].append(res)
        return d
    
def bs_checker(input_json):
    if len(input_json['data']['Balance Sheet_BS'])>0:
        return True
    else:
        return False

def is_checker(input_json):
    if len(input_json['data']['Profit and Loss_IS'])>0:
        return True
    else:
        return False
    pass

def cf_checker(input_json):
    if len(input_json['data']['Cash Flow'])>0:
        return True
    else:
        return False
    pass

def formatInput(input_data : dict, year_count: int) -> dict:
    """
    This modules  generates the meta_data format and sends it to json reformat function (i.e json_renderer).
    Parameters
    --------- 
    input_data:dict
        Input json from classification and mapping module.
    
    Returns
    --------
    res:dict
        Output JSON generted after reformatting.
    
    """

    global year_count_bs, year_count_is

    year_count_bs = year_count
    year_count_is = year_count

    # if year_count_bs == year_count_is:
    #   year_count = year_count_bs      

    # print('BS, IS year::::',year_count_bs, year_count_is)

    meta_format = {"periods": []}

    # meta_sub_format = {
    #       "periodtype": "ANNUAL",
    #       "periodkey": '',
    #       "quarteridx": 0,
    #       "monthidx": 0,
    #       "yearidx" : 0,
    #       "year": '',
    #       "year value": ''
    #   }

    # meta_format["periods"] = [meta_sub_format for i in range(0, year_count)]
    # print(meta_format)
 
    input_json = {'data' : { 'Balance Sheet_BS': input_data['Balance Sheet_BS'],  'Profit and Loss_IS': input_data['Profit and Loss_IS'], 'Cash Flow': input_data['Cash Flow']}}

    if bs_checker(input_json):
        avavilabe = 'Balance Sheet_BS'
        index = 0

    elif is_checker(input_json):
        avavilabe = 'Profit and Loss_IS'
        index = 1

    elif cf_checker(input_json):
        avavilabe = 'Cash Flow'
        index = 2


    for idx in range(0, year_count_bs):
        # print(input_json['data'][avavilabe][index])
        print(input_json['data'][avavilabe][index]['Year'+str(idx+1)],"-------year",)
        print(input_json['data'][avavilabe][index]['Year'+str(idx+1)+" Value"],"-------year value")

        # if len(input_json['data']['Balance Sheet_BS'][0]['Year'+str(idx+1)+" Meta"]) == 0:
        if not "Quarter" in list(input_json['data'][avavilabe][index]['Year'+str(idx+1)+" Meta"].keys()):
            meta_sub_format = {
            "periodtype": "ANNUAL",
            "year": "",
            "yearidx": "",
            "periodidx": ""

            }

        else:
            meta_sub_format = {
            "periodtype": "QUARTER",
            "year": "",
            "yearidx": "",
            "periodidx": "",
            "startdate": "",
            "enddate": "",
            }
            meta_sub_format["enddate"] = input_json['data'][avavilabe][index]['Year'+str(idx+1)+" Meta"]["Quarter"]

        # meta_sub_format['year'] = input_json['data']['Balance Sheet_BS'][0]['Year'+str(idx+1)].split('-')[0]
        meta_sub_format["yearidx"] = input_json['data'][avavilabe][index]['Year'+str(idx+1)+" Meta"]["yearidx"]
        meta_sub_format["periodidx"] = input_json['data'][avavilabe][index]['Year'+str(idx+1)+" Meta"]["periodidx"]
        meta_sub_format['year value'] = 'Year'+str(idx+1)+" Value"
        meta_sub_format['year'] = input_json['data'][avavilabe][index]['Year'+str(idx+1)]

        meta_format["periods"].append(meta_sub_format)

    # print('--------------------------------------------------------')
    # print(input_json)
    print('---------------------------------------------------------')
    print(meta_format)
    res = json_renderer(input_json,meta_format)
    for idx,k in enumerate(meta_format["periods"]):
        meta_format["periods"][idx]['year'] = input_json['data'][avavilabe][index]['Year'+str(idx+1)].split('-')[0]
        del meta_format["periods"][idx]['year value']

    print('$$$$$$$$$$$$$$$$$$$$$$$$$$', meta_format)


    res['source'] = copy.deepcopy(input_data['Source'])
    report_type = {"balance_sheet":"Balance Sheet","income_statement":"Income Statement",'cash_flow': 'Cash Flow'}
    fin_page_meta_data = res['source'].pop('financial_page')
    # print(fin_page_meta_data)
    fin_page_meta = []
    try:
        for k,v in fin_page_meta_data.items():
            if k=='doc_type':
                continue
            else:
                temp = {"type":"","pages":""}
                temp['type'] = report_type[v['type']]
                temp['pages'] = v['pages'] 
                fin_page_meta.append(temp)
    except:
        pass

    res['source'] = {'financial_page':''}
    res['source']['financial_page'] = fin_page_meta
    res['periods'] = meta_format['periods']
    res['source']['documentid'] = input_data['Source']['documentid']
    res['source']['filename'] = input_data['Source']['filename']
    res['source']['filetype'] = input_data['Source']['filetype']
    res['source']['fileurl'] = input_data['Source']['fileurl']
    if 'externalfileurl' in input_data['Source'].keys():
        res['source']['externalfileurl'] = input_data['Source']['externalfileurl']
    res['source']['mappingid'] = input_data['Source']['mappingid']
    res['source']['templateid'] = str(input_data['Source']['templateid'])
    res['source']['templatename'] = input_data['Source']['templatename']
    res['source']['type'] = input_data['Source']['type']
    res['customer'] = input_data['Customer']
    res['customer_code'] = input_data['Customer Code']

    return res
