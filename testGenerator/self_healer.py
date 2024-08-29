from functionGraber import get_functions_and_imports, format_function_as_string,get_test_functions
from testGenConfig import root_dir
from prompts import self_healing_prompt_template

class Healer:
    def __init__(self, test_function_name,test_file_path, function_code, test_run_output,retry=3):
        self.test_function_name = test_function_name
        self.test_file_path = test_file_path
        self.function_code = function_code
        self.test_run_output = test_run_output
        self.retry = retry

    def heal(self):
        test_functions_definations=get_functions_and_imports(self.test_file_path,"tests",root_dir)
          # Find the matching test function definition
        matching_test_function = next(
            (func for func in test_functions_definations if func['name'] == self.test_function_name), 
            None
        )
        
        if matching_test_function:
            # Work with the matching test function
            formated_test_code=format_function_as_string(matching_test_function)
        else:
            print(f"No matching test function found for {self.test_function_name}")
            
        

