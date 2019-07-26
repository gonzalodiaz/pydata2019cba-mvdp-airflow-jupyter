FROM puckel/docker-airflow:1.10.3

## Setup Python environment
ADD requirements.txt /requirements.txt
RUN pip install -r /requirements.txt --user

ENV PYTHONPATH /usr/local/airflow

ENV AIRFLOW__CORE__REMOTE_LOGGING = False
