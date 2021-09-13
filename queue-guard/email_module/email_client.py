import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import os
def read_credentials():
    #directory = os.getcwd()
    #f = open('./email_module/creds/config.json','r')
    
    #creds = json.load(f)
    creds  ={
    "username":"xlrt.prod.mq.python@gmail.com",
    "password":"1@B3ngal1",
    "receivers":[
        "santanukhan@prmfincon.com",
        "rajdeep@prmfincon.com",
        "ashim@prmfincon.com"
    ]
        }
    return  creds


def message_client(module,error_log):
    mail_creds = read_credentials()
    mail_content = "Hi Admin,\n\nModule :: {}\n\nERROR LOG::\n\n{}".format(module,error_log)
    #The mail addresses and password
    sender_address =mail_creds['username'] #'xlrt.prod.mq.python@gmail.com'
    sender_pass = mail_creds['password']#'1@B3ngal1
    receivers = mail_creds['receivers']
    for receiver in receivers:

        receiver_address = receiver
        #Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = 'XLRT MQ::: '+module   #The subject line
        #The body and the attachments for the mail
        message.attach(MIMEText(mail_content, 'plain'))
        #Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
        session.starttls() #enable security
        session.login(sender_address, sender_pass) #login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        print('Mail Sent')
