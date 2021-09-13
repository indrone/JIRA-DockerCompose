from flask import Flask, render_template, request, jsonify, redirect, url_for


from src import balance_sheet_class
from src import income_statement_class
from src import cash_flow_class

from utils import *
from service import *
import json
import requests
import pprint
import csv
from datetime import datetime
import pandas as pd

import os, glob
import logging
from logging.handlers import RotatingFileHandler
global logger
import json_logging
import config
from signage_check import *
import traceback

if not os.path.exists('logs'):
    os.makedirs('logs')

if not os.path.exists('classification_output/Final_Output'):
    os.makedirs('classification_output/Final_Output')

logger = ''

#app = Flask(__name__, template_folder="templates", )
app = Flask(__name__)
json_logging.ENABLE_JSON_LOGGING = True
json_logging.init_flask()
json_logging.init_request_instrument(app)


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
    logger = logging.getLogger('gunicorn.error')
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler('logs/classification.log', maxBytes=10000000, backupCount=50)
    logger.addHandler(handler)


def file_removal(folder, limit):

    if len(os.listdir(folder)) >= limit:
        docid = list(os.listdir(folder))
        print("\n\n\n")
        print(f'Flushing docids::: {docid}')
        print("\n\n\n")

        for files in glob.glob(folder+'*'):
            if files.split('.')[-1] in ['json','csv']:
                os.remove(files)

        print("Removed all files from ", folder)



@app.route('/class_mapping', methods=['POST'])
def class_mapping():
    global logger, documnentid, mappingid
    rqst_data = request.get_json()

    # file_removal('./classification_output/', 60)
    if not os.path.exists('classification_output/Final_Output/'+rqst_data['Source']['documentid']):
        os.makedirs('classification_output/Final_Output/'+rqst_data['Source']['documentid'])

    print('##################################################### STARTING-> '+ rqst_data['Source']['documentid'] +' #########################################################')
    logger.info('@@@@@@@@@@@@@@@@@@@@@@@@@@STARTING-> '+ rqst_data['Source']['documentid'], extra={'props': {"documentid": rqst_data['Source']['documentid']}})

    #print(rqst_data)
    rqst_dynamic_map = requests.get(url=find_url_template(rqst_data),verify=False)
    dynamic_data = rqst_dynamic_map.json()
    DATA = rqst_data
    input_filename = "ABC_"
    # initialize_app_logger()
    # logger.info(DATA['Source'])
    
    logger.info("balance_sheet classification has started..", extra={'props': {"documentid": rqst_data['Source']['documentid']}})
    # logger.info("DATA..")
    # logger.info(DATA)
    # logger.info("input filename..")
    # logger.info(input_filename)
    # logger.info("Dynamic data..")
    # logger.info(dynamic_data)
    # logger.info("----------------------------------")
    balance_sheet = balance_sheet_service(DATA, input_filename, dynamic_data)
    # logger.info(balance_sheet)
    logger.info("balance_sheet classification has ended..", extra={'props': {"documentid": rqst_data['Source']['documentid']}})


    logger.info("income_statement classification has started..", extra={'props': {"documentid": rqst_data['Source']['documentid']}})

    income_statement = income_statement_service(DATA, input_filename, dynamic_data)
    print(income_statement)
    # logger.info(income_statement)
    logger.info("income_statement classification has ended..", extra={'props': {"documentid": rqst_data['Source']['documentid']}})


    logger.info(" cash_flow has classification started..", extra={'props': {"documentid": rqst_data['Source']['documentid']}})

    cash_flow = cash_flow_service(DATA, input_filename, dynamic_data)
    logger.info(cash_flow)

    logger.info(" cash_flow has classification ended..", extra={'props': {"documentid": rqst_data['Source']['documentid']}})

    res = {"Customer": DATA["Customer"], "Customer Code": DATA["Customer Code"], "Source": DATA["Source"],
           "Balance Sheet_BS": balance_sheet, "Profit and Loss_IS": income_statement, "Cash_Flow_CF": cash_flow}

    res["Extraction"] = rqst_data['Data']['Financial Tables']
    # print(res,"------------------------------------------------------------------------")
    with open("classification_output/Final_Output/"+rqst_data['Source']['documentid']+"/"+DATA["type"]+"_PreSignageClassification_"+DATA['Source']['filename'].replace('.pdf','')+".json", 'w') as f:
        json.dump(res, f)

    print('-----------------------------Starting Signage-------------------------------------')
    # print(res)
    try:
        if res["Profit and Loss_IS"]:
            km_index = res['Profit and Loss_IS']['km_index']
            res['Profit and Loss_IS']['km_index'] = []

            finance_cost_index = res['Profit and Loss_IS']['finance_cost_index']
            res['Profit and Loss_IS']['finance_cost_index'] = []

            signage_index = res['Profit and Loss_IS']['signage_index']
            res['Profit and Loss_IS']['signage_index'] = []

            is_graph_output = res['Profit and Loss_IS']['graph_output']
            res['Profit and Loss_IS']['graph_output'] = []

        if res["Balance Sheet_BS"]:
            bs_graph_output = res['Balance Sheet_BS']['graph_output']
            res['Balance Sheet_BS']['graph_output'] = []

        try:
            res = start_signage(res)
        except:
            print(traceback.print_exc())
            pass

        if res["Profit and Loss_IS"]:
            res['Profit and Loss_IS']['km_index'] = km_index
            res['Profit and Loss_IS']['finance_cost_index'] = finance_cost_index
            res['Profit and Loss_IS']['signage_index'] = signage_index
            res['Profit and Loss_IS']['graph_output'] = is_graph_output
            
        if res["Balance Sheet_BS"]:
            res['Balance Sheet_BS']['graph_output'] = bs_graph_output

    except Exception as e:
        print(traceback.print_exc())
        logger.error(e, extra={'props': {"documentid": rqst_data['Source']['documentid']}})


    # print(res)
    with open("classification_output/Final_Output/"+rqst_data['Source']['documentid']+"/"+DATA["type"]+"_PostSignageClassification_"+DATA['Source']['filename'].replace('.pdf','')+".json", 'w') as f:
        json.dump(res, f)

    print('##################################################### ENDED-> '+ rqst_data['Source']['documentid'] +' #########################################################')
    logger.info('@@@@@@@@@@@@@@@@@@@@@@@@@@ENDED-> '+ rqst_data['Source']['documentid'], extra={'props': {"documentid": rqst_data['Source']['documentid']}})
    
    return json.dumps(res, default=str, indent=4)


@app.route('/classification/health')
def health_check():
    """
    Health checking handler

    """
    return "Running"

@app.before_first_request
def execute_this():
    initialize_app_logger()

if __name__ == '__main__':
    # app.run(host="0.0.0.0",debug=False,port=5001)
    # app.run(host=config.host, debug=False, port=config.port)
    app.run(host=config.get_host(), debug=False, port=config.get_port())
