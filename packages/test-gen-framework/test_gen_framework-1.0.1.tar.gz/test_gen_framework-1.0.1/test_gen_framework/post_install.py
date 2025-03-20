import os


def create_github_actions():
    gh_actions_dir = os.path.join(os.getcwd(), ".github", "workflows")
    os.makedirs(gh_actions_dir, exist_ok=True)

    ci_pipeline = """name: CI Pipeline
# ... (pipeline contents)
"""
    ci_pipeline_path = os.path.join(gh_actions_dir, "ci.yml")
    with open(ci_pipeline_path, "w") as file:
        file.write(ci_pipeline)


def create_config_file():
    config_path = os.path.join(os.getcwd(), "config.yaml")
    config_content = """GITHUB_TOKEN: ""
                        REPO_OWNER: ""
                        REPO_NAME: ""
                        PROJECT_NAME: ""
                        TEST_LOC: ""
                        IS_REPORTING: True
                    """
    with open(config_path, "w") as file:
        file.write(config_content)


def init_config():
    create_github_actions()
    create_config_file()
