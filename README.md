# [PyData 2019 CBA] - Minimum Valuable Data Products with Airflow and Jupyter

## Build
```
docker-compose build
```

## Launch
```
docker-compose up
```
Go to http://localhost:8888 to Open Jupyter Labs

Go to http://localhost:8080 to Open Airflow 

## Test it
In Airflow, turn on the DAG and press "Trigger DAG". This will run an execution.

Once the DAG complete, check the output csv files in the folder `jupyter/templates/datasets/output`.