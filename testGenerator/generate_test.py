from setup import chain
import ast
import os
from functionGraber import get_functions_and_imports, format_function_as_string, get_test_functions
from test_analyzer import run_tests
from self_healer import Healer
import json
from testGenConfig import source_dir, test_dir, project_root_module_name, root_dir
from worker import capture_working_function_responses, save_response_code, save_failure_summary


# def save_test_to_file(func_name, generated_test_code):
#     # Get the base name of the source file with extension
#     base_name_with_extension = os.path.basename(get_source_file)
#     # Split the base name and the extension
#     file_name, file_extension = os.path.splitext(base_name_with_extension)
    
#     file_name_with_extension = file_name + file_extension
#     print(f"File name with extension: {file_name_with_extension}")


#     file_name = os.path.splitext(os.path.basename(get_source_file))[0]
#     print(file_name)
#     # Create the directory if it doesn't exist
#     test_file_dir = os.path.join(test_dir, file_name)
#     os.makedirs(test_file_dir, exist_ok=True)
    
#     test_file_path = os.path.join(test_file_dir+ f'/{func_name}_test.py')
    
#     with open(test_file_path, 'w') as f:
#         f.write(generated_test_code)
#     f.close()
    
#     return test_file_path
    
def start_healing(test_function, test_file_path, function_code, test_run_output):
    # Create a Healer instance
    healer = Healer(test_function, test_file_path, function_code, test_run_output)
    # Start the healing process
    healer.heal()

get_source_file = os.path.join(source_dir, 'services', 'user_services.py')  

# def generate_test_with_LLM():
    
    
#     functionsWithImport=get_functions_and_imports(get_source_file,project_root_module_name,root_dir)
#     #print(functionsWithImport)
#     for function in functionsWithImport:
#         formatted_string = format_function_as_string(function)    
#         print(formatted_string)
#         response = chain.invoke({"input": formatted_string})
        
#         test_file_path=save_test_to_file(function.get('name', 'noNameFound'), response['text']['code'])
#         print(test_file_path)
#         test_functions=get_test_functions(test_file_path)

#         for test_function in test_functions:        
#             failure_summery=run_tests(test_file_path, test_function)
#             if failure_summery:
#                 print("Healing process started")
#                 start_healing(test_function, test_file_path, function.get('code', 'noCodeFound'), failure_summery)
            
#             break
#         break


def start_healing(test_function, test_file_path, function_code, test_run_output):
    # Create a Healer instance
    healer = Healer(test_function, test_file_path, function_code, test_run_output)
    # Start the healing process
    healer.heal()



def generate_test_with_LLM():
    
    
    functionsWithImport = get_functions_and_imports(get_source_file, project_root_module_name, root_dir)
    #capture_function_responses()
    for function in functionsWithImport:
        # Format the function as a string
        formatted_string = format_function_as_string(function)    
        print(f"Formatted function string: {formatted_string}")
        
        # Invoke the LLM chain and get the response
        response = chain.invoke({"input": formatted_string},return_only_outputs=True)
        #print(response)
        response = json.dumps(response)
        
        #save response to the worker file
        
        
        # print(response)
        
        # Handle multiple parts of the response: "common code", "test1", "test2", etc.
        
        response_code,response_code_dict = extract_code_from_llm_response(response)
        print(f"Response code extracted:\n{response_code}")
        print(type(response_code))
        #response_code_json_to_dict = json.loads(response_code)
        # save_response_code(response_code_dict)
        
        # print(f"Response code is: {response_code}")
        
        #print(response_code)
        # Save the test to a file
        # test_file_path = save_test_to_file(function.get('name', 'noNameFound'), response_code)
        test_file_path = save_test_to_file(function.get('name'), response_code) #make sure to handle noNameFound
        print(f"Test file saved at: {test_file_path}")
        
        # Get the test functions from the saved file
        test_functions = get_test_functions(test_file_path)

        for test_function in test_functions:
            # Run tests on the function
            failure_summary = run_tests(test_file_path, test_function)
            
            if failure_summary:
                print("Healing process started")
                save_failure_summary(failure_summary)
                # Start the healing process if tests fail
                start_healing(test_function, test_file_path, function.get('code', 'noCodeFound'), failure_summary)
            
            # Break after the first test function for now (as per your original code)
            break
        break
    



