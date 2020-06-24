import Algorithmia
from Algorithmia.errors import AlgorithmException
import json
import time

def parse_json(stringdata):
    try:
        data = json.loads(stringdata)
        return data
    except Exception:
        raise Exception("{} is not json compatible, please check", stringdata)


def call_algo(client, algo_name, algo_hash, input, attempt_num=0):
    try:
        output = client.algo("{}/{}".format(algo_name, algo_hash)).pipe(input).result
        return output
    except AlgorithmException as e:
        if attempt_num <= 10:
            attempt_num += 1
            time.sleep(attempt_num)
            return call_algo(client, algo_name, algo_hash, input, attempt_num)
        else:
            raise Exception("attempted {} times.\n", e)

def test_algo(regular_api_key, api_address, case_data, algo_name, algo_hash):
    client = Algorithmia.client(api_key=regular_api_key, api_address=api_address)
    failures = []
    successes = []
    for case in case_data:
        input = case['input']
        if "expected_output" in case:
            expected = case['expected_output']
        else:
            expected = None
        if 'type' in case:
            type = case['type']
        else:
            type = "EXACT_MATCH"
        if 'tree' in case:
            traversal_tree = case['tree']
        else:
            traversal_tree = None
        name = case['case_name']
        print("--- testing case: {} ---".format(name))
        if type == "EXACT_MATCH":
            output = call_algo(client, algo_name, algo_hash, input)
            if traversal_tree:
                for elm in traversal_tree:
                    output = output[elm]
            if output == expected:
                success = {"output": output, "expected_output": expected, "case_name": name}
                successes.append(success)
            else:
                failure = {"output": output, "expected_output": expected, "case_name": name}
                failures.append(failure)
        elif type == "GREATER_OR_EQUAL":
            output = call_algo(client, algo_name, algo_hash, input)
            if traversal_tree:
                for elm in traversal_tree:
                    output = output[elm]
            if output >= expected:
                success = {"output": output, "expected_output": expected, "case_name": name}
                successes.append(success)
            else:
                failure = {"output": output, "expected_output": expected, "case_name": name}
                failures.append(failure)
        elif type == "LESS_OR_EQUAL":
            output = call_algo(client, algo_name, algo_hash, input)
            if traversal_tree:
                for elm in traversal_tree:
                    output = output[elm]
            if output <= expected:
                success = {"output": output, "expected_output": expected, "case_name": name}
                successes.append(success)
            else:
                failure = {"output": output, "expected_output": expected, "case_name": name}
                failures.append(failure)
        elif type == "NO_EXCEPTION":
            try:
                _ = call_algo(client, algo_name, algo_hash, input)
                success = {"output": None, "expected_output": expected, "case_name": name}
                successes.append(success)
            except AlgorithmException as e:
                failure = {"output": e.message, "case_name": name}
                failures.append(failure)
                pass
            except Exception as e:
                failure = {"output": str(e), "case_name": name}
                failures.append(failure)
                pass
        elif type == "EXCEPTION":
            try:
                output = call_algo(client, algo_name, algo_hash, input)
                failure = {"output": output, "case_name": name}
                failures.append(failure)
            except AlgorithmException:
                success = {"output": None, "expected_output": expected, "case_name": name}
                successes.append(success)
            except Exception as e:
                failure = {"output": str(e), "case_name": name}
                failures.append(failure)
                pass

        else:
            raise Exception("case type '{}' not implemented".format(type))

    print("--- testing complete ---")
    print("sucessful tests {}/{}".format(str(len(successes)), str(len(successes) + len(failures))))

    if len(failures) > 0:
        fail_msg = "At least one test case failed:\n"
        for failure in failures:
            fail_msg += "case_name: {}\nexpected_output: {}\nreal_output: {}\n".format(failure['case_name'],
                                                                                       failure.get('expected_output',
                                                                                                   "None"),
                                                                                       failure['output'])
        raise Exception(fail_msg)
    else:
        print("--- all test cases pass for {}/{} ---".format(algo_name, algo_hash))
