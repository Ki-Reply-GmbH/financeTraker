from setup import llm
import ast
import os

from testGenConfig import source_dir, test_dir

def get_functions(source_file):
    with open(source_file) as f:
        root = ast.parse(f.read())

    functions = [node for node in ast.walk(root) if isinstance(node, ast.FunctionDef)]
    return functions
get_source_file = os.path.join(source_dir, 'services', 'user_services.py')

functions = get_functions(get_source_file)

import json

def get_test_for_func(functions):
    json_obj = {}

    for function in functions:
        function_code = ast.unparse(function)
        escaped_code = json.dumps(function_code)
        json_obj[function.name] = escaped_code

    return list(json_obj.items())

func_list = get_test_for_func(functions)
# for func_name, escaped_code in func_list:
    
func_name, escaped_code = func_list[0]
response= llm.invoke({"input": "give me the code for palindrome number"})

print(response)

# response={'input': 'give me the code for palindrome number', 'text': {"code":"def add_numbers(a, b):\n\tsum = a + b\n\tprint(sum)\n\tif sum > 10:\n\t\treturn True\n\telse:\n\t\treturn False\n"}}

# Extract the 'code' value
# code = response['text']['code']
# print(code)

# def save_test_to_file():
#     file_name = os.path.splitext(os.path.basename(get_source_file))[0]
#     # Create the directory if it doesn't exist
#     test_file_dir = os.path.join(test_dir, file_name)
#     os.makedirs(test_file_dir, exist_ok=True)
    
    
    
# test_file_dir = os.path.join(test_dir, '')

# with open(test_file_dir, 'w') as f:
#     f.write(code)