def extract_code_from_llm_response(response):
    """
    Extracts and concatenates the different sections of the LLM response, including 'commoncode', 'test1', 'test2', etc.
    Uses a for loop to count and process the test cases. Handles missing or None values gracefully.
    
    """
    # Initialize an empty string for the full code
    full_code = ""
    full_code_dict = {}
    
    try:
        # Parse the response into a Python dictionary
        response_dict = json.loads(response)
        
        # Extract the common code (imports and shared fixtures)
        common_code = response_dict.get('text', {}).get('commoncode')
        if common_code:
            common_code = common_code.strip()  # Remove surrounding spaces
            print(f"Common code extracted:\n{common_code}")
            full_code_dict['commoncode'] = common_code
            full_code += common_code + "\n\n"  # Add common code with spacing
            
        else:
            print("No common code found in response")
        
        # Initialize a list to gather all 'test' keys
        test_keys = [key for key in response_dict['text'] if key.startswith("test") and response_dict['text'][key] is not None]

        # Sort the test keys by the numeric value of their name (test1, test2, ...)
        sorted_test_keys = sorted(test_keys, key=lambda x: int(x.replace("test", "")))

        # Iterate over the test keys using a for loop
        for test_key in sorted_test_keys:  # Sorted ensures processing in correct order
            test_code = response_dict['text'][test_key].strip()  # Extract and strip each test case
            print(f"{test_key} extracted:\n{test_code}")
            full_code_dict[test_key] = test_code  # Add the test code to the dictionary
            # Ensure the test code is properly indented and formatted
            full_code += test_code + "\n\n"
        
        print(f"Final concatenated code:\n{full_code}")
        return full_code.strip(),full_code_dict  # Return final concatenated code without extra trailing spaces
    
    except json.JSONDecodeError:
        print("Invalid JSON format in response.")
        return ""
    except KeyError as e:
        print(f"Missing key in the response: {e}")
        return ""
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return ""


def save_test_to_file(function_name, test_code):
   
    # Construct the test file name and path
    test_file_name = f"test_{function_name}.py"
    test_file_path = os.path.join("tests", test_file_name)  # Save in 'tests' folder
    
    # Print the path where the file will be saved
    print(f"Saving test code to: {test_file_path}")
    
    # Ensure the directory exists
    try:
        os.makedirs(os.path.dirname(test_file_path), exist_ok=True)
        print(f"Directory created or already exists: {os.path.dirname(test_file_path)}")
    except Exception as e:
        print(f"Error creating directory: {e}")
        return ""
    
    # Check if test_code is empty before writing
    if not test_code.strip():
        print("Test code is empty. File will not be written.")
        return ""

    # Write the test code to the file
    try:
        with open(test_file_path, 'w') as test_file:
            test_file.write(test_code)
        print(f"Test code written successfully to: {test_file_path}")
    except Exception as e:
        print(f"Error writing to file: {e}")
        return ""

    return test_file_path


if __name__ == "__main__":
    capture_working_function_responses()
    generate_test_with_LLM()
    save_response_code()

# function_code= '''Function Code:
# def create_user(user: UserCreate):
#     with get_db() as db:
#         db_user = models.User(**user.model_dump())
#         db.add(db_user)
#         db.commit()
#         db.refresh(db_user)
#         return db_user

# Modules and Imports:
# - Function to Test: app.services.user_services.create_user
# - Dependencies:
#   - app.models.models
#   - app.models.models.get_db
#   - app.models.user.UserCreate

# Model Definitions:
# class UserCreate(BaseModel):
#     name: str = Field(..., min_length=3)
#     email: str = Field(..., pattern='^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$')
#     password: str = Field(..., min_length=8)'''
    
# failure_summery='''
# E   psycopg2.OperationalError: connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused (0x0000274D/10061)
# E       Is the server running on that host and accepting TCP/IP connections?
# E   connection to server at "localhost" (::1), port 5432 failed: Connection refused (0x0000274D/10061)
# E       Is the server running on that host and accepting TCP/IP connections?

# E   sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused (0x0000274D/10061)
# E       Is the server running on that host and accepting TCP/IP connections?
# E   connection to server at "localhost" (::1), port 5432 failed: Connection refused (0x0000274D/10061)
# E       Is the server running on that host and accepting TCP/IP connections?
# E
# E   (Background on this error at: https://sqlalche.me/e/20/e3q8)'''
# get_test_file = os.path.join(test_dir, 'user_services', 'create_user_test.py')
# test_functions=get_test_functions(get_test_file)
# print(test_functions)
# for test_function in test_functions: 
           
#     failure_summery=run_tests(get_test_file, test_function)
#     if failure_summery:
#         print("Healing process started")
#         start_healing(test_function, get_test_file, function_code, failure_summery)
#         break


























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
