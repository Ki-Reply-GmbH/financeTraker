from pydantic import BaseModel
from typing import List, Tuple
from enum import Enum


class statusEnum(Enum):
    DONE = "Done"
    FAILED = "Failed"   
    NOT_STARTED = "Not Started"
    
class GeneratedTestForFunction(BaseModel):
    test_function_key: str = ""
    test_function_code: str = ""
    test_function_generated_name: str = ""
    test_error: str = ""
    retry_count: int = 0
    status: statusEnum = statusEnum.NOT_STARTED

class TestFunctionGenerator(BaseModel):
    function_name: str = ""
    function_common_code: str = ""
    function_code: str = ""  
    is_test_passed: bool = False
    generated_tests: List[GeneratedTestForFunction] = []

