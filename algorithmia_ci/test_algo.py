import Algorithmia
from Algorithmia.errors import AlgorithmException
import json


def parse_json(stringdata):
    try:
        data = json.loads(stringdata)
        return data
    except Exception:
        raise Exception("{} is not json compatible, please check", stringdata)




def test_algo(regular_api_key, api_address, case_data, algo_name, algo_hash):
    client = Algorithmia.client(api_key=regular_api_key, api_address=api_address)
    failures = []
    for case in case_data:
        input = case['input']
        if "expected_output" in input:
            expected = input['expected_output']
        else:
            expected = "'expected_output' not defined"
        if 'type' in case:
            type = case['type']
        else:
            type = "EXACT_MATCH"
        if 'tree' in case:
            traversal_tree = case['tree']
        else:
            traversal_tree = None
        name = case['case_name']
        print("testing case: {}".format(name))
        if type == "EXACT_MATCH":
            output = client.algo("{}/{}".format(algo_name, algo_hash)).pipe(input).result
            if traversal_tree:
                for elm in traversal_tree:
                    output = output[elm]
            if output == expected:
                print("case: {} -- success".format(name))
            else:
                failure = {"output": output, "expected_output": expected, "case_name": name}
                failures.append(failure)
                print("case: {} -- fail".format(name))
        elif type == "GREATER_OR_EQUAL":
            output = client.algo("{}/{}".format(algo_name, algo_hash)).pipe(input).result
            if traversal_tree:
                for elm in traversal_tree:
                    output = output[elm]
            if output >= expected:
                print("case: {} -- success".format(name))
            else:
                failure = {"output": output, "expected_output": expected, "case_name": name}
                failures.append(failure)
                print("case: {} -- fail".format(name))
        elif type == "LESS_OR_EQUAL":
            output = client.algo("{}/{}".format(algo_name, algo_hash)).pipe(input).result
            if traversal_tree:
                for elm in traversal_tree:
                    output = output[elm]
            if output <= expected:
                print("case: {} -- success".format(name))
            else:
                failure = {"output": output, "expected_output": expected, "case_name": name}
                failures.append(failure)
                print("case: {} -- fail".format(name))
        elif type == "NO_EXCEPTION":
            try:
                _ = client.algo("{}/{}".format(algo_name, algo_hash)).pipe(input).result
                print("case: {} -- success".format(name))
            except AlgorithmException as e:
                failure = {"output": e.message, "case_name": name}
                failures.append(failure)
                print("case: {} -- fail".format(name))
            except Exception as e:
                failure = {"output": str(e), "case_name": name}
                failures.append(failure)
                print("case: {} -- fail".format(name))
        elif type == "EXCEPTION":
            try:
                output = client.algo("{}/{}".format(algo_name, algo_hash)).pipe(input).result
                failure = {"output": output, "case_name": name}
                failures.append(failure)
                print("case: {} -- fail".format(name))
            except AlgorithmException:
                print("case: {} -- success".format(name))
            except Exception as e:
                failure = {"output": str(e), "case_name": name}
                failures.append(failure)
                print("case: {} -- fail".format(name))

        else:
            raise Exception("case type '{}' not implemented".format(type))

    if len(failures) > 0:
        fail_msg = "At least one test case failed:\n"
        for failure in failures:
            fail_msg += "case_name: {}\nexpected_output: {}\nreal_output: {}\n".format(failure['case_name'],
                                                                                       failure['expected_output'],
                                                                                       failure['output'])
        raise Exception(fail_msg)
    else:
        print("all test cases pass for {}/{}".format(algo_name, algo_hash))
