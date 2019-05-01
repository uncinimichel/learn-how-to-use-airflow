from __future__ import division, absolute_import, print_function

import helpers
import operators
from airflow.plugins_manager import AirflowPlugin


# Defining the plugin class
class DataLabPlugin(AirflowPlugin):
    name = "data_lab_plugin"
    operators = [
        operators.DataToPostgresOperator
    ]
    helpers = [
        helpers.SqlQueries
    ]
