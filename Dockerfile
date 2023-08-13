FROM python:3.8

RUN apt update -y && apt install awscli -y

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "sapp.py", "--server.port=8501", "--server.address=0.0.0.0"]

#CMD ["streamlit", "run", "sapp.py"]

