from airflow.models import DAG
from dags.operators.papermill_operator import PapermillOperator

from datetime import datetime

args = {
    'owner': 'airflow',
    'start_date': datetime(2019, 3, 1)
}
with DAG(
    dag_id='example_papermill_operator', default_args=args,
    schedule_interval=None
) as dag:

    titanic_100_estimators = PapermillOperator(
        task_id="titanic-100-estimators",
        input_nb="/home/jovyan/work/jupyter/templates/nb_originals/KaggleTitanic.ipynb",
        output_nb="/home/jovyan/work/jupyter/templates/nb_outputs/KaggleTitanic-100-estimators.ipynb",
        parameters={"n_estimators": 100}
    )

    titanic_200_estimators = PapermillOperator(
        task_id="titanic-200-estimators",
        input_nb="/home/jovyan/work/jupyter/templates/nb_originals/KaggleTitanic.ipynb",
        output_nb="/home/jovyan/work/jupyter/templates/nb_outputs/KaggleTitanic-200-estimators.ipynb",
        parameters={"n_estimators": 200}
    )

    titanic_500_estimators = PapermillOperator(
        task_id="titanic-500-estimators",
        input_nb="/home/jovyan/work/jupyter/templates/nb_originals/KaggleTitanic.ipynb",
        output_nb="/home/jovyan/work/jupyter/templates/nb_outputs/KaggleTitanic-500-estimators.ipynb",
        parameters={"n_estimators": 500}
    )

    dag >> titanic_100_estimators >> titanic_200_estimators >> titanic_500_estimators
