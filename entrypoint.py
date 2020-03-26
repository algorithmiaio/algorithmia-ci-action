#!/usr/bin/python

import os, json
from algorithmia_ci import build_wait, test_algo, publish_algo

if __name__ == "__main__":
    api_key = os.getenv("INPUT_ALGO_API_KEY")
    api_address = os.getenv("INPUT_API_ADDRESS")
    publish_schema = os.getenv("INPUT_VERSION_SCHEMA")

    algo_hash = os.getenv("GITHUB_SHA")

    if os.path.isfile("/github/workspace/algorithmia.conf"):
        with open('/github/workspace/algorithmia.conf') as f:
            conf_data = json.load(f)
            algo_user = conf_data['username']
            algo_name = conf_data['algoname']
            algo_full_path = "algo://{}/{}".format(algo_user, algo_name)
    else:
        raise Exception("'algorithmia.conf' not found, malformed algorithm detected")
    if os.path.isfile("/github/workspace/TEST_CASES.json"):
        with open('/github/workspace/TEST_CASES.json') as f:
            test_cases = json.load(f)

    if not api_key:
        raise Exception("field 'api_key' not defined in workflow")
    if not api_address:
        raise Exception("field 'api_address' not defined in workflow")
    if not publish_schema:
        raise Exception("field 'version_schema' not defined in workflow")

    build_wait(api_key, api_address, algo_full_path, algo_hash)
    test_algo(api_key, api_address, test_cases, algo_full_path, algo_hash)
    publish_algo(api_key, api_address, publish_schema, algo_full_path, algo_hash)
