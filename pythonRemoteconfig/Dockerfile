FROM python:3

ADD uploadRemoteConfig.py /

RUN pip install --upgrade firebase-admin

CMD [ "python", "./uploadRemoteConfig.py" ]
