FROM python:3.8-slim-buster

WORKDIR /app

COPY . .

EXPOSE 5000

RUN pip install -r requirements.txt 

CMD ["python", "app.py"]