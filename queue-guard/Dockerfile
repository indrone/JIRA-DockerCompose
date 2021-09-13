FROM python:3.6-slim


RUN mkdir classification_queue

WORKDIR /classification_queue

ADD . /classification_queue

RUN apt-get update -y

RUN apt-get install build-essential -y

RUN apt-get install  libsm6 libxext6 libxrender-dev -y

RUN apt-get install libglib2.0-0 -y

RUN apt-get install screen -y

RUN pip install -r requirements.txt

CMD ["python3","multithreaded_classification_mapping.py"]
