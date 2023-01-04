FROM dhaura/agri-app-rs-base:latest

COPY microservice_rs.py .
COPY config.py .
COPY CNN.py .

COPY /feed ./feed

EXPOSE 8001

ENTRYPOINT ["python", "./microservice_rs.py"]
