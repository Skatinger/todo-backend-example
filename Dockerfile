FROM python:3.6

ENV APP_HOME /myapp

RUN mkdir $APP_HOME
WORKDIR $APP_HOME

ADD requirements.txt $APP_HOME/
ADD ./

RUN pip3 install -r requirements.txt


