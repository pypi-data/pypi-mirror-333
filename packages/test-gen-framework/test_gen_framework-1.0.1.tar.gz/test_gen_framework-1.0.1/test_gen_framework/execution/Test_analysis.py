import json
import os


def load_test_data(metadata_file: str):
    """Load existing test data from the JSON file using an absolute path."""
    absolute_path = os.path.abspath(metadata_file)
    if os.path.exists(absolute_path):
        with open(absolute_path, "r") as file:
            return json.load(file)
    return {}


def save_test_data(test_data, metadata_file: str):
    """Save updated test data to the JSON file using an absolute path."""
    absolute_path = os.path.abspath(metadata_file)
    with open(absolute_path, "w") as file:
        json.dump(test_data, file, indent=4)


def update_test_result(file_name, outcome, execution_time, metadata_file, is_same_file):
    """Update test results after each test execution at the file level."""
    test_data = load_test_data(metadata_file)

    if file_name not in test_data:
        test_data[file_name] = {
            "failures": 0,
            "executions": 0,
            "total_execution_time": 0.0,
            "stability_score": 1.0,
        }

    file_info = test_data[file_name]

    if not is_same_file:
        file_info["executions"] += 1

    if outcome == "failed":
        file_info["failures"] += 1

    file_info["total_execution_time"] += execution_time

    file_info["avg_execution_time"] = (
        file_info["total_execution_time"] / file_info["executions"]
    )

    file_info["stability_score"] = 1 - (file_info["failures"] / file_info["executions"])

    save_test_data(test_data, metadata_file)


def update_test_results_from_json(results_file, metadata_file="test_metadata.json"):
    """Update test data from a JSON results file (such as pytest's JSON output)."""
    base_path = os.path.dirname(__file__)
    metadata_file = os.path.join(base_path, "./../storage", metadata_file)

    with open(results_file, "r") as file:
        results = json.load(file)["report"]["tests"]

    last_file_name = None

    for test in results:
        test_name = test["name"]
        outcome = test["outcome"]
        execution_time = test["duration"]
        file_name = test_name.split("::")[0]
        is_same_file = file_name == last_file_name

        update_test_result(
            file_name, outcome, execution_time, metadata_file, is_same_file
        )

        last_file_name = file_name
