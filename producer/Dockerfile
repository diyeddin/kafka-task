FROM python:3
WORKDIR /producer
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "producer.py"]