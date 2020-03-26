#!/usr/bin/python

import os
from algorithmia_ci import build_wait, test_algo, publish_algo

if __name__ == "__main__":
    api_key = os.getenv("INPUT_API_KEY")
    api_address = os.getenv("INPUT_API_ADDRESS")
    publish_schema = os.getenv("INPUT_VERSION_SCHEMA")
    algo_hash = os.getenv("GITHUB_SHA")


    if not api_key:
        raise Exception("field 'api_key' not defined in workflow")
    if not api_address:
        raise Exception("field 'api_address' not defined in workflow")
    if not algo_name:
        raise Exception(os.listdir("/github/workspace"))
        # raise Exception("field 'algo_name' not defined in workflow")
    if not case_data:
        raise Exception("field 'test_cases' not defined in workflow")
    if not publish_schema:
        raise Exception("field 'version_schema' not defined in workflow")

    build_wait(api_key, api_address, algo_name, algo_hash)
    test_algo(api_key, api_address, case_data, algo_name, algo_hash)
    publish_algo(api_key, api_address, publish_schema, algo_name, algo_hash)
