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
from airflow.operators.python_operator import ShortCircuitOperator

args = {
    'owner': 'Airflow',
    'start_date': airflow.utils.dates.days_ago(2),
}


def greater_than_one(foo):
    result = float(foo) / 10
    print("got result {}".format(result))
    return result < 1


with DAG(dag_id='example_short_circuit_operator', default_args=args) as dag:
    last = dag
    for i in range(0, 1000):
        attempt = ShortCircuitOperator(
            task_id='conditional_{}'.format(i),
            python_callable=greater_than_one,
            op_kwargs={"foo": i},
            dag=dag,
        )
        last >> attempt
        last = attempt
