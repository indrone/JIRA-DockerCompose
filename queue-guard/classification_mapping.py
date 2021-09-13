import sys, traceback
#sys.path.insert(0,'/home/ubuntu/XLRT_Python/')
# sys.path.insert(0,'/home/dev/XLRT_Python')
# sys.path.insert(0,'/home/dev/XLRT_Python/XLRT_RabbitMQ_configuration/')
# sys.path.insert(0,'/home/dev/XLRT_Python/utils/')
import pika
from config import *
import requests
import json

from email_module.email_client import *
from datetime import datetime
from copy import deepcopy
from time import sleep

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



mq_url = get_message_url()
mq_port = get_message_port()
mq_username = get_message_username()
mq_password = get_message_password()
mq_start_que = get_class_mapping_que_name()
# quelist = rest_queue_list(user = str(mq_username),password=str(mq_password),host=str(mq_url),port=str(15672),virtual_host='/')
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
def callback(ch, method, properties, body):
    global mappingid

    try:
        current_time = datetime.now()
        print("...............  Recieved message  .................")
        print('The current time (START):',current_time)
        print('-----------------------')

        data_ = body
        data_ = str(data_.decode("utf-8"))
        data_ = json.loads(data_)
        #templateid = data_['templateId']
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
        #print(data_)
        res = data_
        res = classification_mapping_api(res)
        
        print("Response::",res)
        print("Response type::",type(res))
        #print("Response value::",res)
        # res = res.json()
        print(res)

        d = res
        # f = open('class_mapping_output.txt','w')
        # f.write(json.dumps(d,default=str))
        # f.close()
        # op_q = get_end_que_name()
        # # if op_q not in quelist:
        #     # channel.queue_declare(queue=op_q,durable=True)
        # # channel.basic_publish(exchange='', routing_key=op_q, body=json.dumps(d))
        # routing_key_output = get_route_key_output()
        # if op_q not in quelist:
        #     channel.queue_declare(queue = op_q,durable=True)
        #     # routing_key_output = get_route_key_output()
        #     channel.queue_bind(exchange='parseResponses', queue=op_q, routing_key=routing_key_output)

            # channel.queue_declare(queue=op_q,durable=True)
        routing_key_output = get_route_key_output()
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

        main_op = data_['extra']
        main_op["status"] = { "status": "false", "code": 500, "message": "Line item Classification Mapping::: "+str(e) }
        main_op["extracteddata"] = {}
        main_op["extracteddata"].update({"pages": []})
        main_op["extracteddata"].update({"parseddata": {"source": {"mappingid":mappingId,"module":"Line item Classification Mapping::: "+str(e)}}})
        res = main_op

        # res = {"status":500,"data":"Classification Mapping","mappingId":mappingId}
        op_q = get_end_que_name()
        # if op_q not in quelist:
        #     channel.queue_declare(queue=op_q,durable=True)
        # channel.basic_publish(exchange='', routing_key=op_q, body=json.dumps(res))
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
        # exc_type, exc_value, exc_traceback = sys.exc_info()
        # traceback.print_exception(exc_type, exc_value, exc_traceback,limit=2, file=sys.stdout)
        # print(traceback)
        track = traceback.format_exc()
        text = json.dumps(meta,indent=2) + '\n\n\n' +str(track)

        #message_client("Sandbox US:::Lineitem Classification Mapping",str(track));pass


    

    
# start_process(body)
while True:
    try:

        init_start = datetime.now()
        print("Que here:   ", mq_start_que)

        ''' Consuming message '''	
        channel.basic_consume(
            queue=mq_start_que, on_message_callback=callback, auto_ack=True)

        channel.start_consuming()
    except Exception as e:
        #message_client("Sandbox US:::Lineitem Classification Mapping",'service restarted.....!')
        sleep(5)
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
        print("Que here:   ", mq_start_que)
        op_q = get_end_que_name()
        # error_res = {"data": {"source": {"mappingid":mappingid,"module":"Line item Classification Mapping(Connection reset)"}},"status": 500} 

        main_op = data_['extra']
        main_op["status"] = { "status": "false", "code": 500, "message": "Line item Classification Mapping::: "+str(e) }
        main_op["extracteddata"] = {}
        main_op["extracteddata"].update({"pages": []})
        main_op["extracteddata"].update({"parseddata": {"source": {"mappingid":mappingId,"module":"Line item Classification Mapping::: "+str(e)}}})
        error_res = main_op

        # if op_q not in quelist:
        #     channel.queue_declare(queue=op_q,durable=True)
        # channel.basic_publish(exchange='', routing_key=op_q, body=json.dumps(error_res))
        routing_key_output = get_route_key_output()
        if op_q not in quelist:
            channel.queue_declare(queue = op_q,durable=True)
            # routing_key_output = get_route_key_output()
            channel.queue_bind(exchange='parseResponses', queue=op_q, routing_key=routing_key_output)

            # channel.queue_declare(queue=op_q,durable=True)
        channel.basic_publish(exchange='parseResponses', routing_key=routing_key_output, body=json.dumps(error_res))
        print("::ERROR MESSAGE SENT FROM MAIN::")
        print(error_res)
        print('The current time:',datetime.now())

        ''' Consuming message '''	
        channel.basic_consume(
            queue=mq_start_que, on_message_callback=callback, auto_ack=True)

        channel.start_consuming()
        continue

