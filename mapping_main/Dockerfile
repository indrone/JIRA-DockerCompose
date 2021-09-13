FROM python:3.6-slim

RUN mkdir mapping_main

WORKDIR /mapping_main 

ADD . /mapping_main

RUN apt-get update -y

RUN apt-get install build-essential -y

RUN apt-get install  libsm6 libxext6 -y

RUN apt-get install libglib2.0-0 -y

RUN apt-get install curl -y

RUN pip install -r requirements.txt

RUN python -m spacy download en_core_web_sm

RUN python3 -m nltk.downloader all

RUN chmod u+x compile.sh

RUN ./compile.sh

#EXPOSE 8026

CMD [ "gunicorn", "app:app", "-b", "0.0.0.0:8026", "-w", "5", "--timeout", "500", "--graceful-timeout", "490" ]
