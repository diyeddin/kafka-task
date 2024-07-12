FROM python:3
WORKDIR /consumer
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "consumer.py"]