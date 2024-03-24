FROM python:3.8

ENV PYTHONUNBUFFERED 1
COPY ./e_com_backend /e_com_backend

COPY  ./requirements.txt /tmp/requirements.txt  

WORKDIR /e_com_backend

RUN pip install -r /tmp/requirements.txt 

EXPOSE 8000