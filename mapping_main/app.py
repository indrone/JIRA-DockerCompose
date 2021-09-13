from flask import Flask, render_template,request,jsonify
from src import mapping
from utils import *
from service import *
import json
import requests
import pprint
import csv
from datetime import datetime
import pandas as pd
from mapping_json_format import *
import os
import logging
from logging.handlers import RotatingFileHandler
global logger
import json_logging
import config
import ssl
from event_publisher import send_event
import glob, shutil
import copy

if not os.path.exists('logs'):
    os.makedirs('logs')
if not os.path.exists('mapping_output/Final_Output'):
    os.makedirs('mapping_output/Final_Output')



app = Flask(__name__) 
app.name ="classificationmapping"
send_event(app)


json_logging.ENABLE_JSON_LOGGING = True
json_logging.init_flask()
json_logging.init_request_instrument(app)

documnentid = ''
logger = ''

def initialize_app_logger():

    """
 
    Initialize the logger
 
    Parameters
    ----------
    
    Returns
    -------
    None
        
    """

    if not os.path.exists('logs'):
        os.makedirs('logs')

    global logger
    logger = logging.getLogger('gunicorn.info')
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler('logs/Mapping.log', maxBytes=10000000, backupCount=50)
    logger.addHandler(handler)


def wrapper(data:dict, type_:str)->dict:

    ''' Removing the standalone and consolidated part and converted into previous format'''
    data['Data']['Financial Tables'] = [{p["page_type"] : p["values"]} for p in data['Data']['Financial Tables'] if p['report_type'] == type_]
    data['Source']['financial_page'] = {k:v[0] if isinstance(v,list) and v[0]['type'] == type_ else v for k,v in data['Source']['financial_page'].items()}

    for k,v in data['Source']['financial_page'].items():
        if isinstance(v,dict):
            data['Source']['financial_page'][k]['type'] = k

    return data


def json_validation(res):

    ''' Checking the final json is valid or not'''
    global logger , documnentid, mappingid

    if "data" in res["extracteddata"]["parseddata"].keys() and "periods" in res["extracteddata"]["parseddata"].keys():

        print('\n\n************************************RESPONSE 200************************************')
        logger.info('************************************RESPONSE 200************************************', extra={'props': {"documentid": res['document']['dmscode']}})

    else:
        print('\n\n************************************JSON VALIDATION FAILED************************************')
        logger.error('************************************JSON VALIDATION FAILED************************************', extra={'props': {"documentid": res['document']['dmscode']}})
        raise ValueError('JSON VALIDATION FAILED')


def file_removal(folder, limit):

    ''' Delete all saved files after the count reaches'''
    if len(os.listdir(folder)) >= limit:
        docid = list(os.listdir(folder))
        print("\n\n\n")
        print(f'Flushing docids::: {docid}')
        print("\n\n\n")

        for files in glob.glob(folder+'*'):
            if files.split('.')[-1] in ['json','csv']:
                os.remove(files)

        print("Removed all files from ", folder)


def process(each_data:dict, type_:str):

    global logger , documnentid,mappingid

    balance_sheet = []
    income_statement = []

    year_count = year_count_((each_data['Data']['Financial Tables'][1]['Income Statement'] + each_data['Data']['Financial Tables'][0]['Balance Sheet'])[0] if each_data['Data']['Financial Tables'][1]['Income Statement'] + each_data['Data']['Financial Tables'][0]['Balance Sheet'] else {})
    print('year_coun:::',year_count)

    '''Year count 0 means no data in extraction'''
    if year_count != 0:

        for i, itr in enumerate(each_data['Data']['Financial Tables'][0]['Balance Sheet']):

            for yc in range(year_count):
                each_data['Data']['Financial Tables'][0]['Balance Sheet'][i]['Year'+str(yc+1)+' Value'] = junkremover(each_data['Data']['Financial Tables'][0]['Balance Sheet'][i]['Year'+str(yc+1)+' Value'])
                

        for i, itr in enumerate(each_data['Data']['Financial Tables'][1]['Income Statement']):

            for yc in range(year_count):
                each_data['Data']['Financial Tables'][1]['Income Statement'][i]['Year'+str(yc+1)+' Value'] = junkremover(each_data['Data']['Financial Tables'][1]['Income Statement'][i]['Year'+str(yc+1)+' Value'])


        # print(each_data)
        ssl._create_default_https_context = ssl._create_unverified_context
        rqst_dynamic_map = requests.get(url=find_url_template(each_data),verify=False)
        dynamic_data = rqst_dynamic_map.json()
        each_data['type'] = type_

        classification_data = requests.post(config.get_url(), json=each_data)
        DATA = each_data

        classification_data=classification_data.json()
        
        # logger.info(DATA['Source'])

        if each_data['Data']['Financial Tables'][0]['Balance Sheet']:

            logger.info("balance_sheet mapping has STARTED..", extra={'props': {"documentid": each_data['Source']['documentid']}})

            balance_sheet=balance_sheet_service(DATA,classification_data["Balance Sheet_BS"],dynamic_data, logger)
            # logger.info(balance_sheet)
            logger.info("balance_sheet mapping has ENDED..", extra={'props': {"documentid": each_data['Source']['documentid']}})


        if balance_sheet:
            balance_sheet = balance_sheet['Data']['Financial Tables'][0]['Balance Sheet']

        if each_data['Data']['Financial Tables'][1]['Income Statement']:

            logger.info("income_statement mapping has STARTED..", extra={'props': {"documentid": each_data['Source']['documentid']}})

            income_statement=income_statement_service(DATA,classification_data["Profit and Loss_IS"],dynamic_data, logger)
            # logger.info(income_statement)
            logger.info("income_statement mapping has ENDED..", extra={'props': {"documentid": each_data['Source']['documentid']}})


        if income_statement:
            income_statement = income_statement['Data']['Financial Tables'][1]['Income Statement']

        cash_flow = []

    else:
        DATA = each_data
        balance_sheet, income_statement, cash_flow = [], [], []

    try:

        res = {"Customer":DATA["Customer"] ,"Customer Code":DATA["Customer Code"],"Source":DATA["Source"],"Balance Sheet_BS":balance_sheet,"Profit and Loss_IS":income_statement,"Cash Flow":cash_flow}

        # with open("mapping_output/Final_Output/documentid/preprocessing_"+DATA['Source']['documentid']+'_'+DATA['Source']['filename'].replace('.pdf','')+".json", 'w') as f:
        #     json.dump(res, f)


        if DATA['Source']['templateid']:
            res['Source']['templateid']=DATA['Source']['templateid']
        else:
            res['Source']['templateid']=config.templateid

        if year_count != 0:
            res = formatInput(res, year_count)

            main_op = each_data['extra']
            main_op["status"] = { "status": "true", "code": 200, "message": "" }
            main_op["extracteddata"] = {}
            main_op["extracteddata"].update({"pages": []})
            main_op["extracteddata"].update({"parseddata": res})
            res = main_op

            # mapped_lineitems = []
            mapped_lineitems = list(set([each['suggestion']["name"] for each in res["extracteddata"]["parseddata"]["data"][0]["extracteddata"] if each['suggestion']]))

            unmapped_lineitems = remaining_lineitems(dynamic_data, mapped_lineitems)
            res["extracteddata"]["parseddata"]["data"][0].update({"unmappeditems" : unmapped_lineitems})

        else:
            return []

    except Exception as e:
        print(e)
        print(traceback.print_exc())
        logger.error(e, extra={'props': {"documentid": each_data['Source']['documentid']}})
        return []


    return res


