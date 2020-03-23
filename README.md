# algorithmia-ci-action
An algorithmia github Action to test and deploy github backed Algorithmia.com algorithms. When attached as a workflow for an Algorithmia algorithm, can automatically deploy new versions when provided tests pass.


# Action Input

```
inputs:
  regular_api_key:
    description: 'Your typical Algorithmia API key'
    required: true
  mgmt_api_key:
    description: 'Your algorithm management capable Algorithmia API key'
    required: true
  api_address:
    description: 'The API address for the Algorithmia Cluster you wish to connect to'
    required: false
    default: 'https://api.algorithmia.com'
  algorithm_name:
    description: 'The name of the Algorithm you want to test'
    required: true
  test_cases:
    description: 'A list of Json Case objects that describe the desired test cases'
    required: True
  version_schema:
    description: 'identifier to describe how to promote this release'
    required: false
    default: "minor"
```

```
  regular_api_key - (required) - An Algorithmia api key that has execute access for the algorithm you wish to test, read more about that [here](https://algorithmia.com/developers/platform/customizing-api-keys)
  mgmt_api_key - (required) - your Algorithmia Management API key, which you can learn about [here](https://algorithmia.com/developers/algorithm-development/algorithm-management).
  api_address - (optional) - The Algorithmia API cluster address you wish to connect to, if using a private cluster; please provide the correct path to your environment.
  algorithm_name - (required) - The algorithmia algorithm name for project you're testing. This algorithm name must refer to the github repository you attach this action to in order to work properly.
  version_schema - (optional) - The [semantic version](https://semver.org/) parameter that will get incremented whenever this action gets triggered. May be "Major", "Minor", or "Revision"
  test_cases - (required) - a stringified json list containing test cases to try your algorithm with, if any of the test cases fails - this action will return with an exception indicating which case failed.
```


# Case Schema
Your test cases should follow the following json schema
```
[
 { 
    "case_name": String,
    "input": Any,
    "expected_output": Any
  },
  ...
]
```

`input` and `expected_output` will be expected to be the raw input/output that the algorithm you're testing should expect.
