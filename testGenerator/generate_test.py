from setup import llm
import ast
import os
from functionGraber import get_functions_and_imports, format_functions_as_string

from testGenConfig import source_dir, test_dir

# Get the functions from the source file for llm invocation
def get_functions(source_file):
    functions= get_functions_and_imports(source_file)
    formatted_string = format_functions_as_string(functions)
    return formatted_string
get_source_file = os.path.join(source_dir, 'services', 'user_services.py')                               

functionsDetails = get_functions(get_source_file)


# for item in functionsDetails:
response= llm.invoke({"input": functionsDetails[0]})
    
    
# def save_test_to_file():
#     # Get the base name of the source file with extension
#     base_name_with_extension = os.path.basename(get_source_file)
#     # Split the base name and the extension
#     file_name, file_extension = os.path.splitext(base_name_with_extension)
    
#     print(f"File name: {file_name}")
#     print(f"Extension: {file_extension}")
    
#     file_name_with_extension = file_name + file_extension
#     print(f"File name with extension: {file_name_with_extension}")


#     file_name = os.path.splitext(os.path.basename(get_source_file))[0]
#     print(file_name)
#     # Create the directory if it doesn't exist
#     test_file_dir = os.path.join(test_dir, file_name)
#     os.makedirs(test_file_dir, exist_ok=True)
    
#     test_file_path = os.path.join(test_file_dir+ f'/{func_name}.py')
    
#     with open(test_file_path, 'w') as f:
#         f.write(code)
#     f.close()
    

# save_test_to_file()






























# import json

# def get_function_in_JSON_Object_List(functions):
#     json_obj = {}

#     for function in functions:
#         function_code = ast.unparse(function)
#         escaped_code = json.dumps(function_code)
#         json_obj[function.name] = escaped_code

#     return list(json_obj.items())


# # def generate_test_with_LLM(func_list):
# #     pass
# # func_list = get_function_in_JSON_Object_List(functions)
# # print(func_list[0])
# # # for func_name, escaped_code in func_list:
    
# # func_name, escaped_code = func_list[0]
# # # response= llm.invoke({"input": "give me the code for palindrome number"})

# # # print(response)

# # response={'input': 'give me the code for palindrome number', 'text': {"code":"def add_numbers(a, b):\n\tsum = a + b\n\tprint(sum)\n\tif sum > 10:\n\t\treturn True\n\telse:\n\t\treturn False\n"}}

# # # Extract the 'code' value
# # code = response['text']['code']
# # # print(code)
# def llm_invocation(input):
#     response= llm.invoke({"input": input})
#     code = response['text']['code']
#     return code

def save_test_to_file():
    # Get the base name of the source file with extension
    base_name_with_extension = os.path.basename(get_source_file)
    # Split the base name and the extension
    file_name, file_extension = os.path.splitext(base_name_with_extension)
    
    print(f"File name: {file_name}")
    print(f"Extension: {file_extension}")
    
    file_name_with_extension = file_name + file_extension
    print(f"File name with extension: {file_name_with_extension}")


    file_name = os.path.splitext(os.path.basename(get_source_file))[0]
    print(file_name)
    # Create the directory if it doesn't exist
    test_file_dir = os.path.join(test_dir, file_name)
    os.makedirs(test_file_dir, exist_ok=True)
    
    test_file_path = os.path.join(test_file_dir+ f'/{func_name}.py')
    
    with open(test_file_path, 'w') as f:
        f.write(code)
    f.close()
    

save_test_to_file()




