FROM python:3

ADD uploadFirestore.py /

RUN pip install --upgrade firebase-admin

CMD [ "python", "./uploadFirestore.py" ]
