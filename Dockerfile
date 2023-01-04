FROM python:3.7
WORKDIR /master

RUN python -m pip install --upgrade pip

COPY /wheels ./wheels
RUN pip install --extra-index-url https://www.piwheels.org/simple ./wheels/torch-1.7.0a0-cp37-cp37m-linux_armv7l.whl
RUN pip install --extra-index-url https://www.piwheels.org/simple ./wheels/torchvision-0.8.0a0+45f960c-cp37-cp37m-linux_armv7l.whl

COPY requirements.txt .
RUN pip install --extra-index-url https://www.piwheels.org/simple -r requirements.txt


COPY microservice_rs.py .
COPY config.py .
COPY CNN.py .

EXPOSE 8001

ENTRYPOINT ["python", "./microservice_rs.py"]
