import os
import json
import pytest
import sys
from test_gen_framework.execution.Test_analysis import update_test_results_from_json
from test_gen_framework.prioritization.test_prioritizer import prioritize_tests
from test_gen_framework.reporting.Test_report import report_test_results
from test_gen_framework.config import read_config

config = read_config()


def load_test_priorities(priority_file: str):
    try:
        with open(priority_file, "r") as file:
            priorities = json.load(file)
        return priorities
    except Exception as e:
        print(f"Error reading the priorities file: {e}")
        return {}


def execute_tests(test_directory: str, pr_number: str):
    test_directory = os.path.abspath(test_directory)
    if not os.path.exists(test_directory):
        print(f"Error: The directory '{test_directory}' does not exist.")
        return

    priorities_path = test_directory + "/test_priorities.json"
    prioritize_tests(priorities_path, pr_number)

    priorities = load_test_priorities(priorities_path)
    prioritized_tests = [test for test, _ in priorities.items()]

    prioritized_tests = [
        os.path.join(test_directory, test) for test in prioritized_tests
    ]
    results_path = test_directory + "/test_results.json"

    pytest_args = [test_directory] + prioritized_tests
    pytest_args += ["--disable-warnings", "--json=" + results_path]
    result = pytest.main(pytest_args)

    update_test_results_from_json(results_path)
    if config["IS_REPORTING"]:
        print("Syncing results with dashboard")
        results = report_test_results(results_path)

    if result == 0:
        print("Tests executed successfully.")
    else:
        print("Test execution failed.")

    return result
