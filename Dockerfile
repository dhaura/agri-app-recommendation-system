FROM python:alpine3.17
WORKDIR /master

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY microservice_rs.py .
COPY config.py .

EXPOSE 8001

ENTRYPOINT ["python", "./microservice_rs.py"]
