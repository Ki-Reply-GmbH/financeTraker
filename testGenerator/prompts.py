self_healing_prompt_template = """

You are tasked with debugging failing unit tests. Below is the information required:

Function Code: This is the original code of the function being tested.
Test Code: This is the generated unit test code.
Test Run Output: This includes the error messages and traceback from running the tests.

Function Code:{funtion_code}
Test Code:{test_code}
Test Run Output:{test_run_output}
###Instructions:
Analyze the provided function code, test code, and test run output.
Identify the root cause of the test failures.
Regenerate the corrected unit test code if necessary.
Your response must be structured as shown in the example below.

{
    "corrected_code": "CORRECTED CODE HERE"
}

"""