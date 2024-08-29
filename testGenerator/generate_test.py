from setup import llm
import ast
import os
from functionGraber import get_functions_and_imports, format_function_as_string,get_test_functions
from test_analyzer import run_tests
from self_healer import Healer

from testGenConfig import source_dir, test_dir,project_root_module_name,root_dir
    
    
def save_test_to_file(func_name, generated_test_code):
    # Get the base name of the source file with extension
    base_name_with_extension = os.path.basename(get_source_file)
    # Split the base name and the extension
    file_name, file_extension = os.path.splitext(base_name_with_extension)
    
    file_name_with_extension = file_name + file_extension
    print(f"File name with extension: {file_name_with_extension}")


    file_name = os.path.splitext(os.path.basename(get_source_file))[0]
    print(file_name)
    # Create the directory if it doesn't exist
    test_file_dir = os.path.join(test_dir, file_name)
    os.makedirs(test_file_dir, exist_ok=True)
    
    test_file_path = os.path.join(test_file_dir+ f'/{func_name}_test.py')
    
    with open(test_file_path, 'w') as f:
        f.write(generated_test_code)
    f.close()
    
    return test_file_path
    
def start_healing(test_function, test_file_path, function_code, test_run_output):
    # Create a Healer instance
    healer = Healer(test_function, test_file_path, function_code, test_run_output)
    # Start the healing process
    healer.heal()

get_source_file = os.path.join(source_dir, 'services', 'user_services.py')  
def generate_test_with_LLM():
    
    
    functionsWithImport=get_functions_and_imports(get_source_file,project_root_module_name,root_dir)
    # print(functionsWithImport)
    for function in functionsWithImport:
        formatted_string = format_function_as_string(function)    
        print(formatted_string)
        response = llm.invoke({"input": formatted_string})
        test_file_path=save_test_to_file(function.get('name', 'noNameFound'), response['text']['code'])
        print(test_file_path)
        test_functions=get_test_functions(test_file_path)

        for test_function in test_functions:        
            failure_summery=run_tests(test_file_path, test_function)
            if failure_summery:
                print("Healing process started")
                start_healing(test_function, test_file_path, function.get('code', 'noCodeFound'), failure_summery)
            
            break
        break

   
# generate_test_with_LLM()
function_code= '''Function Code:
def create_user(user: UserCreate):
    with get_db() as db:
        db_user = models.User(**user.model_dump())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

Modules and Imports:
- Function to Test: app.services.user_services.create_user
- Dependencies:
  - app.models.models
  - app.models.models.get_db
  - app.models.user.UserCreate

Model Definitions:
class UserCreate(BaseModel):
    name: str = Field(..., min_length=3)
    email: str = Field(..., pattern='^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$')
    password: str = Field(..., min_length=8)'''
    
failure_summery='''
E   psycopg2.OperationalError: connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused (0x0000274D/10061)
E       Is the server running on that host and accepting TCP/IP connections?
E   connection to server at "localhost" (::1), port 5432 failed: Connection refused (0x0000274D/10061)
E       Is the server running on that host and accepting TCP/IP connections?

E   sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused (0x0000274D/10061)
E       Is the server running on that host and accepting TCP/IP connections?
E   connection to server at "localhost" (::1), port 5432 failed: Connection refused (0x0000274D/10061)
E       Is the server running on that host and accepting TCP/IP connections?
E
E   (Background on this error at: https://sqlalche.me/e/20/e3q8)'''
get_test_file = os.path.join(test_dir, 'user_services', 'create_user_test.py')
test_functions=get_test_functions(get_test_file)
print(test_functions)
for test_function in test_functions: 
           
    failure_summery=run_tests(get_test_file, test_function)
    if failure_summery:
        print("Healing process started")
        start_healing(test_function, get_test_file, function_code, failure_summery)
        break


























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
