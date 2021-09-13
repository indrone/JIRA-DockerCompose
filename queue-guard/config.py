from ruamel import yaml
import sys
#sys.path.insert(0,'/home/dev/XLRT_Python')
#sys.path.insert(0,'/home/dev/XLRT_Python/XLRT_RabbitMQ_configuration/')
#sys.path.insert(0,'/home/dev/XLRT_Python/utils/')
from pyrabbit.api import Client
#path  = '/home/dev/XLRT_Python/XLRT_RabbitMQ_configuration'
import requests

'''
    Parsing config.yaml file and collenting required data

    Copyright : PRM FINCON Services pvt ltd
    Author: ark@007
'''



# def rest_queue_list(user='guest', password='guest', host='localhost', port=5672, virtual_host='/'):
    
#     cl = Client(host+':'+str(port), user, password)
#     queues = [q['name'] for q in cl.get_queues()]
#     # url = 'http://%s:%s/api/queues/%s' % (host, port, virtual_host or '')
#     # print("URL::::",url)
#     # response = requests.get(url, auth=(user, password))
#     # print(response.text)
#     # queues = [q['name'] for q in response.json()]
#     return queues


def rest_queue_list(url,user, password):
    
    # cl = Client(host+':'+str(port), user, password)
    res = 'default'
    if 'https' in url:
        res = requests.get(url,auth=(user,password),verify=False)
    else:
        res = requests.get(url,auth=(user,password))
    queues = [q['name'] for q in res.json()]
    return queues



def get_queue_list_url():
    info = parse_yaml('./config.yaml')
    if info:
        try:
            return info['queue_list_url']
        except Exception as e:
            print("Unable to find URL..... ")
            return False
    else:
        return False
        

def get_route_key_input():
    info = parse_yaml('./queue_list.yaml')
    if info:
        try:
            return info['route_key_input']
        except Exception as e:
            print("Unable to find Que name..... ")
            return False
    else:
        return False

def get_route_key_output():
    info = parse_yaml('./queue_list.yaml')
    if info:
        try:
            return info['route_key_output']
        except Exception as e:
            print("Unable to find Que name..... ")
            return False
    else:
        return False


def parse_yaml(file: str) -> dict:
    ''' Parse yaml file into dict '''
    try:
        info = yaml.safe_load(open(file))
        return info
    except Exception as e:
        print(e)
        print("Unable to find file....... ")
        return False


def get_message_url() -> str:
    import os 
    print(os.getcwd())
    ''' Collecting rabbit mq connection url '''
    info = parse_yaml('./config.yaml')
    if info:
        try:
            return info['host_rabbitMQ']
        except Exception as e:
            print("Unable to find URL..... ")
            return False
    else:
        return False

def get_page_identification_api() ->str:
    ''' Collecting rabbit mq connection port '''
    info = parse_yaml('./config.yaml')
    if info:
        try:
            return info['page_identification']
        except Exception as e:
            print("Unable to find port..... ")
            return False
    else:
        return False

def get_classification_mapping_api() ->str:
    ''' Collecting rabbit mq connection port '''
    info = parse_yaml('./config.yaml')
    if info:
        try:
            return info['classification_mapping']
        except Exception as e:
            print("Unable to find port..... ")
            return False
    else:
        return False

def get_message_port() -> str:
    ''' Collecting rabbit mq connection port '''
    info = parse_yaml('./config.yaml')
    if info:
        try:
            return info['port_rabbitMQ']
        except Exception as e:
            print("Unable to find port..... ")
            return False
    else:
        return False


def get_message_username() -> str:
    ''' Collecting rabbit mq connection username '''
    info = parse_yaml('./config.yaml')
    if info:
        try:
            return info['username']
        except Exception as e:
            print("Unable to find User Name..... ")
            return False
    else:
        return False


def get_message_password() -> str:
    ''' Collecting rabbit mq connection password '''
    info = parse_yaml('./config.yaml')
    if info:
        try:
            return info['password']
        except Exception as e:
            print("Unable to find password..... ")
            return False
    else:
        return False


def get_start_que_name() -> str:
    ''' Collecting Que name to start process '''
    info = parse_yaml('./queue_list.yaml')
    if info:
        try:
            return info['input_queue']
        except Exception as e:
            print("Unable to find Que name..... ")
            return False
    else:
        return False


def get_end_que_name() -> str:
    ''' Collecting Que name to start process '''
    info = parse_yaml('./queue_list.yaml')
    if info:
        try:
            return info['output_queue']
        except Exception as e:
            print("Unable to find Que name..... ")
            return False
    else:
        return False

def get_fin_page_que_name() -> str:
    ''' Collecting fin page que name '''
    info = parse_yaml('./queue_list.yaml')
    if info:
        try:
            return info['fin_page_identification']
        except Exception as e:
            print("Unable to find Que name..... ")
            return False
    else:
        return False

def get_table_extraction_annual()-> str:
    '''Collecting table extraction queue name'''
    info = parse_yaml('./queue_list.yaml')
    if info:
        try:
            return info['table_extraction_annual']
        except Exception as e:
            print("Unable to find Que name..... ")
            return False
    else:
        return False

def get_class_mapping_que_name()-> str:
    '''Collecting table extraction queue name'''
    info = parse_yaml('./queue_list.yaml')
    if info:
        try:
            return info['classification_mapping']
        except Exception as e:
            print("Unable to find Que name..... ")
            return False
    else:
        return False

def get_table_extractionUI_que_name()-> str:
    ''' Getting table Extraction que name for UI '''
    info = parse_yaml('./queue_list.yaml')
    if info:
        try:
            return info['UI_table_extraction']
        except Exception as e:
            print("Unable to find Que name..... ")
            return False
    else:
        return False

def get_tally_extraction_que_name()->str:
    info = parse_yaml('./queue_list.yaml')
    if info:
        try:
            return info['Tally_Extraction']
        except Exception as e:
            print("Unable to find Que name..... ")
            return False
    else:
        return False
