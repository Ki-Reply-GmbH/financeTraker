from functionGraber import get_test_functions, get_functions_and_imports, format_function_as_string
from testGenConfig import source_dir, test_dir, project_root_module_name, root_dir  
import os
import json

get_source_file = os.path.join(source_dir, 'services', 'user_services.py') 

# Capture function responses and print or save them
def capture_working_function_responses():
    #test_file_path = os.path.join(test_dir, 'path_to_your_test_file.py')  
    source_file_path = get_source_file  
    project_base_path = source_dir
    app_dir_name = project_root_module_name

    try:
        # Capture test function names
        #test_function_results = get_test_functions(test_file_path)
        #print("Test Functions Captured:")
        #print(test_function_results)

        # Capture function and import details
        function_imports_results = get_functions_and_imports(get_source_file, project_root_module_name, root_dir)
        for func in function_imports_results:
            formatted_func = format_function_as_string(func)
            print(f"\nFormatted Function inside worker:\n{formatted_func}")   
        # store the whole test code in this variable  
        
    except Exception as e:
        print(f"Error while capturing responses: {e}")

def save_response_code(code):
    
    
    global response_code_storage
    
    response_code_storage = code
    print(f"Raw response code before conversion:\n{response_code_storage}")
    try:
        response_code_to_dict = json.loads(response_code_storage)
        print(f"Response code saved as a dictionary inside worker.py:\n{response_code_to_dict}")
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")
        response_code_to_dict = None
    
    # Return the dictionary or None if conversion failed
    return response_code_to_dict
    
    # You can also print or log it here if needed
    #print(f"Response code saved inside worker.py:\n{response_code_storage}")
    
    #return response_code_storage






