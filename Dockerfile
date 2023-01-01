FROM python:3.9
WORKDIR /master

RUN python -m pip install --upgrade pip

COPY requirements.txt .
RUN pip install --extra-index-url https://www.piwheels.org/simple -r requirements.txt

COPY microservice_rs.py .
COPY config.py .
COPY CNN.py .

EXPOSE 8001

ENTRYPOINT ["python", "./microservice_rs.py"]
