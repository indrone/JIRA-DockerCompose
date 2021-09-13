import sys, traceback
import pika
from config import *
import requests
import json

from email_module.email_client import *
from datetime import datetime
from copy import deepcopy
from time import sleep
from _thread import start_new_thread
import time

init_start = None
mappingid = None

def classification_mapping_api(data):
    url = get_classification_mapping_api()
    #url = "http://130.61.23.77:8026/class_mapping"
    res = requests.post(url,json=data)
    res = res.json()
    return res

''' Consumer will always listent the rabbitmq port,
    get a valid message and start the process '''

''' All credecnitals '''



def init_queue():

    try:
        mq_url = get_message_url()
        mq_port = get_message_port()
        mq_username = get_message_username()
        mq_password = get_message_password()
        mq_start_que = get_class_mapping_que_name()
       
        que_list_url = get_queue_list_url()
        quelist = rest_queue_list(que_list_url,user = str(mq_username),password=str(mq_password))
        print(quelist)
        print("############### Handler #################")
        print('')
        print('')

        print(" Que  :", mq_start_que)

        print('----------------')
        ''' Initialize credential '''
        credentials = pika.PlainCredentials(mq_username, mq_password)
        print('credentials initializing.....!')
        ''' Initialize parameters'''
        parameters = pika.ConnectionParameters(mq_url,
                                           mq_port,
                                           '/',
                                           credentials)

        ''' Building connection '''
        connection = pika.BlockingConnection(parameters)
        print('building connections.....!')
        ''' Building channel '''
        channel = connection.channel()
        channel.exchange_declare(exchange='parseResponses', exchange_type='topic', durable=True)

        ''' Declearing que ''' 

        if mq_start_que not in quelist:
            channel.queue_declare(queue=mq_start_que,durable=True)

        op_q = get_end_que_name()

        routing_key_output = get_route_key_output()
        if op_q not in quelist:
            channel.queue_declare(queue = op_q,durable=True)
            # routing_key_output = get_route_key_output()
            channel.queue_bind(exchange='parseResponses', queue=op_q, routing_key=routing_key_output)

        print('Queue declare.....!')
        print("------- Here??? ------------------")

        return channel, mq_start_que, quelist

    except Exception as e:
        print(str(e))
        print("----------- Problem while establishing connection with RabbitMQ -----------")


def error_response(e:object, msg:str, data_raw_:dict)->dict:
    try:
        main_op = data_raw_
        main_op["status"] = { "status": "false", "code": 500, "message": "Classification Mapping::: " }
        main_op["extracteddata"] = {}
        main_op["extracteddata"].update({"pages": []})
        main_op["extracteddata"].update({"parseddata": {"source": {"mappingid":data_raw_["messageid"]+'-'+data_raw_["document"]["dmscode"],"module":"Classification Mapping" +msg+"::: "}}})
    except:
        print('Exception handeled in error response!!!!')
        main_op["extracteddata"].update({"parseddata": {"source": {"mappingid":'Unable to fetch',"module":"Classification Mapping" +msg+"::: "}}})
        return main_op

    return main_op


def publish_threads(body, quelist):

    try:

        print("Reinitializing Channel in publisher for avoiding channel sharing across thread ..............................")
        channel, mq_start_que, quelist = init_queue()
        
        current_time = datetime.now()
        print("...............  Recieved message  .................")
        print('The current time (START):',current_time)
        print('-----------------------')

        data_ = body
        data_ = str(data_.decode("utf-8"))
        data_ = json.loads(data_)

        print('---------------------Not raw--------------------------------')
        mappingId = None
        meta = None
        if 'documents' in data_.keys():
            mappingId = data_['documents'][0]['mappingId']
            meta = data_['documents'][0]
        else:
            mappingId = data_['Source']['mappingid']
            meta = data_['Source']
        mappingid = mappingId

        res = data_
        url = get_classification_mapping_api()
        res = requests.post(url,json=res)
        res = res.json()
        
        print("Response::",res)
        print("Response type::",type(res))

        print(res)

        d = res
        
        routing_key_output = get_route_key_output()
        time.sleep(2)
        channel.basic_publish(exchange='parseResponses', routing_key=routing_key_output, body=json.dumps(res))
        end_time = datetime.now()
        print('The current time(END):',end_time)
        print('Duration::::',(end_time - current_time).total_seconds()/60)
        print('-----------------------')

    except Exception as e:

        print(str(e))
        data_ = body
        data_ = str(data_.decode("utf-8"))
        data_ = json.loads(data_)
        
        mappingId = None
        mappingId = data_['Source']['mappingid']
        meta = data_['Source']
        # res = {"data": {"source": {"mappingid":mappingId,"module":"Line item Classification Mapping"}},"status": 500}

        res = error_response(e, '', data_['extra'])
        op_q = get_end_que_name()
        
        routing_key_output = get_route_key_output()
        if op_q not in quelist:
            channel.queue_declare(queue = op_q,durable=True)
            # routing_key_output = get_route_key_output()
            channel.queue_bind(exchange='parseResponses', queue=op_q, routing_key=routing_key_output)

            # channel.queue_declare(queue=op_q,durable=True)
        channel.basic_publish(exchange='parseResponses', routing_key=routing_key_output, body=json.dumps(res))
        print("::ERROR MESSAGE SENT FROM CALL BACK::")
        print(res)
        print('The current time:',datetime.now())
        print('-----------------------')


    
def publish_main(body, quelist):
    start_new_thread(publish_threads,(body, quelist))
    
if __name__ == "__main__":

    ''' Initialize the queue'''

    channel, mq_start_que, quelist = init_queue()

    ######## Consumer Section #########
    
    while True:
        try:

            print("Starting Consumer ..............................")
            init_start = datetime.now()

            ''' Consuming message '''   
            channel.basic_consume(
                queue=mq_start_que, on_message_callback= lambda ch, method, properties, body: publish_main(body, quelist), auto_ack=True)

            channel.start_consuming()

        except Exception as e:

            print(traceback.print_exc())

            channel, mq_start_que, quelist = init_queue()

            op_q = get_end_que_name()
            routing_key_output = get_route_key_output()

            error_res = error_response(e, '(Connection reset)', {})
            print('@@@@@@@@@@@@ Error Response @@@@@@@@@@@@@@@@', error_res)

            ''' If Exception occured then the error response will be sent to the END queue'''

            if op_q not in quelist:
                channel.queue_declare(queue = op_q,durable=True)
                channel.queue_bind(exchange='parseResponses', queue=op_q, routing_key=routing_key_output)

  
            channel.basic_publish(exchange='parseResponses', routing_key=routing_key_output, body=json.dumps(error_res))
            print("::ERROR MESSAGE SENT FROM MAIN::")
            print(error_res)
            print('The current time:',datetime.now())

            continue

