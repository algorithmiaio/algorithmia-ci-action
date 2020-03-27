#!/usr/bin/python

import os, json
from algorithmia_ci import build_wait, test_algo, publish_algo

if __name__ == "__main__":
    api_key = os.getenv("INPUT_API_KEY")
    api_address = os.getenv("INPUT_API_ADDRESS")
    publish_schema = os.getenv("INPUT_VERSION_SCHEMA")
    repo_name = os.getenv("INPUT_PATH")

    algo_hash = os.getenv("GITHUB_SHA")


    repo_path = "/github/workspace/{}".format(repo_name)

    if not api_key:
        raise Exception("field 'api_key' not defined in workflow")
    if not api_address:
        raise Exception("field 'api_address' not defined in workflow")
    if not publish_schema:
        raise Exception("field 'version_schema' not defined in workflow")
    if not repo_name:
        raise Exception("field 'repo_name' not defined in workflow")

    if os.path.exists(repo_path):
        with open("{}/{}".format(repo_path, "algorithmia.conf")) as f:
            config_data = json.load(f)
        with open("{}/{}".format(repo_path, "TEST_CASES.json")) as f:
            case_data = json.load(f)
        algo_name = "algo://{}/{}".format(config_data['username'], config_data['algoname'])

        build_wait(api_key, api_address, algo_name, algo_hash)
        test_algo(api_key, api_address, case_data, algo_name, algo_hash)
        publish_algo(api_key, api_address, publish_schema, algo_name, algo_hash)
    else:
        raise Exception("actions/checkout on the local repo must be run before this action can be completed")

