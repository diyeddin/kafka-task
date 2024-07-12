FROM python:3
WORKDIR /api
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8501
ENTRYPOINT ["python", "api.py"]