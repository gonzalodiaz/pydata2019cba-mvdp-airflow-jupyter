FROM puckel/docker-airflow:1.10.3

RUN set -xe && \
    pip install papermill==1.0.1 --user

ENV PYTHONPATH /usr/local/airflow

ENV AIRFLOW__CORE__REMOTE_LOGGING = False
