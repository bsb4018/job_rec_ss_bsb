FROM python:3.8

COPY . /app

WORKDIR /app

RUN apt update -y && apt install awscli -y

RUN pip install -r requirements.txt


CMD ["python", "rec_app.py"]

#CMD ["uvicorn", "rec_app:app", "--host", "0.0.0.0", "--port", "8080"]