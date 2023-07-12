FROM python:3.8-alpine
WORKDIR /code
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY toPostgresDB.py toPostgresDB.py
COPY toMongoDB.py toMongoDB.py
COPY apiconnector.py apiconnector.py
