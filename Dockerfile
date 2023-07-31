FROM python:3.8

RUN apt update -y && apt install awscli -y

WORKDIR /app

COPY . /app

#RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 unzip -y && pip install -r requirements.txt

RUN pip install -r requirements.txt

CMD ["python3", "rec_app.py"]

#CMD ["uvicorn", "rec_app:app", "--host", "0.0.0.0", "--port", "8080"]