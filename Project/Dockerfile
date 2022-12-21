FROM python:3.8-slim-buster
WORKDIR /project
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install psycopg2-binary
COPY . .
ENTRYPOINT ["python","manage.py","runserver","0.0.0.0:8000"]