@app.errorhandler(Exception)
def all_exception_handler(error):
    print('Doc ID::::::',app.config['SECRET_KEY'], 'Error::::::', traceback.format_exc())
    return 'Error', 500

    
@app.route('/class_mapping',methods=['POST'])
def class_mapping(): 

    '''Handler for mapping'''
    global logger , documnentid,mappingid
    processed_data = []
    rqst_data = request.get_json()

    # file_removal('./mapping_output/', 60)
    if not os.path.exists('mapping_output/Final_Output/'+rqst_data['Source']['documentid']):
        os.makedirs('mapping_output/Final_Output/'+rqst_data['Source']['documentid'])

    app.config['SECRET_KEY'] = rqst_data['Source']['documentid']
    documentid = rqst_data['Source']['documentid']

    print('\n\n************************************ STARTING '+ rqst_data['Source']['documentid'] +' ************************************')
    logger.info('************************************STARTING************************************'+ rqst_data['Source']['documentid'], extra={'props': {"documentid": rqst_data['Source']['documentid']}})

    print('\n\n************************************STANDALONE STARTING************************************')
    standalone_rqst_data = process(wrapper(copy.deepcopy(rqst_data), "standalone"), "standalone")
    print('\n\n************************************CONSOLIDATED STARTING************************************')
    consolidated_rqst_data = process(wrapper(copy.deepcopy(rqst_data), "consolidated"), "consolidated")

    if standalone_rqst_data:
        standalone_rqst_data['extracteddata']["parseddata"]['data'][0].update({"metadata":{"type":"standalone"}})

    if consolidated_rqst_data:
        consolidated_rqst_data['extracteddata']["parseddata"]['data'][0].update({"metadata":{"type":"consolidated"}})

    if standalone_rqst_data and consolidated_rqst_data:
        standalone_rqst_data['extracteddata']["parseddata"]['data'] = standalone_rqst_data['extracteddata']["parseddata"]['data'] + consolidated_rqst_data['extracteddata']["parseddata"]['data']

    elif standalone_rqst_data:
        standalone_rqst_data['extracteddata']["parseddata"]['data'] = standalone_rqst_data['extracteddata']["parseddata"]['data'] + [{"extracteddata":[], "unmappeditems":[], "metadata":{"type":"consolidated"}}]

    elif consolidated_rqst_data:
        consolidated_rqst_data['extracteddata']["parseddata"]['data'] = [{"extracteddata":[], "unmappeditems":[], "metadata":{"type":"standalone"}}] + consolidated_rqst_data['extracteddata']["parseddata"]['data']
        standalone_rqst_data = consolidated_rqst_data


    standalone_rqst_data['extracteddata']["parseddata"]['source']['financial_page'] = rqst_data['Source']['financial_page']
    res = standalone_rqst_data

    with open("mapping_output/Final_Output/"+rqst_data['Source']['documentid']+"/Mapping_"+rqst_data['Source']['filename'].replace('.pdf','')+".json", 'w') as f:
        json.dump(res, f)

    print('\n\n************************************ ENDED '+ rqst_data['Source']['documentid'] +' ************************************')
    logger.info('************************************ENDED************************************ '+ rqst_data['Source']['documentid'], extra={'props': {"documentid": rqst_data['Source']['documentid']}})


    json_validation(res)

    # print(res)

    return json.dumps(res,default=str,indent=4)

    

@app.route('/mapping/health')
def health_check() :
	"""
	Health checking handler

	"""
	return "Running"



@app.route('/worker_test',methods= ['GET', 'POST'])
def worker_test():
    """
    Health checking handler
    """
    if request.method == 'POST':
        json_data = json.loads(request.data, strict=False)
        time.sleep(1)
    return json.dumps({"ok":"done"})


@app.before_first_request
def execute_this():
    initialize_app_logger()

if __name__ == '__main__':

    # initialize_app_logger()
    app.run(host=config.get_host(),debug=False,port=config.get_port())


