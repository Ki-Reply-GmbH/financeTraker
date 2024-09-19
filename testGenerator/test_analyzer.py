import pytest
import sys
import io
import os
import re
from testGenConfig import root_dir

def run_tests(file_path: str = None, function_name: str = None):
    os.chdir(root_dir)
    # Capture the output using a StringIO object
    captured_output = io.StringIO()
    sys.stdout = captured_output

    # Construct the pytest arguments
    pytest_args = ["-q", "--tb=short", "--disable-warnings", "--cov-report=term-missing"]
    
    # Add file path and function name if provided
    if file_path:
        pytest_args.append(file_path)
    # Add function name if provided
    if function_name:
        pytest_args[-1] += f"::{function_name}"

    # Run the tests
    result = pytest.main(pytest_args)

    # Reset stdout
    sys.stdout = sys.__stdout__

    # Fetch the captured output
    output = captured_output.getvalue()

    # Process the output
    # print("Captured Output:")
    # print(output)

    # Check the result for further action
    if result == 0:
        print("All tests passed!")
        # You can add your further processing code here
    else:
        print(f"Some tests failed. Result code: {result}")
            # Extract specific part of the output (e.g., failure summary)
        failure_summary = extract_failure_summary(output)
        print("Failure Summary:")
        print(failure_summary)
        return failure_summary
        # Handle the failure case

def extract_failure_summary(output):
    # Use regular expressions to find the failure summary
    match = re.search(r"=+ FAILURES =+\n(.*?)\n=+ short test summary info =+", output, re.DOTALL)
    if match:
        failure_section = match.group(1)
        # Extract error messages from the failure section
        error_messages = re.findall(r"E\s+.*?\nE\s+.*?(?=\n\n|\Z)", failure_section, re.DOTALL)
        return "\n\n".join(error_messages)
    return "No failures found."