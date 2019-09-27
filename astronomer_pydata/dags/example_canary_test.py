# -*- coding: utf-8 -*-
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""Example DAG demonstrating the usage of the ShortCircuitOperator."""

import airflow.utils.helpers
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import ShortCircuitOperator, PythonOperator, BranchPythonOperator

args = {
    'owner': 'Airflow',
    'start_date': airflow.utils.dates.days_ago(2),
}

models_to_compare = ["model-1", "model-bar", "model-foo"]


def compare_results(**context):
    new_model_result = context['task_instance'].xcom_pull(task_ids='new_model')
    old_results = []
    for model_name in models_to_compare:
        old_results.append(context['task_instance'].xcom_pull(task_ids='old-model-{}'.format(model_name)))
    if new_model_result > max(old_results):
        return "deploy_new_model"
    else:
        return "alert_of_failed_model"


with DAG(dag_id='example_canary_test', default_args=args) as dag:
    num_tasks = 6
    compare_all_results = BranchPythonOperator(
        task_id='compare_results',
        python_callable=compare_results,
        dag=dag,
        provide_context=True
    )

    deploy_new_model = DummyOperator(task_id="deploy_new_model")
    alert_of_failed_model = DummyOperator(task_id="alert_of_failed_model")
    compare_all_results >> deploy_new_model
    compare_all_results >> alert_of_failed_model

    new_model = PythonOperator(
        task_id="new_model",
        python_callable=lambda: 5
    )
    new_model >> compare_all_results
    i = 5

    for model in models_to_compare:
        attempt = PythonOperator(
            task_id="old-model-{}".format(model),
            python_callable=lambda: i
        )
        i += 1
        attempt >> compare_all_results
