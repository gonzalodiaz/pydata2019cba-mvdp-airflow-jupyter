from airflow.models import DAG
from dags.operators.papermill_operator import PapermillOperator
from airflow.operators.dummy_operator import DummyOperator

from datetime import datetime

args = {
    'owner': 'airflow',
    'start_date': datetime(2019, 3, 1)
}
with DAG(
        dag_id='example_papermill_operator_hyperparam', default_args=args,
        schedule_interval=None
) as dag:
    estimator_numbers = [100, 200, 500]
    loss_rates = [i * .05 for i in range(2,20,2)]
    upstream = dag
    previous_tasks = []
    last_step=dag
    for n_estimators in estimator_numbers:
        current_step = DummyOperator(task_id="titanic-{}-estimators".format(n_estimators))
        [p_step >> current_step for p_step in previous_tasks]
        previous_tasks = []
        for loss_rate in loss_rates:
            task_name = 'KaggleTitanic-{}-estimators-{}-lossrate'.format(n_estimators, loss_rate)
            output_name = "/nb_outputs/{}.ipynb".format(task_name)
            titanic_estimator = PapermillOperator(
                task_id=task_name,
                input_nb="/nb_originals/KaggleTitanic.ipynb",
                output_nb="foo",
                parameters={"n_estimators": n_estimators, "loss_rate": loss_rate}
            )
            current_step >> titanic_estimator
            previous_tasks.append(titanic_estimator)
