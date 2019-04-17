FROM python:3

ADD uploadRemoteConfig.py /

RUN pip install --upgrade firebase-admin

ENTRYPOINT [ "python", "./uploadRemoteConfig.py" ]
